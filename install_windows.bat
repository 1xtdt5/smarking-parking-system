@echo off

REM Windows 安装脚本
REM 智慧停车位检测系统

echo ================================================
echo 智慧停车位检测系统 - Windows 安装脚本
echo ================================================

echo 检查 Python 是否安装...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: Python 未安装！
    echo 请先从 https://www.python.org/downloads/ 下载并安装 Python 3.8 或更高版本
    pause
    exit /b 1
)

echo Python 已安装

echo 检查 pip 是否可用...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: pip 不可用！
    echo 请确保 Python 安装时已勾选 "Add Python to PATH" 选项
    pause
    exit /b 1
)

echo pip 已可用

echo 创建虚拟环境...
python -m venv venv
if %errorlevel% neq 0 (
    echo 错误: 创建虚拟环境失败！
    pause
    exit /b 1
)

echo 激活虚拟环境...
call venv\Scripts\activate.bat

echo 安装依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误: 安装依赖失败！
    pause
    exit /b 1
)

echo 复制配置文件模板...
if not exist .env (
    echo 创建 .env 文件...
    copy .env .env
    echo 请编辑 .env 文件配置数据库连接信息
)

echo ================================================
echo 安装完成！
echo ================================================
echo 运行应用程序的步骤：
echo 1. 激活虚拟环境：venv\Scripts\activate.bat
echo 2. 运行应用程序：python app.py
echo 3. 打开浏览器访问：http://localhost:5000
echo ================================================

pause
