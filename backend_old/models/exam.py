from .db import db
from sqlalchemy.orm import relationship
from datetime import datetime


class Exam(db.Model):
    """
    Final exam (A or B version, ≥25 questions, randomized order).
    """
    __tablename__ = 'exams'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False, unique=True)  # "Final A" or "Final B"
    pass_percent = db.Column(db.Integer, nullable=False, default=70)
    active = db.Column(db.Boolean, nullable=False, default=True)

    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # If you truly have exam-specific questions (separate from module quizzes), keep this.
    # Otherwise you can remove this relationship if "Question" belongs only to Quiz, not Exam.
    questions = db.relationship(
        'Question',
        backref='exam',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # ✅ Proper parent→child relation requiring ExamAttempt.exam_id FK
    attempts = db.relationship(
        'ExamAttempt',
        back_populates='exam',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Exam {self.label}>'

    def to_dict(self, include_answers=False):
        return {
            'id': self.id,
            'label': self.label,
            'pass_percent': self.pass_percent,
            'active': self.active,
            'questions': [q.to_dict(include_answer=include_answers) for q in self.questions],
        }


class ExamAttempt(db.Model):
    """
    Records a student's attempt at the final exam.
    """
    __tablename__ = 'exam_attempts'

    id = db.Column(db.Integer, primary_key=True)

    # ✅ Add the missing FK to exams.id
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False, index=True)

    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # You can keep exam_label as a denormalized copy for convenience / reporting,
    # but the relational link must be exam_id.
    exam_label = db.Column(db.String(50), nullable=False)

    score_percent = db.Column(db.Float, nullable=True)
    passed = db.Column(db.Boolean, nullable=False, default=False)

    # Metadata
    started_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, nullable=True)
    question_order = db.Column(db.JSON, nullable=True)  # [q_id1, q_id2, ...] randomized order

    # ✅ Child→parent relationship
    exam = relationship('Exam', back_populates='attempts')

    def __repr__(self):
        return f'<ExamAttempt {self.id} Student {self.student_id} {self.exam_label}>'

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'exam_id': self.exam_id,
            'exam_label': self.exam_label,
            'score_percent': self.score_percent,
            'passed': self.passed,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
        }