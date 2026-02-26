from fastapi.testclient import TestClient
import main
import os
import shutil

client = TestClient(main.app)

def verify_api():
    print("--- Starting API Verification ---")
    
    # 1. Create a dummy file
    with open("verify_test.txt", "w") as f:
        f.write("test content for verification")
    
    # 2. Upload the file
    print("Testing POST /api/v1/employees/VERIFY_EMP/documents...")
    with open("verify_test.txt", "rb") as f:
        response = client.post(
            "/api/v1/employees/VERIFY_EMP/documents?document_type=VERIFICATION_DOC",
            files={"file": ("verify_test.txt", f, "text/plain")}
        )
    
    os.remove("verify_test.txt")
    
    if response.status_code == 201:
        print("SUCCESS: Document uploaded.")
        data = response.json()
        doc_id = data["id"]
        print(f"Document ID: {doc_id}")
        
        # 3. List documents
        print("Testing GET /api/v1/employees/VERIFY_EMP/documents...")
        list_response = client.get("/api/v1/employees/VERIFY_EMP/documents")
        if list_response.status_code == 200:
            print(f"SUCCESS: Found {len(list_response.json())} documents for employee VERIFY_EMP.")
            
            # 4. Delete document
            print(f"Testing DELETE /api/v1/documents/{doc_id}...")
            delete_response = client.delete(f"/api/v1/documents/{doc_id}")
            if delete_response.status_code == 200:
                print("SUCCESS: Document deleted.")
            else:
                print(f"FAILURE: Received {delete_response.status_code}")
        else:
            print(f"FAILURE: Received {list_response.status_code}")
    else:
        print(f"FAILURE: Received {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    verify_api()
