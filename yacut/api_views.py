"""API-модуль приложения yacut."""

from flask import jsonify, request

from .error_handlers import APIError
from .support_func import (
    get_unique_short_id,
    get_url_map,
    is_short_ident_valid,
    is_short_ident_exists,
    save_short_ident
)
from . import app


@app.route('/api/id/', methods=['POST'])
def add_url_map() -> tuple:
    """Добавить которкую ссылку для указанной ссылки."""
    data = request.get_json(silent=True)
    if not data:
        raise APIError(message='Отсутствует тело запроса')
    if 'url' not in data:
        raise APIError(message='"url" является обязательным полем!')
    original_link = data.get('url')
    short_ident = data.get('custom_id') or None
    if short_ident is not None:
        if len(short_ident) > 16 or not is_short_ident_valid(short_ident):
            raise APIError(
                message='Указано недопустимое имя для короткой ссылки')
        if is_short_ident_exists(short_ident):
            raise APIError(
                message='Предложенный вариант короткой ссылки уже существует.')
    else:
        short_ident = get_unique_short_id()
    save_short_ident(short_ident, original_link)
    short_link = f'{request.host_url}{short_ident}'
    return jsonify(url=original_link, short_link=short_link), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id) -> tuple:
    """Получить оригинальную ссылку по короткому идентификатору."""
    url_map = get_url_map(short_id)
    if url_map is None:
        raise APIError(message='Указанный id не найден', status_code=404)
    return jsonify(url=url_map.original), 200
