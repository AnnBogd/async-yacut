"""Вспомогательные функции приложения yacut."""

from random import choices

from .constants import LINK_ALPHABET, PATTERN, RESERVED
from .models import URLMap
from . import db


def save_short_ident(
        short_ident: str, original_link: str) -> None:
    """Сохранить в базе данных короткую ссылку."""
    new_url_map = URLMap(
        original=original_link,
        short=short_ident
    )
    db.session.add(new_url_map)
    db.session.commit()


def is_short_ident_exists(short_ident: str) -> bool:
    """Проверить, есть ли уже такой короткий идентификатор."""
    stmt = db.select(URLMap.id).where(URLMap.short == short_ident)
    return db.session.execute(stmt).scalar_one_or_none() is not None


def is_short_ident_valid(short_ident: str) -> bool:
    """Проверить валидность короткого идентификатора."""
    return bool(PATTERN.fullmatch(short_ident))


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
        if not is_short_ident_exists(short_ident):
            return short_ident
