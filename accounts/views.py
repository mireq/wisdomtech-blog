# -*- coding: utf-8 -*-
from .models import User
from web.utils.generic_views import AttachmentListAndUploadView


class UserAttachmentsList(AttachmentListAndUploadView):
	model_class = User
