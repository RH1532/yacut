import random
from datetime import datetime

from yacut import db
from .constants import (ALLOWED_CHARACTERS,
                        ALLOWED_CHARACTERS_REGEX,
                        MAX_FIELD_LENGTH,
                        SHORT_LENGTH,
                        DUPLICATE_SHORT_ID,
                        INVALID_SHORT_ID_NAME,
                        MAX_CUSTOM_ID_LENGTH,
                        MAX_CUSTOM_ATTEMPTS,)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_FIELD_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_CUSTOM_ID_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_short_id(short_id):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def is_custom_id_unique(custom_id):
        return URLMap.query.filter(URLMap.short == custom_id).first() is None

    @staticmethod
    def get_unique_short_id():
        for _ in range(MAX_CUSTOM_ATTEMPTS):
            random_id = ''.join(random.choices(ALLOWED_CHARACTERS,
                                               k=SHORT_LENGTH))
            if URLMap.is_custom_id_unique(random_id):
                return random_id
        return URLMap.get_unique_short_id()

    @staticmethod
    def create_short_url(original_link, custom_id=None):
        if not custom_id:
            custom_id = URLMap.get_unique_short_id()
        if URLMap.is_invalid_short_id(custom_id):
            raise Exception(INVALID_SHORT_ID_NAME)
        if not URLMap.is_custom_id_unique(custom_id):
            raise Exception(DUPLICATE_SHORT_ID)
        new_url = URLMap(original=original_link, short=custom_id)
        #if URLMap.length_validation(new_url, MAX_CUSTOM_ID_LENGTH):
        #    raise Exception(TOO_CUSTOM_ID_LENGTH)
        db.session.add(new_url)
        db.session.commit()
        return new_url

    @staticmethod
    def length_validation(url, length):
        if len(url) > length:
            return True

    @staticmethod
    def is_invalid_short_id(short_id):
        if URLMap.length_validation(short_id, SHORT_LENGTH):
            raise ValueError(INVALID_SHORT_ID_NAME)
        if not ALLOWED_CHARACTERS_REGEX.match(short_id):
            raise ValueError(INVALID_SHORT_ID_NAME)
        return False
