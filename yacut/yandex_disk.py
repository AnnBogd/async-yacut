"""Модуль для функций загрузки файлов на Яндекс диск."""

import asyncio

import aiohttp
import urllib

from .constants import AUTH_HEADERS, REQUEST_DOWNLOAD_URL, REQUEST_UPLOAD_URL


async def upload_files(session, file) -> str:
    """Загрузить файл на Яндекс диск и получить ссылку на скачивание."""
    async with session.get(
        REQUEST_UPLOAD_URL,
        params={
            'path': f'app:/{file.filename}',   # noqa: E231
            'overwrite': 'True'
        },
        headers=AUTH_HEADERS
    ) as response:
        response.raise_for_status()
        data = await response.json()
        upload_url = data.get('href')
    async with session.put(data=file.read(), url=upload_url) as response:
        response.raise_for_status()
        file_location = urllib.parse.unquote(response.headers.get('Location'))
    file_location = file_location.replace('/disk', '')
    async with session.get(
        headers=AUTH_HEADERS,
        url=REQUEST_DOWNLOAD_URL,
        params={'path': file_location}
    ) as response:
        response.raise_for_status()
        data = await response.json()
        download_link = data.get('href')
    return download_link


async def async_upload_files(files) -> list:
    """Создать сессию для загрузки файлов."""
    async with aiohttp.ClientSession() as session:
        tasks = [upload_files(session, file) for file in files]
        results = await asyncio.gather(*tasks)
        return results
