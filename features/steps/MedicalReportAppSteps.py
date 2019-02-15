import behave
from pip._vendor import requests
from nose.tools.trivial import ok_
from selenium import webdriver


@given('Request for all Patients')
def fetch_all_patients(context):
    context.patients = requests.get('http://localhost:5000/web/manager')

# @then('Have all Patients available from application')
# def check_all_patients_present(context):
#     ok_(len(context.patients)>0, "Patients Not Available")

@given('Request for Patients')
def request_view_patients(context):
    context.driver = webdriver.Chrome()
    context.driver.get('http://localhost:5000/web/manager')
    context.countText = context.driver.find_element_by_id("count").text
    print(context.countText)

@then('Able to fetch the Patient Count')
def check_patient_count(context):
    context.driver.save_screenshot("snaps/PatientList.png")
    ok_(len(context.countText)>0,"Patient Count Found")

