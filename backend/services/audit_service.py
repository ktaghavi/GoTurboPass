"""
AuditService — compliance event logging with PII redaction.

All events that touch student data or course state must be logged here.
This table is the authoritative compliance trail for CA DMV audits.

Standard event names (use these constants; do not invent new strings):
  REGISTER          — new account created
  LOGIN             — successful authentication
  LOGIN_FAIL        — bad credentials attempt (logs IP, no user_id)
  ENROLL            — student profile + citation saved
  PAYMENT_INIT      — Stripe checkout session created
  PAYMENT_COMPLETE  — Stripe webhook confirmed payment
  MODULE_START      — student entered a module page (timer started)
  MODULE_HEARTBEAT  — server-side timer heartbeat received
  MODULE_COMPLETE   — module timer + quiz requirements satisfied
  QUIZ_SUBMIT       — module quiz answers submitted
  EXAM_START        — final exam session opened
  EXAM_SUBMIT       — final exam answers submitted
  CERT_GENERATE     — certificate PDF generated
  TVCC_SUBMIT       — TVCC API payload dispatched (stub: logged but not sent)
  IDLE_LOGOUT       — session expired due to inactivity
  TAB_SWITCH        — student switched tabs during course (anti-cheat)
"""
import traceback
from datetime import datetime, timezone

from flask import request

from config import Config
from models.db import db
from models.audit_log import AuditLog


class AuditService:

    @staticmethod
    def log_event(
        event: str,
        student_id: int | None = None,
        details: dict | None = None,
    ) -> None:
        """
        Persist one audit event.

        Never raises — errors are printed server-side and swallowed so that
        a logging failure cannot abort the student's active session.

        Args:
            event:      Event name constant (see module docstring).
            student_id: users.id of the acting student (None for pre-auth events).
            details:    Arbitrary key-value context (PII-redacted before storage).
        """
        try:
            safe_details = AuditService._redact_pii(details or {})

            # Safely extract request context (may be called outside request ctx)
            try:
                ip = request.remote_addr
                user_agent = request.headers.get("User-Agent", "")[:500]
            except RuntimeError:
                ip = None
                user_agent = None

            entry = AuditLog(
                event=event,
                student_id=student_id,
                ip=ip,
                user_agent=user_agent,
                details=safe_details,
                created_at=datetime.now(timezone.utc),
            )

            db.session.add(entry)
            db.session.commit()

        except Exception:
            db.session.rollback()
            traceback.print_exc()  # visible in dev; route to structured logging in prod

    @staticmethod
    def _redact_pii(data: dict) -> dict:
        """
        Return a shallow copy with known PII fields replaced by '[REDACTED]'.
        Keys are checked case-insensitively to catch camelCase variants.
        """
        if not isinstance(data, dict):
            return {}

        pii = {f.lower() for f in getattr(Config, "PII_FIELDS", set())}
        redacted = {}
        for k, v in data.items():
            redacted[k] = "[REDACTED]" if k.lower() in pii else v
        return redacted
