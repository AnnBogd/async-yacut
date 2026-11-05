"""Представления приложения yacut."""

from random import choices

from flask import render_template

from .constants import LINK_ALPHABET
from . import app, db


def get_unique_short_id(link_len=6):
    """Сгенерировать случайную короткую ссылку."""
    return ''.join(choices(LINK_ALPHABET, k=link_len))


@app.route('/')
def index():
    """Отобразить главную страницу проекта."""
    # не готовы шаблоны
    # сделаны base, header, footer
    # делается index - форма
    render_template()
