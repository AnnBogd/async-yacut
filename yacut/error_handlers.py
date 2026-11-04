"""Обработчики исключений приложения yacut."""

from wtforms.validators import ValidationError


class InvalidShortLink(ValidationError):
    """Кастомное исключение для короткого идентификатора ссылки."""

    pass
