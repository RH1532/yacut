import random
from datetime import datetime
from flask import url_for

from yacut import db
from .constants import (ALLOWED_CHARACTERS,
                        MAX_FIELD_LENGTH,
                        SHORT_LENGTH,
                        DUPLICATE_SHORT,
                        MAX_SHORT_LENGTH,
                        MAX_SHORT_ATTEMPTS,
                        SHORT_CREATION_ERROR,
                        SHORT_REDIRECT_FUNCTION,
                        MAX_SHORT_LENGTH,
                        ALLOWED_CHARACTERS_REGEX,
                        INVALID_SHORT_NAME,
                        MAX_FIELD_LENGTH)
from .exceptions import DuplicateShortError, InvalidShortNameError, OriginalLinkError


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_FIELD_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short():
        for _ in range(MAX_SHORT_ATTEMPTS):
            short = ''.join(random.choices(ALLOWED_CHARACTERS,
                                           k=SHORT_LENGTH))
            if URLMap.get(short) is None:
                return short
        raise DuplicateShortError(SHORT_CREATION_ERROR)

    @staticmethod
    def create(original_link, short=None, source=None):
        if source:
            if len(original_link) > MAX_FIELD_LENGTH:
                raise OriginalLinkError(INVALID_SHORT_NAME)
            if short and (len(short) > MAX_SHORT_LENGTH
                          or not ALLOWED_CHARACTERS_REGEX.match(short)):
                raise InvalidShortNameError(INVALID_SHORT_NAME)
        if not short:
            short = URLMap.get_unique_short()
        elif URLMap.get(short):
            raise DuplicateShortError(DUPLICATE_SHORT)
        url_map = URLMap(original=original_link, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def short_url(url_map):
        return url_for(SHORT_REDIRECT_FUNCTION, short_id=url_map.short, _external=True)
