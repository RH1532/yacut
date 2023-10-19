import random
from datetime import datetime

from yacut import db
from .constants import ALLOWED_CHARACTERS


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(100), nullable=False)
    short = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def get_unique_short_id(self):
        while True:
            random_id = ''.join(
                random.choice(ALLOWED_CHARACTERS) for _ in range(6))
            if not URLMap.query.filter_by(short=random_id).first():
                return random_id
