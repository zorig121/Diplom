from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from core.config import config
from db.mongodb import get_db
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(raw: str, hashed: str):
    return pwd_context.verify(raw, hashed)

def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await db["users"].find_one({"username": username})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
