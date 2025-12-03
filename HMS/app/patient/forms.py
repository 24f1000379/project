# app/patient/forms.py
from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired

class AppointmentForm(FlaskForm):
    doctor_id = IntegerField("Doctor ID", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    time = TimeField("Time", validators=[DataRequired()])
    submit = SubmitField("Book Appointment")
