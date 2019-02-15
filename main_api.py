from flask import Flask, jsonify, request, Response, Blueprint
import json
from flask_sqlalchemy import SQLAlchemy
import jsonpickle
from mysql import connector
from flask.templating import render_template
from werkzeug.utils import redirect
from classes import db, Patient, Report

main_blueprint = Blueprint('main',__name__, url_prefix='/')

@main_blueprint.route('/')
def application_home():
    return 'Welcome to NHS Application'

#Patient class http methods

@main_blueprint.route('/patients/register',methods=['POST'])
def create_Patient(p):
    patient = Patient(p)

    db.session.add(patient)
    db.session.commit()
    return jsonpickle.encode(patient)
    


@main_blueprint.route('/patients/list')
def get_Patients():
    
    patient_list = db.session.query(Patient).all()
    display_patient_list = []
    for patient in patient_list:
        display_patient_list.append({"patient_id":patient.patient_id,"name":patient.name,"gender":patient.gender,
        "date_of_birth":patient.date_of_birth,"area":patient.area,"phone_no":patient.phone_no})
    #print(display_patient_list)
    return jsonpickle.encode(display_patient_list)



@main_blueprint.route('/patients/<int:patient_id>')
def get_patient_by_patient_id(patient_id):

    patient_list = db.session.query(Patient).filter_by(patient_id=int(patient_id)).all()
    display_patient_list = []

    for patient in patient_list:
        display_patient_list.append({"patient_id":patient.patient_id,"name":patient.name,"gender":patient.gender,
        "date_of_birth":patient.date_of_birth,"area":patient.area,"phone_no":patient.phone_no})
    return jsonpickle.encode(display_patient_list)


@main_blueprint.route('/patients/<int:patient_id>', methods = ['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get(int(patient_id))
    db.session.delete(patient)
    db.session.commit()
    return jsonpickle.encode(patient)

#Report class http methods

@main_blueprint.route("/add-report/",methods=['POST'])
def add_report(r):
    report = Report(r)

    db.session.add(report)
    db.session.commit()
    return jsonify(report)

@main_blueprint.route("/get-reports/<int:patient_id>")
def get_reports(patient_id):
    report_list = db.session.query(Report).filter_by(patient_id=int(patient_id)).all()
    display_report_list = []
    for report in report_list:
        display_report_list.append({"report_id":report.report_id,"symptoms":report.symptoms,"date":report.date,"diagnosis":report.diagnosis,"patient_id":report.patient_id})
    return jsonpickle.encode(display_report_list)

@main_blueprint.route("/delete-report/<int:report_id>",methods=['DELETE'])
def delete_report(report_id):
    report = Report.query.get(int(report_id))
    db.session.delete(report)
    db.session.commit()
    return_report = {"report_id":report.report_id,"symptoms":report.symptoms,"date":report.date,"diagnosis":report.diagnosis,"patient_id":report.patient_id}
    return jsonpickle.encode(return_report)

@main_blueprint.route("/update-report/<int:report_id>",methods=['POST'])
def edit_report(report_id):
    request_data = request.get_json()
    report = Report.query.get(int(report_id))
    report.symptoms = request_data["symptoms"]
    report.date = request_data["date"]
    report.diagnosis = request_data["diagnosis"]
    report.patient_id = request_data["patient_id"]
    db.session.commit()
    return_report = {"report_id":report.report_id,"symptoms":report.symptoms,"date":report.date,"diagnosis":report.diagnosis,"patient_id":report.patient_id}
    return jsonpickle.encode(return_report)


#html links

@main_blueprint.route('/web/patients/register', methods=["POST"])
def register_patient_web():
    
    p={"patient_id":int(request.form.get("patient_id")),
         "name":request.form.get("name"),
         "gender":request.form.get("gender"),
         "date_of_birth":request.form.get("date_of_birth"),
         "area":request.form.get("area"),
         "phone_no":int(request.form.get("phone_no"))}
    create_Patient(p)
    return redirect("/web/patients") # redirects user to patient list

@main_blueprint.route('/web/patients')
def display_patient_page():
    return render_template("patient.html", result=jsonpickle.decode(get_Patients()), 
                           content_type="application/json")

@main_blueprint.route('/web/')
def display_home_page():
    return render_template("home.html", 
                           content_type="application/json")


@main_blueprint.route('/web/manager')
def display_patient_page_for_manager():
    return render_template("patient-list-manager.html", result=jsonpickle.decode(get_Patients()), 
                           content_type="application/json")
    


@main_blueprint.route("/web/manager/reports/<int:patient_id>")
def display_reports_by_id(patient_id):
    return render_template("manager-reports.html", result=jsonpickle.decode(get_reports(int(patient_id))), 
                           content_type="application/json")


#section of things that don't work


@main_blueprint.route("/web/manager/reports/add-report/<int:patient_id>",methods=['POST'])
def add_report_to_patient(patient_id):

    r={"patient_id":int(patient_id),
        "symptoms":request.form.get("symptoms"),
        "date":request.form.get("date"),
        "diagnosis":request.form.get("diagnosis")
        }
    
    add_report(r)

    return redirect("/web/manager/reports")

@main_blueprint.route("/web/manager/reports/delete",methods=['DELETE'])
def delete_report_as_manager(report_id):
    delete_report(report_id)
    return redirect("/web/manager/reports")


# @app.route("/web/manager/reports/edit",methods=['POST'])
# def edit_report_as_manager(report_id):