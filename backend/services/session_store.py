# services/session_store.py

import time
from typing import Dict

# Хуурамч GPU slice pool (MIG uuid-ууд)
MIG_UUID_POOL = {"FAKE-MIG-001", "FAKE-MIG-002", "FAKE-MIG-003"}

#  Аль хэрэглэгчид аль GPU-г авч байгааг тэмдэглэх
ALLOCATED_UUIDS = set()

#  RAM-д хадгалагдах session-ийн мэдээлэл
SESSIONS: Dict[str, Dict] = {}

#  Session-ийн үргэлжлэх хугацаа (секундээр)
SESSION_DURATION_SEC = 1800  # 30 min


def allocate_gpu() -> str:
    # Чөлөөт slice байгаа эсэхийг шалган, олгоно
    available = MIG_UUID_POOL - ALLOCATED_UUIDS
    if not available:
        return None
    uuid = available.pop()
    ALLOCATED_UUIDS.add(uuid)
    return uuid


def free_gpu(uuid: str):
    # Session дуусах үед GPU slice-ыг чөлөөлнө
    ALLOCATED_UUIDS.discard(uuid)


def save_session(user_id: str, session: Dict):
    # Session-г RAM-д хадгална
    SESSIONS[user_id] = session


def get_session(user_id: str) -> Dict:
    # Session-г шалгах эсвэл хэрэглэх үед
    return SESSIONS.get(user_id)


def remove_session(user_id: str):
    #  Session-г RAM-аас устгах үед
    if user_id in SESSIONS:
        del SESSIONS[user_id]
