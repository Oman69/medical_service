import os
from datetime import timedelta
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Настройки базы данных
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://medical_user:medical_password@localhost:5432/medical_db',
    )
}

# Остальные настройки остаются такими же...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',

    # Local apps
    'apps.users',
    'apps.consultions',
    'apps.clinics',
]

# ... остальные настройки ...

# Настройки статических файлов для Docker
STATIC_URL = '/static/'
STATIC_ROOT = '/app/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media/'

# Настройки JWT из переменных окружения
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(
        days=int(os.environ.get('JWT_ACCESS_TOKEN_LIFETIME_DAYS', 1))
    ),
    'REFRESH_TOKEN_LIFETIME': timedelta(
        days=int(os.environ.get('JWT_REFRESH_TOKEN_LIFETIME_DAYS', 7))
    ),
}