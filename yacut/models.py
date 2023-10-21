import random
from datetime import datetime

from yacut import db
from .constants import (ALLOWED_CHARACTERS,
                        ALLOWED_CHARACTERS_REGEX,
                        MAX_FIELD_LENGTH,
                        SHORT_LENGTH,
                        DUPLICATE_SHORT,
                        INVALID_SHORT_NAME,
                        MAX_CUSTOM_LENGTH,
                        MAX_CUSTOM_ATTEMPTS,
                        SHORT_CREATION_ERROR)
from .exceptions import InvalidShortNameError, DuplicateShortError


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_FIELD_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_CUSTOM_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_id(short_id):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def is_custom_id_unique(custom_id):
        return URLMap.get_id(custom_id) is None

    @staticmethod
    def get_unique_short_id():
        for _ in range(MAX_CUSTOM_ATTEMPTS):
            random_id = ''.join(random.choices(ALLOWED_CHARACTERS,
                                               k=SHORT_LENGTH))
            if URLMap.is_custom_id_unique(random_id):
                return random_id
        raise InvalidShortNameError(SHORT_CREATION_ERROR)

    @staticmethod
    def create(original_link, custom_id=None):
        if not custom_id:
            try:
                custom_id = URLMap.get_unique_short_id()
            except Exception as e:
                raise InvalidShortNameError(str(e))
        if len(custom_id) > SHORT_LENGTH:
            raise InvalidShortNameError(INVALID_SHORT_NAME)
        if not ALLOWED_CHARACTERS_REGEX.match(custom_id):
            raise InvalidShortNameError(INVALID_SHORT_NAME)
        if not URLMap.is_custom_id_unique(custom_id):
            raise DuplicateShortError(DUPLICATE_SHORT)
        new_url = URLMap(original=original_link, short=custom_id)
        db.session.add(new_url)
        db.session.commit()
        return new_url
