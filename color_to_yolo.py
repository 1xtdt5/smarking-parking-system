import cv2
import numpy as np
import os
import csv

# 创建标签目录
os.makedirs('labels', exist_ok=True)

print("开始从颜色掩码中提取YOLO标注...")

# 定义颜色阈值（BGR格式）
# 蓝色：空缺车位
lower_blue = np.array([240, 60, 60])
upper_blue = np.array([250, 65, 65])

# 红色：已占用车位
lower_red = np.array([50, 80, 200])
upper_red = np.array([100, 100, 255])

# 读取parking.csv文件
total_rows = 0
processed_rows = 0

with open('parking.csv', 'r') as f:
    reader = csv.DictReader(f)
    
    # 统计总行数
    all_rows = list(reader)
    total_rows = len(all_rows)
    print(f"找到 {total_rows} 行数据")
    
    # 遍历每个图像
    for idx, row in enumerate(all_rows):
        print(f"\n处理第 {idx+1}/{total_rows} 行:")
        print(f"  ID: {row['id']}")
        print(f"  图像路径: {row['image']}")
        print(f"  掩码路径: {row['mask']}")
        
        try:
            image_path = row['image']
            mask_path = row['mask']
        except KeyError as e:
            print(f"  错误: CSV行中缺少必要字段 {e}")
            continue
        
        try:
            # 检查文件是否存在
            if not os.path.exists(image_path):
                print(f"  警告: 图像文件不存在 - {image_path}")
                continue
            if not os.path.exists(mask_path):
                print(f"  警告: 掩码文件不存在 - {mask_path}")
                continue
            
            # 读取原始图像和掩码图像
            img = cv2.imread(image_path)
            if img is None:
                print(f"  警告: 无法读取图像 - {image_path}")
                continue
            
            mask = cv2.imread(mask_path)
            if mask is None:
                print(f"  警告: 无法读取掩码图像 - {mask_path}")
                continue
            
            # 获取图像尺寸
            height, width = mask.shape[:2]
            print(f"  图像尺寸: {width}x{height}")
            
            # 创建YOLO格式的标注内容
            yolo_annotations = []
            
            # 提取蓝色区域（空缺车位）
            blue_mask = cv2.inRange(mask, lower_blue, upper_blue)
            contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            print(f"  找到 {len(contours)} 个蓝色框（空缺车位）")
            for contour in contours:
                # 计算边界框
                x, y, w, h = cv2.boundingRect(contour)
                
                # 过滤太小的边界框
                if w < 10 or h < 10:
                    continue
                
                # 转换为YOLO格式（归一化坐标）
                class_id = 0  # 空缺车位
                x_center = (x + w / 2) / width
                y_center = (y + h / 2) / height
                normalized_w = w / width
                normalized_h = h / height
                
                # 确保坐标在0-1范围内
                x_center = max(0, min(1, x_center))
                y_center = max(0, min(1, y_center))
                normalized_w = max(0, min(1, normalized_w))
                normalized_h = max(0, min(1, normalized_h))
                
                # 添加到标注列表
                yolo_annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {normalized_w:.6f} {normalized_h:.6f}")
            
            # 提取红色区域（已占用车位）
            red_mask = cv2.inRange(mask, lower_red, upper_red)
            contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            print(f"  找到 {len(contours)} 个红色框（已占用车位）")
            for contour in contours:
                # 计算边界框
                x, y, w, h = cv2.boundingRect(contour)
                
                # 过滤太小的边界框
                if w < 10 or h < 10:
                    continue
                
                # 转换为YOLO格式（归一化坐标）
                class_id = 1  # 已占用车位
                x_center = (x + w / 2) / width
                y_center = (y + h / 2) / height
                normalized_w = w / width
                normalized_h = h / height
                
                # 确保坐标在0-1范围内
                x_center = max(0, min(1, x_center))
                y_center = max(0, min(1, y_center))
                normalized_w = max(0, min(1, normalized_w))
                normalized_h = max(0, min(1, normalized_h))
                
                # 添加到标注列表
                yolo_annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {normalized_w:.6f} {normalized_h:.6f}")
            
            # 保存YOLO格式的标注文件
            if yolo_annotations:
                image_name = os.path.basename(image_path)
                annotation_name = os.path.splitext(image_name)[0] + '.txt'
                annotation_path = os.path.join('labels', annotation_name)
                
                with open(annotation_path, 'w') as f:
                    f.write('\n'.join(yolo_annotations))
                
                print(f"  ✓ 处理完成: {image_path} -> {annotation_path}")
                processed_rows += 1
            else:
                print(f"  警告: 未找到任何边界框")
                
        except Exception as e:
            print(f"  错误处理此图像: {e}")
            import traceback
            traceback.print_exc()
            continue

print(f"\n处理完成！共处理 {total_rows} 行数据，成功处理 {processed_rows} 个图像。")
