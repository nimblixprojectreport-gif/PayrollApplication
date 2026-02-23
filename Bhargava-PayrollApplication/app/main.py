
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import uuid

SECRET_KEY = "secretkey123"
REFRESH_SECRET_KEY = "refreshsecret123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

app = FastAPI(title="Auth API v2")
from fastapi.responses import RedirectResponse

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# --------------------
# Models
# --------------------

class User(BaseModel):
    id: str
    company_id: str
    username: str
    email: str
    password: str
    is_active: bool


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


# --------------------
# Fake Database
# --------------------

fake_users_db = {
    "admin": {
        "id": str(uuid.uuid4()),
        "company_id": "COMP001",
        "username": "admin",
        "email": "admin@test.com",
        "hashed_password": pwd_context.hash("admin123"),
        "is_active": True,
    }
}

refresh_tokens_db = {}

# --------------------
# Utils
# --------------------

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username, password):
    user = fake_users_db.get(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)

    user = fake_users_db.get(username)

    if user is None or not user["is_active"]:
        raise HTTPException(status_code=401)

    return user


# --------------------
# APIs
# --------------------

@app.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends()):

    user = authenticate_user(form.username, form.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = create_refresh_token(
        data={"sub": user["username"]}
    )

    refresh_tokens_db[user["username"]] = refresh_token

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@app.post("/logout")
def logout(user=Depends(get_current_user)):

    username = user["username"]

    if username in refresh_tokens_db:
        del refresh_tokens_db[username]

    return {"message": "Logout successful"}


@app.post("/refresh", response_model=TokenResponse)
def refresh_token(token: str):

    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    saved_token = refresh_tokens_db.get(username)

    if saved_token != token:
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    new_access = create_access_token({"sub": username})
    new_refresh = create_refresh_token({"sub": username})

    refresh_tokens_db[username] = new_refresh

    return {
        "access_token": new_access,
        "refresh_token": new_refresh
    }


@app.post("/change-password")
def change_password(data: ChangePassword, user=Depends(get_current_user)):

    username = user["username"]

    if not verify_password(data.old_password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Wrong old password")

    fake_users_db[username]["hashed_password"] = get_password_hash(
        data.new_password
    )

    return {"message": "Password updated successfully"}


@app.get("/me")
def get_profile(user=Depends(get_current_user)):
    return {
        "id": user["id"],
        "company_id": user["company_id"],
        "username": user["username"],
        "email": user["email"],
        "is_active": user["is_active"]
    }
