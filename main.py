from fastapi import FastAPI, Request
import uvicorn
import os
from src.hcc import HCCEngine
from models import DBHCCProfile, DBPatient
from schema import ProfileRequest, ProfileResponse
from middleware import log_request_middleware
from exception_handlers import request_validation_exception_handler, http_exception_handler, unhandled_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv

load_dotenv(".env")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

app.middleware("http")(log_request_middleware)
app.add_exception_handler(RequestValidationError,
                          request_validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.post("/hcc_profile", response_model=ProfileResponse)
async def hcc_profile(patient_data: ProfileRequest):

    hcc_engine_instance = HCCEngine(version="28", dx2cc_year="Combined", cif=0.059, norm_params={
        "C": 1.015, "D": 1.022, "G": 1.028})

    result = hcc_engine_instance.profile(
        dx_lst=patient_data.dx_lst,
        age=patient_data.age,
        sex=patient_data.sex,
        elig=patient_data.elig,
        orec=patient_data.orec,
        medicaid=patient_data.medicaid)

    db_patient = DBPatient(
        icd10_codes=patient_data.dx_lst,
        age=patient_data.age,
        sex=patient_data.sex,
        elig=patient_data.elig,
        orec=patient_data.orec,
        medicaid=patient_data.medicaid

    )

    db_profile = DBHCCProfile(
        risk_score=result["risk_score"],
        risk_score_age=result["risk_score_age"],
        risk_score_adj=result["risk_score_adj"],
        risk_score_age_adj=result["risk_score_age_adj"],
        details=result["details"],
        hcc_lst=result["hcc_lst"],
        hcc_map=result["hcc_map"]
    )
    db.session.add(db_profile)
    db.session.add(db_patient)
    db.session.commit()

    # Collect evidence and descriptions
    evidence = []
    for icd10_code, hcc_list in result["hcc_map"].items():
        for hcc_code in hcc_list:
            hcc_description = hcc_engine_instance.describe_hcc(hcc_code)
            evidence.append(
                {"icd10_code": icd10_code, "hcc_code": hcc_code, "description": hcc_description})

    descriptions = []
    for hcc_code in result["hcc_lst"]:
        hcc_description = hcc_engine_instance.describe_hcc(hcc_code)
        descriptions.append(
            {"hcc_code": hcc_code, "description": hcc_description})

    # Update the response object
    result.update({"evidence": evidence, "descriptions": descriptions})

    return JSONResponse(content={
        "risk_score": result["risk_score"],
        "risk_score_age": result["risk_score_age"],
        "risk_score_adj": result["risk_score_adj"],
        "risk_score_age_adj": result["risk_score_age_adj"],
        "details": result["details"],
        "hcc_lst": result["hcc_lst"],
        "hcc_map": result["hcc_map"],
        "parameters": result["parameters"],
        "model": result["model"],
        "evidence": result["evidence"],
        "descriptions": result["descriptions"]
    })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0 ", port=8000)
