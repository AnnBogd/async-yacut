"""Представления приложения yacut."""

from flask import Response, abort, redirect, render_template, request

from .forms import UploadFileForm, URLForm
from .support_func import get_unique_short_id, get_url_map, save_short_ident
from .yandex_disk import async_upload_files
from . import app


@app.route('/', methods=['GET', 'POST'])
def index_view() -> str:
    """Отобразить главную страницу проекта и создать короткую ссылку."""
    form = URLForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data or None
        short_ident = get_unique_short_id() if custom_id is None else custom_id
        short_link = f'{request.host_url}{short_ident}'
        save_short_ident(short_ident, original_link)
        return render_template(
            'index.html',
            short_link=short_link,
            form=form
        )
    return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def upload_files() -> str:
    """Загрузить файлы на Яндекс диск через сайт."""
    form = UploadFileForm()
    if form.validate_on_submit():
        files = form.files.data
        if not files:
            form.files.errors.append('Файл не выбран.')
            return render_template('files.html', form=form)
        filenames = [file.filename for file in files]
        download_links = await async_upload_files(files)
        short_links = []
        for link in download_links:
            short_ident = get_unique_short_id()
            short_link = f'{request.host_url}{short_ident}'
            save_short_ident(short_ident, link)
            short_links.append(short_link)
        files_data = list(zip(filenames, short_links))
        return render_template(
            'files.html',
            form=form,
            files_data=files_data
        )
    return render_template('files.html', form=form)


@app.route('/<short_id>', methods=['GET'])
def redirect_from_short_link(short_id: str) -> Response:
    """Выполнить переадресацию с корткой ссылки."""
    url_map = get_url_map(short_id)
    if url_map is None:
        abort(404)
    return redirect(url_map.original)
