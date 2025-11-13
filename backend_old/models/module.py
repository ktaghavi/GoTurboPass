from .db import db
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime



class Module(db.Model):
    """
    Course module with content, timer requirement, and optional quiz.
    """
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, nullable=False, unique=True)  # Ordering (1, 2, 3...)
    title = db.Column(db.String(255), nullable=False)
    min_seconds = db.Column(db.Integer, nullable=False, default=600)  # Timer requirement
    content_html = db.Column(db.Text, nullable=True)  # Course content
    active = db.Column(db.Boolean, nullable=False, default=True)

    # Optional quiz (one-to-one)
    quiz = relationship("Quiz", uselist=False, back_populates="module", cascade="all,delete-orphan")

    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    progress = db.relationship('Progress', backref='module', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Module {self.index}: {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'index': self.index,
            'title': self.title,
            'min_seconds': self.min_seconds,
            'content_html': self.content_html,
            'active': self.active,
            'quiz_id': self.quiz_id,
        }
