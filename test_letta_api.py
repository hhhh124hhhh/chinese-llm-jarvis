import requests
import json

# 测试Letta API
def test_letta_api():
    base_url = "http://localhost:8284/v1"
    headers = {"Authorization": "Bearer letta"}
    
    # 获取工具列表
    print("获取工具列表...")
    response = requests.get(f"{base_url}/tools", headers=headers)
    if response.status_code == 200:
        tools = response.json()
        print(f"成功获取到 {len(tools)} 个工具")
        # 查找我们需要的工具
        required_tools = ['memory_replace', 'conversation_search', 'memory_insert', 'send_message']
        found_tools = [tool for tool in tools if tool['name'] in required_tools]
        print(f"找到 {len(found_tools)} 个必需工具: {[t['name'] for t in found_tools]}")
    else:
        print(f"获取工具失败，状态码: {response.status_code}")
        return False
    
    # 测试创建代理
    print("\n测试创建代理...")
    agent_data = {
        "name": "test_agent",
        "llm_config": {
            "model": "gpt-4o-mini"
        },
        "embedding_config": {
            "model": "text-embedding-3-small",
            "provider": "openai"
        }
    }
    
    response = requests.post(f"{base_url}/agents", headers=headers, json=agent_data)
    if response.status_code == 200:
        agent = response.json()
        print(f"成功创建代理: {agent['name']} (ID: {agent['id']})")
        print(f"代理工具: {[t['name'] for t in agent['tools']]}")
        return True
    else:
        print(f"创建代理失败，状态码: {response.status_code}")
        print(f"错误信息: {response.text}")
        return False

if __name__ == "__main__":
    test_letta_api()