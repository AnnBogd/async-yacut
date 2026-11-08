"""API-модуль приложения yacut."""

from http import HTTPStatus

from flask import jsonify, request, url_for

from .models import get_url_map, URLMap
from .error_handlers import APIError, InvalidShortLink
from . import app


@app.route('/api/id/', methods=['POST'])
def add_url_map() -> tuple:
    """Добавить короткую ссылку для указанной ссылки."""
    data = request.get_json(silent=True)
    if not data:
        raise APIError(message='Отсутствует тело запроса')
    if 'url' not in data:
        raise APIError(message='"url" является обязательным полем!')
    try:
        url_map = URLMap.create(
            data.get('url'),
            data.get('custom_id') or None
        )
    except InvalidShortLink as error:
        raise APIError(message=str(error))
    response_data = url_map.to_dict()
    short_link = url_for(
        'redirect_from_short_link',
        short_id=response_data.get('short'),
        _external=True
    )
    return (
        jsonify(url=response_data.get('original'), short_link=short_link),
        HTTPStatus.CREATED
    )


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id) -> tuple:
    """Получить оригинальную ссылку по короткому идентификатору."""
    url_map = get_url_map(short_id)
    if url_map is None:
        raise APIError(message='Указанный id не найден', status_code=404)
    response_data = url_map.to_dict()
    return jsonify(url=response_data.get('original')), HTTPStatus.OK
