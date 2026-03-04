"""
Quiz + Question — module-level knowledge check.

Each module has at most one Quiz.  A Quiz contains 4–10 MCQs.
Students must score >= Quiz.pass_percent to have the module count as complete.

The Question model is shared between Quiz and Exam:
  - quiz_id is set for module-level quiz questions
  - exam_id is set for final exam questions
  - Exactly one of (quiz_id, exam_id) should be non-null per row.

Answer key security:
  Question.answer_key is NEVER sent to the client.
  to_dict(include_answer=False) is the safe default for all API responses.
  Answers are only accessed server-side during quiz/exam grading.
"""
from datetime import datetime, timezone

from models.db import db


class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)

    module_id = db.Column(
        db.Integer,
        db.ForeignKey("modules.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,   # one quiz per module
        index=True,
    )

    # Minimum score to pass (percentage, 0–100)
    pass_percent = db.Column(db.Integer, nullable=False, default=70)

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
    module = db.relationship("Module", back_populates="quiz")
    questions = db.relationship(
        "Question",
        back_populates="quiz",
        lazy="dynamic",
        cascade="all, delete-orphan",
        foreign_keys="Question.quiz_id",
    )

    def __repr__(self):
        return f"<Quiz {self.id} module={self.module_id}>"

    def to_dict(self, include_answers: bool = False):
        return {
            "id": self.id,
            "module_id": self.module_id,
            "pass_percent": self.pass_percent,
            "questions": [
                q.to_dict(include_answer=include_answers)
                for q in self.questions
            ],
        }


class Question(db.Model):
    """
    MCQ shared by both quiz and final exam question banks.

    options format: {"A": "...", "B": "...", "C": "...", "D": "..."}
    answer_key:     one of "A", "B", "C", "D"
    """
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)

    # Exactly one of these should be set per row
    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    exam_id = db.Column(
        db.Integer,
        db.ForeignKey("exams.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    stem = db.Column(db.Text, nullable=False)           # Question text
    options = db.Column(db.JSON, nullable=False)        # {"A":…, "B":…, "C":…, "D":…}
    answer_key = db.Column(db.String(1), nullable=False)  # "A" | "B" | "C" | "D"

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    quiz = db.relationship(
        "Quiz",
        back_populates="questions",
        foreign_keys=[quiz_id],
    )
    exam = db.relationship(
        "Exam",
        back_populates="questions",
        foreign_keys=[exam_id],
    )

    def __repr__(self):
        return f"<Question {self.id}>"

    def to_dict(self, include_answer: bool = False):
        """
        Safe serialization.  NEVER set include_answer=True in API responses.
        """
        data = {
            "id": self.id,
            "stem": self.stem,
            "options": self.options,
        }
        if include_answer:
            data["answer_key"] = self.answer_key
        return data
