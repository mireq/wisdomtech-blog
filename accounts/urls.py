# -*- coding: utf-8 -*-
from django.urls import path

from . import views


app_name = 'accounts'


urlpatterns = [
	path('accounts/', views.UserListView.as_view(), name='user_list'),
	path('accounts/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
]
