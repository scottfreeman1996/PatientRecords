from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
import jsonpickle
from classes import db, Patient, Report
# from app import Patient, Report

area_blueprint = Blueprint('area_report', __name__, url_prefix='/area_report')

@area_blueprint.route('/show_areas')
def area_reports():
    # areas = db.session.query(Patient.area).distinct()
    # return areas
    return "YES"