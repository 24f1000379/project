# app/auth/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db, login_manager
from ..models import User, Patient, Doctor
from .forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth", __name__, template_folder="templates/auth")

# user_loader for flask-login
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except Exception:
        return None

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # redirect based on role
        if current_user.role == "admin":
            return redirect(url_for("admin.index"))
        if current_user.role == "doctor":
            return redirect(url_for("doctor.index"))
        return redirect(url_for("patient.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            # redirect to role dashboard
            if user.role == "admin":
                return redirect(url_for("admin.index"))
            if user.role == "doctor":
                return redirect(url_for("doctor.index"))
            return redirect(url_for("patient.index"))
        flash("Invalid credentials", "danger")
    return render_template("auth/login.html", form=form)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    form = RegisterForm()
    if form.validate_on_submit():
        # ensure unique email
        exists = User.query.filter_by(email=form.email.data).first()
        if exists:
            flash("Email already registered", "danger")
            return render_template("auth/register.html", form=form)
        user = User(email=form.email.data, name=form.username.data, role="patient")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # create Patient profile
        patient = Patient(user_id=user.id)
        db.session.add(patient)
        db.session.commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))
