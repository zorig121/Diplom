# models/session.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SessionMetadata(BaseModel):
    user_id: str
    container_id: str
    gpu_uuid: str
    notebook_url: str
    start_time: float  # Unix timestamp


class SessionStatusResponse(BaseModel):
    status: str  # "running", "none"
    remaining_sec: Optional[int] = None
    notebook_url: Optional[str] = None
    gpu_uuid: Optional[str] = None


class SessionCreateResponse(BaseModel):
    user_id: str
    container_id: str
    gpu_uuid: str
    notebook_url: str
    expiry_sec: int


class SessionHistoryItem(BaseModel):
    started_at: float
    status: str
    gpu_uuid: str
    image: str
