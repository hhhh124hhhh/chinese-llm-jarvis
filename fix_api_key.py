#!/usr/bin/env python3
"""
修复.env.local文件中KIMI_API_KEY末尾空格问题的脚本
"""

import os

def fix_api_key():
    env_file_path = os.path.join(os.path.dirname(__file__), '.env.local')
    
    # 读取文件内容
    with open(env_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找并修复KIMI_API_KEY行
    lines = content.split('\n')
    fixed = False
    
    for i, line in enumerate(lines):
        if line.startswith('KIMI_API_KEY='):
            # 检查是否末尾有空格
            if line.endswith(' '):
                # 移除末尾空格
                lines[i] = line.rstrip()
                fixed = True
                print(f"已修复API密钥行: {line} -> {lines[i]}")
            break
    
    if fixed:
        # 写入修复后的内容
        with open(env_file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print("API密钥修复完成!")
    else:
        print("API密钥无需修复")

if __name__ == "__main__":
    fix_api_key()