from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from services.eligibility_engine import eligibility_engine
from routers.auth import get_current_user

router = APIRouter(prefix="/api/schemes", tags=["Schemes"])

@router.get("/evaluate/{company_id}")
def evaluate_company_schemes(company_id: UUID, db: Session = Depends(get_db)):
    comp = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")
    
    matches = eligibility_engine.evaluate(comp)
    return {"company": comp.legal_name, "zone": comp.zone, "matches": matches}

@router.post("/publish")
def publish_scheme(
    data: schemas.SchemeCreate, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if current_user.role not in ["entity", "admin"]:
        raise HTTPException(status_code=403, detail="Unauthorized to publish schemes")
    
    scheme = models.Scheme(**data.model_dump())
    db.add(scheme)
    db.commit()
    db.refresh(scheme)
    return {"status": "success", "scheme_code": scheme.code}
