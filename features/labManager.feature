Feature: Patient Management using Flask

Scenario: Get the Patient list from DB as a Lab Manager
    Given Request for all Patients
    Then list all Patients available

Scenario: Get the Patient Count
    Given Request for Patients
    Then Able to fetch the Patient Count
