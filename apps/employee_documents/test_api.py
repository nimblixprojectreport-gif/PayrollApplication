from fastapi.testclient import TestClient
from main import app
import os
import shutil

client = TestClient(app)

def test_upload_document():
    # Cleanup if needed
    if os.path.exists("uploads"):
        shutil.rmtree("uploads")
    
    with open("test.txt", "w") as f:
        f.write("test content")
    
    with open("test.txt", "rb") as f:
        response = client.post(
            "/api/v1/employees/emp123/documents?document_type=ID_PROOF",
            files={"file": ("test.txt", f, "text/plain")},
            headers={"Authorization": "Bearer testtoken"}
        )
    
    os.remove("test.txt")
    assert response.status_code == 201
    data = response.json()
    assert data["employee_id"] == "emp123"
    assert data["document_type"] == "ID_PROOF"
    return data["id"]

def test_list_documents():
    response = client.get("/api/v1/employees/emp123/documents", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_delete_document():
    # First upload
    doc_id = test_upload_document()
    response = client.delete(f"/api/v1/documents/{doc_id}", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200
    assert response.json()["message"] == "Document deleted successfully"
