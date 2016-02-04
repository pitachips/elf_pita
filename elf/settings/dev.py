from .common import *

INSTALLED_APPS += [
    'debug_toolbar',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

