from flask import Blueprint, jsonify
from ..models import Doctor

api = Blueprint('api', __name__)

@api.route('/doctors')
def list_doctors():
    doctors = Doctor.query.all()
    doctors_data = [{'id': d.user_id, 'name': d.user.name, 'specialization': d.specialization} for d in doctors]
    return jsonify(doctors=doctors_data)