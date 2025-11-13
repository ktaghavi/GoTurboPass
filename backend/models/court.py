from models.db import db


class Court(db.Model):
    __tablename__ = "courts"

    id = db.Column(db.Integer, primary_key=True)

    county_id = db.Column(
        db.Integer,
        db.ForeignKey("counties.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    name = db.Column(db.String(255), nullable=False, index=True)
    court_type = db.Column(db.String(50), nullable=True)  # 'TRAFFIC', 'SUPERIOR', etc.

    dmv_code = db.Column(db.String(50), nullable=True)
    court_portal_code = db.Column(db.String(50), nullable=True)
    legacy_vendor_code = db.Column(db.String(50), nullable=True)

    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(50), nullable=True)

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    county = db.relationship("County", back_populates="courts")
    citations = db.relationship("Citation", back_populates="court", lazy="dynamic")

    def __repr__(self):
        return f"<Court {self.name} (county_id={self.county_id})>"
