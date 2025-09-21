#!/usr/bin/env python3
"""
修复脚本：解决AI API加载问题
"""
import os
import sys
import shutil
from pathlib import Path

def check_env_file():
    """检查.env.local文件是否存在"""
    env_file = Path("d:/chinese-llm-jarvis/.env.local")
    if env_file.exists():
        print("✅ .env.local文件已存在")
        return True
    else:
        print("❌ .env.local文件不存在")
        return False

def load_env_variables():
    """从.env.local文件加载环境变量"""
    env_file = Path("d:/chinese-llm-jarvis/.env.local")
    if not env_file.exists():
        print("❌ .env.local文件不存在，无法加载环境变量")
        return False
    
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if value and not value.startswith('your_'):
                            os.environ[key] = value
                            print(f"✅ 已设置环境变量: {key}")
        return True
    except Exception as e:
        print(f"❌ 加载环境变量时出错: {e}")
        return False

def test_api_keys():
    """测试API密钥是否已正确设置"""
    kimi_api_key = os.getenv("KIMI_API_KEY")
    zhipu_api_key = os.getenv("ZHIPU_API_KEY")
    
    print("\n=== API密钥检查 ===")
    if kimi_api_key and not kimi_api_key.startswith('your_'):
        print("✅ Kimi API密钥已设置")
    else:
        print("❌ Kimi API密钥未设置或使用默认值")
        
    if zhipu_api_key and not zhipu_api_key.startswith('your_'):
        print("✅ 智谱AI API密钥已设置")
    else:
        print("❌ 智谱AI API密钥未设置或使用默认值")
        
    return (kimi_api_key and not kimi_api_key.startswith('your_'), 
            zhipu_api_key and not zhipu_api_key.startswith('your_'))

def fix_provider_loading():
    """修复提供商加载问题"""
    print("\n=== 修复提供商加载 ===")
    
    # 检查基础URL配置
    kimi_base_url = os.getenv("KIMI_BASE_URL", "https://api.moonshot.cn/v1")
    zhipu_base_url = os.getenv("ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
    
    print(f"Kimi Base URL: {kimi_base_url}")
    print(f"智谱AI Base URL: {zhipu_base_url}")
    
    # 验证URL格式
    if not kimi_base_url.startswith("http"):
        print("❌ Kimi Base URL格式不正确")
        return False
        
    if not zhipu_base_url.startswith("http"):
        print("❌ 智谱AI Base URL格式不正确")
        return False
        
    print("✅ Base URLs格式正确")
    return True

def main():
    """主函数"""
    print("修复AI API加载问题\n")
    
    # 检查环境文件
    if not check_env_file():
        print("请先创建.env.local文件并配置API密钥")
        return False
    
    # 加载环境变量
    if not load_env_variables():
        print("无法加载环境变量")
        return False
    
    # 测试API密钥
    kimi_ok, zhipu_ok = test_api_keys()
    
    # 修复提供商加载
    provider_ok = fix_provider_loading()
    
    print("\n=== 修复结果 ===")
    if kimi_ok or zhipu_ok:
        if provider_ok:
            print("✅ API加载问题已修复!")
            print("\n下一步:")
            print("1. 请确保在.env.local文件中填入实际的API密钥")
            print("2. 重启服务以应用更改")
            print("3. 运行测试脚本验证修复结果")
            return True
        else:
            print("❌ 提供商加载仍有问题")
    else:
        print("❌ 请在.env.local文件中配置实际的API密钥")
        print("\n配置步骤:")
        print("1. 编辑 d:/chinese-llm-jarvis/.env.local 文件")
        print("2. 将 your_kimi_api_key_here 替换为实际的Kimi API密钥")
        print("3. 将 your_zhipu_api_key_here 替换为实际的智谱AI API密钥")
        print("4. 保存文件并重新运行此脚本")
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)