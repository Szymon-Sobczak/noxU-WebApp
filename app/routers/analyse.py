from datetime import datetime
import json
from io import BytesIO
from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user, UserMixin
from forms.user_forms import LoginForm
import requests
from werkzeug.security import check_password_hash, generate_password_hash
import base64
from PIL import Image, ImageDraw, ImageFont

analyse_bp = Blueprint('analyse', __name__, url_prefix='/analyse')


def draw_detection_boxes(raw_image: base64, detecion_result: list[dict]):
    image = Image.open(BytesIO(raw_image)).convert("RGB")
    draw = ImageDraw.Draw(image)

    font_size = 82

    for result in detecion_result:
        x1, x2, y1, y2 = (result.get("box").get("x1"), result.get("box").get("x2"),
                          result.get("box").get("y1"), result.get("box").get("y2"))
        status, name = result.get("status"), result.get("name")

        font = ImageFont.load_default().font_variant(size=font_size)
        position = (x1, y1-font_size)
        left, top, right, bottom = draw.textbbox(position, name, font=font)

        colour = "green" if status == "ok" else "red"

        draw.rectangle([(x1, y1), (x2, y2)], outline=colour, width=8)
        draw.rectangle((left, top-5, right+5, bottom+5), fill=colour)

        draw.text(position, name, font=font, fill="white")

    with BytesIO() as b:
        image.save(b, 'jpeg')
        im_bytes = b.getvalue()

    base64_encoded = base64.b64encode(im_bytes).decode('utf-8')
    return base64_encoded


@analyse_bp.route('/', methods=['GET', 'POST'])
@login_required
def upload():
    backend_uri = app.config['BACKEND_URI']
    if request.method == "POST" and "photo" in request.files:
        photo = request.files["photo"]
        if photo:
            user_id = current_user.user_json.get("user_id")
            photo_data = photo.read()

            response = requests.post(f"{backend_uri}/api/analyse/detect/?user_id={user_id}",
                                     files={"new_image": ("photo.jpg", photo_data, "image/jpeg")})

            session['uploaded_photo'] = photo_data
            session['analysis_response'] = response.text

            return redirect(url_for('analyse.summary'))

    return render_template("analyse/analyse.html")


@analyse_bp.route('/summary')
@login_required
def summary():
    photo = session.get('uploaded_photo')
    analysis_response = session.get('analysis_response')

    analysis = json.loads(analysis_response)
    print(analysis)
    analysis_status = analysis.get("analysis").get("detection_result")
    analysis_report = analysis.get("analysis").get("detection_report")
    analysis_report = dict(sorted(analysis_report.items(),
                                  key=lambda x: x[0].lower()))
    print(analysis_report)
    if analysis.get("detection_result"):
        photo = draw_detection_boxes(photo,
                                     analysis.get("detection_result"))
    else:
        photo = base64.b64encode(photo).decode('utf-8')

    return render_template("analyse/summary.html",
                           uploaded_photo=photo,
                           analysis_status=analysis_status,
                           analysis_report=analysis_report)
