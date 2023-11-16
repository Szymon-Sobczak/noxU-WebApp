from datetime import datetime
import json

from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from forms.user_forms import LoginForm
import requests
from routers.admin import Admin
from routers.employee import Employee
from werkzeug.security import check_password_hash, generate_password_hash


account_bp = Blueprint('account', __name__, url_prefix='/account')


@account_bp.route('/login', methods=['GET', 'POST'])
def login():
    backend_uri = app.config['BACKEND_URI']
    form = LoginForm()

    if current_user.is_authenticated:
        print(current_user)
        if current_user.is_admin and session.get('is_admin'):
            return redirect(url_for('admin.profile'))
        else:
            return redirect(url_for('employee.profile'))

    if form.validate_on_submit():
        error = None
        api_request = requests.get(
            url=f'{backend_uri}/api/users/username/{form.username.data}')
        if api_request.status_code == 404:
            error = "Wrong username."
        if error is None:
            user_json = json.loads(api_request.text)
            if user_json.get('is_active'):
                if user_json.get('password') == form.password.data:
                    if user_json.get('is_admin'):
                        user = Admin(user_json)
                        session['is_admin'] = True
                        login_user(user)
                        return redirect(url_for('admin.profile'))
                    else:
                        user = Employee(user_json)
                        session['is_admin'] = False
                        login_user(user)
                        return redirect(url_for('employee.profile'))
                else:
                    error = "Wrong password"

            else:
                error = "User blocked!"

        flash(error)
    else:
        print(form.errors)

    return render_template('home.html', form=form)


@account_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
