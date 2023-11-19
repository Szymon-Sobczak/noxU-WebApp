from datetime import datetime
from io import BytesIO
import json

from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, session, url_for, send_file
from flask_login import current_user, login_required, login_user, logout_user, UserMixin
from forms.user_forms import LoginForm
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
def orders():
    backend_uri = app.config['BACKEND_URI']
    response = requests.get(f"{backend_uri}/api/orders/list")
    orders = json.loads(response.text)
    return render_template("employee/orders.html", orders=orders)


@employee_bp.route('/generate_qrcode/<order_name>')
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
