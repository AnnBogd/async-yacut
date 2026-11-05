"""Формы приложения yacut."""

from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL

from yacut import db
from .constants import PATTERN, RESERVED
from .error_handlers import InvalidShortLink
from .models import URLMap


class URLForm(FlaskForm):
    """Форма для ссылок."""

    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(1, 16)
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        """Проверить вводимый короткий идентификатор ссылки."""
        if not field.data:
            return
        if not PATTERN.fullmatch(field.data):
            raise InvalidShortLink(
                'Указано недопустимое имя для короткой ссылки'
            )
        if field.data.lower() in RESERVED:
            raise InvalidShortLink(
                'Указано недопустимое имя для короткой ссылки'
            )
        stmt = db.select(URLMap).where(URLMap.short == field.data)
        if db.session.execute(stmt).scalar_one_or_none() is not None:
            raise InvalidShortLink(
                'Предложенный вариант короткой ссылки уже существует.')


class UploadFileForm(FlaskForm):
    """Форма для загрузки файлов."""

    files = MultipleFileField(
        'Выбрать файлы',
        validators=[FileRequired()]
    )
