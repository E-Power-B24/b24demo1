"""
Routes and views for the flask application.
"""
from b24demo1.admin.views.base import *
from datetime import datetime
from flask import render_template,redirect,url_for,request

class HomeView(AdminSecuredView):
    route_base = '/'
    @route('/')
    def home(self):
        user_id = get_session('user_id')
        return render_template('home/home.html',user_id=user_id)

    @route('/dashboard')
    def dashboard(self):
        user_id = get_session('user_id')
        return render_template('home/home.html',user_id=user_id)

    @route("/manage")
    def manage(self):
        user_id = get_session('user_id')
        return render_template('home/manage.html',user_id=user_id)
    @route("/people")
    def people(self):
        user_id = get_session('user_id')
        return render_template('home/people.html',user_id=user_id)
    


HomeView.register(admin_blueprint)





