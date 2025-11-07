from models import db
from datetime import datetime


class Certificate(db.Model):
    """
    Certificate of completion (generated after passing final exam).
    """
    __tablename__ = 'certificates'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    certificate_no = db.Column(db.String(50), unique=True, nullable=False)  # Unique cert number
    completion_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    score_percent = db.Column(db.Float, nullable=False)  # Final exam score

    # PDF path (for Phase 2+)
    pdf_url = db.Column(db.String(500), nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Certificate {self.certificate_no} Student {self.student_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'certificate_no': self.certificate_no,
            'completion_at': self.completion_at.isoformat() if self.completion_at else None,
            'score_percent': self.score_percent,
            'pdf_url': self.pdf_url,
        }
