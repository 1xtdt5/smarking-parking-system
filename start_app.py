import os
import sys
import subprocess

# 设置输出文件路径
output_file = 'app_output.log'

def run_app():
    """运行应用程序并捕获输出"""
    print(f"开始运行应用程序...")
    print(f"所有输出将保存到: {output_file}")
    
    # 构建命令
    cmd = [sys.executable, 'app.py']
    
    try:
        # 打开输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            # 运行命令并捕获输出
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=os.getcwd(),
                text=True,
                bufsize=1
            )
            
            # 实时读取输出并写入文件
            for line in process.stdout:
                f.write(line)
                f.flush()
                print(line, end='')
            
            # 等待进程结束
            process.wait()
            
            print(f"\n应用程序退出，退出码: {process.returncode}")
            f.write(f"\n应用程序退出，退出码: {process.returncode}")
            
            return process.returncode
            
    except Exception as e:
        print(f"运行应用程序时出错: {str(e)}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"运行应用程序时出错: {str(e)}")
        return -1

if __name__ == "__main__":
    run_app()