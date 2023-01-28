# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include, register_converter
from django.views.generic import TemplateView, RedirectView
from django_universal_paginator.converter import CursorPageConverter

from .sitemaps import sitemaps


register_converter(CursorPageConverter, 'page')


urlpatterns = [
	path('dashboard/', admin.site.urls),
	path('tinymce/', include('tinymce.urls')),
	path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/favicon.ico'), permanent=True)),
	path('i18n/', include('django.conf.urls.i18n')),
	path('robots.txt', TemplateView.as_view(template_name='robots.txt'), name='robots'),
]
urlpatterns += i18n_patterns(
	path('', include('accounts.urls')),
	path('', include('blog.urls')),
	path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
	prefix_default_language=False,
)
urlpatterns += [
	path('elements/', TemplateView.as_view(template_name='elements.html')),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

