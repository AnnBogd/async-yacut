"""Обработчики исключений приложения yacut."""

from flask import jsonify, render_template
from wtforms.validators import ValidationError

from . import app, db


class InvalidShortLink(ValidationError):
    """Кастомное исключение для короткого идентификатора ссылки."""

    pass


class APIError(Exception):
    """Кастомное исключение для ошибок API."""
    status_code = 400

    def __init__(self, message, status_code=None) -> None:
        """Инициализировать исключение - передать сообщение и статус-код."""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self) -> dict:
        """Сериализацировать сообщения об ошибке."""
        return dict(message=self.message)


@app.errorhandler(APIError)
def invalid_api_usage(error) -> tuple:
    """Вернуть ответ кастомного обработчика ошибок API."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error) -> tuple:
    """Отобразить шаблон ошибки not found."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error) -> tuple:
    """Отобразить шаблон ошибки internal server error."""
    db.session.rollback()
    return render_template('500.html'), 500
