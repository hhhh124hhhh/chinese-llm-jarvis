#!/usr/bin/env python3
"""
更新.env.local配置文件的脚本
"""

import os
from pathlib import Path


def update_env_config():
    """更新.env.local配置文件"""
    project_root = Path(__file__).parent
    env_file = project_root / ".env.local"
    
    print("=== 更新.env.local配置文件 ===")
    
    if not env_file.exists():
        print("❌ 未找到.env.local文件")
        return False
    
    # 读取现有内容
    with open(env_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 更新配置
    updated_lines = []
    kimi_key_updated = False
    zhipu_key_updated = False
    zhipu_url_updated = False
    
    for line in lines:
        # 检查是否需要更新Zhipu API密钥
        if line.startswith('ZHIPU_API_KEY=') and 'your_zhipu_api_key_here' in line:
            # 如果是注释行，取消注释并提示用户输入实际API密钥
            if line.startswith('#'):
                print("请提供您的智谱AI API密钥 (可以从 https://open.bigmodel.cn/ 获取):")
                zhipu_api_key = input("智谱AI API密钥: ").strip()
                if zhipu_api_key:
                    updated_lines.append(f'ZHIPU_API_KEY={zhipu_api_key}\n')
                    zhipu_key_updated = True
                    print("✅ 智谱AI API密钥已更新")
                else:
                    updated_lines.append(line)  # 保持原样
            else:
                # 如果不是注释行但仍是占位符，提示更新
                print("请提供您的智谱AI API密钥 (可以从 https://open.bigmodel.cn/ 获取):")
                zhipu_api_key = input("智谱AI API密钥: ").strip()
                if zhipu_api_key:
                    updated_lines.append(f'ZHIPU_API_KEY={zhipu_api_key}\n')
                    zhipu_key_updated = True
                    print("✅ 智谱AI API密钥已更新")
                else:
                    updated_lines.append(line)  # 保持原样
        elif line.startswith('# ZHIPU_API_KEY=') and 'your_zhipu_api_key_here' in line:
            # 取消注释并提示用户输入实际API密钥
            print("请提供您的智谱AI API密钥 (可以从 https://open.bigmodel.cn/ 获取):")
            zhipu_api_key = input("智谱AI API密钥: ").strip()
            if zhipu_api_key:
                updated_lines.append(f'ZHIPU_API_KEY={zhipu_api_key}\n')
                zhipu_key_updated = True
                print("✅ 智谱AI API密钥已更新")
            else:
                updated_lines.append(line[1:])  # 只是取消注释
        # 检查是否需要更新Zhipu Base URL
        elif line.startswith('# ZHIPU_BASE_URL='):
            updated_lines.append('ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4\n')
            zhipu_url_updated = True
            print("✅ 智谱AI Base URL已更新")
        elif line.startswith('ZHIPU_BASE_URL='):
            updated_lines.append('ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4\n')
            zhipu_url_updated = True
            print("✅ 智谱AI Base URL已更新")
        else:
            updated_lines.append(line)
    
    # 如果没有找到Zhipu配置，添加默认配置
    if not any('ZHIPU_API_KEY=' in line for line in updated_lines):
        print("\n未找到智谱AI API密钥配置，将添加默认配置")
        print("请提供您的智谱AI API密钥 (可以从 https://open.bigmodel.cn/ 获取):")
        zhipu_api_key = input("智谱AI API密钥: ").strip()
        if zhipu_api_key:
            # 在合适的位置插入Zhipu配置
            insert_index = -1
            for i, line in enumerate(updated_lines):
                if 'KIMI_BASE_URL=' in line:
                    insert_index = i + 1
                    break
            
            if insert_index != -1:
                updated_lines.insert(insert_index, f'ZHIPU_API_KEY={zhipu_api_key}\n')
                updated_lines.insert(insert_index + 1, 'ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4\n')
                zhipu_key_updated = True
                zhipu_url_updated = True
                print("✅ 已添加智谱AI配置")
    
    # 写入更新后的内容
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)
    
    print("\n=== 更新完成 ===")
    if zhipu_key_updated:
        print("✅ 智谱AI API密钥已配置")
    else:
        print("ℹ️  智谱AI API密钥未更改")
        
    if zhipu_url_updated:
        print("✅ 智谱AI Base URL已配置")
    else:
        print("ℹ️  智谱AI Base URL未更改")
    
    print("\n请重新启动服务以使配置生效")
    return True


def main():
    """主函数"""
    print("AI模型配置更新工具")
    print("==================")
    
    try:
        update_env_config()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n❌ 更新过程中出现错误: {e}")


if __name__ == "__main__":
    main()