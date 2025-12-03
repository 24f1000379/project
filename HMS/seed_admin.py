# seed_admin.py
from app import create_app
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    db.create_all()
    admin = User.query.filter_by(email="24f1000379@ds.study.iitm.ac.in").first()
    if admin:
        print("Admin already exists:", admin.email)
    else:
        admin = User(email="24f1000379@ds.study.iitm.ac.in", name="Admin", role="admin")
        admin.set_password("Ritik@123")  # uses model helper
        db.session.add(admin)
        db.session.commit()
        print("Created admin: 24f1000379@ds.study.iitm.ac.in / Ritik@123")
