from fastapi import APIRouter, Depends, HTTPException
from models.user import UserCreate, LoginRequest
from db.mongodb import get_db
from core.security import hash_password, verify_password, create_token

router = APIRouter()

@router.post("/api/register")
async def register(user: UserCreate, db=Depends(get_db)):
    if await db["users"].find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    if await db["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed = hash_password(user.password)
    await db["users"].insert_one({
        "username": user.username,
        "password": hashed,
        "email": user.email,
        "fullname": user.fullname
    })

    return {"access_token": create_token(user.username)}

@router.post("/api/login")
async def login(user: LoginRequest, db=Depends(get_db)):
    existing = await db["users"].find_one({"username": user.username})
    if not existing or not verify_password(user.password, existing["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": create_token(existing["username"])}
