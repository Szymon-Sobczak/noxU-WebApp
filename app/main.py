"""Main entrypoint to NoxU web application"""


from flask import Flask, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, LoginManager, logout_user
from forms.user_forms import LoginForm
from routers.account import account_bp
from routers.admin import Admin, admin_bp
from routers.employee import Employee, employee_bp
from routers.analyse import analyse_bp

import requests

app = Flask(__name__)

Bootstrap(app)

app.config['SECRET_KEY'] = 'def8fb9574fc58b0b55ae68f368eaa4703d59815d7bfccd03bb1fdb557626693'
app.config['BACKEND_URI'] = "http://127.0.0.1:8000"

app.register_blueprint(admin_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(account_bp)
app.register_blueprint(analyse_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "account.login"


@login_manager.user_loader
def load_user(id: int):
    backend_uri = app.config['BACKEND_URI']

    if session.get('is_admin'):
        request = requests.get(
            url=f'{backend_uri}/api/users/id/{id}')
        if request.status_code == 404:
            return None
        current_admin = Admin(request.json())
        return current_admin
    else:
        request = requests.get(
            url=f'{backend_uri}/api/users/id/{id}')
        if request.status_code == 404:
            return None
        current_employee = Employee(request.json())
        return current_employee


@app.route("/")
def home():
    return redirect(url_for('account.login'))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
