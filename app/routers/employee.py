from datetime import datetime
import json

from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user, UserMixin
from forms.user_forms import LoginForm
import requests
from werkzeug.security import check_password_hash, generate_password_hash


class Employee(UserMixin):
    def __init__(self, employee_json):
        self.user_json = employee_json
        self.is_admin = False

    def get_id(self):
        object_id = self.user_json.get('user_id')
        return str(object_id)


employee_bp = Blueprint('employee', __name__, url_prefix='/employee')


@employee_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('employee/employee_main_page.html', employee=current_user.user_json)
