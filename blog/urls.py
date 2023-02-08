# -*- coding: utf-8 -*-
from django.urls import path

from . import views


app_name = 'blog'


urlpatterns = [
	path('', views.BlogPostListView.as_view(), name='post_list'),
	path('feed/', views.BlogPostFeed(), name='post_feed'),
	path('<slug:slug>-p<int:pk>/', views.BlogPostDetailView.as_view(), name='post_detail'),
	path('category/<slug:slug>-p<int:pk>/', views.CategoryBlogPostListView.as_view(), name='category_detail'),
	path('category/<slug:slug>-p<int:pk>/feed/', views.BlogPostFeed(), name='category_feed'),
	path('accounts/<int:user_id>/feed/', views.BlogPostFeed(), name='user_feed'),
]
