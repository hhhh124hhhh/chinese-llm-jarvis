#!/bin/bash
# Git Bash环境下的Letta启动脚本

# 解决cygpath缺失问题
fix_cygpath() {
    if ! command -v cygpath &> /dev/null; then
        # 创建cygpath的替代函数
        cygpath() {
            case "$1" in
                -u|--unix)
                    echo "$2" | sed 's/\\/\//g' | sed 's/^C:/\/c/' | sed 's/^D:/\/d/' | sed 's/^E:/\/e/' | sed 's/^F:/\/f/'
                    ;;
                -w|--windows)
                    echo "$2" | sed 's/^\///' | sed 's/^c\//C:\//' | sed 's/^d\//D:\//' | sed 's/^e\//E:\//' | sed 's/^f\//F:\//' | sed 's/\//\\/g'
                    ;;
                *)
                    echo "$1"
                    ;;
            esac
        }
        export -f cygpath
    fi
}

# 设置环境变量
set_env_vars() {
    export TMPDIR="/tmp"
    export TEMP="/tmp"
    export TMP="/tmp"
    
    # 如果.env.local存在，加载它
    if [ -f ".env.local" ]; then
        echo "加载环境变量从 .env.local"
        set -a
        source .env.local
        set +a
    fi
    
    # 确保API密钥已设置
    if [ -z "$KIMI_API_KEY" ]; then
        echo "警告: KIMI_API_KEY 未设置"
    fi
}

# 检查Python和uv
check_dependencies() {
    if ! command -v python &> /dev/null; then
        echo "错误: Python未找到"
        return 1
    fi
    
    if ! command -v uv &> /dev/null; then
        echo "错误: uv未找到"
        return 1
    fi
    
    echo "Python版本: $(python --version)"
    echo "uv版本: $(uv --version)"
}

# 主函数
main() {
    echo "=== Git Bash Letta 启动器 ==="
    
    # 修复环境
    fix_cygpath
    set_env_vars
    check_dependencies
    
    if [ $? -ne 0 ]; then
        echo "依赖检查失败"
        exit 1
    fi
    
    # 构建启动命令
    local cmd="uv run letta server"
    
    # 添加参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --debug)
                cmd="$cmd --debug"
                shift
                ;;
            --port=*)
                cmd="$cmd --port=${1#*=}"
                shift
                ;;
            --port)
                cmd="$cmd --port=$2"
                shift 2
                ;;
            --reload)
                cmd="$cmd --reload"
                shift
                ;;
            *)
                cmd="$cmd $1"
                shift
                ;;
        esac
    done
    
    echo "启动命令: $cmd"
    echo "按Ctrl+C停止服务器"
    echo "================================"
    
    # 执行命令
    exec $cmd
}

# 如果直接运行脚本
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi