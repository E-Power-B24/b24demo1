from b24demo1.admin.views.base import *
from flask_wtf import Form
from wtforms import TextField, PasswordField

from b24demo1.core.logics.logic_user import UserLogic


class LoginForm(Form):
    username = TextField(
        ('Username'),
        render_kw = {
            'placeholder':('Username'),
            'data-val':'true',
            'data-val-required':('Input Required')
        }
    )
    password = PasswordField(
        ('Password'),
        render_kw = {
            'placeholder':('Password'),
            'data-val':'true',
            'data-val-required':('Input Required')
        }
    )

class SecurityView(AdminView):
    route_base = '/securities/'

    @route('/login', methods=['GET', 'POST'])
    def login(self):
        form = LoginForm()
        error = None

        if form.validate_on_submit():
             user = UserLogic().authenticate(form.username.data, form.password.data)

             if user:
                set_session('user_id', user.id)
                set_session('username', user.name)
                return redirect(url_for('admin.HomeView:home'))
             else:
                error = ('The username or password you entered is incorrect.')

        return render_template(
            'securities/login.html',
            form = form,
            error = error
        )

    def logout(self):
        session.clear()
        return redirect(url_for('admin.SecurityView:login'))
SecurityView.register(admin_blueprint)