import os
import aiofiles
from fastapi import UploadFile
from config import settings

class StorageService:
    def __init__(self):
        self.base_dir = settings.STORAGE_DIR
        os.makedirs(self.base_dir, exist_ok=True)

    async def save_file(self, company_id: str, doc_type: str, file: UploadFile) -> str:
        safe_filename = f"{company_id}_{doc_type}_{os.path.basename(file.filename or 'doc.bin')}"
        dest_path = os.path.join(self.base_dir, safe_filename)
        
        async with aiofiles.open(dest_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                await buffer.write(chunk)
                
        return dest_path

storage_service = StorageService()
