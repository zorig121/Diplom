# services/container_manager.py

import subprocess
import threading
import uuid
import os
import time
import json

from services.session_store import (
    SESSION_DURATION_SEC,
    free_gpu,
    remove_session,
    get_session,
)


def spawn_container(user_id: str, image: str = "my-jupyter-cpu") -> tuple[str, str]:
    # Контейнер нэрийг хэрэглэгч ID болон санамсаргүй UUID-р ялгана
    container_name = f"jupyter-{user_id}-{uuid.uuid4().hex[:6]}"

    # Хэрэглэгч тус бүрт volume фолдер үүсгэж өгнө
    volume_path = f"/home/workspace/{user_id}"
    os.makedirs(volume_path, exist_ok=True)

    # Docker container-г spawn хийнэ (random port bind-тай)
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

    # Container-ын host порт ямар дээр bind хийгдсэнийг олно
    inspect = subprocess.run(["docker", "inspect", container_id], capture_output=True, text=True)
    info = json.loads(inspect.stdout)[0]
    host_port = info["NetworkSettings"]["Ports"]["8888/tcp"][0]["HostPort"]

    return container_id, host_port


def expire_session_later(user_id: str):
    # Session хадгалагдаагүй бол container зогсоох шаардлагагүй
    session = get_session(user_id)
    if not session:
        return

    container_id = session["container_id"]
    gpu_uuid = session["gpu_uuid"]

    def stopper():
        # Session хугацаа дуусахыг хүлээнэ
        time.sleep(SESSION_DURATION_SEC)

        # Container-ийг зогсоож устгана
        subprocess.run(["docker", "stop", container_id])
        subprocess.run(["docker", "rm", container_id])

        # GPU slice-г буцааж pool-д нэмнэ
        free_gpu(gpu_uuid)

        # Session-г RAM-аас устгана
        remove_session(user_id)

    # Container expiry-г background thread-р ажиллуулна
    threading.Thread(target=stopper).start()
