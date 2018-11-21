from .base import *  # noqa: F403 F401

DEBUG = True

ALLOWED_HOSTS = [
    '0.0.0.0'
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# a private key is necessary if this service is responsible for generating JWTs
PRIVATE_KEY = PemKeyLoader.load_private_key(os.getenv('DJANGO_JWT_PRIVATE_KEY', ''))  # noqa: F405
assert PRIVATE_KEY is not None, 'Private Key not found'

JWT_AUTH: dict = {
    **JWT_AUTH,
    'JWT_PRIVATE_KEY': PRIVATE_KEY,
    'JWT_VERIFY_EXPIRATION': False,
}
