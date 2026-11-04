"""Константы приложения yacut."""

import re

PATTERN = re.compile(r'[a-zA-Z0-9]+')
RESERVED = {'files', 'api', 'static', 'admin', 'login', 'logout'}
