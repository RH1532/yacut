from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .constants import (ALLOWED_CHARACTERS,
                        MISSING_REQUEST_BODY,
                        MISSING_URL_FIELD,
                        INVALID_SHORT_ID_NAME,
                        DUPLICATE_SHORT_ID,
                        INVALID_SHORT_ID)


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    url_map = URLMap()
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(MISSING_REQUEST_BODY)
    original_link = data.get('url')
    if not original_link:
        raise InvalidAPIUsage(MISSING_URL_FIELD)
    custom_id = data.get('custom_id')
    if not custom_id:
        custom_id = url_map.get_unique_short_id()
        data.update({'custom_id': custom_id})
    if len(custom_id) > 16:
        raise InvalidAPIUsage(INVALID_SHORT_ID_NAME)
    for value in custom_id:
        if value not in ALLOWED_CHARACTERS:
            raise InvalidAPIUsage(INVALID_SHORT_ID_NAME)
    existing_url = URLMap.query.filter_by(short=custom_id).first()
    if existing_url:
        raise InvalidAPIUsage(DUPLICATE_SHORT_ID)
    short_id = URLMap(original=original_link, short=custom_id)
    db.session.add(short_id)
    db.session.commit()
    return jsonify({'url': short_id.original, 'short_link': 'http://localhost/' + short_id.short}), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_short_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        return jsonify({'message': INVALID_SHORT_ID}), 404
    return jsonify({'url': url_map.original}), 200
