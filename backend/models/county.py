from models.db import db


class County(db.Model):
    __tablename__ = "counties"

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(2), nullable=False, index=True)  # 'CA'
    name = db.Column(db.String(255), nullable=False, index=True)

    # External mapping (DMV / portal / legacy vendor codes)
    dmv_code = db.Column(db.String(50), nullable=True)
    court_portal_code = db.Column(db.String(50), nullable=True)
    legacy_vendor_code = db.Column(db.String(50), nullable=True)

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    courts = db.relationship("Court", back_populates="county", lazy="dynamic")

    def __repr__(self):
        return f"<County {self.state} - {self.name}>"
