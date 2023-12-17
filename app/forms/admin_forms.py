from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SelectField, SubmitField, FieldList, FormField, FloatField
import wtforms.validators as validators
from wtforms import DateField
from datetime import datetime, timedelta
from wtforms import IntegerField
from wtforms.validators import NumberRange


class UserPasswordUpdateForm(FlaskForm):
    user = SelectField('User', coerce=int, validators=[
                       validators.DataRequired()], choices=[
                           (1, 'Anne'),
                           (2, 'Thomas'),
                           (3, 'admin')])
    new_user_password = PasswordField('New User Password', validators=[
        validators.InputRequired()],
        render_kw={"placeholder": "Password"})

    password = PasswordField('Admin password', validators=[validators.InputRequired()], render_kw={
                             "placeholder": "Password"})

    submit = SubmitField("Update user password")


class UserUsernameUpdateForm(FlaskForm):
    user = SelectField('User', coerce=int, validators=[
                       validators.DataRequired()], choices=[
                           (1, 'Anne'),
                           (2, 'Thomas'),
                           (3, 'admin')])
    new_user_username = StringField('New Username', validators=[
        validators.InputRequired()],
        render_kw={"placeholder": "Username"})

    password = PasswordField('Admin password', validators=[validators.InputRequired()], render_kw={
                             "placeholder": "Password"})

    submit = SubmitField("Update username")


class QuantityForm(FlaskForm):
    pass


class UserVisablityForm(FlaskForm):
    user = SelectField('User', coerce=int, validators=[
                       validators.DataRequired()], choices=[
                           (1, 'Anne'),
                           (2, 'Thomas'),
                           (3, 'admin')])
    is_active = BooleanField('Is active', default=True)

    password = PasswordField('Admin password', validators=[validators.InputRequired()], render_kw={
                             "placeholder": "Password"})

    submit = SubmitField("Update user visability")


class DateTimeForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[validators.DataRequired()], default=(datetime.now() - timedelta(days=1)).date())
    enddate = DateField('End Date', format='%Y-%m-%d',
                        validators=[validators.DataRequired()], default=datetime.now().date())
    user = SelectField('User', coerce=int, validators=[
                       validators.DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, user_data, *args, **kwargs):
        super(DateTimeForm, self).__init__(*args, **kwargs)
        self.user.choices = [(user['user_id'], user['user_name'])
                             for user in user_data]

    def validate_enddate(form, field):
        if field.data <= form.startdate.data:
            raise validators.ValidationError(
                'End Date must be greater than Start Date')
