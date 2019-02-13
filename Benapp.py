from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import jsonpickle

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/patient_records'
db = SQLAlchemy(app)

class Patient:
    pass

class Report(db.Model):
    __tablename__ = "reports"
    report_id = db.Column(db.Integer,primary_key=True)
    symptoms = db.Column(db.String(1000))
    date = db.Column(db.String(10))
    diagnosis = db.Column(db.String(50))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_id'),nullable=False)


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

db.create_all()

# r = {"symptoms":"RAH IT HURTS","date":"3/4/29","diagnosis":"bubonic plague"}
# add_report(r,78)

app.run(port=5000)