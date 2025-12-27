import chardet
import os

# 检查app.py的编码
file_path = 'app.py'
if os.path.exists(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        print(f"文件编码: {result['encoding']}")
        print(f"置信度: {result['confidence']:.2f}")
        
        # 尝试用检测到的编码读取文件
        try:
            with open(file_path, 'r', encoding=result['encoding']) as f:
                content = f.read()
            print(f"成功用{result['encoding']}编码读取文件")
        except Exception as e:
            print(f"用{result['encoding']}编码读取文件失败: {e}")
            
            # 尝试用utf-8编码读取
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print("成功用utf-8编码读取文件")
            except Exception as e:
                print(f"用utf-8编码读取文件失败: {e}")
else:
    print(f"文件{file_path}不存在")
