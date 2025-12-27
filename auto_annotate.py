import os
import cv2
from ultralytics import YOLO
import glob

# 配置参数
MODEL_PATH = 'parking_train/yolov8s_parking/weights/best.pt'  # 可以替换为 yolov5s_parking 的 best.pt
INPUT_DIR = 'dataset/images/test'  # 要标注的图像目录
OUTPUT_DIR = 'auto_annotations'  # 标注结果保存目录
CONF_THRESH = 0.5  # 置信度阈值

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, 'images'), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, 'labels'), exist_ok=True)

# 加载训练好的模型
print(f"加载模型: {MODEL_PATH}")
model = YOLO(MODEL_PATH)

# 获取所有图像文件
image_files = glob.glob(os.path.join(INPUT_DIR, '*.jpg')) + glob.glob(os.path.join(INPUT_DIR, '*.png')) + glob.glob(os.path.join(INPUT_DIR, '*.jpeg'))

print(f"找到 {len(image_files)} 张图像进行自动标注")

for i, image_path in enumerate(image_files):
    print(f"处理第 {i+1}/{len(image_files)} 张图像: {os.path.basename(image_path)}")
    
    # 读取图像
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图像: {image_path}")
        continue
    
    # 获取图像尺寸
    h, w, _ = img.shape
    
    # 执行推理
    results = model(image_path, conf=CONF_THRESH)
    
    # 获取检测结果
    detections = results[0].boxes
    
    # 准备YOLO格式的标注内容
    yolo_annotations = []
    for box in detections:
        # 获取类别ID
        class_id = int(box.cls.item())
        
        # 获取边界框坐标
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        
        # 计算YOLO格式的坐标 (x_center, y_center, width, height) - 归一化到0-1
        x_center = (x1 + x2) / 2 / w
        y_center = (y1 + y2) / 2 / h
        box_width = (x2 - x1) / w
        box_height = (y2 - y1) / h
        
        # 获取置信度
        conf = box.conf.item()
        
        # 添加到标注列表
        yolo_annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}")
    
    # 保存标注文件
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    label_path = os.path.join(OUTPUT_DIR, 'labels', f"{base_name}.txt")
    with open(label_path, 'w') as f:
        f.write('\n'.join(yolo_annotations))
    
    # 可视化检测结果
    annotated_img = results[0].plot()
    
    # 保存带有检测框的图像
    output_image_path = os.path.join(OUTPUT_DIR, 'images', f"{base_name}_annotated.jpg")
    cv2.imwrite(output_image_path, annotated_img)
    
    # 复制原始图像到输出目录
    original_output_path = os.path.join(OUTPUT_DIR, 'images', f"{base_name}.jpg")
    cv2.imwrite(original_output_path, img)

print("\n自动标注完成！")
print(f"标注结果保存在: {OUTPUT_DIR}")
print(f"- 原始图像: {os.path.join(OUTPUT_DIR, 'images')}")
print(f"- 标注文件: {os.path.join(OUTPUT_DIR, 'labels')}")
print(f"- 带有检测框的图像: {os.path.join(OUTPUT_DIR, 'images')} (文件名包含_annotated)")
