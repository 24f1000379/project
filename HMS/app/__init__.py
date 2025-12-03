# app/__init__.py
from flask import Flask, redirect, url_for
from config import Config

from .extensions import db, login_manager
# import blueprints by their variable names
from .auth.routes import auth_bp
from .admin.routes import admin_bp
from .doctor.routes import doctor_bp
from .patient.routes import patient_bp
#from .api.routes import api_bp if False else None  # placeholder if you don't have api_bp
from .api.routes import api as api_bp
...


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)
    app.register_blueprint(api_bp, url_prefix='/api')

    # ensure instance folder exists (sqlite file location)
    import os
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except Exception:
        pass

    # init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # endpoint name for login

    # register blueprints (each only once)
    app.register_blueprint(auth_bp)                 # no prefix -> /login
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(doctor_bp, url_prefix="/doctor")
    app.register_blueprint(patient_bp, url_prefix="/patient")
    # api_bp is optional; register if implemented:
    # if api_bp:
    #     app.register_blueprint(api_bp, url_prefix='/api')

    # root: redirect to login (safe)
    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    # temporary health check
    @app.route("/_ping")
    def _ping():
        return "HMS OK", 200

    return app
