#!/usr/bin/env python3
"""
使用修复后的环境变量启动Letta服务
"""

import os
import subprocess
import sys

def load_fixed_env():
    """从.env.local文件加载修复后的环境变量"""
    env_file_path = os.path.join(os.path.dirname(__file__), '.env.local')
    
    if os.path.exists(env_file_path):
        with open(env_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        # 移除值末尾的空格
                        value = value.rstrip()
                        os.environ[key] = value
                        print(f"设置环境变量: {key}={value}")
    else:
        print(f"警告: 找不到环境文件 {env_file_path}")

def start_letta_server():
    """启动Letta服务"""
    process = None
    try:
        # 加载修复后的环境变量
        load_fixed_env()
        
        # 构建命令
        cmd = [sys.executable, "-m", "letta.server.rest_api.app"]
        
        # 添加其他参数（如果需要）
        # cmd.extend(["--host", "0.0.0.0", "--port", "8283"])
        
        print("启动Letta服务...")
        print(f"命令: {' '.join(cmd)}")
        
        # 启动服务
        process = subprocess.Popen(cmd, cwd=os.path.dirname(__file__))
        print(f"Letta服务已启动，PID: {process.pid}")
        
        # 等待进程结束
        process.wait()
        
    except KeyboardInterrupt:
        print("\n收到中断信号，正在停止服务...")
        if process:
            process.terminate()
            process.wait()
        print("服务已停止")
    except Exception as e:
        print(f"启动服务时出错: {e}")

if __name__ == "__main__":
    start_letta_server()