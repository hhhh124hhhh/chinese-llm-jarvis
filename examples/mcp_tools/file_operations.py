import os
import json
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("file_operations")


@mcp.tool()
def read_file(file_path: str) -> str:
    """读取文件内容
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"读取文件时出错: {str(e)}"


@mcp.tool()
def write_file(file_path: str, content: str, mode: str = "w") -> str:
    """写入文件内容
    
    Args:
        file_path: 文件路径
        content: 要写入的内容
        mode: 写入模式，'w'为覆盖，'a'为追加
        
    Returns:
        操作结果
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, mode, encoding='utf-8') as f:
            f.write(content)
        return f"成功写入文件: {file_path}"
    except Exception as e:
        return f"写入文件时出错: {str(e)}"


@mcp.tool()
def list_files(directory: str) -> List[str]:
    """列出目录中的文件
    
    Args:
        directory: 目录路径
        
    Returns:
        文件列表
    """
    try:
        return os.listdir(directory)
    except Exception as e:
        return [f"列出文件时出错: {str(e)}"]


@mcp.tool()
def file_exists(file_path: str) -> bool:
    """检查文件是否存在
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件是否存在
    """
    return os.path.exists(file_path)


@mcp.tool()
def delete_file(file_path: str) -> str:
    """删除文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        操作结果
    """
    try:
        os.remove(file_path)
        return f"成功删除文件: {file_path}"
    except Exception as e:
        return f"删除文件时出错: {str(e)}"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")