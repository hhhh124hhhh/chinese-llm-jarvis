# 国产大模型配置和启动指南

## 问题分析

我发现了导致启动失败的主要原因：

1. **环境变量配置不完整** - 缺少Kimi和Zhipu的base_url配置
2. **数据库配置问题** - SQLite配置未正确生效
3. **Git Bash环境问题** - cygpath工具缺失导致路径转换失败

## 修复内容

### 1. 更新了 `.env.local` 文件
- 添加了 `KIMI_BASE_URL=https://api.moonshot.cn/v1`
- 添加了 `ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4`
- 添加了 `LETTA_ENVIRONMENT=DEV`
- 添加了 `LETTA_DEFAULT_LLM_HANDLE=kimi/moonshot-v1-128k`

### 2. 修改了 `letta/settings.py`
- 添加了SQLite配置支持
- 修改了数据库引擎选择逻辑

### 3. 验证了Provider配置
- Kimi和Zhipu Provider都正确使用 `model_endpoint_type="openai"`
- 所有模型配置都正确

## 启动方法

### 方法1：使用PowerShell（推荐）
```powershell
# 设置环境变量
$env:LETTA_DEBUG = "True"
$env:KIMI_API_KEY = "sk-qgxX3Yb6RsOhvXroQDKXNjFk0DArzRJFzy1iimef7V5naTWH"

# 启动服务器
uv run letta server --debug
```

### 方法2：使用Windows命令提示符
```cmd
set KIMI_API_KEY=sk-qgxX3Yb6RsOhvXroQDKXNjFk0DArzRJFzy1iimef7V5naTWH
uv run letta server --debug
```

### 方法3：修复Git Bash环境
如果需要使用Git Bash，请先安装cygpath工具或使用以下命令：
```bash
# 使用cmd模拟器
cmd /c "uv run letta server --debug"
```

## 配置验证

你可以使用以下方法验证配置：

### 1. 检查环境变量
```python
import os
from letta.settings import model_settings, settings

print(f"KIMI_API_KEY: {'已设置' if model_settings.kimi_api_key else '未设置'}")
print(f"ZHIPU_API_KEY: {'已设置' if model_settings.zhipu_api_key else '未设置'}")
print(f"存储类型: {settings.storage_type}")
print(f"数据库引擎: {settings.database_engine}")
```

### 2. 测试Provider
```python
from letta.schemas.providers.kimi import KimiProvider
from letta.schemas.providers.zhipu import ZhipuProvider

# 测试Kimi
kimi_provider = KimiProvider()
models = kimi_provider.list_llm_models()
print(f"Kimi模型数量: {len(models)}")

# 测试Zhipu
zhipu_provider = ZhipuProvider()
models = zhipu_provider.list_llm_models()
print(f"Zhipu模型数量: {len(models)}")
```

## 可能的其他问题

如果还有问题，请检查：

1. **网络连接** - 确保能访问Kimi和Zhipu的API
2. **API密钥** - 确保API密钥有效
3. **依赖包** - 确保所有依赖都已安装
4. **端口占用** - 确保端口8283未被占用

## 故障排除

1. **端口占用错误**：
   ```bash
   # 检查端口占用
   netstat -ano | findstr :8283
   # 使用不同端口启动
   uv run letta server --port 8284
   ```

2. **数据库错误**：
   ```bash
   # 删除旧的SQLite数据库
   rm -f ~/.letta/sqlite.db
   ```

3. **权限问题**：
   ```bash
   # 确保letta目录存在且有权限
   mkdir -p ~/.letta
   chmod 755 ~/.letta
   ```

现在应该可以正常启动了！建议使用PowerShell来启动服务器。