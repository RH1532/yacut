from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .constants import (MISSING_REQUEST_BODY,
                        MISSING_URL_FIELD,
                        INVALID_SHORT)
from .exceptions import DuplicateShortError, InvalidShortNameError


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(MISSING_REQUEST_BODY)
    original_link = data.get('url')
    if not original_link:
        raise InvalidAPIUsage(MISSING_URL_FIELD)
    short = data.get('custom_id')
    try:
        url_map = URLMap.create(original_link, short, enable_validation='yes')
    except (InvalidShortNameError, DuplicateShortError) as e:
        raise InvalidAPIUsage(str(e))
    return jsonify({
        'url': url_map.original,
        'short_link': URLMap.short_url(url_map)
    }), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_short_url(short_id):
    url_map = URLMap.get(short_id)
    if not url_map:
        raise InvalidAPIUsage(INVALID_SHORT, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
