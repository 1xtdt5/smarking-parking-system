import subprocess
import sys

# 运行Python命令并捕获详细输出
def run_command(cmd):
    print(f"运行命令: {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            encoding='utf-8',
            timeout=30
        )
        print(f"退出码: {result.returncode}")
        print("标准输出:")
        print(result.stdout)
        if result.stderr:
            print("标准错误:")
            print(result.stderr)
        return result
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return None

# 检查Python版本
print("检查Python版本...")
run_command("python --version")

# 检查app.py是否存在
print("\n检查app.py文件...")
run_command("dir app.py")

# 检查文件大小
print("\n检查app.py文件大小...")
run_command("powershell -Command (Get-Item app.py).Length")

# 尝试简单的语法检查
print("\n尝试语法检查...")
run_command("python -c \"import ast; ast.parse(open('app.py', 'r', encoding='utf-8').read())\""),

# 尝试运行应用的一小部分
print("\n尝试导入app模块...")
run_command("python -c \"try: import app; print('成功导入app模块') except Exception as e: print(f'导入错误: {e}')\"")
