from datetime import datetime, timedelta
from io import BytesIO
import json

from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, session, url_for, send_file
from flask_login import current_user, login_required, login_user, logout_user, UserMixin
from forms.admin_forms import DateTimeForm, UserPasswordUpdateForm, UserUsernameUpdateForm, UserVisablityForm, QuantityForm
import requests
from werkzeug.security import check_password_hash, generate_password_hash
import qrcode
from wtforms import IntegerField, FieldList
from wtforms.validators import NumberRange
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
    response = requests.get(f"{backend_uri}/api/orders/list/ordercontet")
    orders = json.loads(response.text)

    items_response = requests.get(f"{backend_uri}/api/items/list")
    items = json.loads(items_response.text)

    items_names = [item.get("item_name") for item in items]

    for order in orders:
        order["creation_date"] = datetime.strptime(
            order["creation_date"], "%Y-%m-%dT%H:%M:%S")

    return render_template("admin/orders.html", orders=orders, items=items_names)


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    backend_uri = app.config['BACKEND_URI']
    user_password_form = UserPasswordUpdateForm()
    user_username_form = UserUsernameUpdateForm()
    user_visability_form = UserVisablityForm()
    return render_template('admin/settings.html',
                           form=user_password_form,
                           username_form=user_username_form,
                           visablility_form=user_visability_form)


@admin_bp.route('/timelog', methods=['GET', 'POST'])
@login_required
def timelog():
    try:
        backend_uri = app.config['BACKEND_URI']
        user_id = current_user.user_json.get("user_id")

        response = requests.get(f"{backend_uri}/api/users/list/")
        users = json.loads(response.text)
        form = DateTimeForm(user_data=users)

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
            if entry['additional_info']:
                entry['additional_info'] = json.loads(entry['additional_info'])
            entry["creation_date"] = datetime.strptime(
                entry["creation_date"][:-7], "%Y-%m-%dT%H:%M:%S")

    except Exception as e:
        flash(e)

    if form.validate_on_submit():
        try:
            start_date = (form.startdate.data
                          .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
            end_date = (datetime.combine(form.enddate.data, datetime.max.time())
                        .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
            response = requests.get(f"{backend_uri}/api/production_log/list/timeseries/{form.user.data}",
                                    params={"min_timestamp": start_date,
                                            "max_timestamp": end_date})
            timelog = json.loads(response.text)
            for entry in timelog:
                if entry['additional_info']:
                    entry['additional_info'] = json.loads(
                        entry['additional_info'])
                entry["creation_date"] = datetime.strptime(
                    entry["creation_date"][:-7], "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            flash(e)
        return render_template('admin/timelog.html', form=form, timelog=timelog, users=users)
    else:
        form.user.default = user_id
        form.process()

    return render_template('admin/timelog.html', form=form, timelog=timelog, users=users)


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
