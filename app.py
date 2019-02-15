from flask import Flask, jsonify, request, Response
import json
import jsonpickle
from mysql import connector
from classes import db, Report, Patient
from area_api import area_blueprint
from main_api import main_blueprint

app = Flask(__name__)
app.register_blueprint(area_blueprint)
app.register_blueprint(main_blueprint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/patient_records'

with app.app_context():
    db.init_app(app)
    db.create_all()
    db.session.commit()

app.run(port=5000)