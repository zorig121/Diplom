from fastapi import FastAPI
from api import auth, session, user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(session.router, prefix="/api")
app.include_router(user.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
