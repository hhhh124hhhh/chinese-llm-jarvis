#!/usr/bin/env python3
"""
诊断AI模型加载问题的脚本
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from letta.settings import model_settings
from letta.server.server import SyncServer
from letta.schemas.providers import KimiProvider, ZhipuProvider
from letta.schemas.enums import ProviderType, ProviderCategory


def check_env_file():
    """检查.env.local文件中的API密钥配置"""
    env_file = project_root / ".env.local"
    print("=== 检查.env.local配置文件 ===")
    
    if not env_file.exists():
        print("❌ 未找到.env.local文件")
        return False
    
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"✅ 找到.env.local文件")
        
        # 检查Kimi API密钥
        if "KIMI_API_KEY=your_kimi_api_key_here" in content:
            print("❌ Kimi API密钥仍为占位符值，请替换为实际的API密钥")
        elif "KIMI_API_KEY=" in content:
            kimi_key_line = [line for line in content.split('\n') if line.startswith('KIMI_API_KEY=')][0]
            kimi_key = kimi_key_line.split('=', 1)[1]
            if kimi_key and kimi_key != "your_kimi_api_key_here":
                print("✅ Kimi API密钥已配置")
            else:
                print("❌ Kimi API密钥未正确配置")
        else:
            print("❌ 未找到Kimi API密钥配置")
            
        # 检查Zhipu API密钥
        if "ZHIPU_API_KEY=your_zhipu_api_key_here" in content:
            print("❌ 智谱AI API密钥仍为占位符值，请替换为实际的API密钥")
        elif "ZHIPU_API_KEY=" in content:
            zhipu_key_line = [line for line in content.split('\n') if line.startswith('ZHIPU_API_KEY=')][0]
            zhipu_key = zhipu_key_line.split('=', 1)[1]
            if zhipu_key and zhipu_key != "your_zhipu_api_key_here":
                print("✅ 智谱AI API密钥已配置")
            else:
                print("❌ 智谱AI API密钥未正确配置")
        else:
            print("❌ 未找到智谱AI API密钥配置")
            
    return True


def check_model_settings():
    """检查模型设置"""
    print("\n=== 检查模型设置 ===")
    
    print(f"Kimi API密钥: {'已设置' if model_settings.kimi_api_key else '未设置'}")
    print(f"Kimi Base URL: {model_settings.kimi_base_url}")
    
    print(f"智谱AI API密钥: {'已设置' if model_settings.zhipu_api_key else '未设置'}")
    print(f"智谱AI Base URL: {model_settings.zhipu_base_url}")
    
    return model_settings.kimi_api_key, model_settings.zhipu_api_key


def test_kimi_provider():
    """测试Kimi提供商"""
    print("\n=== 测试Kimi提供商 ===")
    
    try:
        kimi_provider = KimiProvider(
            name="kimi",
            provider_type=ProviderType.kimi,
            provider_category=ProviderCategory.base,
            api_key=model_settings.kimi_api_key,
            base_url=model_settings.kimi_base_url,
            id=None,
            access_key=None,
            region=None,
            api_version=None,
            organization_id=None,
            updated_at=None
        )
        print("✅ Kimi提供商实例创建成功")
        
        # 尝试列出模型
        try:
            models = kimi_provider.list_llm_models()
            print(f"✅ Kimi LLM模型数量: {len(models)}")
            print("前3个模型:")
            for model in models[:3]:
                print(f"  - {model.handle}: {model.model} (上下文窗口: {model.context_window})")
        except Exception as e:
            print(f"❌ 列出Kimi模型时出错: {e}")
            
    except Exception as e:
        print(f"❌ Kimi提供商实例创建失败: {e}")


def test_zhipu_provider():
    """测试智谱AI提供商"""
    print("\n=== 测试智谱AI提供商 ===")
    
    try:
        zhipu_provider = ZhipuProvider(
            name="zhipu",
            provider_type=ProviderType.zhipu,
            provider_category=ProviderCategory.base,
            api_key=model_settings.zhipu_api_key,
            base_url=model_settings.zhipu_base_url,
            id=None,
            access_key=None,
            region=None,
            api_version=None,
            organization_id=None,
            updated_at=None
        )
        print("✅ 智谱AI提供商实例创建成功")
        
        # 尝试列出LLM模型
        try:
            llm_models = zhipu_provider.list_llm_models()
            print(f"✅ 智谱AI LLM模型数量: {len(llm_models)}")
            print("前3个模型:")
            for model in llm_models[:3]:
                print(f"  - {model.handle}: {model.model} (上下文窗口: {model.context_window})")
        except Exception as e:
            print(f"❌ 列出智谱AI LLM模型时出错: {e}")
            
        # 尝试列出嵌入模型
        try:
            embedding_models = zhipu_provider.list_embedding_models()
            print(f"✅ 智谱AI嵌入模型数量: {len(embedding_models)}")
            print("嵌入模型:")
            for model in embedding_models:
                print(f"  - {model.handle}: {model.embedding_model} (维度: {model.embedding_dim})")
        except Exception as e:
            print(f"❌ 列出智谱AI嵌入模型时出错: {e}")
            
    except Exception as e:
        print(f"❌ 智谱AI提供商实例创建失败: {e}")


def test_server_providers():
    """测试服务器端提供商加载"""
    print("\n=== 测试服务器提供商加载 ===")
    
    try:
        server = SyncServer()
        print("✅ 服务器实例创建成功")
        
        # 检查启用的提供商
        provider_names = [provider.name for provider in server._enabled_providers]
        print(f"启用的提供商: {', '.join(provider_names)}")
        
        # 检查Kimi和Zhipu是否在启用列表中
        if "kimi" in provider_names:
            print("✅ Kimi提供商已启用")
        else:
            print("❌ Kimi提供商未启用")
            
        if "zhipu" in provider_names:
            print("✅ 智谱AI提供商已启用")
        else:
            print("❌ 智谱AI提供商未启用")
            
    except Exception as e:
        print(f"❌ 服务器实例创建失败: {e}")


def main():
    """主函数"""
    print("开始诊断AI模型加载问题...")
    
    # 检查环境文件
    check_env_file()
    
    # 检查模型设置
    kimi_key, zhipu_key = check_model_settings()
    
    # 如果API密钥已设置，测试提供商
    if kimi_key:
        test_kimi_provider()
    else:
        print("\n跳过Kimi提供商测试（API密钥未设置）")
        
    if zhipu_key:
        test_zhipu_provider()
    else:
        print("\n跳过智谱AI提供商测试（API密钥未设置）")
        
    # 测试服务器提供商
    test_server_providers()
    
    print("\n诊断完成!")


if __name__ == "__main__":
    main()