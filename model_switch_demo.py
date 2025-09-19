import requests
import json

def list_available_models():
    """列出所有可用的模型"""
    try:
        response = requests.get("http://localhost:8283/v1/models/", headers={"accept": "application/json"})
        if response.status_code == 200:
            models = response.json()
            print("=== 可用模型列表 ===")
            for i, model in enumerate(models):
                print(f"{i+1}. {model['handle']} - {model['model']} ({model['model_endpoint_type']})")
            return models
        else:
            print(f"错误: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"获取模型列表时出错: {e}")
        return []

def create_agent_with_model(model_handle, agent_name=None):
    """使用指定模型创建智能体"""
    if not agent_name:
        agent_name = f"agent_with_{model_handle.replace('/', '_')}"
    
    try:
        # 创建智能体的请求数据
        agent_data = {
            "name": agent_name,
            "model": model_handle,
            "embedding": "letta/letta-free"  # 使用默认的嵌入模型
        }
        
        response = requests.post(
            "http://localhost:8283/v1/agents", 
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json=agent_data
        )
        
        if response.status_code == 200:
            agent = response.json()
            print(f"成功创建智能体: {agent['name']} (ID: {agent['id']})")
            print(f"使用的模型: {agent['llm_config']['model']}")
            return agent
        else:
            print(f"创建智能体失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"创建智能体时出错: {e}")
        return None

def get_agent_details(agent_id):
    """获取智能体详细信息"""
    try:
        response = requests.get(
            f"http://localhost:8283/v1/agents/{agent_id}",
            headers={"accept": "application/json"}
        )
        
        if response.status_code == 200:
            agent = response.json()
            print(f"智能体详情:")
            print(f"  名称: {agent['name']}")
            print(f"  ID: {agent['id']}")
            print(f"  模型: {agent['llm_config']['model']}")
            print(f"  嵌入模型: {agent['embedding_config']['embedding_model']}")
            return agent
        else:
            print(f"获取智能体详情失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"获取智能体详情时出错: {e}")
        return None

def send_message_to_agent(agent_id, message):
    """向智能体发送消息"""
    try:
        response = requests.post(
            f"http://localhost:8283/v1/agents/{agent_id}/messages",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "role": "user",
                "content": message
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"智能体回复: {result['messages'][0]['content']}")
            return result
        else:
            print(f"发送消息失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"发送消息时出错: {e}")
        return None

def main():
    print("=== Letta 模型切换演示 ===\n")
    
    # 1. 列出所有可用模型
    models = list_available_models()
    if not models:
        print("没有可用的模型")
        return
    
    # 2. 显示当前支持的模型类型
    print("\n=== 当前支持的模型提供商 ===")
    providers = set(model['provider_name'] for model in models)
    for provider in providers:
        print(f"- {provider}")
    
    # 3. 检查是否配置了Kimi和智谱AI的API密钥
    print("\n=== API密钥配置检查 ===")
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            env_content = f.read()
            if 'KIMI_API_KEY=sk-' in env_content:
                print("✓ Kimi API密钥已配置")
            else:
                print("⚠ Kimi API密钥未配置或无效")
                
            if 'ZHIPU_API_KEY=your_zhipu_api_key_here' in env_content:
                print("⚠ 智谱AI API密钥未配置 (需要替换为实际密钥)")
            else:
                print("✓ 智谱AI API密钥已配置")
    except FileNotFoundError:
        print("⚠ 未找到.env文件")
    except UnicodeDecodeError:
        # 尝试使用其他编码
        try:
            with open('.env', 'r', encoding='gbk') as f:
                env_content = f.read()
                if 'KIMI_API_KEY=sk-' in env_content:
                    print("✓ Kimi API密钥已配置")
                else:
                    print("⚠ Kimi API密钥未配置或无效")
                    
                if 'ZHIPU_API_KEY=your_zhipu_api_key_here' in env_content:
                    print("⚠ 智谱AI API密钥未配置 (需要替换为实际密钥)")
                else:
                    print("✓ 智谱AI API密钥已配置")
        except Exception:
            print("⚠ 无法读取.env文件")
    
    # 4. 说明如何添加Kimi和智谱AI模型
    print("\n=== 如何添加Kimi和智谱AI模型 ===")
    print("1. 在.env文件中配置API密钥:")
    print("   KIMI_API_KEY=your_actual_kimi_api_key")
    print("   ZHIPU_API_KEY=your_actual_zhipu_api_key")
    print("\n2. 重启Letta服务以加载新配置")
    print("\n3. Kimi支持的模型:")
    print("   - moonshot-v1-8k")
    print("   - moonshot-v1-32k")
    print("   - moonshot-v1-128k")
    print("   - kimi-k2-0905-preview (您提供的模型)")
    print("   - kimi-k2-0711-preview (您提供的模型)")
    print("   - kimi-k2-turbo-preview (您提供的模型)")
    print("\n4. 智谱AI支持的模型:")
    print("   - glm-4-plus")
    print("   - glm-4-0520")
    print("   - glm-4")
    print("   - glm-4-air")
    print("   - glm-4-airx")
    print("   - glm-4-long")
    print("   - glm-4-flash")
    print("   - glm-4-flashx")

if __name__ == "__main__":
    main()