#!/bin/bash

# 快速启动应用程序脚本

# 检查虚拟环境是否已激活
if [ -z "$VIRTUAL_ENV" ]; then
    # 检查虚拟环境目录是否存在
    if [ -d "venv" ]; then
        echo "激活虚拟环境..."
        source venv/bin/activate
    else
        echo "错误: 虚拟环境不存在！"
        echo "请先运行安装脚本: ./install_linux.sh 或 ./install_macos.sh"
        exit 1
    fi
fi

# 检查.env文件是否存在
if [ ! -f .env ]; then
    echo "警告: .env 文件不存在！"
    echo "请复制 .env 文件并配置数据库连接信息"
fi

# 运行应用程序
echo "启动应用程序..."
echo "应用程序将在 http://localhost:5000 运行"
echo "按 Ctrl+C 停止应用程序"
echo "========================================="
python app.py
