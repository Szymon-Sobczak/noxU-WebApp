import json
import requests

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, session, request, current_app as app
from flask_login import UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms.user_forms import LoginForm


users_bp = Blueprint('users', __name__, url_prefix='/users')


class User(UserMixin):
    def __init__(self, user_json):
        self.employee_json = user_json

    def get_id(self):
        object_id = self.user_json.get('user_id')
        return str(object_id)


@users_bp.route('/', methods=['GET', 'POST'])
def login():
    backend_uri = app.config['BACKEND_URI']
    form = LoginForm()

    # if current_user.is_authenticated and session['is_employee']:
    #     if current_user.employee_json['user_name'] != 'admin':
    #         return redirect(url_for('employees.profile'))
    #     else:
    #         return redirect(url_for('employees.admin_profile'))

    if form.validate_on_submit():
        error = None
        api_request = requests.get(
            url=f'{backend_uri}/api/employees/user_name/{form.username.data}')

        if api_request.status_code == 404:
            error = "Wrong username."
        if error is None:
            employee_json = json.loads(api_request.text)
            if employee_json['password'] == form.password.data:
                current_employee = Employee(employee_json)
                session['is_employee'] = True
                login_user(current_employee)
                print(current_employee)
                if current_user.employee_json['user_name'] != 'admin':
                    return redirect(url_for('employees.profile'))
                else:
                    return redirect(url_for('employees.admin_profile'))
            else:
                error = "Wrong password"
        flash(error)
    else:
        print(form.errors)

    return render_template('login_employee.html', form=form)
