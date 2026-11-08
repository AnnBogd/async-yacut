"""Модели приложения yacut."""

from datetime import datetime, timezone
from random import choices
from typing import Optional

from .constants import LINK_ALPHABET, PATTERN, RESERVED
from .error_handlers import InvalidShortLink
from . import db


class URLMap(db.Model):
    """Модель ссылки."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), unique=True, index=True, nullable=False)
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    @staticmethod
    def create(original_link: str, short_ident: Optional[str] = None) -> str:
        """Создать и сохранить короткую ссылку.

        Проверяет short_ident, генерирует при необходимости,
        сохраняет запись и возвращает короткий идентификатор.
        Бросает InvalidShortLink при проблемах.
        """
        if short_ident is not None:
            if not PATTERN.fullmatch(short_ident):
                raise InvalidShortLink(
                    'Указано недопустимое имя для короткой ссылки')
            if (
                short_ident.lower() in RESERVED
                or get_url_map(short_ident) is not None
            ):
                raise InvalidShortLink(
                    'Предложенный вариант короткой ссылки '
                    'уже существует.'
                )
        else:
            short_ident = get_unique_short_id()
        new_url_map = URLMap(
            original=original_link,
            short=short_ident
        )
        db.session.add(new_url_map)
        db.session.commit()
        return new_url_map

    def to_dict(self):
        """Сериализовать данные для ответа API."""
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp
        )


def get_url_map(short_ident: str) -> URLMap:
    """Получить объект из базы данных по короткому идентификатору."""
    return db.session.execute(
        db.select(URLMap).where(URLMap.short == short_ident)
    ).scalar_one_or_none()


def get_unique_short_id(link_len: int = 6) -> str:
    """Сгенерировать случайную короткую ссылку."""
    while True:
        short_ident = ''.join(choices(LINK_ALPHABET, k=link_len))
        if short_ident.lower() in RESERVED:
            continue
        if get_url_map(short_ident) is None:
            return short_ident
