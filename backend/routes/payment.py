"""
Payment routes — Stripe Checkout integration.

Endpoints:
  POST /api/payment/create-session   JWT-protected  Create checkout session
  POST /api/payment/webhook          Public (Stripe) Stripe webhook handler
  GET  /api/payment/status           JWT-protected  Current payment status

Stripe Checkout flow:
  1. Student calls POST /api/payment/create-session → backend creates
     Payment(status=PENDING) + Stripe session, returns {url}.
  2. Frontend redirects student to url (Stripe-hosted checkout page).
  3. Student pays → Stripe fires POST /api/payment/webhook.
  4. Webhook verifies signature, marks Payment.status=PAID, records paid_at.
  5. Frontend polls GET /api/payment/status; on paid=true, unlocks modules.

Webhook note: raw request body MUST be read via request.get_data() before
any JSON parsing — stripe.Webhook.construct_event requires raw bytes for
HMAC-SHA256 signature verification.
"""
import stripe
from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from models import db
from models.citation import Citation
from models.payment import Payment, PaymentStatus
from services.audit_service import AuditService

payment_bp = Blueprint("payment", __name__)


# ── 1. Create Checkout Session ─────────────────────────────────────────────────

@payment_bp.post("/api/payment/create-session")
@jwt_required()
def create_session():
    """
    Create a Stripe Checkout session for the authenticated student.

    Guards:
    - Student must have completed enrollment (citation exists).
    - If a PAID payment already exists, returns 409 (idempotent).
    - Any pending/failed sessions from prior attempts are left as-is;
      a new session is created so the student gets a fresh payment link.

    Returns:
        {"url": "<stripe-hosted-checkout-url>"}
    """
    identity = get_jwt_identity()
    user_id  = identity["user_id"]

    # Guard: course already purchased?
    already_paid = Payment.query.filter_by(
        user_id=user_id, status=PaymentStatus.PAID
    ).first()
    if already_paid:
        return jsonify({"error": "Course already purchased."}), 409

    # Must have an enrolled citation (enrollment route creates this)
    citation = (
        Citation.query
        .filter_by(user_id=user_id)
        .order_by(Citation.created_at.desc())
        .first()
    )
    if not citation:
        return jsonify({"error": "Complete enrollment before purchasing."}), 400

    stripe.api_key    = current_app.config["STRIPE_SECRET_KEY"]
    frontend_base     = current_app.config["FRONTEND_ORIGINS"][0].rstrip("/")
    price_cents       = current_app.config["STRIPE_PRICE_CENTS"]

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": price_cents,
                    "product_data": {
                        "name": "GoTurboPass Online Traffic School",
                        "description": "CA DMV-approved 340-minute online traffic school",
                    },
                },
                "quantity": 1,
            }],
            # Frontend URLs — Stripe appends ?session_id={CHECKOUT_SESSION_ID}
            success_url=f"{frontend_base}/dashboard?payment=success",
            cancel_url=f"{frontend_base}/payment?payment=cancelled",
            # Metadata for webhook lookup (belt-and-suspenders alongside DB record)
            client_reference_id=str(user_id),
            metadata={
                "user_id":     str(user_id),
                "citation_id": str(citation.id),
            },
        )
    except stripe.StripeError as exc:
        current_app.logger.error("Stripe session creation failed: %s", exc)
        return jsonify({"error": "Payment service unavailable. Try again later."}), 502

    # Persist PENDING record — webhook will update status to PAID
    payment = Payment(
        user_id           = user_id,
        citation_id       = citation.id,
        stripe_session_id = session.id,
        amount_cents      = price_cents,
        status            = PaymentStatus.PENDING,
    )
    db.session.add(payment)
    db.session.commit()

    AuditService.log_event(
        "PAYMENT_INIT",
        student_id=user_id,
        request=request,
        details={"stripe_session_id": session.id, "citation_id": citation.id},
    )

    return jsonify({"url": session.url}), 200


# ── 2. Stripe Webhook ──────────────────────────────────────────────────────────

@payment_bp.post("/api/payment/webhook")
def stripe_webhook():
    """
    Stripe delivers signed events here for payment lifecycle notifications.

    IMPORTANT: This endpoint must NOT be protected by JWT — Stripe calls it,
    not the student.  Authenticity is verified via HMAC-SHA256 signature using
    STRIPE_WEBHOOK_SECRET from your Stripe dashboard (or `stripe listen` CLI).

    To test locally:
        stripe listen --forward-to localhost:5000/api/payment/webhook
    """
    payload    = request.get_data()                    # raw bytes — never request.json
    sig_header = request.headers.get("Stripe-Signature", "")
    secret     = current_app.config.get("STRIPE_WEBHOOK_SECRET", "")

    stripe.api_key = current_app.config["STRIPE_SECRET_KEY"]

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, secret)
    except ValueError:
        current_app.logger.warning("Stripe webhook: invalid payload")
        return jsonify({"error": "Invalid payload"}), 400
    except stripe.SignatureVerificationError:
        current_app.logger.warning("Stripe webhook: signature mismatch — check STRIPE_WEBHOOK_SECRET")
        return jsonify({"error": "Invalid signature"}), 400

    event_type = event["type"]
    data_obj   = event["data"]["object"]

    if event_type == "checkout.session.completed":
        _handle_checkout_completed(data_obj)

    elif event_type == "checkout.session.expired":
        _handle_checkout_expired(data_obj)

    # Always return 200 for unhandled event types — prevents Stripe retry storms
    return jsonify({"received": True}), 200


def _handle_checkout_completed(session: dict) -> None:
    """Mark payment PAID when Stripe confirms the charge."""
    payment = Payment.query.filter_by(stripe_session_id=session["id"]).first()
    if not payment:
        current_app.logger.error(
            "Webhook: no Payment record for session %s — possible race condition",
            session["id"],
        )
        return

    payment.status                    = PaymentStatus.PAID
    payment.stripe_payment_intent_id  = session.get("payment_intent")
    payment.paid_at                   = datetime.now(timezone.utc)
    db.session.commit()

    AuditService.log_event(
        "PAYMENT_COMPLETE",
        student_id=payment.user_id,
        details={
            "stripe_session_id":        session["id"],
            "stripe_payment_intent_id": payment.stripe_payment_intent_id,
            "amount_cents":             payment.amount_cents,
        },
    )
    current_app.logger.info(
        "Payment confirmed: user_id=%s session=%s intent=%s",
        payment.user_id,
        session["id"],
        payment.stripe_payment_intent_id,
    )


def _handle_checkout_expired(session: dict) -> None:
    """Mark payment FAILED when a Checkout session expires (30-min window)."""
    payment = Payment.query.filter_by(stripe_session_id=session["id"]).first()
    if payment and payment.status == PaymentStatus.PENDING:
        payment.status = PaymentStatus.FAILED
        db.session.commit()
        current_app.logger.info(
            "Checkout session expired: session=%s user_id=%s",
            session["id"],
            payment.user_id,
        )


# ── 3. Payment Status ──────────────────────────────────────────────────────────

@payment_bp.get("/api/payment/status")
@jwt_required()
def payment_status():
    """
    Return the most recent payment record for the authenticated student.

    The frontend polls this after returning from Stripe to confirm the webhook
    has fired and status is 'paid' before unlocking course modules.

    Response:
        {"paid": bool, "status": str|null, ...payment fields}
    """
    identity = get_jwt_identity()
    user_id  = identity["user_id"]

    payment = (
        Payment.query
        .filter_by(user_id=user_id)
        .order_by(Payment.created_at.desc())
        .first()
    )

    if not payment:
        return jsonify({"paid": False, "status": None}), 200

    return jsonify({
        **payment.to_dict(),
        "paid": payment.status == PaymentStatus.PAID,
    }), 200
