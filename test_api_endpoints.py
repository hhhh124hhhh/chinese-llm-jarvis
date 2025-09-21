import requests
import time

def test_api_endpoints():
    """Test the API endpoints to verify they are working correctly."""
    base_url = "http://localhost:8080"
    
    # Test the health endpoint
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✓ Health endpoint is working")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Health endpoint returned status code {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to the server. Is it running?")
    except Exception as e:
        print(f"✗ Error testing health endpoint: {e}")
    
    # Test the API version endpoint
    print("\nTesting API version endpoint...")
    try:
        response = requests.get(f"{base_url}/v1", timeout=5)
        if response.status_code == 200:
            print("✓ API version endpoint is working")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ API version endpoint returned status code {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to the server. Is it running?")
    except Exception as e:
        print(f"✗ Error testing API version endpoint: {e}")
    
    # Test the organizations endpoint
    print("\nTesting organizations endpoint...")
    try:
        response = requests.get(f"{base_url}/v1/orgs", timeout=5)
        if response.status_code == 200:
            print("✓ Organizations endpoint is working")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Organizations endpoint returned status code {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to the server. Is it running?")
    except Exception as e:
        print(f"✗ Error testing organizations endpoint: {e}")

if __name__ == "__main__":
    test_api_endpoints()