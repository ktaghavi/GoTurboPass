"""
Exam + ExamAttempt — final exam (CA DMV OL-613 compliant).

CA DMV requirements (OL-613):
  • ≥ 25 questions drawn from the question bank
  • Questions and answer options randomized per attempt
  • 60-minute countdown, server-side enforced
  • Passing threshold: 70% correct (≥18/25)
  • Retake policy: a student may attempt up to MAX_EXAM_ATTEMPTS times
    before requiring instructor review (configurable in config.py)
  • Total course time (340 min) must be met before exam unlocks

ExamAttempt records:
  • started_at   — server clock when attempt was opened (not client clock)
  • expires_at   — started_at + 60 minutes; server rejects submissions after this
  • finished_at  — when the student submitted answers
  • question_order — JSON list of Question IDs in the order shown to the student
                     (stored for audit reproduction)
  • answer_order — JSON map of {question_id: [shuffled option keys]}
                   (stored for audit reproduction)
  • score_percent — graded server-side after submission
  • passed        — score_percent >= exam.pass_percent
"""
from datetime import datetime, timezone

from models.db import db


class Exam(db.Model):
    """
    The final exam definition.  Seed with one active Exam row.
    A and B versions are supported via the label field.
    """
    __tablename__ = "exams"

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False, unique=True)  # "Final A" | "Final B"
    pass_percent = db.Column(db.Integer, nullable=False, default=70)
    duration_seconds = db.Column(db.Integer, nullable=False, default=3600)  # 60 min
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
    questions = db.relationship(
        "Question",
        back_populates="exam",
        lazy="dynamic",
        cascade="all, delete-orphan",
        foreign_keys="Question.exam_id",
    )
    attempts = db.relationship(
        "ExamAttempt",
        back_populates="exam",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Exam {self.label}>"

    def to_dict(self, include_answers: bool = False):
        return {
            "id": self.id,
            "label": self.label,
            "pass_percent": self.pass_percent,
            "duration_seconds": self.duration_seconds,
            "active": self.active,
            "question_count": self.questions.count(),
        }


class ExamAttempt(db.Model):
    """
    One student's attempt at the final exam.

    COMPLIANCE NOTE: started_at and expires_at are set by the server.
    The client-side countdown timer is for UX only; the server MUST
    reject any submission received after expires_at.
    """
    __tablename__ = "exam_attempts"

    id = db.Column(db.Integer, primary_key=True)

    exam_id = db.Column(
        db.Integer,
        db.ForeignKey("exams.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Server clock timestamps (NEVER trust client-provided times)
    started_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    expires_at = db.Column(
        db.DateTime(timezone=True), nullable=False
    )  # set to started_at + exam.duration_seconds on creation
    finished_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Audit trail: exact question order and option shuffling shown to this student
    question_order = db.Column(db.JSON, nullable=True)   # [q_id, q_id, ...]
    answer_order = db.Column(db.JSON, nullable=True)     # {q_id: ["A","C","B","D"], ...}

    # Results (set after submission)
    score_percent = db.Column(db.Float, nullable=True)
    passed = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    exam = db.relationship("Exam", back_populates="attempts")
    student = db.relationship("User", back_populates="exam_attempts")

    def __repr__(self):
        return f"<ExamAttempt {self.id} student={self.student_id} passed={self.passed}>"

    @property
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def is_submitted(self) -> bool:
        return self.finished_at is not None

    def to_dict(self):
        return {
            "id": self.id,
            "exam_id": self.exam_id,
            "student_id": self.student_id,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "score_percent": self.score_percent,
            "passed": self.passed,
        }
