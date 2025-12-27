import torch
import os
from ultralytics import YOLO

# 设置工作目录为当前目录
os.chdir(r'c:\Users\25031\Desktop\parking_system')

# 配置参数
DATA_YAML = "parking.yaml"  # 使用当前目录下的parking.yaml
EPOCHS = 50  # 训练轮数
BATCH_SIZE = 8  # 根据CPU内存调整
IMG_SIZE = 640  # 输入图片尺寸
DEVICE = "cpu"  # CPU训练
PROJECT = "parking_train"
NAME = "yolov5su_parking"

print("开始训练YOLO5模型...")

# 加载YOLO5模型
model = YOLO('yolov5su.pt')

# 开始训练
try:
    results = model.train(
        data=DATA_YAML,
        epochs=EPOCHS,
        batch=BATCH_SIZE,
        imgsz=IMG_SIZE,
        device=DEVICE,
        project=PROJECT,
        name=NAME,
        save=True,  # 保存模型
        val=True    # 训练中验证
    )
    print("YOLO5训练完成!")
    
    # 验证模型
    print("开始评估YOLO5模型...")
    metrics = model.val(data=DATA_YAML, device=DEVICE)
    
    # 保存测试结果
    with open("yolov5_metrics.txt", "w") as f:
        f.write(f"mAP@0.5: {metrics.box.map50:.4f}\n")
        f.write(f"空缺车位AP@0.5: {metrics.box.ap50[0]:.4f}\n")
        f.write(f"已占用车位AP@0.5: {metrics.box.ap50[1]:.4f}\n")
        f.write(f"Precision: {metrics.box.mp:.4f}\n")
        f.write(f"Recall: {metrics.box.mr:.4f}\n")
    
    print("YOLO5评估完成！关键指标：")
    print(f"mAP@0.5: {metrics.box.map50:.4f}")
    print(f"空缺车位检测AP: {metrics.box.ap50[0]:.4f}")
    print(f"已占用车位检测AP: {metrics.box.ap50[1]:.4f}")
    
    # 保存模型到根目录
    model_path = os.path.join(PROJECT, NAME, "weights", "best.pt")
    if os.path.exists(model_path):
        new_model_path = "yolov5su_new.pt"
        os.system(f"copy {model_path} {new_model_path}")
        print(f"新训练的YOLO5模型已保存为: {new_model_path}")
    
except Exception as e:
    print(f"训练过程中发生错误: {e}")
    import traceback
    traceback.print_exc()