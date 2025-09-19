# chinese-llm-jarvis
一个基于Letta平台构建的本地化智能助手系统，具备持续记忆、个性化服务和智能任务执行能力。

## 项目概述

本项目致力于构建一个本地化的贾维斯系统，具备以下特性：
- **持续记忆**: 能够记住与用户的长期对话历史和个人偏好
- **个性化服务**: 根据用户习惯提供定制化服务
- **离线可用**: 核心功能可在本地运行，保护用户隐私
- **智能助手**: 集成日程管理、信息检索、任务执行等功能

## 增强计划

本项目在原始Letta基础上进行了增强，专注于以下两个方面：

### 1. 国内模型深度集成
- 增强对国内大模型的支持，包括Kimi、智谱AI、通义千问、文心一言等
- 优化国内网络环境下的API调用性能
- 提供针对中文场景的预设模板和工具

### 2. MCP工具生态系统扩展
- 增强MCP (Model Context Protocol) 工具集成能力
- 构建丰富的本地工具生态系统
- 支持自定义工具的快速开发和部署

## 快速开始

### 环境设置和安装
```bash
# 使用uv进行开发环境安装
uv sync --all-extras

# 安装前端依赖
npm run setup
```

### 启动本地贾维斯系统
有两种方式启动系统：

1. **使用启动脚本**（推荐）：
   ```bash
   # Windows
   start.bat
   
   # Linux/macOS
   ./start.sh
   ```

2. **手动启动**：
   ```bash
   # 启动后端服务器
   uv run letta server --type rest --port 8283 --reload
   
   # 在另一个终端启动前端开发服务器
   cd frontend
   npm run dev
   ```

启动成功后，访问 http://localhost:3000 使用现代化的贾维斯UI界面。

### 配置国内大模型
在 `.env` 文件中添加您的API密钥：
```bash
# 国内大模型API密钥
KIMI_API_KEY=your_kimi_api_key_here
ZHIPU_API_KEY=your_zhipu_api_key_here
QWEN_API_KEY=your_qwen_api_key_here
ERNIE_API_KEY=your_ernie_api_key_here
```

### 使用MCP工具
```python
from letta_client import Letta

client = Letta(base_url="http://localhost:8283")

# 添加MCP服务器
client.tools.add_mcp_server({
    "server_name": "current_time",
    "type": "stdio",
    "command": "python",
    "args": ["-m", "examples.mcp_tools.get_current_time"]
})

# 获取工具并添加到代理
tools = client.tools.list_mcp_tools_by_server("current_time")
current_time_tool = client.tools.add_mcp_tool(
    mcp_server_name="current_time",
    mcp_tool_name="get_current_time"
)
```

## 最新更新进度

### 国内大模型集成已完成
- [x] 成功集成 Kimi (月之暗面) 和 Zhipu AI (智谱AI) 模型
- [x] 实现完整的模型列表获取功能，支持所有 Kimi 和 Zhipu 模型
- [x] 修复了模型在前端不显示的问题，确保 API 正确返回模型列表
- [x] 优化了模型配置，支持通过 .env 文件灵活配置 API 密钥

### 启动指令优化
为方便用户使用，项目提供了多种启动方式：

1. **一键启动脚本**（推荐）：
   ```bash
   # Windows 用户
   start.bat
   
   # Linux/macOS 用户
   ./start.sh
   ```

2. **手动启动后端服务**：
   ```bash
   # 启动后端服务器（带热重载）
   uv run letta server --type rest --port 8283 --reload
   
   # 或者不带热重载（生产环境）
   uv run letta server --type rest --port 8283
   ```

3. **启动前端开发服务器**：
   ```bash
   # 进入前端目录并启动开发服务器
   cd frontend
   npm run dev
   ```

4. **生产环境部署**：
   ```bash
   # 构建前端应用
   cd frontend
   npm run build
   
   # 启动生产服务器
   cd ..
   uv run letta server --type rest --port 8283
   ```

## 开发计划

### 第一阶段：国内模型兼容性增强 (1-2周)

#### 任务1: 完善国内模型提供商支持
- [x] 在 ProviderType 枚举中添加 Kimi 和 Zhipu 类型
- [x] 在 LLMClient 工厂方法中添加 Kimi 和 Zhipu 支持
- [x] 在 ModelSettings 中添加 kimi_base_url 和 zhipu_base_url 配置
- [x] 实现完整的模型列表获取功能

#### 任务2: 添加更多国内模型支持
- [ ] 实现通义千问(Qwen)支持
- [ ] 实现文心一言(ERNIE Bot)支持
- [ ] 实现百川(Baichuan)支持

#### 任务3: 网络优化和错误处理
- [ ] 实现国内网络环境下的重试机制
- [ ] 添加超时和错误处理优化
- [ ] 实现模型调用的缓存机制

### 第二阶段：MCP工具生态系统扩展 (2-3周)

#### 任务1: 丰富内置MCP工具
- [x] 开发文件系统操作工具集
- [x] 开发网络搜索工具集
- [ ] 开发代码执行工具集
- [ ] 开发本地应用控制工具集

#### 任务2: 自定义MCP工具开发框架
- [ ] 创建MCP工具模板生成器
- [ ] 实现工具自动注册机制
- [ ] 开发工具测试框架

#### 任务3: 工具管理界面
- [ ] 实现MCP工具的可视化管理界面
- [ ] 提供工具配置和测试功能
- [ ] 实现工具版本管理

### 第三阶段：本地贾维斯功能开发 (3-4周)

#### 任务1: 记忆增强模块
- [ ] 实现个人偏好学习模块
- [ ] 开发习惯模式识别模块
- [ ] 实现长期记忆优化模块

#### 任务2: 本地工具开发
- [ ] 开发系统控制工具
- [ ] 实现文件管理工具
- [ ] 开发应用集成工具

#### 任务3: 离线功能实现
- [ ] 实现本地向量数据库
- [ ] 开发离线索引构建机制
- [ ] 支持离线模型运行

### 第四阶段：系统集成和优化 (1-2周)

#### 任务1: 系统集成测试
- [ ] 进行端到端集成测试
- [ ] 优化系统性能
- [ ] 修复发现的问题

#### 任务2: 用户体验优化
- [x] 实现现代化React前端界面
- [ ] 提供使用文档和示例
- [ ] 实现配置向导

#### 任务3: 部署和发布准备
- [ ] 准备部署文档
- [ ] 创建安装脚本
- [ ] 准备发布版本