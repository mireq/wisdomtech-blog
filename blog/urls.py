# -*- coding: utf-8 -*-
from django.urls import path

from . import views


app_name = 'blog'


urlpatterns = [
	path('', views.BlogPostListView.as_view(), name='post_list'),
	path('dashboard/blog/blogpost/<int:pk>/attachments/', views.BlogPostAttachmentsList.as_view(), name='post_attachments'),
]
