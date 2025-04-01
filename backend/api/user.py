from fastapi import APIRouter, Depends
from core.security import get_current_user
from db.mongodb import get_db
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/me")
async def get_profile(current_user=Depends(get_current_user)):
    return {"username": current_user["username"]}

@router.get("/users")
async def get_users(db=Depends(get_db)):
    cursor = db["users"].find({}, {"_id": 0, "username": 1})
    return [doc async for doc in cursor]

@router.post("/logout")
async def logout():
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("access_token")
    return response

