from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class DBPatient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    icd10_codes = Column(JSON, nullable=False)
    age = Column(Integer)
    sex = Column(String)
    elig = Column(String)
    orec = Column(String)
    medicaid = Column(Boolean)


class DBHCCProfile(Base):
    __tablename__ = "hcc_profiles"

    id = Column(Integer, primary_key=True, index=False)
    risk_score = Column(Float)
    risk_score_age = Column(Float)
    risk_score_adj = Column(Float)
    risk_score_age_adj = Column(Float)
    details = Column(JSON)
    hcc_lst = Column(JSON)
    hcc_map = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    patient_id = Column(Integer, ForeignKey("patients.id"))
    patient = relationship("DBPatient", backref="hcc_profiles", uselist=False)
