# -*- coding: utf-8 -*-
import os

from django.core.wsgi import get_wsgi_application
import bjoern

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

application = get_wsgi_application()

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
	return "Hello, World!"

bjoern.run(application, "127.0.0.1", 8000)
