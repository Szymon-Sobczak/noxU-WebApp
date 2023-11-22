from datetime import datetime, timedelta
from io import BytesIO
import json

from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, send_file, session, url_for
from flask_login import current_user, login_required, login_user, logout_user, UserMixin
from forms.user_forms import DateTimeForm, LoginForm, PasswordUpdateForm
import qrcode
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


@employee_bp.route('/orders/')
@login_required
def orders():
    backend_uri = app.config['BACKEND_URI']
    response = requests.get(f"{backend_uri}/api/orders/list/ordercontet")
    orders = json.loads(response.text)
    for order in orders:
        order["creation_date"] = datetime.strptime(
            order["creation_date"], "%Y-%m-%dT%H:%M:%S")

    return render_template("employee/orders.html", orders=orders)


@employee_bp.route('/admin/employees/new_password', methods=['GET', 'POST'])
@login_required
def settings():
    backend_uri = app.config['BACKEND_URI']

    password_form = PasswordUpdateForm()
    if password_form.validate_on_submit():
        if password_form.password.data == current_user.user_json.get("password"):
            user_id = current_user.user_json.get("user_id")
            request = requests.put(
                url=f'{backend_uri}/api/users/{user_id}',
                params={"user_name": current_user.user_json.get("user_name"),
                        "password": password_form.new_password.data})
            if request.status_code != 200:
                flash(f"Error: {request.text}")
            else:
                flash("Password updated successfully!")
                redirect(url_for('employee_bp.settings'))
        else:
            flash("Current password is incorrect.")

    return render_template('employee/settings.html', form=password_form)


@employee_bp.route('/timelog/', methods=['GET', 'POST'])
@login_required
def timelog():
    form = DateTimeForm()
    backend_uri = app.config['BACKEND_URI']
    user_id = current_user.user_json.get("user_id")

    start_date = ((datetime.now()-timedelta(days=1))
                  .date()
                  .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
    end_date = (datetime.combine(datetime.now().date(), datetime.max.time())
                .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])

    response = requests.get(f"{backend_uri}/api/production_log/list/timeseries/{user_id}",
                            params={"min_timestamp": start_date,
                                    "max_timestamp": end_date})
    timelog = json.loads(response.text)
    for entry in timelog:
        entry["creation_date"] = datetime.strptime(
            entry["creation_date"][:-7], "%Y-%m-%dT%H:%M:%S")
    if form.validate_on_submit():
        try:
            start_date = (form.startdate.data
                          .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
            end_date = (form.enddate.data
                        .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])

            response = requests.get(f"{backend_uri}/api/production_log/list/timeseries/{user_id}",
                                    params={"min_timestamp": start_date,
                                            "max_timestamp": end_date})
            timelog = json.loads(response.text)
            for entry in timelog:
                entry["creation_date"] = datetime.strptime(
                    entry["creation_date"][:-7], "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            flash(e)
        return render_template('employee/timelog.html', form=form, timelog=timelog)

    return render_template('employee/timelog.html', form=form, timelog=timelog)


@employee_bp.route('/generate_qrcode/<order_name>')
@login_required
def generate_qrcode(order_name):
    if order_name:
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=2)

        qr.add_data(order_name)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save image to BytesIO buffer
        img_buffer = BytesIO()
        img.save(img_buffer)
        img_buffer.seek(0)

        return send_file(img_buffer, download_name=f"order-{order_name}-qrcode.png", as_attachment=True, mimetype='image/png')

    return "Order not found"
