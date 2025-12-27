#!/bin/bash

# Linux 安装脚本
# 智慧停车位检测系统

echo "========================================="
echo "智慧停车位检测系统 - Linux 安装脚本"
echo "========================================="

# 检查 Python 是否安装
echo "检查 Python 是否安装..."
if ! command -v python3 &> /dev/null; then
    echo "错误: Python 3 未安装！"
    echo "尝试安装 Python 3..."
    
    # 检查包管理器
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian 系统
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL 系统
        sudo yum update -y
        sudo yum install -y python3 python3-pip python3-venv
    else
        echo "错误: 不支持的包管理器！"
        echo "请手动安装 Python 3.8 或更高版本"
        exit 1
    fi
fi

echo "Python 已安装"

# 检查 pip 是否可用
echo "检查 pip 是否可用..."
if ! command -v pip3 &> /dev/null; then
    echo "错误: pip 不可用！"
    echo "请手动安装 pip3"
    exit 1
fi

echo "pip 已可用"

# 检查系统依赖
echo "安装系统依赖..."
if command -v apt-get &> /dev/null; then
    # Ubuntu/Debian 系统
    sudo apt-get install -y libmysqlclient-dev libssl-dev
elif command -v yum &> /dev/null; then
    # CentOS/RHEL 系统
    sudo yum install -y mysql-devel openssl-devel
fi

# 创建虚拟环境
echo "创建虚拟环境..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "错误: 创建虚拟环境失败！"
    exit 1
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "错误: 安装依赖失败！"
    exit 1
fi

# 复制配置文件模板
echo "检查配置文件..."
if [ ! -f .env ]; then
    echo "创建 .env 文件..."
    touch .env
    echo "请编辑 .env 文件配置数据库连接信息"
fi

echo "========================================="
echo "安装完成！"
echo "========================================="
echo "运行应用程序的步骤："
echo "1. 激活虚拟环境：source venv/bin/activate"
echo "2. 运行应用程序：python app.py"
echo "3. 打开浏览器访问：http://localhost:5000"
echo "========================================="

# 给脚本添加执行权限
chmod +x run_app.sh

echo "可以使用 ./run_app.sh 快速启动应用程序"
