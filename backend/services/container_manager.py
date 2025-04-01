import subprocess
import threading
import uuid
import os
import time
import json
import re

from services.session_store import (
    SESSION_DURATION_SEC,
    free_gpu,
    remove_session,
    get_session,
)

def wait_for_token(container_id: str, timeout: int = 10) -> str | None:
    for i in range(timeout):
        logs = subprocess.run(
            ["docker", "logs", container_id],
            capture_output=True, text=True
        ).stdout

        print(f"🔁 {i}s log snapshot:")
        print(logs)

        match = re.search(r"[?&]token=([a-zA-Z0-9]+)", logs)
        if match:
            return match.group(1)

        time.sleep(1)

    return None

def get_token_via_exec(container_id: str) -> str | None:
    result = subprocess.run(
        ["docker", "exec", container_id, "jupyter", "server", "list"],
        capture_output=True, text=True
    )
    match = re.search(r"token=([a-zA-Z0-9]+)", result.stdout)
    return match.group(1) if match else None

def spawn_container(user_id: str, image: str = "my-jupyter-cpu") -> tuple[str, str, str]:
    container_name = f"jupyter-{user_id}-{uuid.uuid4().hex[:6]}"
    volume_path = f"/home/workspace/{user_id}"
    os.makedirs(volume_path, exist_ok=True)

    result = subprocess.run([
        "docker", "run", "-d",
        "--name", container_name,
        "-v", f"{volume_path}:/home/jovyan/work",
        "-p", "0:8888",
        image
    ], capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    container_id = result.stdout.strip()

    inspect = subprocess.run(["docker", "inspect", container_id], capture_output=True, text=True)
    info = json.loads(inspect.stdout)[0]
    host_port = info["NetworkSettings"]["Ports"]["8888/tcp"][0]["HostPort"]

    # token = wait_for_token(container_id)
    if not token:
        print("⚠️ Token лог дээр харагдсангүй, docker exec ашиглаж байна...")
        token = get_token_via_exec(container_id)
        if not token:
            raise RuntimeError("❌ Token not found via logs or exec fallback")

    return container_id, host_port, token

def expire_session_later(user_id: str):
    session = get_session(user_id)
    if not session:
        return

    container_id = session["container_id"]
    gpu_uuid = session["gpu_uuid"]

    def stopper():
        time.sleep(SESSION_DURATION_SEC)
        subprocess.run(["docker", "stop", container_id])
        subprocess.run(["docker", "rm", container_id])
        free_gpu(gpu_uuid)
        remove_session(user_id)

    threading.Thread(target=stopper, daemon=True).start()