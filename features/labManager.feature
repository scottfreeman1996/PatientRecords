Feature: Patient Management using Flask

Scenario: Get the Patient list from DB as a Lab Manager
    Given Request for all Patients
    Then Have all Patients available from application

Scenario: Get the Patient Count
    Given Request for Patients
    Then Able to fetch the Patient Count

Scenario: Add Patient Details
	Given a set of patients
	|patient_id	|name		|gender	|date_of_birth  |area   |phone_no   |
	|23 	    |Test   	|34333	|01/01/2000     |Leeds  |123        |
	Then increases Patient Count
    
