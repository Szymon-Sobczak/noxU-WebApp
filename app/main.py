import requests

from flask import render_template, Flask, session, flash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from routers.users import User, users_bp
from forms.user_forms import LoginForm

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'def8fb9574fc58b0b55ae68f368eaa4703d59815d7bfccd03bb1fdb557626693'
app.config['BACKEND_URI'] = "http://127.0.0.1:8000"

app.register_blueprint(users_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "customers.login"


@app.route("/")
def home():
    backend_uri = app.config['BACKEND_URI']
    form = LoginForm()

    # if current_user.is_authenticated and session['is_employee']:
    #     if current_user.employee_json['user_name'] != 'admin':
    #         return redirect(url_for('employees.profile'))
    #     else:
    #         return redirect(url_for('employees.admin_profile'))

    if form.validate_on_submit():
        pass
        # error = None
        # api_request = requests.get(
        #     url=f'{backend_uri}/api/employees/user_name/{form.username.data}')

        # if api_request.status_code == 404:
        #     error = "Wrong username."
        # if error is None:
        #     employee_json = json.loads(api_request.text)
        #     if employee_json['password'] == form.password.data:
        #         current_employee = Employee(employee_json)
        #         session['is_employee'] = True
        #         login_user(current_employee)
        #         print(current_employee)
        #         if current_user.employee_json['user_name'] != 'admin':
        #             return redirect(url_for('employees.profile'))
        #         else:
        #             return redirect(url_for('employees.admin_profile'))
        #     else:
        #         error = "Wrong password"
        # flash(error)
    else:
        print(form.errors)

    return render_template('home.html', form=form)


@login_manager.user_loader
def load_user(id: int):
    backend_uri = app.config['BACKEND_URI']
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
