# -*- coding: utf-8 -*-
from django.urls import path

from . import views


app_name = 'accounts'


urlpatterns = [
	path('dashboard/accounts/user/<int:pk>/attachments/', views.UserAttachmentsList.as_view(), name='user_attachments'),
]
