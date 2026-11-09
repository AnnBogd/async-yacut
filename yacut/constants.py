"""Константы приложения yacut."""

import os
import re
from string import ascii_letters, digits

from dotenv import load_dotenv

load_dotenv()

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
DISK_TOKEN = os.getenv('DISK_TOKEN')
AUTH_HEADERS = {
    'Authorization': f'OAuth {DISK_TOKEN}'
}
LINK_ALPHABET = ascii_letters + digits
STANDARD_SHORT_LEN = 6
MAX_SHORT_LEN = 16
MIN_SHORT_LEN = 1
PATTERN = re.compile(
    rf'[a-zA-Z0-9]{{{MIN_SHORT_LEN},{MAX_SHORT_LEN}}}'   # noqa: E231
)
FORM_PATTERN = re.compile(
    rf'^[a-zA-Z0-9]{{{MIN_SHORT_LEN},{MAX_SHORT_LEN}}}$'   # noqa: E231
)
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
REQUEST_DOWNLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
UPLOAD_FILES_PREFIX = 'files'
RESERVED = {UPLOAD_FILES_PREFIX, 'api', 'static', 'admin', 'login', 'logout'}
UPLOAD_FILES_URL = f'/{UPLOAD_FILES_PREFIX}'
