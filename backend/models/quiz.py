from models import db
from datetime import datetime
import json


class Quiz(db.Model):
    """
    Quiz attached to a module (4-10 MCQs, ≥70% to pass).
    """
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=True)
    pass_percent = db.Column(db.Integer, nullable=False, default=70)

    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy='dynamic', cascade='all, delete-orphan')
    module = db.relationship('Module', backref='quiz', foreign_keys='Quiz.module_id')

    def __repr__(self):
        return f'<Quiz {self.id} for Module {self.module_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'pass_percent': self.pass_percent,
            'questions': [q.to_dict() for q in self.questions],
        }


class Question(db.Model):
    """
    MCQ question for either Quiz or Exam.
    """
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=True)

    stem = db.Column(db.Text, nullable=False)  # Question text
    options = db.Column(db.JSON, nullable=False)  # {"A": "...", "B": "...", "C": "...", "D": "..."}
    answer_key = db.Column(db.String(1), nullable=False)  # "A", "B", "C", or "D"

    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Question {self.id}>'

    def to_dict(self, include_answer=False):
        """Safe serialization - excludes answer_key unless requested."""
        data = {
            'id': self.id,
            'stem': self.stem,
            'options': self.options,
        }
        if include_answer:
            data['answer_key'] = self.answer_key
        return data
