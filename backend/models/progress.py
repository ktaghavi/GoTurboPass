"""
Progress — per-student, per-module timer and quiz tracking.

One row per (student_id, module_id) pair.  This row is the authoritative
record of how much verified time a student has spent in a module.

Server-side timer design (to be wired up in the course engine sprint):
  • timer_seconds      — accumulated verified seconds (updated on heartbeat)
  • last_heartbeat_at  — server timestamp of the last valid heartbeat
                         Used to detect time fraud (gap > expected interval)
  • started_at         — when the student first entered the module
  • completed_at       — set when timer_seconds >= module.min_seconds
                         AND quiz_passed is True (or module has no quiz)

Anti-cheat rules enforced at the heartbeat endpoint:
  1. Heartbeat interval must not exceed HEARTBEAT_GRACE_SECONDS
     (configurable, default 35 s for a 30 s client interval).
  2. timer_seconds increments only by the actual elapsed wall-clock gap,
     capped at HEARTBEAT_INTERVAL_SECONDS to prevent catch-up fraud.
  3. Tab-switch events set tab_switch_count; repeated violations can pause timer.
"""
from datetime import datetime, timezone

from models.db import db


class Progress(db.Model):
    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    module_id = db.Column(
        db.Integer,
        db.ForeignKey("modules.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Timer tracking ───────────────────────────────────────────────────────
    started_at = db.Column(db.DateTime(timezone=True), nullable=True)
    timer_seconds = db.Column(db.Integer, nullable=False, default=0)
    last_heartbeat_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Anti-cheat: count how many times the student switched tabs during this module
    tab_switch_count = db.Column(db.Integer, nullable=False, default=0)

    # ── Completion ───────────────────────────────────────────────────────────
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    quiz_score = db.Column(db.Float, nullable=True)        # 0.0–100.0
    quiz_passed = db.Column(db.Boolean, nullable=True)

    # ── Constraints ──────────────────────────────────────────────────────────
    __table_args__ = (
        db.UniqueConstraint("student_id", "module_id", name="uq_progress_student_module"),
    )

    # ── Relationships ────────────────────────────────────────────────────────
    student = db.relationship("User", back_populates="progress_records")
    module = db.relationship("Module", back_populates="progress_records")

    def __repr__(self):
        return f"<Progress student={self.student_id} module={self.module_id} secs={self.timer_seconds}>"

    @property
    def is_complete(self) -> bool:
        return self.completed_at is not None

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "module_id": self.module_id,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "timer_seconds": self.timer_seconds,
            "last_heartbeat_at": (
                self.last_heartbeat_at.isoformat() if self.last_heartbeat_at else None
            ),
            "tab_switch_count": self.tab_switch_count,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "quiz_score": self.quiz_score,
            "quiz_passed": self.quiz_passed,
        }
