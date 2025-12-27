@echo off
setlocal enabledelayedexpansion

echo 开始运行停车位检测系统...
echo 所有输出将保存到 app_output.log 文件中...

REM 运行应用并将所有输出重定向到文件
python app.py > app_output.log 2>&1

if %errorlevel% equ 0 (
    echo 应用程序已退出，退出码：0
    echo 请查看 app_output.log 文件获取详细输出
) else (
    echo 应用程序已退出，退出码：%errorlevel%
    echo 请查看 app_output.log 文件获取错误信息
)

pause