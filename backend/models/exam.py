from models import db
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

    # Relationships
    questions = db.relationship('Question', backref='exam', lazy='dynamic', cascade='all, delete-orphan')
    attempts = db.relationship('ExamAttempt', backref='exam_ref', lazy='dynamic', cascade='all, delete-orphan')

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
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    exam_label = db.Column(db.String(50), nullable=False)  # "Final A" or "Final B"
    score_percent = db.Column(db.Float, nullable=True)
    passed = db.Column(db.Boolean, nullable=False, default=False)

    # Metadata
    started_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, nullable=True)
    question_order = db.Column(db.JSON, nullable=True)  # [q_id1, q_id2, ...] randomized order

    def __repr__(self):
        return f'<ExamAttempt {self.id} Student {self.student_id} {self.exam_label}>'

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'exam_label': self.exam_label,
            'score_percent': self.score_percent,
            'passed': self.passed,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
        }
