# -*- coding: utf-8 -*-
from . import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
	path('', views.BlogPostListView.as_view(), name='post_list'),
]