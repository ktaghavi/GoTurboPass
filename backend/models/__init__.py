"""
models/__init__.py

Import every model here so SQLAlchemy metadata is fully populated before
Flask-Migrate generates or applies migrations.

Order: tables referenced by FKs must appear before tables that reference them.
"""
from .db import db

# ── Core identity & enrollment ────────────────────────────────────────────────
from .user            import User
from .county          import County
from .court           import Court
from .student_profile import StudentProfile, GenderEnum, DLClassEnum
from .citation        import Citation

# ── Payments (paywall gate) ───────────────────────────────────────────────────
from .payment         import Payment, PaymentStatus

# ── Compliance audit trail ────────────────────────────────────────────────────
from .audit_log       import AuditLog

# ── Course engine ─────────────────────────────────────────────────────────────
from .module          import Module
from .exam            import Exam, ExamAttempt   # before Quiz/Question (Question.exam_id FK)
from .quiz            import Quiz, Question
from .progress        import Progress

# ── Completion ────────────────────────────────────────────────────────────────
from .certificate     import Certificate

# ── Student support ───────────────────────────────────────────────────────────
from .inquiry         import Inquiry, InquiryStatus

__all__ = [
    "db",
    # Identity
    "User", "County", "Court",
    "StudentProfile", "GenderEnum", "DLClassEnum",
    "Citation",
    # Commerce
    "Payment", "PaymentStatus",
    # Audit
    "AuditLog",
    # Course
    "Module", "Exam", "ExamAttempt", "Quiz", "Question", "Progress",
    # Completion
    "Certificate",
    # Support
    "Inquiry", "InquiryStatus",
]
