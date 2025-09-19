#!/bin/bash
# 本地贾维斯系统启动脚本

echo "🚀 启动本地贾维斯系统..."

# 检查是否已安装uv
if ! command -v uv &> /dev/null
then
    echo "❌ 未找到uv，正在安装..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✅ uv安装完成"
fi

# 检查是否已安装Node.js
if ! command -v node &> /dev/null
then
    echo "❌ 未找到Node.js，请先安装Node.js"
    exit 1
fi

# 检查.env文件
if [ ! -f .env ]; then
    echo "📝 创建.env配置文件..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "请编辑.env文件添加您的API密钥"
    else
        echo "# 本地贾维斯系统配置文件" > .env
        echo "LETTA_PG_DB=letta" >> .env
        echo "LETTA_PG_USER=letta" >> .env
        echo "LETTA_PG_PASSWORD=letta" >> .env
        echo "LETTA_PG_HOST=localhost" >> .env
        echo "LETTA_PG_PORT=5432" >> .env
        echo "# 国内大模型API密钥" >> .env
        echo "KIMI_API_KEY=your_kimi_api_key_here" >> .env
        echo "ZHIPU_API_KEY=your_zhipu_api_key_here" >> .env
        echo "QWEN_API_KEY=your_qwen_api_key_here" >> .env
        echo "ERNIE_API_KEY=your_ernie_api_key_here" >> .env
        echo "请编辑.env文件添加您的API密钥"
    fi
fi

# 安装前端依赖
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 安装前端依赖..."
    cd frontend
    npm install
    cd ..
fi

# 启动服务
echo "🔧 启动Letta服务器和前端开发服务器..."
ENV_FILE=.env.local uv run letta server --type rest --port 8283 --reload &
cd frontend && npm run dev &

echo "✅ 本地贾维斯系统已启动！"
echo "访问 http://localhost:3000 使用新UI"
echo "访问 http://localhost:8283 查看API文档"