from datetime import datetime
from models.db import db


class Citation(db.Model):
    __tablename__ = "citations"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    county_id = db.Column(
        db.Integer,
        db.ForeignKey("counties.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    court_id = db.Column(
        db.Integer,
        db.ForeignKey("courts.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    case_number = db.Column(db.String(100), nullable=True)
    docket_number = db.Column(db.String(100), nullable=True)

    certificate_due_date = db.Column(db.Date, nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", back_populates="citations")
    county = db.relationship("County")
    court = db.relationship("Court", back_populates="citations")

    def __repr__(self):
        return f"<Citation {self.id} user={self.user_id} court={self.court_id}>"
