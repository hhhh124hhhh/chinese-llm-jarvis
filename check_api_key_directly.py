#!/usr/bin/env python3
"""
直接从.env.local文件中读取API密钥并测试
"""

import os
import httpx

def check_api_key_directly():
    print("=== 直接从文件读取API密钥 ===")
    
    # 直接从文件读取
    env_file_path = os.path.join(os.path.dirname(__file__), '.env.local')
    with open(env_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    api_key = None
    for line in content.split('\n'):
        if line.startswith('KIMI_API_KEY='):
            api_key = line.split('=', 1)[1]
            print(f"从文件读取的API密钥: {repr(api_key)}")
            print(f"API密钥长度: {len(api_key)}")
            print(f"末尾是否有空格: {api_key.endswith(' ')}")
            break
    
    if api_key:
        # 测试API调用
        print("\n=== 测试Kimi API调用 ===")
        url = "https://api.moonshot.cn/v1/models"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = httpx.get(url, headers=headers, timeout=30.0)
            print(f"API请求状态码: {response.status_code}")
            if response.status_code == 200:
                print("✅ API密钥认证成功!")
                data = response.json()
                print(f"可用模型数量: {len(data.get('data', []))}")
                for model in data.get('data', [])[:5]:  # 只显示前5个模型
                    print(f"  - {model.get('id', 'N/A')}: {model.get('object', 'N/A')}")
            else:
                print(f"❌ API请求失败: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ API请求异常: {e}")
    else:
        print("❌ 未找到API密钥")

if __name__ == "__main__":
    check_api_key_directly()