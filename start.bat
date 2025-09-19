@echo off
REM 本地贾维斯系统启动脚本

echo 🚀 启动本地贾维斯系统...

REM 检查是否已安装uv
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到uv，正在安装...
    powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"
    echo ✅ uv安装完成
) else (
    echo ✅ 已安装uv
)

REM 检查.env文件
if not exist .env (
    echo 📝 创建.env配置文件...
    if exist .env.example (
        copy .env.example .env
    ) else (
        echo # 本地贾维斯系统配置文件 > .env
        echo LETTA_PG_DB=letta >> .env
        echo LETTA_PG_USER=letta >> .env
        echo LETTA_PG_PASSWORD=letta >> .env
        echo LETTA_PG_HOST=localhost >> .env
        echo LETTA_PG_PORT=5432 >> .env
        echo # 国内大模型API密钥 >> .env
        echo KIMI_API_KEY=your_kimi_api_key_here >> .env
        echo ZHIPU_API_KEY=your_zhipu_api_key_here >> .env
        echo QWEN_API_KEY=your_qwen_api_key_here >> .env
        echo ERNIE_API_KEY=your_ernie_api_key_here >> .env
        echo 请编辑.env文件添加您的API密钥
    )
)

REM 检查是否已安装Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Node.js，请先安装Node.js
    pause
    exit /b 1
)

REM 安装前端依赖
if not exist frontend\node_modules (
    echo 📦 安装前端依赖...
    cd frontend
    npm install
    cd ..
)

REM 启动服务
echo 🔧 启动Letta服务器和前端开发服务器...
start "Letta服务器" /D . cmd /c "set ENV_FILE=.env.local && uv run letta server --type rest --port 8283 --reload"
start "前端开发服务器" /D frontend cmd /c "npm run dev"

echo ✅ 本地贾维斯系统已启动！
echo 访问 http://localhost:3000 使用新UI
echo 访问 http://localhost:8283 查看API文档

echo.
echo 按任意键关闭此窗口...
pause >nul