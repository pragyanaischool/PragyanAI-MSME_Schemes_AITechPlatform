from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from services.groq_agent import groq_agent_graph

router = APIRouter(prefix="/api/ai", tags=["AI Advisor"])

@router.post("/advisor")
def copilot_query(payload: schemas.ChatQuery, db: Session = Depends(get_db)):
    context = "Enterprise context not specified."
    if payload.company_id:
        comp = db.query(models.Company).filter(models.Company.id == payload.company_id).first()
        if comp:
            context = f"Company: {comp.legal_name}, Sector: {comp.sector}, Turnover: ₹{comp.turnover_lakhs}L, Machinery: ₹{comp.plant_machinery_inv_lakhs}L, Zone: {comp.zone}, State: {comp.state}"

    state_input = {
        "query": payload.query,
        "language": payload.language or "English",
        "company_context": context,
        "rag_context": "",
        "response": ""
    }

    result = groq_agent_graph.invoke(state_input)
    return {"response": result["response"], "language": payload.language}
