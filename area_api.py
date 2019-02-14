from flask import Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
import jsonpickle
from classes import db, Patient, Report
# from app import Patient, Report

area_blueprint = Blueprint('area_report', __name__, url_prefix='/area_report')

@area_blueprint.route('/show_areas')
def area_reports():
    areas = []
    patients_by_area = []
    diagnoses_by_area = []

    for a in db.session.query(Patient.area).distinct().all():
        areas.append(a[0])
    
    for a in areas:
        p = []
        for q in db.session.query(Patient.patient_id).filter_by(area=a).all():
            p.append(q[0])
        patients_by_area.append({"area":a,"patient_ids":p})
    
    for dict in patients_by_area:
        for id in dict["patient_ids"]:
            diagnoses_by_id = []
            #returns all diagnoses for a given patient:
            q = db.session.query(Report.diagnosis).filter_by(patient_id=id).all()
            for diagnosis in q:
                diagnoses_by_id.append(diagnosis[0])
        diagnoses_by_area.append({"area":dict["area"],"diagnoses":diagnoses_by_id})
        
    
    return jsonify(diagnoses_by_area)