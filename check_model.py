import os

print("=== 检查模型文件 ===")
print(f"当前工作目录: {os.getcwd()}")

# 检查模型文件
yolo5_path = 'parking_train/yolov5s_parking/weights/best.pt'
yolo8_path = 'parking_train/yolov8s_parking/weights/best.pt'

print(f"\nYOLO5模型路径: {yolo5_path}")
print(f"YOLO5模型是否存在: {os.path.exists(yolo5_path)}")

print(f"\nYOLO8模型路径: {yolo8_path}")
print(f"YOLO8模型是否存在: {os.path.exists(yolo8_path)}")

# 检查目录结构
print("\n=== 检查目录结构 ===")
print("parking_train目录:")
for item in os.listdir('parking_train'):
    print(f"  {item}")
    if os.path.isdir(f'parking_train/{item}'):
        print(f"    子目录内容:")
        for subitem in os.listdir(f'parking_train/{item}')[:10]:  # 只显示前10个
            print(f"      {subitem}")

# 检查是否有其他模型文件
print("\n=== 检查根目录的模型文件 ===")
for file in os.listdir('.'):
    if file.endswith('.pt'):
        print(f"  {file} (大小: {os.path.getsize(file)//1024} KB)")