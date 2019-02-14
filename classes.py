#classes

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__= "patient_details"
    patient_id= db.Column(db.Integer, primary_key = True)
    name = db.Column("patient_name", db.String(50))
    gender = db.Column("gender",db.String(6))
    date_of_birth = db.Column("date_of_birth", db.String(10))
    area = db.Column("area", db.String(20))
    phone_no = db.Column("phone_no", db.Integer)
    # reports = db.relationship('report',backref='patient',lazy=True)
    
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
    patient_id = db.Column(db.Integer)#, db.ForeignKey('patient_details.patient_id'),nullable=False)