from flask import session, request, Response, redirect, url_for
from functools import wraps
from b24demo1.core.logics.logic_user import UserLogic

def check_auth(username, password):
    print 'Check_auth username password'
    user = UserLogic().authenticate(username, password)

    if user:
        session['user_id'] = user.id
        session['username']= user.name

        print 'User Session' + session['user_id']
    return user

def authenticate():
    print 'Authenticate'
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                if 'X-Requested-With' in request.args and request.args['X-Requested-With']=='XMLHttpRequest':
                    return authenticate()
                else:
                    return redirect(url_for('admin.SecurityView:login'))
        return f(*args, **kwargs)
    return decorated