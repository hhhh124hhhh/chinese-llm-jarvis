import requests
import json

# 测试获取模型列表
response = requests.get("http://localhost:8283/v1/models/", headers={"accept": "application/json"})
print("Status code:", response.status_code)
if response.status_code == 200:
    models = response.json()
    print("Models:")
    for model in models:
        print(f"  - {model['handle']}: {model['model']}")
else:
    print("Error:", response.text)