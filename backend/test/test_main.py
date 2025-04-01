import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.container_manager import spawn_container

if __name__ == "__main__":
    cid, port, token = spawn_container("testuser", image="my-jupyter-cpu")
    print(f"Container: {cid}, Port: {port}, Token: {token}")
