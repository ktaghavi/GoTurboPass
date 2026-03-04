"""
Payment — Stripe Checkout session record and paywall gate.

A student must have a Payment row with status='paid' before they are
allowed to access any course module.  The status is updated by the
Stripe webhook (routes/payment.py — to be built in the payment sprint).

Stripe Checkout flow:
  1. POST /api/payment/create-session  → create Payment(status=pending) + Stripe session
  2. Student completes payment on Stripe-hosted page
  3. Stripe fires webhook → POST /api/payment/webhook
  4. Webhook verifies signature, sets Payment.status='paid', records paid_at
  5. Student is redirected to /dashboard; backend checks payment status on module access
"""
from datetime import datetime, timezone
from enum import Enum

from models.db import db


class PaymentStatus(str, Enum):
    PENDING  = "pending"   # Session created, awaiting payment
    PAID     = "paid"      # Stripe confirmed payment
    FAILED   = "failed"    # Payment attempt failed
    REFUNDED = "refunded"  # Refund issued (student loses course access)


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    citation_id = db.Column(
        db.Integer,
        db.ForeignKey("citations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Stripe identifiers
    stripe_session_id = db.Column(db.String(255), unique=True, nullable=True)
    stripe_payment_intent_id = db.Column(db.String(255), nullable=True)

    amount_cents = db.Column(db.Integer, nullable=False, default=500)  # $5.00
    status = db.Column(
        db.Enum(PaymentStatus),
        nullable=False,
        default=PaymentStatus.PENDING,
        index=True,
    )

    paid_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user = db.relationship("User", back_populates="payments")
    citation = db.relationship("Citation")

    def __repr__(self):
        return f"<Payment {self.id} user={self.user_id} status={self.status}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "citation_id": self.citation_id,
            "amount_cents": self.amount_cents,
            "status": self.status.value,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
