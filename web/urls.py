# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include, register_converter
from django.views.generic import TemplateView, RedirectView
from django_universal_paginator.converter import CursorPageConverter


register_converter(CursorPageConverter, 'page')


urlpatterns = [
	path('dashboard/', admin.site.urls),
	path('', include('blog.urls')),
	path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon/favicon.ico'), permanent=True)),
]
urlpatterns += [
	path('elements/', TemplateView.as_view(template_name='elements.html')),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

