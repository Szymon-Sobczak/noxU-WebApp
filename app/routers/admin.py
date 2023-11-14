from datetime import datetime
import json

from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user, UserMixin
from forms.user_forms import LoginForm
import requests
from werkzeug.security import check_password_hash, generate_password_hash


class Admin(UserMixin):
    def __init__(self, admin_json):
        self.admin_json = admin_json

    def get_id(self):
        object_id = self.admin_json.get('user_id')
        return str(object_id)


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('admin_main_page.html', admin=current_user.admin_json)
