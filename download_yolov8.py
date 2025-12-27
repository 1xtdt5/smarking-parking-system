from ultralytics import YOLO

# 加载指定版本模型（自动下载权重到本地缓存）
# 可选版本：yolov8n.pt（最小）、yolov8s.pt（中等）、yolov8m.pt（中大型）、yolov8l.pt（大型）
model = YOLO("yolov8s.pt")  # 首次运行会自动下载，缓存路径：~/.ultralytics/weights/
print("YOLOv8模型加载成功！")