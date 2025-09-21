# Git Bash 完整修复指南

## 问题根源

Git Bash 缺少 `cygpath` 工具，导致路径转换失败。我已经创建了几个解决方案。

## 解决方案

### 方案1：使用专门的启动脚本（推荐）

```bash
# 1. 首先加载修复脚本
source git_bash_fix.sh

# 2. 使用专门的启动脚本
./start_with_git_bash.sh --debug
```

### 方案2：手动修复环境

```bash
# 在Git Bash中运行以下命令：
export TMPDIR="/tmp"
export TEMP="/tmp"
export TMP="/tmp"

# 创建cygpath替代函数
cygpath() { echo "$2"; }
export -f cygpath

# 现在可以正常启动
uv run letta server --debug
```

### 方案3：使用Windows子系统

如果上述方案都不工作，建议使用：

1. **Windows PowerShell**（推荐）
2. **Windows命令提示符**
3. **WSL**（如果已安装）

## 使用方法

### 快速启动
```bash
# 一步启动
source git_bash_fix.sh && uv run letta server --debug
```

### 带参数启动
```bash
# 使用启动脚本
./start_with_git_bash.sh --debug --port 8284 --reload
```

### 后台启动
```bash
# 后台启动（需要安装nohup或类似工具）
source git_bash_fix.sh && nohup uv run letta server --debug > server.log 2>&1 &
```

## 创建的文件说明

1. **git_bash_fix.sh** - 环境修复脚本
2. **start_with_git_bash.sh** - 专用启动脚本
3. **set_permissions.bat** - 权限设置脚本
4. **fix_git_bash.sh** - 完整环境修复脚本

## 故障排除

### 1. 如果仍然出现cygpath错误
```bash
# 完全重置环境
unset TMPDIR TEMP TMP
export TMPDIR="/tmp"
export TEMP="/tmp"
export TMP="/tmp"

# 重新定义cygpath
unset -f cygpath
cygpath() { echo "$2"; }
export -f cygpath
```

### 2. 如果权限问题
```bash
# 在Windows命令提示符中运行：
set_permissions.bat
```

### 3. 如果路径问题
```bash
# 确保在正确的目录
pwd
ls -la

# 如果需要，手动设置路径
export PATH="/usr/bin:/bin:$PATH"
```

## 验证修复

```bash
# 测试基本命令
echo "测试命令..."
python --version
uv --version

# 测试启动命令（不真正启动）
echo "测试启动命令..."
uv run letta server --help
```

## 长期解决方案

为了避免以后再次遇到这个问题：

1. **安装完整的Cygwin**（包含cygpath）
2. **使用WSL**（Linux子系统）
3. **切换到PowerShell**

## 推荐的工作流程

```bash
# 1. 打开Git Bash
# 2. 进入项目目录
cd /d/chinese-llm-jarvis

# 3. 加载环境
source git_bash_fix.sh

# 4. 启动服务器
uv run letta server --debug
```

现在Git Bash应该可以正常工作了！如果还有问题，请告诉我具体的错误信息。