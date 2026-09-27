import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # "msme", "entity", "admin"
    jurisdiction = Column(String(50), default="Karnataka", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Company(Base):
    __tablename__ = "companies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    legal_name = Column(String(255), nullable=False)
    udyam_reg_no = Column(String(50), unique=True, index=True, nullable=False)
    gstn = Column(String(15), unique=True, index=True, nullable=False)
    state = Column(String(50), default="Karnataka", nullable=False)
    district = Column(String(50), nullable=False)
    zone = Column(String(50), default="Zone 2 (Developing)", nullable=False)
    sector = Column(String(50), nullable=False)
    turnover_lakhs = Column(Float, nullable=False)
    plant_machinery_inv_lakhs = Column(Float, nullable=False)
    employees = Column(Integer, default=1, nullable=False)
    is_woman_owned = Column(Boolean, default=False, nullable=False)
    verification_status = Column(String(30), default="pending", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Scheme(Base):
    __tablename__ = "schemes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    level = Column(String(20), default="State", nullable=False)
    department = Column(String(100), nullable=False)
    subsidy_percentage = Column(Float, default=0.0, nullable=False)
    max_cap_lakhs = Column(Float, default=0.0, nullable=False)
    target_sector = Column(JSON, default=list, nullable=False)
    required_documents = Column(JSON, default=list, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

class Application(Base):
    __tablename__ = "applications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    scheme_code = Column(String(50), nullable=False)
    current_stage = Column(String(50), default="Submitted", nullable=False)
    claimed_amount_lakhs = Column(Float, nullable=False)
    sanctioned_amount_lakhs = Column(Float, default=0.0, nullable=False)
    attached_documents = Column(JSON, default=dict, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
