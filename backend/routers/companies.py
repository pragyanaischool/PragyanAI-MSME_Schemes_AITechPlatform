from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from routers.auth import get_current_user

router = APIRouter(prefix="/api/company", tags=["Companies"])

@router.post("/register")
def upsert_company(
    data: schemas.ProfileInput, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    comp = db.query(models.Company).filter(models.Company.user_id == current_user.id).first()
    if not comp:
        comp = models.Company(user_id=current_user.id, **data.model_dump())
        db.add(comp)
    else:
        for k, v in data.model_dump().items():
            setattr(comp, k, v)
    db.commit()
    db.refresh(comp)
    return {"status": "success", "company_id": str(comp.id), "legal_name": comp.legal_name}

@router.get("/me")
def get_my_company(
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    comp = db.query(models.Company).filter(models.Company.user_id == current_user.id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company profile not created")
    return comp
