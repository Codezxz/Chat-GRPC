import os
import subprocess
import time

def run_uvicorn():
    port = os.environ.get("PORT", "8000")
    return subprocess.Popen(
        ["uvicorn", "server_ws_chat:app", "--host", "0.0.0.0", "--port", port]
    )

def run_python_server():
    return subprocess.Popen(["python", "server_chat.py"])

if __name__ == "__main__":
    print("Starting both servers...")

    uvicorn_process = run_uvicorn()
    chat_process = run_python_server()

    try:
        uvicorn_process.wait()
        chat_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")

        uvicorn_process.terminate()
        chat_process.terminate()

        time.sleep(1)
        print("Servers stopped.")
