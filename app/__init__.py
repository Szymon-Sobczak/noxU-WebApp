import requests

from flask import render_template, Flask, session
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from routers.users import User, users_bp


app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'def8fb9574fc58b0b55ae68f368eaa4703d59815d7bfccd03bb1fdb557626693'
app.config['BACKEND_URL'] = "http://127.0.0.1:8000"

app.register_blueprint(users_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "customers.login"


@app.route("/")
def home():
    return render_template('home.html')


@login_manager.user_loader
def load_user(id: int):
    backend_url = app.config['FASTAPI_BASE_URL']
    # if not session['is_employee']:
    #     request = requests.get(
    #         url=f'{backend_url}/api/customers/id/{id}')
    #     if request.status_code == 404:
    #         return None
    #     current_customer = Customer(request.json())
    #     return current_customer
    # else:
    #     request = requests.get(
    #         url=f'{backend_url}/api/employees/id/{id}')
    #     if request.status_code == 404:
    #         return None
    #     current_employee = Employee(request.json())
    #     return current_employee


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
