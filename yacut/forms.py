"""Формы приложения yacut."""

from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .constants import FORM_PATTERN, MAX_SHORT_LEN, MIN_SHORT_LEN


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
            Length(MIN_SHORT_LEN, MAX_SHORT_LEN),
            Regexp(
                regex=FORM_PATTERN,
                message='Указано недопустимое имя для короткой ссылки'
            )
        ]
    )
    submit = SubmitField('Создать')


class UploadFileForm(FlaskForm):
    """Форма для загрузки файлов."""

    files = MultipleFileField(
        'Выбрать файлы',
        validators=[FileRequired(message='Файл не выбран')]
    )
    submit = SubmitField('Загрузить')
