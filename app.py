from flask import Flask, jsonify, request, Response
import json
from flask_sqlalchemy import SQLAlchemy
import jsonpickle
from mysql import connector

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/patient_records'
db = SQLAlchemy(app)

#classes

class Patient(db.Model):
    __tablename__= "patient_details"
    patient_id= db.Column(db.Integer, primary_key = True)
    name = db.Column("patient_name", db.String(50))
    gender = db.Column("gender",db.String(6))
    date_of_birth = db.Column("date_of_birth", db.String(10))
    area = db.Column("area", db.String(20))
    phone_no = db.Column("phone_no", db.Integer)
    reports = db.relationship('report',backref='patient',lazy=True)
    
    def __init__(self,params):
        self.name = params["name"]
        self.gender = params["gender"]
        self.date_of_birth = params["date_of_birth"]
        self.area = params["area"]
        self.phone_no = params["phone_no"]
        pass
    
    def __str__(self):
        return"Id:"+ str(self.patient_id)+" Name:"+self.name+" Gender:"+self.gender+" Date of Birth:"+self.date_of_birth+" Area:"+self.area+" Phone Number:"+str(self.phone_no)

class Report(db.Model):
    __tablename__ = "reports"
    report_id = db.Column(db.Integer,primary_key=True)
    symptoms = db.Column(db.String(1000))
    date = db.Column(db.String(10))
    diagnosis = db.Column(db.String(50))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_details.patient_id'),nullable=False)

db.create_all()

#Patient class http methods

@app.route('/patients/register',methods=['POST'])
def create_Patient():
    p = Patient({"name":"Test Patient","gender":"male","date_of_birth":"01/01/2010",
                "area":"Leeds","phone_no":67})
    
    db.session.add(p)
    db.session.commit()

    patients = Patient.query.all()

    for p in patients:
        print("ID:",p.patient_id,"Name:",p.name,"Gender:",p.gender, "Date of Birth:",p.date_of_birth,
            "Area:",p.area, "Phone Number:",p.phone_no)

    pass
    
    


@app.route('/patients/list')
def get_Patients():
    
    patient_list = db.session.query(Patient).all()
    display_patient_list = []
    for patient in patient_list:
        display_patient_list.append({"patient_id":patient.patient_id,"name":patient.name,"gender":patient.gender,
        "date_of_birth":patient.date_of_birth,"area":patient.area,"phone_no":patient.phone_no})
    return jsonpickle.encode(display_patient_list)



@app.route('/patients/<int:patient_id>')
def get_patient_by_patient_id(patient_id):

    patient_list = db.session.query(Patient).filter_by(patient_id=int(patient_id)).all()
    display_patient_list = []

    for patient in patient_list:
        display_patient_list.append({"patient_id":patient.patient_id,"name":patient.name,"gender":patient.gender,
        "date_of_birth":patient.date_of_birth,"area":patient.area,"phone_no":patient.phone_no})
    return jsonpickle.encode(display_patient_list)


@app.route('/patients/<int:patient_id>', methods = ['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get(int(patient_id))
    db.session.delete(patient)
    db.session.commit()
    return jsonpickle.encode(patient)

#Report class http methods

@app.route("/add-report/<int:patient_id>",methods=['POST'])
def add_report(patient_id):
    request_data = request.get_json()
    request_data["patient_id"] = int(patient_id)
    r = Report(**request_data)
    db.session.add(r)
    db.session.commit()
    return jsonify(request_data)

@app.route("/get-reports/<int:patient_id>")
def get_reports(patient_id):
    report_list = db.session.query(Report).filter_by(patient_id=int(patient_id)).all()
    display_report_list = []
    for report in report_list:
        display_report_list.append({"report_id":report.report_id,"symptoms":report.symptoms,"date":report.date,"diagnosis":report.diagnosis,"patient_id":report.patient_id})
    return jsonpickle.encode(display_report_list)

@app.route("/delete-report/<int:report_id>",methods=['DELETE'])
def delete_report(report_id):
    report = Report.query.get(int(report_id))
    db.session.delete(report)
    db.session.commit()
    return_report = {"report_id":report.report_id,"symptoms":report.symptoms,"date":report.date,"diagnosis":report.diagnosis,"patient_id":report.patient_id}
    return jsonpickle.encode(return_report)

@app.route("/update-report/<int:report_id>",methods=['POST'])
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

app.run(port=5000)