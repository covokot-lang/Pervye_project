import os
from pathlib import Path
import dj_database_url

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Папка, куда Django будет физически загружать аватарки и файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Секретный ключ для разработки (конкурсный вариант)
SECRET_KEY = 'django-insecure-pervye-platform-secret-key-2026-hackathon'

# Включаем режим отладки для локального запуска и проверки верстки
DEBUG = True

# Разрешенные хосты (добавлен локальный хост и порты хакатона)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0']

# УСТАНОВЛЕННЫЕ ПРИЛОЖЕНИЯ ПЛАТФОРМЫ
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core', # Ваше главное приложение каталога и тестов
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pervye_platform.urls'

# ИСПРАВЛЕННЫЙ МАССИВ ШАБЛОНОВ: Django теперь гарантированно видит base.html и catalog.html
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Указываем Django точный путь к вашей папке с шаблонами
        'DIRS': [BASE_DIR / 'core' / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pervye_platform.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.jgeevtlktkumtxlxqfzr',
        'PASSWORD': 'DDzKC8tM-#6xmnt',
        'HOST': 'aws-1-eu-west-1.pooler.supabase.com',
        'PORT': '6543',
    }
}




# ВАЛИДАЦИЯ ПАРОЛЕЙ (Стандартная политика безопасности Django)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ЛОКАЛИЗАЦИЯ И РУССКИЙ ЯЗЫК ИНТЕРФЕЙСА УПРАВЛЕНИЯ
LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# НАСТРОЙКА СТАТИЧЕСКИХ ФАЙЛОВ И КАРТИНОК БРЕНДБУКА (STATIC)
STATIC_URL = '/static/'

# Пути, где Django будет собирать и искать картинки, иконки и логотипы
STATICFILES_DIRS = [
    BASE_DIR / 'core' / 'static',
]

# Папка сборщика статики для деплоя на server в интернет
STATIC_ROOT = BASE_DIR / 'staticfiles'


# Поле по умолчанию для моделей данных
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



