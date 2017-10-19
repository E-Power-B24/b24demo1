from b24demo1.admin.views.auth_views import requires_auth
from b24demo1.admin import admin_blueprint
from b24demo1.core.models.helper import *
from flask import current_app as app, url_for, render_template, redirect, request,session, send_from_directory,flash
from flask_classy import FlaskView, route
from wtforms import *
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf import Form
from common.flask_helpers import *
from common.flask_helpers import *
from common.json_helpers import *
from common.ui.dynamicselect import DynamicSelectField
from common.ui.table import Table, Column, CheckColumn, RowNumberColumn, LamdaColumn, DateColumn, DateTimeColumn, DecimalColumn, ActionColumn
from common.ui.dataview import DataView
from werkzeug.utils import secure_filename
class AdminView(FlaskView):
    pass

class AdminSecuredView(FlaskView):
    decorators = [requires_auth]