"""Представления приложения yacut."""

from random import choices

from flask import render_template, request

from .constants import LINK_ALPHABET, RESERVED
from .forms import UploadFileForm, URLForm
from .models import URLMap
from . import app, db


def get_unique_short_id(link_len: int = 6) -> str:
    """Сгенерировать случайную короткую ссылку."""
    while True:
        short_ident = ''.join(choices(LINK_ALPHABET, k=link_len))
        if short_ident.lower() in RESERVED:
            continue
        stmt = db.select(URLMap).where(URLMap.short == short_ident)
        if db.session.execute(stmt).scalar_one_or_none() is None:
            return short_ident


@app.route('/', methods=['GET', 'POST'])
def index_view() -> str:
    """Отобразить главную страницу проекта."""
    form = URLForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data or None
        short_ident = get_unique_short_id() if custom_id is None else custom_id
        short_link = f'{request.host_url}{short_ident}'
        new_url_map = URLMap(
            original=original_link,
            short=short_ident
        )
        db.session.add(new_url_map)
        db.session.commit()
        return render_template(
            'index.html',
            short_link=short_link,
            form=form
        )
    return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def upload_files():
    """Загрузить файлы на Яндекс диск."""
    form = UploadFileForm()
    if form.validate_on_submit():
        # пишу функции загрузки файла
        files = form.files.data
        async_upload_files(files)
