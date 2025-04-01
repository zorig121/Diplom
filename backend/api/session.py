from fastapi import APIRouter, Depends, HTTPException
from core.security import get_current_user
from services.session_store import *
from services.container_manager import *
from models.session import SessionCreateResponse, SessionStatusResponse
import time
import subprocess

router = APIRouter()

@router.post("/request-session", response_model=SessionCreateResponse)
async def request_session(current_user=Depends(get_current_user)):
    user_id = current_user["username"]

    existing = get_session(user_id)
    if existing:
        elapsed = time.time() - existing["start_time"]
        remaining = SESSION_DURATION_SEC - elapsed
        if remaining > 0:
            return SessionCreateResponse(
                user_id=user_id,
                container_id=existing["container_id"],
                gpu_uuid=existing["gpu_uuid"],
                notebook_url=existing["notebook_url"],
                expiry_sec=int(remaining)
            )

    gpu_uuid = allocate_gpu()
    if not gpu_uuid:
        raise HTTPException(status_code=503, detail="No GPU slices available")

    try:
        container_id, host_port, token = spawn_container(user_id)
    except Exception as e:
        free_gpu(gpu_uuid)
        try:
            if 'container_id' in locals():
                subprocess.run(["docker", "rm", "-f", container_id])
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=str(e))

    notebook_url = f"http://localhost:{host_port}/?token={token}"

    save_session(user_id, {
        "container_id": container_id,
        "gpu_uuid": gpu_uuid,
        "notebook_url": notebook_url,
        "start_time": time.time()
    })

    expire_session_later(user_id)

    return SessionCreateResponse(
        user_id=user_id,
        container_id=container_id,
        gpu_uuid=gpu_uuid,
        notebook_url=notebook_url,
        expiry_sec=SESSION_DURATION_SEC
    )

@router.get("/session-status", response_model=SessionStatusResponse)
async def session_status(current_user=Depends(get_current_user)):
    user_id = current_user["username"]
    session = get_session(user_id)

    if not session:
        return SessionStatusResponse(status="none")

    elapsed = time.time() - session["start_time"]

    return SessionStatusResponse(
        status="running",
        remaining_sec=max(0, SESSION_DURATION_SEC - int(elapsed)),
        notebook_url=session["notebook_url"],
        gpu_uuid=session["gpu_uuid"]
    )

@router.post("/stop-session")
async def stop_session(current_user=Depends(get_current_user)):
    user_id = current_user["username"]
    session = get_session(user_id)

    if not session:
        raise HTTPException(status_code=404, detail="No active session")

    container_id = session["container_id"]
    gpu_uuid = session["gpu_uuid"]

    subprocess.run(["docker", "stop", container_id])
    subprocess.run(["docker", "rm", container_id])
    free_gpu(gpu_uuid)
    remove_session(user_id)

    return {"status": "stopped"}
