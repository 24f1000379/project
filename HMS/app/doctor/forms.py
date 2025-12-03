from flask_wtf import FlaskForm
from wtforms import SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

class AppointmentForm(FlaskForm):
    patient = SelectField('Patient', coerce=int, validators=[DataRequired()])
    datetime = DateTimeField('Appointment Time', validators=[DataRequired()])
    submit = SubmitField('Schedule')
