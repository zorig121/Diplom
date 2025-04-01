import subprocess
import re

def get_docker_logs(container_id: str) -> str:
    result = subprocess.run(
        ["docker", "logs", container_id],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def extract_token(logs: str) -> str | None:
    match = re.search(r"[?&]token=([a-zA-Z0-9]+)", logs)
    return match.group(1) if match else None

def get_token_via_exec(container_id: str) -> str | None:
    result = subprocess.run(
        ["docker", "exec", container_id, "jupyter", "server", "list"],
        capture_output=True, text=True
    )
    match = re.search(r"token=([a-zA-Z0-9]+)", result.stdout)
    return match.group(1) if match else None

if __name__ == "__main__":
    container_id = input("🧪 Container ID оруулна уу: ").strip()
    logs = get_docker_logs(container_id)

    print("🪵 Docker logs:\n", logs)

    token = extract_token(logs)
    if token:
        print(f"✅ Token лог дээрээс олдлоо: {token}")
    else:
        print("⚠️ Token лог дээр харагдсангүй, docker exec ашиглаж байна...")
        token = get_token_via_exec(container_id)
        if token:
            print(f"✅ Token exec-оор олдлоо: {token}")
        else:
            print("❌ Token огт олдсонгүй (exec + log аль аль нь хоосон)")
