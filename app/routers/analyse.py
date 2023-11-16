from datetime import datetime
import json

from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user, UserMixin
from forms.user_forms import LoginForm
import requests
from werkzeug.security import check_password_hash, generate_password_hash


analyse_bp = Blueprint('analyse', __name__, url_prefix='/analyse')


@analyse_bp.route('/', methods=['GET', 'POST'])
def upload():
    backend_uri = app.config['BACKEND_URI']
    if request.method == "POST" and "photo" in request.files:
        photo = request.files["photo"]
        if photo:
            files = {"new_image": ("photo.jpg", photo, "image/jpeg")}
            user_id = current_user.user_json.get("user_id")

            response = requests.post(f"{backend_uri}/api/analyse/detect/?user_id={user_id}",
                                     files=files)
            print(response.text)
            return render_template("analyse/analyse.html")

    return render_template("analyse/analyse.html")
