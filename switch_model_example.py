import requests
import json

def list_available_models():
    """列出所有可用的模型"""
    try:
        response = requests.get("http://localhost:8283/v1/models/", headers={"accept": "application/json"})
        if response.status_code == 200:
            models = response.json()
            print("Available Models:")
            for i, model in enumerate(models):
                print(f"{i+1}. {model['handle']} - {model['model']} ({model['model_endpoint_type']})")
            return models
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Error listing models: {e}")
        return []

def create_agent_with_model(model_handle):
    """使用指定模型创建智能体"""
    try:
        # 创建智能体的请求数据
        agent_data = {
            "name": f"agent_with_{model_handle.replace('/', '_')}",
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
            print(f"Successfully created agent with ID: {agent['id']}")
            print(f"Model used: {agent['llm_config']['handle']}")
            return agent
        else:
            print(f"Error creating agent: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error creating agent: {e}")
        return None

def main():
    print("=== Letta 模型切换演示 ===\n")
    
    # 1. 列出所有可用模型
    models = list_available_models()
    
    if not models:
        print("No models available.")
        return
    
    # 2. 让用户选择模型
    print("\n请选择要使用的模型:")
    try:
        choice = int(input(f"输入数字 (1-{len(models)}): ")) - 1
        if 0 <= choice < len(models):
            selected_model = models[choice]
            print(f"\n您选择了: {selected_model['handle']}")
            
            # 3. 使用选定的模型创建智能体
            agent = create_agent_with_model(selected_model['handle'])
            
            if agent:
                print(f"\n成功创建智能体!")
                print(f"智能体名称: {agent['name']}")
                print(f"使用的模型: {agent['llm_config']['handle']}")
            else:
                print("创建智能体失败")
        else:
            print("无效的选择")
    except ValueError:
        print("请输入有效的数字")

if __name__ == "__main__":
    main()