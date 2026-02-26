import requests
import json
import io
from PIL import Image

BASE_URL = "http://127.0.0.1:8000/api/v1/"

def test_api():
    # 1. Login
    print("Testing Login...")
    login_url = "http://127.0.0.1:8000/api/v1/auth/login/"
    login_data = {"username": "admin", "password": "admin123"}
    response = requests.post(login_url, json=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
    token = response.json()['access']
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful.")

    # 2. Create Employee
    print("\nCreating Employee...")
    emp_url = BASE_URL + "employees/"
    emp_data = {
        "first_name": "John",
        "last_name": "Doe",
        "company_id": "COMP001",
        "email": "john.doe@example.com"
    }
    response = requests.post(emp_url, json=emp_data, headers=headers)
    if response.status_code not in [200, 201]:
        print(f"Employee creation failed: {response.text}")
        return
    employee_id = response.json()['id']
    print(f"Employee created with ID: {employee_id}")

    # 3. Check-in
    print("\nTesting Check-in...")
    checkin_url = BASE_URL + "attendance/check-in/"
    
    # Create a dummy image for selfie
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    files = {'selfie': ('test_selfie.jpg', img_byte_arr, 'image/jpeg')}
    data = {
        'employee': employee_id,
        'latitude': 12.9716,
        'longitude': 77.5946
    }
    
    response = requests.post(checkin_url, data=data, files=files, headers=headers)
    print(f"Check-in response: {response.status_code}")
    print(response.json())
    
    if response.status_code == 200:
        attendance_id = response.json()['attendance_id']
        
        # 4. Check-out
        print("\nTesting Check-out...")
        checkout_url = BASE_URL + "attendance/check-out/"
        response = requests.post(checkout_url, json={"attendance_id": attendance_id}, headers=headers)
        print(f"Check-out response: {response.status_code}")
        print(response.json())
    else:
        print("Check-in failed, skipping check-out test.")

if __name__ == "__main__":
    test_api()
