"""Константы приложения yacut."""

import re
from string import ascii_letters, digits

LINK_ALPHABET = ascii_letters + digits
PATTERN = re.compile(r'[a-zA-Z0-9]+')
RESERVED = {'files', 'api', 'static', 'admin', 'login', 'logout'}
