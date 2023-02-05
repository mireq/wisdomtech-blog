import re
import sys
from pathlib import Path

from django.templatetags.static import static
from django.utils.translation import pgettext_lazy

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
	'django.contrib.sitemaps',
	'accounts',
	'compressor',
	'django_attachments',
	'django_universal_paginator',
	'easy_thumbnails',
	'tinymce',
	'blog',
	'parler',
	'web',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'web.middleware.ContentSecurityPolicyMiddleware',
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
		'BACKEND': 'django_pylibmc_threadsafe.PyLibMCCache',
		'LOCATION': '127.0.0.1:11211',
		'KEY_PREFIX': 'blog',
		'OPTIONS': {
			'binary': True,
			'ignore_exc': True,
			'behaviors': {
				'ketama': True,
			}
		}
	},
	'jinja': {
		'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
		'KEY_PREFIX': 'jinja',
		'LOCATION': 'blog-jinja',
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

LANGUAGE_CODE = 'en'

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

LOCALE_PATHS = (BASE_DIR / 'locale',)

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

THUMBNAIL_ALIASES = {
	'': {
		# 16:11
		'blog_list_first': {
			'size': (828, 569),
			'quality': 60,
			'crop': 'smart',
			'preserve_aspect': True,
			'alpha': False,
			'sizes': ['328px', '496px', '656px', '984px', '1656px'],
			'size_attrs': {'quality': [60, 60, 60, 50, 20]},
		},
		'blog_list': {
			'size': (546, 375),
			'quality': 70,
			'crop': 'smart',
			'preserve_aspect': True,
			'alpha': False,
			'sizes': ['328px', '496px', '656px', '984px', '1122px'],
			'size_attrs': {'quality': [60, 60, 60, 50, 30]},
		},
		'article': {
			'size': (696, 2000),
			'quality': 80,
			'preserve_aspect': True,
			'sizes': ['328px', '496px', '656px', '1044px', '1392px'],
			'size_attrs': {'quality': [80, 80, 80, 70, 60]},
		},
		'attachment_browser': {
			'size': (256, 256),
			'quality': 60,
			'crop': True,
			'preserve_aspect': True,
			'alpha': False,
			'sizes': [2],
		},
		'user_list': {
			'size': (546, 546),
			'quality': 70,
			'crop': 'smart',
			'preserve_aspect': True,
			'alpha': False,
			'sizes': ['328px', '496px', '656px', '984px', '1122px'],
			'size_attrs': {'quality': [60, 60, 60, 50, 30]},
		},
		'og_image': {
			'size': (1200, 630),
			'quality': 80,
			'crop': 'smart',
			'preserve_aspect': True,
			'alpha': False,
		},
	}
}

THUMBNAIL_PROCESSORS = (
	'easy_thumbnails.processors.colorspace',
	'easy_thumbnails.processors.autocrop',
	'web.utils.thumbnail.processors.scale_and_crop',
	'easy_thumbnails.processors.filters',
	'easy_thumbnails.processors.background',
	'web.utils.thumbnail.processors.alpha',
)

THUMBNAIL_BASEDIR = 'thumbs'

THUMBNAIL_CACHE = 'default'
THUMBNAIL_CACHE_PREFIX = 'tmb_'

NGINX_CACHE_DIR = None

SOURCE_CODE_LEXERS = [
	('c', "C"),
	('cmake', "CMake"),
	('common-lisp', "Common Lisp"),
	('cpp', "C++"),
	('csharp', "C#"),
	('css', "CSS"),
	('d', "D"),
	('django', "Django/Jinja"),
	('docker', "Docker"),
	('glsl', "GLSL"),
	('go', "Go"),
	('haskell', "Haskell"),
	('html', "HTML"),
	('html+django', "HTML+Django/Jinja"),
	('java', "Java"),
	('javascript', "JavaScript"),
	('json', "JSON"),
	('lua', "Lua"),
	('make', "Makefile"),
	('mysql', "MySQL"),
	('php', "PHP"),
	('plpgsql', "PL/pgSQL"),
	('postgresql', "PostgreSQL SQL dialect"),
	('python', "Python"),
	('ruby', "Ruby"),
	('sh', "Bash"),
	('sql', "SQL"),
	('tex', "TeX"),
	('toml', "TOML"),
	('xml', "XML"),
]

TINYMCE_EXTRA_MEDIA = {
	'js': ['/static/js/tinymce_filebrowser.js']
}

TINYMCE_DEFAULT_CONFIG = {
	"theme": "silver",
	"height": 500,
	"menubar": False,
	"plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,code,help,wordcount",
	"toolbar": "undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help",
	'content_css': '/static/css/tinymce.css',
	'file_picker_types': 'file image media',
	'image_caption': True,
	'relative_urls': False,
	'remove_script_host': False,
	'convert_urls': False,
	'rel_list': [
		{'title': "Default", 'value': None},
		{'title': pgettext_lazy('link rel', "Gallery"), 'value': 'gallery'},
	],
	'content_langs': [
		{'title': title, 'code': code}
		for code, title in LANGUAGES
	],
	'table_appearance_options': False,
	'table_default_attributes': {},
	'table_default_styles': {},
	'table_class_list': [
		{'title': pgettext_lazy('table style', "None"), 'value': ''},
		{'title': pgettext_lazy('table style', "Wide"), 'value': 'u-wide'},
	],
	'table_column_resizing': 'preservetable',
	'table_header_type': 'section',
	'table_sizing_mode': 'responsive',
	'image_class_list': [
		{'title': pgettext_lazy('image style', "None"), 'value': ''},
		{'title': pgettext_lazy('image style', "No thumbnail"), 'value': 'no-thumbnail'},
	],
}

TINYMCE_CONFIGS = {
	'basic': {
		'plugins': 'lists,link,charmap,print,preview,anchor,searchreplace,visualblocks,code,fullscreen,insertdatetime,media,paste,code,help,wordcount',
		'toolbar': 'undo redo | bold italic | bullist numlist outdent indent | removeformat | help | code',
	},
	'content': {
		'plugins': 'advlist autolink link image lists charmap print preview hr anchor pagebreak searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking table emoticons template paste help',
		'toolbar': 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media fullscreen | forecolor backcolor emoticons | help | code',
		'menubar': True,
		'style_formats': [
			{'title': pgettext_lazy('style', "Source code"), 'items':
				[{'title': pgettext_lazy('style', "Don't wrap code"), 'format': 'pre_no_wrap'}] +
				[
					{'title': name, 'block': 'pre', 'attributes': {'data-code-highlight': code}}
					for code, name in SOURCE_CODE_LEXERS
				]
			},
			{'title': pgettext_lazy('style', "Wide"), 'format': 'wide'},
		],
		'formats': {
			'alignleft': [
				{'selector': 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,span,article', 'styles': {'textAlign': 'left'}},
				{'selector': 'img,table', 'classes': 'u-float-left'},
				{'selector': 'figure', 'collapsed': False, 'classes': 'u-float-left', 'ceFalseOverride': True }
			],
			'alignright': [
				{'selector': 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,span,article', 'styles': {'textAlign': 'right'}},
				{'selector': 'img,table', 'classes': 'u-float-right'},
				{'selector': 'figure', 'collapsed': False, 'classes': 'u-float-right', 'ceFalseOverride': True }
			],
			'wide': {'selector': 'table,pre', 'classes': 'u-wide'},
			'pre_no_wrap': {'selector': 'pre', 'classes': 'u-nowrap'},
		},
		'style_formats_merge': True,
	}
}
