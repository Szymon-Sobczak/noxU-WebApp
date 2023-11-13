from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, FieldList, FormField, FloatField
import wtforms.validators as validators


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[
                           validators.InputRequired()], render_kw={"placeholder": "Username"})

    password = PasswordField('New Password', validators=[validators.InputRequired()], render_kw={
                             "placeholder": "Password"})

    submit = SubmitField("Login")
