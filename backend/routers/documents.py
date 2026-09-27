from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from services.storage import storage_service
from routers.auth import get_current_user
import models

router = APIRouter(prefix="/api/documents", tags=["Documents"])

@router.post("/upload")
async def upload_document(
    company_id: str = Form(...),
    doc_type: str = Form(...),
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty filename provided")

    saved_path = await storage_service.save_file(company_id, doc_type, file)
    return {
        "status": "uploaded",
        "file_name": file.filename,
        "doc_type": doc_type,
        "local_storage_path": saved_path
    }
