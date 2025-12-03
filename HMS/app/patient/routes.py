# app/patient/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import Doctor, Patient, Appointment
from ..extensions import db
from .forms import AppointmentForm

patient_bp = Blueprint("patient", __name__, template_folder="templates/patient")

@patient_bp.route("/")
@login_required
def index():
    if current_user.role != "patient":
        flash("Patient access required", "danger")
        return redirect(url_for("auth.login"))
    return render_template("patient/index.html")

@patient_bp.route("/book", methods=["GET", "POST"])
@login_required
def book():
    if current_user.role != "patient":
        flash("Patient access required", "danger")
        return redirect(url_for("auth.login"))
    form = AppointmentForm()
    if form.validate_on_submit():
        # Very simple booking: find doctor by id field (form.doctor_id)
        doctor = Doctor.query.filter_by(id=form.doctor_id.data).first()
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not doctor or not patient:
            flash("Doctor or patient record missing", "danger")
            return render_template("patient/book.html", form=form)
        # check double booking
        from datetime import datetime
        date = form.date.data
        time = form.time.data
        conflict = Appointment.query.filter_by(doctor_id=doctor.id, date=date, time=time).first()
        if conflict:
            flash("Time slot already booked for this doctor", "danger")
            return render_template("patient/book.html", form=form)
        appt = Appointment(doctor_id=doctor.id, patient_id=patient.id, date=date, time=time)
        db.session.add(appt)
        db.session.commit()
        flash("Appointment booked", "success")
        return redirect(url_for("patient.index"))
    return render_template("patient/book.html", form=form)
