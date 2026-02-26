from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class EmployeeDocumentBase(BaseModel):
    document_type: str

class EmployeeDocumentCreate(EmployeeDocumentBase):
    employee_id: str

class EmployeeDocument(EmployeeDocumentBase):
    id: str
    employee_id: str
    file_path: str
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SuccessResponse(BaseModel):
    message: str
