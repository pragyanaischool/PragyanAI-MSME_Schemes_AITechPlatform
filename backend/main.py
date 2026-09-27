from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
from routers import auth, companies, schemes, documents, ai

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MSME Scheme & Subsidy AI Platform Core",
    version="2.6.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(schemes.router)
app.include_router(documents.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"status": "online", "system": "MSME Scheme & Subsidy AI Navigator Engine"}

@app.get("/api/dashboard/msme")
def msme_dashboard(
    current_user: models.User = Depends(auth.get_current_user), 
    db: Session = Depends(get_db)
):
    if current_user.role != "msme":
        raise HTTPException(status_code=403, detail="MSME Applicant access only")

    comp = db.query(models.Company).filter(models.Company.user_id == current_user.id).first()
    apps = []
    if comp:
        app_records = db.query(models.Application).filter(models.Application.company_id == comp.id).all()
        apps = [
            {
                "id": str(a.id),
                "scheme": a.scheme_code,
                "stage": a.current_stage,
                "claimed": a.claimed_amount_lakhs,
                "sanctioned": a.sanctioned_amount_lakhs
            } for a in app_records
        ]

    return {
        "user": current_user.full_name,
        "company_profile": comp,
        "applications": apps
    }

@app.get("/api/dashboard/admin")
def admin_dashboard(
    current_user: models.User = Depends(auth.get_current_user), 
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    total_companies = db.query(models.Company).count()
    pending = db.query(models.Company).filter(models.Company.verification_status == "pending").all()
    total_apps = db.query(models.Application).count()

    return {
        "jurisdiction": current_user.jurisdiction,
        "total_registered_msmes": total_companies,
        "pending_verifications_count": len(pending),
        "total_active_applications": total_apps,
        "pending_queue": pending
    }

@app.post("/api/admin/verify-company")
def verify_company_status(
    action: schemas.VerificationAction,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    comp = db.query(models.Company).filter(models.Company.id == action.company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    comp.verification_status = action.status
    db.commit()
    return {"status": "success", "company": comp.legal_name, "verification_status": comp.verification_status}

@app.get("/api/dashboard/entity")
def entity_dashboard(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "entity":
        raise HTTPException(status_code=403, detail="Entity access only")

    schemes_list = db.query(models.Scheme).filter(models.Scheme.department == current_user.full_name).all()
    claims = db.query(models.Application).all()

    return {
        "department": current_user.full_name,
        "published_schemes": schemes_list,
        "claims_to_scrutinize": claims
    }
