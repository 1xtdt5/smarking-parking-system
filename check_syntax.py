import sys
import os

# 检查Python版本
print(f"Python版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")

# 检查app.py文件是否存在
if os.path.exists('app.py'):
    print(f"app.py文件存在，大小: {os.path.getsize('app.py')}字节")
    
    # 尝试打开并读取文件
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"成功读取文件，行数: {len(content.splitlines())}")
        
        # 尝试编译代码
        try:
            compile(content, 'app.py', 'exec')
            print("代码语法检查通过！")
        except SyntaxError as e:
            print(f"语法错误: {e}")
            print(f"错误位置: 第{e.lineno}行，第{e.offset}列")
            # 显示错误行附近的代码
            lines = content.splitlines()
            start = max(0, e.lineno - 3)
            end = min(len(lines), e.lineno + 2)
            print("错误行附近的代码:")
            for i in range(start, end):
                line_num = i + 1
                marker = "-> " if line_num == e.lineno else "   "
                print(f"{marker}{line_num:4d}: {lines[i]}")
        except Exception as e:
            print(f"编译错误: {e}")
            
    except Exception as e:
        print(f"读取文件错误: {e}")
else:
    print("app.py文件不存在")
    
    # 列出当前目录下的文件
    print("当前目录下的文件:")
    for file in os.listdir('.'):
        if os.path.isfile(file):
            print(f"  - {file}")
