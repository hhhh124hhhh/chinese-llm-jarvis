import requests
import json
from typing import List, Dict, Optional

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("web_search")


@mcp.tool()
def search_duckduckgo(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """使用DuckDuckGo进行网络搜索
    
    Args:
        query: 搜索查询
        max_results: 最大结果数量，默认为5
        
    Returns:
        搜索结果列表，每个结果包含标题、链接和摘要
    """
    try:
        # DuckDuckGo Instant Answer API
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        # 添加相关主题
        if "RelatedTopics" in data:
            for topic in data["RelatedTopics"][:max_results]:
                if "FirstURL" in topic and "Text" in topic:
                    results.append({
                        "title": topic["FirstURL"].split("/")[-1].replace("_", " "),
                        "url": topic["FirstURL"],
                        "snippet": topic["Text"]
                    })
        
        return results
    except Exception as e:
        return [{"error": f"搜索时出错: {str(e)}"}]


@mcp.tool()
def get_webpage_content(url: str) -> str:
    """获取网页内容
    
    Args:
        url: 网页URL
        
    Returns:
        网页文本内容
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 简单的文本提取
        import re
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', response.text)
        # 清理多余空白
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 只返回前1000个字符
        return text[:1000] + "..." if len(text) > 1000 else text
    except Exception as e:
        return f"获取网页内容时出错: {str(e)}"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")