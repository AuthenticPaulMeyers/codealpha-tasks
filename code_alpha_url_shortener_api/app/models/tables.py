from datetime import datetime
from ..extensions import db

class ShortUrls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_id = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

    def __repr__(self):
        return f"<ShortUrls {self.short_id} -> {self.original_url}>"