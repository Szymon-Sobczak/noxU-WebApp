from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SelectField, SubmitField, FieldList, FormField, FloatField
import wtforms.validators as validators
from wtforms import DateField
from datetime import datetime, timedelta


class DateTimeForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d',
                          validators=[validators.DataRequired()], default=(datetime.now() - timedelta(days=1)).date())
    enddate = DateField('End Date', format='%Y-%m-%d',
                        validators=[validators.DataRequired()], default=datetime.now().date())
    user = SelectField('User', coerce=int, validators=[
                       validators.DataRequired()])
    submit = SubmitField('Submit')

    def validate_enddate(form, field):
        if field.data <= form.startdate.data:
            raise validators.ValidationError(
                'End Date must be greater than Start Date')
