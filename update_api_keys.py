#!/usr/bin/env python3
"""
更新脚本：帮助用户正确配置API密钥
"""
import os
import sys
from pathlib import Path

def read_env_file():
    """读取.env.local文件"""
    env_file = Path("d:/chinese-llm-jarvis/.env.local")
    if not env_file.exists():
        print("❌ .env.local文件不存在")
        return None
    
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"❌ 读取.env.local文件时出错: {e}")
        return None

def write_env_file(content):
    """写入.env.local文件"""
    env_file = Path("d:/chinese-llm-jarvis/.env.local")
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ .env.local文件已更新")
        return True
    except Exception as e:
        print(f"❌ 写入.env.local文件时出错: {e}")
        return False

def update_api_keys():
    """更新API密钥"""
    print("=== 更新API密钥 ===")
    
    # 读取当前配置
    content = read_env_file()
    if content is None:
        return False
    
    # 检查是否需要更新Kimi API密钥
    if "your_kimi_api_key_here" in content:
        print("\n请输入您的Kimi API密钥:")
        print("获取方式: 访问 https://www.moonshot.cn/ 注册并获取API密钥")
        kimi_key = input("Kimi API密钥: ").strip()
        if kimi_key:
            content = content.replace("your_kimi_api_key_here", kimi_key)
            print("✅ Kimi API密钥已更新")
        else:
            print("⚠️ 未提供Kimi API密钥，保持默认值")
    
    # 检查是否需要更新智谱AI API密钥
    if "your_zhipu_api_key_here" in content:
        print("\n请输入您的智谱AI API密钥:")
        print("获取方式: 访问 https://open.bigmodel.cn/ 注册并获取API密钥")
        zhipu_key = input("智谱AI API密钥: ").strip()
        if zhipu_key:
            content = content.replace("your_zhipu_api_key_here", zhipu_key)
            print("✅ 智谱AI API密钥已更新")
        else:
            print("⚠️ 未提供智谱AI API密钥，保持默认值")
    
    # 保存更新后的配置
    if write_env_file(content):
        print("\n✅ API密钥配置已完成!")
        print("\n下一步:")
        print("1. 重启服务以应用更改")
        print("2. 运行测试脚本验证配置")
        return True
    else:
        print("\n❌ 更新API密钥失败")
        return False

def show_current_config():
    """显示当前配置"""
    print("=== 当前配置 ===")
    
    content = read_env_file()
    if content is None:
        return
    
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key in ['KIMI_API_KEY', 'ZHIPU_API_KEY']:
                    if value.startswith('your_'):
                        print(f"{key}: 未配置 (请更新)")
                    else:
                        # 隐藏实际密钥值
                        print(f"{key}: 已配置 ({len(value)}字符)")
                elif key in ['KIMI_BASE_URL', 'ZHIPU_BASE_URL']:
                    print(f"{key}: {value}")

def main():
    """主函数"""
    print("API密钥配置助手")
    print("=" * 30)
    
    # 显示当前配置
    show_current_config()
    
    # 询问是否需要更新
    print("\n是否需要更新API密钥配置? (y/n): ", end="")
    response = input().strip().lower()
    
    if response in ['y', 'yes', '是']:
        return update_api_keys()
    else:
        print("取消更新")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)