from .db import db
from sqlalchemy.orm import relationship
from datetime import datetime


class Progress(db.Model):
    """
    Tracks a student's progress through a module (timer + quiz).
    """
    __tablename__ = 'progress'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False, index=True)

    # Timer tracking
    started_at = db.Column(db.DateTime, nullable=True)
    timer_seconds = db.Column(db.Integer, nullable=False, default=0)  # Accumulated time

    # Completion
    completed_at = db.Column(db.DateTime, nullable=True)
    quiz_score = db.Column(db.Float, nullable=True)
    quiz_passed = db.Column(db.Boolean, nullable=True)

    # Composite unique constraint
    __table_args__ = (
        db.UniqueConstraint('student_id', 'module_id', name='_student_module_uc'),
    )

    def __repr__(self):
        return f'<Progress Student {self.student_id} Module {self.module_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'module_id': self.module_id,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'timer_seconds': self.timer_seconds,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'quiz_score': self.quiz_score,
            'quiz_passed': self.quiz_passed,
        }
