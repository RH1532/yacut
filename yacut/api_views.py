from http import HTTPStatus

from flask import jsonify, url_for, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .constants import (MISSING_REQUEST_BODY,
                        MISSING_URL_FIELD,
                        INVALID_SHORT_ID,)


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(MISSING_REQUEST_BODY)
    original_link = data.get('url')
    if not original_link:
        raise InvalidAPIUsage(MISSING_URL_FIELD)
    custom_id = data.get('custom_id')
    try:
        url_map = URLMap.create_short_url(original_link, custom_id)
    except Exception as e:
        raise InvalidAPIUsage(str(e))
    return jsonify({'url': url_map.original,
                    'short_link': url_for('redirect_to_original',
                                          short_id=url_map.short,
                                          _external=True)}), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_short_url(short_id):
    url_map = URLMap.get_short_id(short_id)
    if not url_map:
        raise InvalidAPIUsage(INVALID_SHORT_ID, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
