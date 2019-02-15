from flask import Blueprint, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import jsonpickle
from classes import db, Patient, Report
from collections import Counter

area_blueprint = Blueprint('area_report', __name__, url_prefix='/')

@area_blueprint.route('/show_areas')
def area_reports():
    areas = []
    patients_by_area = []
    diagnoses_by_area = []
    counter_by_area = []

    for a in db.session.query(Patient.area).distinct().all():
        areas.append(a[0])
    
    for a in areas:
        p = []
        for q in db.session.query(Patient.patient_id).filter_by(area=a).all():
            p.append(q[0])
        patients_by_area.append({"area":a,"patient_ids":p})
    
    for dict in patients_by_area:
        diagnoses_by_id = []
        for id in dict["patient_ids"]:
            #returns all diagnoses for a given patient:
            q = db.session.query(Report.diagnosis).filter_by(patient_id=id).all()
            for diagnosis in q:
                diagnoses_by_id.append(diagnosis[0])
        diagnoses_by_area.append({"area":dict["area"],"diagnoses":diagnoses_by_id,"patient_ids":dict["patient_ids"]})
        
    for object in diagnoses_by_area:
        keys = list(Counter(object["diagnoses"]).keys())
        values = list(Counter(object["diagnoses"]).values())
        length = sum(values)
        key_values = {}
        for i in range(len(keys)):
            key_values[keys[i]] = values[i]
        counter_by_area.append({"area":object["area"],"total":len(object["patient_ids"]),"diagnosis_count":key_values})

    return jsonpickle.encode(counter_by_area)

@area_blueprint.route('/web/area_reports')
def render_reports():
    return render_template("area-reports.html", result=jsonpickle.decode(area_reports()), 
                           content_type="application/json")