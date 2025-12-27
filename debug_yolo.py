from ultralytics import YOLO
import sys
import os

# 打印环境信息
print(f"Python版本: {sys.version}")
print(f"当前目录: {os.getcwd()}")
# 检查ultralytics版本
import ultralytics
print(f"Ultralytics版本: {ultralytics.__version__}")

print("\n尝试加载YOLOv8n模型(更小的模型)...")
try:
    model = YOLO('yolov8n')
    print("✓ YOLOv8n模型加载成功!")
    print(f"模型类型: {type(model)}")
    print(f"模型名称: {model.name}")
except Exception as e:
    print(f"✗ 加载YOLOv8n模型失败: {e}")
    import traceback
    traceback.print_exc()

print("\n尝试加载YOLOv5n模型(更小的模型)...")
try:
    model = YOLO('yolov5n')
    print("✓ YOLOv5n模型加载成功!")
    print(f"模型类型: {type(model)}")
    print(f"模型名称: {model.name}")
except Exception as e:
    print(f"✗ 加载YOLOv5n模型失败: {e}")
    import traceback
    traceback.print_exc()
