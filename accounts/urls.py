# -*- coding: utf-8 -*-
from django.urls import path

from . import views


app_name = 'accounts'


urlpatterns = [
	path('dashboard/accounts/user/<int:pk>/attachments/', views.UserAttachmentsList.as_view(), name='user_attachments'),
	path('accounts/', views.UserListView.as_view(), name='user_list'),
	path('accounts/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
]
