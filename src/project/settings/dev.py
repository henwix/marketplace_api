from src.project.settings.main import *  # noqa


DEBUG = True


ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5500',
]

INSTALLED_APPS.append('silk')  # noqa
MIDDLEWARE.append('silk.middleware.SilkyMiddleware')  # noqa
