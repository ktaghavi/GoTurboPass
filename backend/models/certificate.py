"""
Certificate — DMV-compliant completion certificate record.

CA DMV OL-613 required fields (must appear on the physical/PDF certificate):
  • Student legal name (as provided during enrollment)
  • Student date of birth
  • Driver license number (last 4 only — full DL is hashed, not stored)
  • Completion date and time
  • Total instructional minutes (must equal 340)
  • Final exam score
  • School name: "GoTurboPass Online Traffic School"
  • School DMV approval number (fill SCHOOL_DMV_NUMBER env var when obtained)
  • Unique certificate number (for DMV cross-reference)
  • Case number / court name

TVCC API stub:
  tvcc_submitted_at  — timestamp when the TVCC payload was dispatched
  tvcc_confirmation  — confirmation token returned by TVCC
  Both are null until the TVCC API module is activated with live credentials.
  See COMPLIANCE NOTE in routes/tvcc_stub.py (to be built).
"""
from datetime import datetime, timezone
import os
import uuid

from models.db import db


def _generate_cert_no() -> str:
    """
    Generate a unique certificate number in the format GTP-YYYYMMDD-XXXX.
    'GTP' prefix identifies GoTurboPass for DMV cross-reference.
    """
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    suffix = uuid.uuid4().hex[:6].upper()
    return f"GTP-{today}-{suffix}"


class Certificate(db.Model):
    __tablename__ = "certificates"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    citation_id = db.Column(
        db.Integer,
        db.ForeignKey("citations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    exam_attempt_id = db.Column(
        db.Integer,
        db.ForeignKey("exam_attempts.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ── Unique certificate identifier ─────────────────────────────────────────
    certificate_no = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        default=_generate_cert_no,
    )

    # ── DMV-required student fields (denormalized at generation time) ─────────
    student_first_name = db.Column(db.String(100), nullable=False)
    student_last_name = db.Column(db.String(100), nullable=False)
    student_dob = db.Column(db.Date, nullable=False)
    student_dl_last4 = db.Column(db.String(4), nullable=False)

    # ── DMV-required course fields ────────────────────────────────────────────
    completion_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    total_minutes = db.Column(db.Integer, nullable=False, default=340)   # must be 340
    score_percent = db.Column(db.Float, nullable=False)

    # ── School info (from environment / seed) ────────────────────────────────
    school_name = db.Column(
        db.String(255),
        nullable=False,
        default="GoTurboPass Online Traffic School",
    )
    # TODO: fill SCHOOL_DMV_NUMBER env var with the DMV-issued school number
    school_dmv_number = db.Column(
        db.String(50),
        nullable=True,
        default=lambda: os.getenv("SCHOOL_DMV_NUMBER", "PENDING"),
    )

    # ── Court / citation info (denormalized at generation time) ───────────────
    case_number = db.Column(db.String(100), nullable=True)
    court_name = db.Column(db.String(255), nullable=True)
    county_name = db.Column(db.String(255), nullable=True)
    certificate_due_date = db.Column(db.Date, nullable=True)

    # ── PDF storage ───────────────────────────────────────────────────────────
    # Relative path or cloud URL of the generated PDF.
    # Null until the PDF generation service runs (Phase 4+).
    pdf_url = db.Column(db.String(500), nullable=True)

    # ── TVCC API stub ─────────────────────────────────────────────────────────
    tvcc_submitted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    tvcc_confirmation = db.Column(db.String(255), nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    student = db.relationship("User", back_populates="certificates")
    citation = db.relationship("Citation")

    def __repr__(self):
        return f"<Certificate {self.certificate_no} student={self.student_id}>"

    def to_dict(self, include_pdf_url: bool = False):
        data = {
            "id": self.id,
            "certificate_no": self.certificate_no,
            "student_id": self.student_id,
            "student_name": f"{self.student_first_name} {self.student_last_name}",
            "student_dob": self.student_dob.isoformat() if self.student_dob else None,
            "student_dl_last4": self.student_dl_last4,
            "completion_at": self.completion_at.isoformat() if self.completion_at else None,
            "total_minutes": self.total_minutes,
            "score_percent": self.score_percent,
            "school_name": self.school_name,
            "school_dmv_number": self.school_dmv_number,
            "case_number": self.case_number,
            "court_name": self.court_name,
            "county_name": self.county_name,
            "certificate_due_date": (
                self.certificate_due_date.isoformat() if self.certificate_due_date else None
            ),
            "tvcc_submitted_at": (
                self.tvcc_submitted_at.isoformat() if self.tvcc_submitted_at else None
            ),
            "tvcc_confirmation": self.tvcc_confirmation,
        }
        if include_pdf_url:
            data["pdf_url"] = self.pdf_url
        return data
