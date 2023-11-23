from datetime import datetime, timedelta
from io import BytesIO
import json

from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, session, url_for, send_file
from flask_login import current_user, login_required, login_user, logout_user, UserMixin
from forms.user_forms import LoginForm
import requests
from werkzeug.security import check_password_hash, generate_password_hash
import qrcode
# Rewrite to Flask.Admin


class Admin(UserMixin):
    def __init__(self, admin_json):
        self.user_json = admin_json
        self.is_admin = True

    def get_id(self):
        object_id = self.user_json.get('user_id')
        return str(object_id)


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('admin/admin_main_page.html', admin=current_user.user_json)


@admin_bp.route('/orders')
@login_required
def orders():
    backend_uri = app.config['BACKEND_URI']

    return render_template("admin/orders.html", orders=orders)


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    backend_uri = app.config['BACKEND_URI']

    return render_template('admin/settings.html', form=password_form)


@admin_bp.route('/timelog', methods=['GET', 'POST'])
@login_required
def timelog():
    backend_uri = app.config['BACKEND_URI']

    return render_template('admin/timelog.html', form=form, timelog=timelog)


@admin_bp.route('/generate_qrcode/<order_name>')
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
