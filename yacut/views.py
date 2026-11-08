"""Представления приложения yacut."""

import asyncio

import aiohttp
from flask import Response, flash, redirect, render_template, url_for

from .constants import UPLOAD_FILES_URL
from .forms import UploadFileForm, URLForm
from .error_handlers import InvalidShortLink
from .models import URLMap
from .yandex_disk import async_upload_files
from . import app


@app.route('/', methods=['GET', 'POST'])
def index_view() -> str:
    """Отобразить главную страницу проекта и создать короткую ссылку."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(
            form.original_link.data,
            form.custom_id.data or None
        )
    except InvalidShortLink as error:
        flash(str(error), 'danger')
        return render_template('index.html', form=form)
    response_data = url_map.to_dict()
    short_link = url_for(
        'redirect_from_short_link',
        short_id=response_data.get('short'),
        _external=True
    )
    return render_template(
        'index.html',
        short_link=short_link,
        form=form
    )


@app.route(UPLOAD_FILES_URL, methods=['GET', 'POST'])
async def upload_files() -> str:
    """Загрузить файлы на Яндекс диск через сайт."""
    form = UploadFileForm()
    if not form.validate_on_submit():
        return render_template('files.html', form=form)
    files = form.files.data
    if not files:
        form.files.errors.append('Файл не выбран.')
        return render_template('files.html', form=form)
    filenames = [file.filename for file in files]
    try:
        download_links = await async_upload_files(files)
    except (aiohttp.ClientError, asyncio.TimeoutError):
        flash(
            'Не удалось загрузить файлы на Яндекс.Диск. Попробуйте позже.',
            'danger'
        )
        return render_template('files.html', form=form)
    short_links = []
    for link in download_links:
        url_map = URLMap.create(link)
        response_data = url_map.to_dict()
        short_link = url_for(
            'redirect_from_short_link',
            short_id=response_data.get('short'),
            _external=True
        )
        short_links.append(short_link)
    files_data = list(zip(filenames, short_links))
    return render_template(
        'files.html',
        form=form,
        files_data=files_data
    )


@app.route('/<short_id>', methods=['GET'])
def redirect_from_short_link(short_id: str) -> Response:
    """Выполнить переадресацию с короткой ссылки."""
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
