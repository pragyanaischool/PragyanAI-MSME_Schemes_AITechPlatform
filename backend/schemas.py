from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from uuid import UUID

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    role: str = Field(pattern="^(msme|entity|admin)$")
    jurisdiction: Optional[str] = "Karnataka"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    jurisdiction: str
    user_id: str
    full_name: str

class ProfileInput(BaseModel):
    legal_name: str
    udyam_reg_no: str
    gstn: str = Field(min_length=15, max_length=15)
    state: str = "Karnataka"
    district: str
    zone: str
    sector: str
    turnover_lakhs: float = Field(gt=0)
    plant_machinery_inv_lakhs: float = Field(gt=0)
    employees: int = Field(gt=0)
    is_woman_owned: bool = False

class SchemeCreate(BaseModel):
    code: str
    title: str
    level: str = "State"
    department: str
    subsidy_percentage: float
    max_cap_lakhs: float
    target_sector: List[str]
    required_documents: List[str]

class VerificationAction(BaseModel):
    company_id: UUID
    status: str = Field(pattern="^(verified|rejected)$")
    notes: Optional[str] = None

class ApplicationSubmit(BaseModel):
    company_id: UUID
    scheme_code: str
    claimed_amount_lakhs: float = Field(gt=0)
    attached_documents: Optional[Dict[str, Any]] = {}

class ChatQuery(BaseModel):
    query: str
    language: Optional[str] = "English"
    company_id: Optional[UUID] = None
