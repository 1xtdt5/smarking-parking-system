import re

def main():
    try:
        print("========== YOLOv5 vs YOLOv8 停车场景对比结果 ==========")
        
        # 解析YOLOv8指标
        with open("yolov8_metrics.txt", "r") as f:
            v8_lines = f.readlines()
        
        v8_map50 = float(v8_lines[0].split(":")[1].strip())
        v8_empty_ap = float(v8_lines[1].split(":")[1].strip())
        v8_occupied_ap = float(v8_lines[2].split(":")[1].strip())
        v8_precision = float(v8_lines[3].split(":")[1].strip())
        v8_recall = float(v8_lines[4].split(":")[1].strip())
        
        # 解析YOLOv5指标
        with open("yolov5_metrics.txt", "r") as f:
            v5_lines = f.readlines()
        
        v5_map50 = float(v5_lines[0].split(":")[1].strip())
        v5_empty_ap = float(v5_lines[1].split(":")[1].strip())
        v5_occupied_ap = float(v5_lines[2].split(":")[1].strip())
        v5_precision = float(v5_lines[3].split(":")[1].strip())
        v5_recall = float(v5_lines[4].split(":")[1].strip())
        
        # 生成对比表格
        print(f"{'指标':<20} {'YOLOv5':<10} {'YOLOv8':<10} {'更优模型':<10}")
        print(f"{'='*50}")
        
        # 比较各指标
        print(f"{'mAP@0.5':<20} {v5_map50:.4f}     {v8_map50:.4f}     {'v8' if v8_map50>v5_map50 else 'v5' if v5_map50>v8_map50 else '持平'}")
        print(f"{'空缺车位AP@0.5':<20} {v5_empty_ap:.4f}     {v8_empty_ap:.4f}     {'v8' if v8_empty_ap>v5_empty_ap else 'v5' if v5_empty_ap>v8_empty_ap else '持平'}")
        print(f"{'已占用车位AP@0.5':<20} {v5_occupied_ap:.4f}     {v8_occupied_ap:.4f}     {'v8' if v8_occupied_ap>v5_occupied_ap else 'v5' if v5_occupied_ap>v8_occupied_ap else '持平'}")
        print(f"{'Precision':<20} {v5_precision:.4f}     {v8_precision:.4f}     {'v8' if v8_precision>v5_precision else 'v5' if v5_precision>v8_precision else '持平'}")
        print(f"{'Recall':<20} {v5_recall:.4f}     {v8_recall:.4f}     {'v8' if v8_recall>v5_recall else 'v5' if v5_recall>v8_recall else '持平'}")
        
        print("\n========== 对比总结 ==========")
        # 计算综合得分
        v5_score = v5_map50 * 0.4 + v5_empty_ap * 0.3 + v5_occupied_ap * 0.3
        v8_score = v8_map50 * 0.4 + v8_empty_ap * 0.3 + v8_occupied_ap * 0.3
        
        if v8_score > v5_score:
            print(f"YOLOv8整体性能更优，综合得分: {v8_score:.4f} > {v5_score:.4f}")
        elif v5_score > v8_score:
            print(f"YOLOv5整体性能更优，综合得分: {v5_score:.4f} > {v8_score:.4f}")
        else:
            print(f"两个模型性能相当，综合得分: {v5_score:.4f}")
            
    except FileNotFoundError as e:
        print(f"错误: 未找到指标文件 - {e}")
        print("请先训练YOLOv5和YOLOv8模型以生成指标文件")
    except Exception as e:
        print(f"解析指标时发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
