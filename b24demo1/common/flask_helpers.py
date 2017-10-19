from flask import request, session

def get_session(key, *defaults):
    if key in session:
        return session[key]
    else:
        for value in defaults:
            if value:
                return value

def set_session(key, *values):
    for value in values:
        if value:
            session[key] = value
            return value

def del_session(key):
    if key in session:
        del session[key]