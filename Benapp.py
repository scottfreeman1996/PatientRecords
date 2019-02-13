from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy

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
    patient_id = (db.Integer)

    def __init__(self,params):
        self.report_id = params["report_id"]
        self.symptoms = params["symptoms"]
        # self.date = params["date"]
        # self.diagnosis = params["diagnosis"]
        # self.diagnosis = params["patient_id"]

def add_report(params):
    r = Report(params)
    db.session.add(r)
    db.session.commit()

db.create_all()

r = {"report_id":10,"symptoms":"my body hurt sooo bad:("}
add_report(r)

app.run(port=5000)