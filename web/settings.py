import sys
import re
from pathlib import Path

from django.templatetags.static import static

from .scss import scss_load_svg, scss_info_svg


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&yfygk=e+#gb&^#u)6i(=_x0l9zmxg#!x#3y$pzlu4@tx(z5^b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'accounts',
	'compressor',
	'django_attachments',
	'django_universal_paginator',
	'easy_thumbnails',
	'blog',
	'parler',
	'web',
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

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
	{
		"BACKEND": "django_jinja.backend.Jinja2",
		'DIRS': [BASE_DIR / 'templates'],
		'NAME': 'jinja2',
		"OPTIONS": {
			"match_extension": None,
			"match_regex": re.compile(r"^(?!(admin/|debug_toolbar/|profiler/|search/indexes/|reversion/|sitemap.xml|static_sitemaps/|hijack/|django_extensions/)).*"),
			"newstyle_gettext": True,
			"extensions": [
				"jinja2.ext.do",
				"jinja2.ext.loopcontrols",
				"jinja2.ext.i18n",
				"django_jinja.builtins.extensions.CsrfExtension",
				"django_jinja.builtins.extensions.CacheExtension",
				"django_jinja.builtins.extensions.TimezoneExtension",
				"django_jinja.builtins.extensions.UrlsExtension",
				"django_jinja.builtins.extensions.StaticFilesExtension",
				"django_jinja.builtins.extensions.DjangoFiltersExtension",
				"compressor.contrib.jinja2ext.CompressorExtension",
			],
			"context_processors": [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'django.template.context_processors.i18n',
			],
			"autoescape": True,
			"auto_reload": True,
			"translation_engine": "django.utils.translation",
			"bytecode_cache": {
				"name": "jinja",
				"enabled": True,
			}
		}
	},
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR / 'templates'],
		'OPTIONS': {
			'loaders': [
				'django.template.loaders.filesystem.Loader',
				'django.template.loaders.app_directories.Loader',
			],
			'context_processors': [
				#'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
		'KEY_PREFIX': 'linuxos',
		'LOCATION': 'linuxos-default',
	},
	'jinja': {
		'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
		'KEY_PREFIX': 'jinja',
		'LOCATION': 'linuxos-jinja',
	},
}

WSGI_APPLICATION = 'web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',
	}
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
	{ 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
	{ 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
	{ 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
	{ 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'sk'

LANGUAGES = (
	('sk', "Slovensky"),
	('en', "English"),
)
PARLER_LANGUAGES = {
	None: (
		{'code': 'sk',},
		{'code': 'en',},
	),
	'default': {
		'fallbacks': ['sk'],
		'hide_untranslated': False,
	}
}

TIME_ZONE = 'Europe/Bratislava'

USE_I18N = True

USE_TZ = True

LIBSASS_CUSTOM_FUNCTIONS = {
	'static': static,
	'load_svg': scss_load_svg,
	'info_svg': scss_info_svg,
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent / 'static_assets' / 'static'
STATICFILES_DIRS = (BASE_DIR.joinpath('static'),)
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	'compressor.finders.CompressorFinder',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / 'static_assets' / 'media'


COMPRESS_PRECOMPILERS = (
	('text/x-scss', 'django_libsass.SassCompiler'),
)
COMPRESS_FILTERS = {
	'css': ['web.compressor_filters.CssAbsoluteFilter',],
	'js': [],
}

COMPRESS_ENABLED = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ALWAYS_TRANSLATION_FALLBACK = True

CURRENT_COMMAND = sys.argv[1:2]
if CURRENT_COMMAND:
	CURRENT_COMMAND = CURRENT_COMMAND[0]
else:
	CURRENT_COMMAND = ''

THUMBNAIL_NAMER = 'web.utils.thumbnail.namers.hashed'

THUMBNAIL_PROCESSORS = (
	'easy_thumbnails.processors.colorspace',
	'easy_thumbnails.processors.autocrop',
	'easy_thumbnails.processors.scale_and_crop',
	'easy_thumbnails.processors.filters',
	'easy_thumbnails.processors.background',
	'web.utils.thumbnail.processors.alpha',
)

THUMBNAIL_ALIASES = {
	'': {
		# 16:11
		'blog_list': {
			'size': (792, 544),
			'upscale': (792, 544),
			'background': '#ffffff',
			'quality': 70,
			'alpha': False,
		},
	}
}
