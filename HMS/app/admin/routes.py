# app/admin/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models import User, Doctor, Patient
from .forms import DoctorForm, PatientForm

admin_bp = Blueprint("admin", __name__, template_folder="templates/admin")

def admin_required(fn):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("Admin access required", "danger")
            return redirect(url_for("auth.login"))
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@admin_bp.route("/")
@login_required
@admin_required
def index():
    doctors = Doctor.query.all()
    patients = Patient.query.all()
    return render_template("admin/index.html", doctors=doctors, patients=patients)

@admin_bp.route("/add_doctor", methods=["GET", "POST"])
@login_required
@admin_required
def add_doctor():
    form = DoctorForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data).first()
        if existing:
            flash("Email already used", "danger")
            return render_template("admin/add_doctor.html", form=form)
        user = User(email=form.email.data, name=form.username.data, role="doctor")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        doctor = Doctor(user_id=user.id, specialization=form.specialization.data)
        db.session.add(doctor)
        db.session.commit()
        flash("Doctor added", "success")
        return redirect(url_for("admin.index"))
    return render_template("admin/add_doctor.html", form=form)

@admin_bp.route("/add_patient", methods=["GET", "POST"])
@login_required
@admin_required
def add_patient():
    form = PatientForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data).first()
        if existing:
            flash("Email already used", "danger")
            return render_template("admin/add_patient.html", form=form)
        user = User(email=form.email.data, name=form.username.data, role="patient")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        patient = Patient(user_id=user.id, age=form.age.data, address=form.address.data)
        db.session.add(patient)
        db.session.commit()
        flash("Patient added", "success")
        return redirect(url_for("admin.index"))
    return render_template("admin/add_patient.html", form=form)
