from pydantic import BaseModel


class ProfileRequest(BaseModel):
    dx_lst: list
    age: int
    sex: str
    elig: str
    orec: str
    medicaid: bool


class Evidence(BaseModel):
    icd10_code: str
    hcc_code: str
    description: dict


class Description(BaseModel):
    hcc_code: str
    description: dict


class ProfileResponse(BaseModel):
    risk_score: float
    risk_score_age: float
    risk_score_adj: float
    risk_score_age_adj: float
    details: dict
    hcc_lst: list
    hcc_map: dict
    parameters: dict
    model: str
    evidence: list[Evidence]
    descriptions: list[Description]
