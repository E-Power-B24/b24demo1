from b24demo1 import app
from flask import url_for, redirect

from b24demo1.admin import admin_blueprint
app.register_blueprint(admin_blueprint)