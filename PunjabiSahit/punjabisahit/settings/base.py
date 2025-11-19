import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = "django-insecure-your-secret-key"
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [ "home", "search", "rest_framework", "modelcluster", "taggit", "wagtail", "wagtail.contrib.forms", "wagtail.contrib.redirects", "wagtail.embeds", "wagtail.sites", "wagtail.users", "wagtail.snippets", "wagtail.documents", "wagtail.images", "wagtail.search", "wagtail.admin", "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles" ]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # For language switching
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    # === ADD OUR NEW MIDDLEWARE HERE ===
    "home.middleware.views.PageViewCounterMiddleware",
]

ROOT_URLCONF = "punjabisahit.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",  # For i18n
            ],
        },
    },
]
WSGI_APPLICATION = "punjabisahit.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "punjabisahit_db",
        "USER": "punjabisahit_user",
        "PASSWORD": "admin123", # Make sure this is your actual password
        "HOST": "localhost",
        "PORT": "5432",
    }
}

AUTH_PASSWORD_VALIDATORS = [ { "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator", }, { "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", }, { "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", }, { "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", }, ]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
from django.utils.translation import gettext_lazy as _
LANGUAGES = [
    ('en', _('English')),
    ('hi', _('Hindi')),
    ('pa', _('Punjabi')),
]
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
STATICFILES_FINDERS = [ "django.contrib.staticfiles.finders.FileSystemFinder", "django.contrib.staticfiles.finders.AppDirectoriesFinder", ]
STATICFILES_DIRS = [ BASE_DIR / "static_compiled", ]
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
WAGTAIL_SITE_NAME = "Punjabi Sahit"
WAGTAILSEARCH_BACKENDS = { "default": { "BACKEND": "wagtail.search.backends.database", } }
WAGTAILADMIN_BASE_URL = "http://localhost:8000"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"