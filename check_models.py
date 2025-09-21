#!/usr/bin/env python3
"""
检查可用模型
"""

import os
import sys

# 添加项目路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from letta.server.server import SyncServer

def check_models():
    """检查可用模型"""
    print("=== 检查可用模型 ===")
    
    try:
        # 创建服务器实例
        server = SyncServer()
        print("✅ 服务器实例创建成功")
        
        # 获取启用的提供商
        providers = server._enabled_providers
        print(f"✅ 找到 {len(providers)} 个启用的提供商:")
        for i, provider in enumerate(providers):
            print(f"  {i+1}. {provider.name} ({provider.provider_type})")
            
        # 检查Kimi提供商
        kimi_provider = None
        for provider in providers:
            if provider.name == "kimi":
                kimi_provider = provider
                break
                
        if kimi_provider:
            print(f"\n--- Kimi提供商详情 ---")
            print(f"名称: {kimi_provider.name}")
            print(f"类型: {kimi_provider.provider_type}")
            print(f"基础URL: {kimi_provider.base_url}")
            
            # 获取模型列表
            print(f"\n--- 获取Kimi模型列表 ---")
            try:
                models = kimi_provider.list_llm_models()
                print(f"✅ 成功获取 {len(models)} 个Kimi模型:")
                for i, model in enumerate(models):
                    print(f"  {i+1}. {model.model} (上下文窗口: {model.context_window})")
            except Exception as e:
                print(f"❌ 获取模型列表失败: {e}")
        else:
            print("❌ 未找到Kimi提供商")
            
    except Exception as e:
        print(f"❌ 检查过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_models()