from flask import Flask, jsonify, request, Response
import json
from settings import *

#so flask knows where to look for stuff
#__name__ returns module name for this file
app = Flask(__name__)

class Patient:
    pass

class Report:
    pass


app.run(port=5000)