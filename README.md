Returns the HCC risk profile of a given patient information.

API to compute risk profile of a patient based on CMS guidelines and Software prototype, Risk Score of a patient based on demographics, insurance category and diagnosis of Chronic Conditions. The adjusted risk Score (RAF Score) helps to predict the reimbursement a provider will receive for the patient. It depends on the weights assigned to the chronic conditions. Sometimes, these chronic conditions gets unnoticed and are not documented properly therefore leading to decreased RAF score and less
reimbursement. Through this project we are aiming to include all the ICDs that are documented in the patient’s chart which count towards the total weight of the RAF score.
Implementation in FASTAPI.

Request Payload-
---- Parameters ----
dx_lst : list of str A list of ICD10 codes for the measurement year.
age : int or float The age of the patient.
sex : str The sex of the patient: M or F
elig : str The eligibility segment of the patient.
Allowed values are as follows: -
"CFA": Community Full Benefit Dual Aged
"CFD": Community Full Benefit Dual Disabled
"CNA": Community NonDual Aged
"CND": Community NonDual Disabled
"CPA": Community Partial Benefit Dual Aged
"CPD": Community Partial Benefit Dual Disabled
"INS": Long Term Institutional
"NE": New Enrollee
"SNPNE": SNP NE
orec: str Original reason for entitlement code.
"0": Old age and survivor's insurance
"1": Disability insurance benefits
"2": End-stage renal disease
"3": Both DIB and ESRD medicaid: bool If the patient is in Medicaid or not.
*Refer Technical Specification document for description of entities in the output file.
Raw Risk Score: Risk Score of a patient based on demographics, insurance category and diagnosis of Chronic Conditions.
RAF Score: Adjusted Risk Score to predict the annual reimbursement of a patient.

