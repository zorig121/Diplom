from fastapi import APIRouter, Depends, HTTPException
from models.user import UserCreate, LoginRequest, TokenResponse
from db.mongodb import get_db
from core.security import hash_password, verify_password, create_token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, db=Depends(get_db)):
    existing = await db["users"].find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user_doc = {
        "username": user.username,
        "email": user.email,
        "fullname": user.fullname,
        "hashed_password": hash_password(user.password),
        "is_active": True,
        "roles": ["user"],
        "created_at": datetime.utcnow()
    }
    await db["users"].insert_one(user_doc)
    return {"message": "User registered successfully"}

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = await db["users"].find_one({"username": form_data.username})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail="User is inactive")

    token = create_token(user["username"])
    return TokenResponse(access_token=token)