import os

# 创建数据集目录结构
directories = [
    'dataset/images/train',
    'dataset/images/val',
    'dataset/images/test',
    'dataset/labels/train',
    'dataset/labels/val',
    'dataset/labels/test'
]

for dir_path in directories:
    os.makedirs(dir_path, exist_ok=True)
    print(f"Created directory: {dir_path}")

print("Dataset directory structure created successfully!")