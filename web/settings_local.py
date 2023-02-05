# pylint: disable=wildcard-import,unused-wildcard-import
from __future__ import unicode_literals

from .settings import *

ALLOWED_HOSTS = ['*']
LOG_SQL = False

DEBUG = True

INSTALLED_APPS = INSTALLED_APPS + [
	'django_extensions',
]

COMPRESS_MTIME_DELAY = 0

LOGGING = {
	'version': 1,
	'filters': {
		'require_debug_true': {
			'()': 'django.utils.log.RequireDebugTrue',
		}
	},
	'handlers': {
		'console': {
			'level': 'WARNING',
			'filters': ['require_debug_true'],
			'class': 'logging.StreamHandler',
		},
		'sql': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
		},
	},
	'loggers': {
		'': {
			'level': 'WARNING',
			'handlers': ['console'],
		},
		'django.db.backends': {
			'level': 'DEBUG' if LOG_SQL else 'WARNING',
			'handlers': ['sql'],
		},
	}
}
