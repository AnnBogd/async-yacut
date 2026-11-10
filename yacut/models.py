"""Модели приложения yacut."""

from datetime import datetime, timezone
from random import choices
from typing import Optional

from flask import url_for

from .constants import (
    LINK_ALPHABET,
    MAX_SHORT_LEN,
    RESERVED,
    STANDARD_SHORT_LEN
)
from .error_handlers import InvalidShortLink
from . import db


class URLMap(db.Model):
    """Модель ссылки."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(MAX_SHORT_LEN),
        unique=True,
        index=True, nullable=False
    )
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    @classmethod
    def is_short_valid(cls, short_ident: str) -> bool:
        """Проверить валидность короткого идентификатора."""
        return (short_ident.lower() not in RESERVED
                and cls.get_url_map(short_ident) is None)

    @classmethod
    def create(
            cls,
            original_link: str,
            short_ident: Optional[str] = None
    ) -> 'URLMap':
        """Создать и сохранить короткую ссылку.

        Проверяет short_ident, генерирует при необходимости,
        сохраняет запись и возвращает короткий идентификатор.
        Бросает InvalidShortLink при проблемах.
        """
        if short_ident is None:
            short_ident = cls.get_unique_short_id()
        elif not URLMap.is_short_valid(short_ident):
            raise InvalidShortLink(
                'Предложенный вариант короткой ссылки '
                'уже существует.'
            )
        new_url_map = URLMap(
            original=original_link,
            short=short_ident
        )
        db.session.add(new_url_map)
        db.session.commit()
        return new_url_map

    @classmethod
    def get_url_map(cls, short_ident: str) -> 'URLMap':
        """Получить объект из базы данных по короткому идентификатору."""
        return db.session.execute(
            db.select(URLMap).where(URLMap.short == short_ident)
        ).scalar_one_or_none()

    @classmethod
    def get_unique_short_id(cls, link_len: int = STANDARD_SHORT_LEN) -> str:
        """Сгенерировать случайную короткую ссылку."""
        while True:
            short_ident = ''.join(choices(LINK_ALPHABET, k=link_len))
            if URLMap.is_short_valid(short_ident):
                return short_ident

    def to_dict(self):
        """Сериализовать данные для ответа API."""
        return dict(
            original=self.original,
            short_link=url_for(
                'redirect_from_short_link',
                short_id=self.short,
                _external=True
            )
        )
