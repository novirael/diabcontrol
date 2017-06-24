import dj_database_url

from diabcontrol.settings import *


ALLOWED_HOSTS = [
    '.herokuapp.com',
]

DATABASES = {
    'default': dj_database_url.config()
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
