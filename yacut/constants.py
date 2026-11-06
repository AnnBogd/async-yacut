"""Константы приложения yacut."""

import os
import re
from string import ascii_letters, digits

from dotenv import load_dotenv

load_dotenv()

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
DISK_TOKEN = os.environ.get('DISK_TOKEN')
AUTH_HEADERS = {
    'Authorization': f'OAuth {DISK_TOKEN}'
}
LINK_ALPHABET = ascii_letters + digits
PATTERN = re.compile(r'[a-zA-Z0-9]+')
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
REQUEST_DOWNLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
RESERVED = {'files', 'api', 'static', 'admin', 'login', 'logout'}
