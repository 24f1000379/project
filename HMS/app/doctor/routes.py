# app/doctor/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

doctor_bp = Blueprint("doctor", __name__, template_folder="templates/doctor")

@doctor_bp.route("/")
@login_required
def index():
    if current_user.role != "doctor":
        flash("Doctor access required", "danger")
        return redirect(url_for("auth.login"))
    return render_template("doctor/index.html")
