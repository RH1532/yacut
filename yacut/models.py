import random
from datetime import datetime
from flask import url_for

from yacut import db
from .constants import (ALLOWED_CHARACTERS,
                        ALLOWED_CHARACTERS_REGEX,
                        MAX_FIELD_LENGTH,
                        SHORT_LENGTH,
                        DUPLICATE_SHORT,
                        MAX_SHORT_LENGTH,
                        MAX_SHORT_ATTEMPTS,
                        SHORT_CREATION_ERROR,
                        INVALID_SHORT_NAME,
                        SHORT_REDIRECT_FUNCTION)
from .exceptions import InvalidShortNameError, DuplicateShortError


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_FIELD_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get(short_id):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def get_unique_short_id():
        for _ in range(MAX_SHORT_ATTEMPTS):
            random_id = ''.join(random.choices(ALLOWED_CHARACTERS,
                                               k=SHORT_LENGTH))
            if URLMap.get(random_id) is None:
                return random_id
        raise InvalidShortNameError(SHORT_CREATION_ERROR)

    @staticmethod
    def create(original_link, custom_id=None):
        if custom_id:
            if (len(custom_id) > MAX_SHORT_LENGTH or not ALLOWED_CHARACTERS_REGEX.match(custom_id)):
                raise InvalidShortNameError(INVALID_SHORT_NAME)
            if URLMap.get(custom_id):
                raise DuplicateShortError(DUPLICATE_SHORT)
        else:
            custom_id = URLMap.get_unique_short_id()
        url_map = URLMap(original=original_link, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        short_url = url_for(SHORT_REDIRECT_FUNCTION, short_id=url_map.short, _external=True)
        return url_map, short_url
