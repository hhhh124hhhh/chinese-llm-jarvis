import subprocess
import time
import requests
import sys

def start_server():
    """Start the Letta server in the background and wait for it to be ready."""
    print("Starting Letta server...")
    
    # Start the server in the background
    process = subprocess.Popen([
        sys.executable, "-m", "letta.server.rest_api.app"
    ], cwd=".", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    print(f"Server process started with PID {process.pid}")
    
    # Wait for the server to start
    base_url = "http://localhost:8283"
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        try:
            response = requests.get(f"{base_url}/health", timeout=1)
            if response.status_code == 200:
                print("✓ Server is running and responding to requests")
                print(f"Server URL: {base_url}")
                return process
        except requests.exceptions.ConnectionError:
            pass
        except Exception as e:
            print(f"Error checking server: {e}")
        
        attempt += 1
        print(f"Waiting for server to start... (attempt {attempt}/{max_attempts})")
        time.sleep(2)
    
    print("✗ Server failed to start within the expected time")
    # Terminate the process if it didn't start correctly
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
    
    return None

if __name__ == "__main__":
    server_process = start_server()
    if server_process:
        print("\nLetta server is now running!")
        print("You can access the API at: http://localhost:8283")
        print("Press Ctrl+C to stop the server")
        
        try:
            # Keep the script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down server...")
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()
            print("Server stopped.")
    else:
        print("Failed to start server")
        sys.exit(1)