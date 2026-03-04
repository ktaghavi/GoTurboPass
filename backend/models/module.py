"""
Module — one of the 12 CA DMV OL-613 curriculum units.

CONTENT POLICY (carry this forward through the build):
  content_html is READ-ONLY source material approved by the CA DMV.
  It must never be rewritten, condensed, paraphrased, or restructured.
  Only format it for HTML delivery.  Content will be dropped in after
  the delivery infrastructure is built and approved.

Timer requirements (min_seconds):
  Each module must be on-screen for at least min_seconds of verified
  server-side time before the student is allowed to proceed.
  The total across all 12 modules must reach 20,400 seconds (340 min).
  Default per-module: 1,700 seconds (≈28.3 min × 12 = 340 min).
"""
from datetime import datetime, timezone

from models.db import db


# 340 minutes ÷ 12 modules = 1,700 seconds per module
DEFAULT_MODULE_SECONDS = 1_700


class Module(db.Model):
    __tablename__ = "modules"

    id = db.Column(db.Integer, primary_key=True)

    # Sequential order (1–12); must be unique and contiguous
    index = db.Column(db.Integer, nullable=False, unique=True, index=True)

    title = db.Column(db.String(255), nullable=False)

    # Minimum verified on-page seconds before module is marked complete.
    # Override per-module if the DMV specifies non-uniform times.
    min_seconds = db.Column(
        db.Integer, nullable=False, default=DEFAULT_MODULE_SECONDS
    )

    # ── CONTENT PLACEHOLDER ──────────────────────────────────────────────────
    # Drop DMV-approved HTML here for each module.
    # Do NOT modify instructional text — formatting only.
    # ─────────────────────────────────────────────────────────────────────────
    content_html = db.Column(db.Text, nullable=True)

    active = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    quiz = db.relationship(
        "Quiz",
        uselist=False,
        back_populates="module",
        cascade="all, delete-orphan",
    )
    progress_records = db.relationship(
        "Progress",
        back_populates="module",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Module {self.index}: {self.title}>"

    def to_dict(self, include_content: bool = False):
        data = {
            "id": self.id,
            "index": self.index,
            "title": self.title,
            "min_seconds": self.min_seconds,
            "active": self.active,
            "quiz_id": self.quiz.id if self.quiz else None,
            "has_content": self.content_html is not None,
        }
        if include_content:
            data["content_html"] = self.content_html
        return data
