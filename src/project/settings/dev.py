from src.project.settings.main import *  # noqa


DEBUG = True


ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

INSTALLED_APPS.append('silk')  # noqa
MIDDLEWARE.append('silk.middleware.SilkyMiddleware')  # noqa
