from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models for Alembic auto-detection
from models.user import User
from models.module import Module
from models.quiz import Quiz, Question
from models.exam import Exam, ExamAttempt
from models.progress import Progress
from models.certificate import Certificate
from models.inquiry import Inquiry
from models.audit_log import AuditLog

__all__ = [
    'db',
    'User',
    'Module',
    'Quiz',
    'Question',
    'Exam',
    'ExamAttempt',
    'Progress',
    'Certificate',
    'Inquiry',
    'AuditLog',
]
