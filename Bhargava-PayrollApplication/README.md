
Auth API v2 (With User Model + Refresh Token)

Features:
- Login (Access + Refresh Token)
- Logout
- Refresh Token
- Change Password
- Get Profile

Default User:
username: admin
password: admin123

Run:
pip install -r requirements.txt
uvicorn app.main:app --reload

Swagger:
http://127.0.0.1:8000/docs
