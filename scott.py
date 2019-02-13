from flask import Flask, jsonify, request, Response
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/patient_records'
db = SQLAlchemy(app)

class Patient(db.Model):
    __tablename__= "patient_details"
    patient_id= db.Column(db.Integer, primary_key = True)
    name = db.Column("patient_name", db.String(50))
    gender = db.Column("gender",db.String(6))
    date_of_birth = db.Column("date_of_birth", db.String(10))
    area = db.Column("area", db.String(20))
    phone_no = db.Column("phone_no", db.Integer)
    
    def __init__(self,params):
        self.name = params["name"]
        self.gender = params["gender"]
        self.date_of_birth = params["date_of_birth"]
        self.area = params["area"]
        self.phone_no = params["phone_no"]
        pass

@app.route('/patients')
def create_Patient():
    p = Patient({"name":"Test Patient","gender":"male","date_of_birth":"01/01/2010",
                "area":"Leeds","phone_no":67})
    
    db.session.add(p)
    db.session.commit()

    patients = Patient.query.all()

    for p in patients:
        print("ID:",p.patient_id,"Name:",p.name,"Gender:",p.gender, "Date of Birth:",p.date_of_birth,
            "Area:",p.area, "Phone Number:",p.phone_no)



if __name__ == '__main__':
    #db.create_all()

    create_Patient()
    app.run(port=5000)
    pass