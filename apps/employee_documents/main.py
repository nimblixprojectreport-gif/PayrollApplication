import os
import shutil
import uuid
from typing import List
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import models, schemas, database

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Employee Management Module - Documents API",
    description="API for managing employee documents",
    version="1.0.0"
)

security = HTTPBearer()

def get_current_user(auth: HTTPAuthorizationCredentials = Depends(security)):
    # In a real app, you would verify the JWT here.
    # For now, we accept any valid bearer token.
    return auth.credentials

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.post("/api/v1/employees/{employee_id}/documents", response_model=schemas.EmployeeDocument, status_code=201)
async def upload_document(
    employee_id: str,
    document_type: str,
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_user)
):
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_document = models.EmployeeDocument(
        employee_id=employee_id,
        document_type=document_type,
        file_path=file_path
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

@app.get("/api/v1/employees/{employee_id}/documents", response_model=List[schemas.EmployeeDocument])
def list_employee_documents(employee_id: str, db: Session = Depends(database.get_db), token: str = Depends(get_current_user)):
    return db.query(models.EmployeeDocument).filter(models.EmployeeDocument.employee_id == employee_id).all()

@app.get("/api/v1/documents/{document_id}", response_model=schemas.EmployeeDocument)
def get_document(document_id: str, db: Session = Depends(database.get_db), token: str = Depends(get_current_user)):
    db_document = db.query(models.EmployeeDocument).filter(models.EmployeeDocument.id == document_id).first()
    if not db_document:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document

@app.delete("/api/v1/documents/{document_id}", response_model=schemas.SuccessResponse)
def delete_document(document_id: str, db: Session = Depends(database.get_db), token: str = Depends(get_current_user)):
    db_document = db.query(models.EmployeeDocument).filter(models.EmployeeDocument.id == document_id).first()
    if not db_document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Optional: Delete actual file
    if os.path.exists(db_document.file_path):
        os.remove(db_document.file_path)
        
    db.delete(db_document)
    db.commit()
    return {"message": "Document deleted successfully"}
