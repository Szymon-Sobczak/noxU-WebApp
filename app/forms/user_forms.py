from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, FieldList, FormField, FloatField
import wtforms.validators as validators
from wtforms import DateField
from datetime import datetime, timedelta


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[
                           validators.InputRequired()], render_kw={"placeholder": "Username"})

    password = PasswordField('Password', validators=[validators.InputRequired()], render_kw={
                             "placeholder": "Password"})

    submit = SubmitField("Login")


class DateTimeForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[validators.DataRequired()], default=(datetime.now() - timedelta(days=1)).date())
    enddate = DateField('End Date', format='%Y-%m-%d',
                        validators=[validators.DataRequired()], default=datetime.now().date())
    submit = SubmitField('Submit')
