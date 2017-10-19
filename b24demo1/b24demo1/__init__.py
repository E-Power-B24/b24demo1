import logging

from flask import Flask, redirect, url_for, request, session
from flask_babel import Babel,refresh

logging.info('app starting...')


app = Flask(__name__)

app.config.from_object("b24demo1.configs.DevelopmentConfig")
ctx = app.app_context()
ctx.push()

import b24demo1.register_blueprint

@app.route('/')
def home():
    return redirect(url_for('admin.HomeView:home'))
ctx.pop()