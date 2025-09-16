import subprocess
import time

def run_uvicorn():
    return subprocess.Popen(
        ["uvicorn", "server_ws_chat:app", "--reload", "--port", "8000"]
    )

def run_python_server():
    return subprocess.Popen(["python", "server_chat.py"])

if __name__ == "__main__":
    print("Starting both servers...")

    uvicorn_process = run_uvicorn()
    chat_process = run_python_server()

    try:
        # Wait for both processes to finish (which normally doesn't happen unless terminated)
        uvicorn_process.wait()
        chat_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")

        # Gracefully terminate both processes
        uvicorn_process.terminate()
        chat_process.terminate()

        # Wait a moment to ensure they are stopped
        time.sleep(1)
        print("Servers stopped.")
