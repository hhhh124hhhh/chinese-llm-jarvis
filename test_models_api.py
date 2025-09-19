import requests
import json

def test_models_api():
    try:
        response = requests.get("http://localhost:8283/v1/models/", headers={"accept": "application/json"})
        print("Status Code:", response.status_code)
        if response.status_code == 200:
            models = response.json()
            print("Available Models:")
            print(json.dumps(models, indent=2, ensure_ascii=False))
        else:
            print("Error Response:")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_models_api()