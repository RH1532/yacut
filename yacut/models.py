import random
import re
from datetime import datetime

from yacut import db
from .constants import (ALLOWED_CHARACTERS,
                        MAX_STRING_LENGTH,
                        SHORT_URL_LENGTH,
                        DUPLICATE_SHORT_ID,
                        INVALID_SHORT_ID_NAME,
                        MAX_CUSTOM_ID_LENGTH,)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_STRING_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_STRING_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def find_by_short_id(cls, short_id):
        return cls.query.filter_by(short=short_id).first()

    def get_original_link(self):
        return self.original

    @staticmethod
    def is_custom_id_unique(custom_id, original_link):
        return URLMap.query.filter(
            (URLMap.short == custom_id) | (URLMap.original == original_link)
        ).first() is None

    @classmethod
    def get_unique_short_id(cls, original_link):
        for _ in range(MAX_CUSTOM_ID_LENGTH):
            random_id = ''.join(random.choices(ALLOWED_CHARACTERS, k=SHORT_URL_LENGTH))
            if cls.is_custom_id_unique(random_id, original_link):
                return random_id
        return None

    @classmethod
    def create_short_url(cls, original_link, custom_id=None):
        if not custom_id:
            custom_id = cls.get_unique_short_id(original_link)
        if custom_id:
            if cls.is_invalid_short_id(custom_id):
                return None, INVALID_SHORT_ID_NAME
            if not cls.is_custom_id_unique(custom_id, original_link):
                return None, DUPLICATE_SHORT_ID
            new_url = cls(original=original_link, short=custom_id)
            db.session.add(new_url)
            db.session.commit()
            return new_url, None
        return None, DUPLICATE_SHORT_ID

    @classmethod
    def is_invalid_short_id(cls, short_id):
        if len(short_id) > SHORT_URL_LENGTH:
            return True
        if not re.match(f'^[{re.escape("".join(ALLOWED_CHARACTERS))}]*$', short_id):
            return True
        return False
