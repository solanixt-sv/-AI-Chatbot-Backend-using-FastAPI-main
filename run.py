import subprocess
import sys
import time
import os

def main():
    # Read environment variables
    api_url = os.environ.get("API_URL", "http://127.0.0.1:8000/chat")
    print(f"Connecting Streamlit frontend to FastAPI backend at: {api_url}")

    # Launch FastAPI backend
    print("Starting FastAPI backend (Uvicorn)...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=None,
        stderr=None
    )
    
    # Wait for the backend to start up
    time.sleep(2)
    
    # Launch Streamlit frontend
    print("Starting Streamlit frontend...")
    try:
        frontend_process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"],
            stdout=None,
            stderr=None
        )
        
        # Wait for the frontend to complete or respond to manual interrupt
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nStopping services...")
    finally:
        # Terminate backend process when frontend exits or upon interruption
        backend_process.terminate()
        try:
            backend_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            backend_process.kill()
        print("Backend and frontend stopped.")

if __name__ == "__main__":
    main()
