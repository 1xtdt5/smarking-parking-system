import torch
import os
from ultralytics import YOLO

# 设置工作目录为当前目录
os.chdir(r'c:\Users\25031\Desktop\parking_system')

# 配置参数（与YOLOv5保持一致，保证对比公平）
DATA_YAML = "parking.yaml"  # 使用当前目录下的parking.yaml
EPOCHS = 50  # 训练轮数
BATCH_SIZE = 12  # 优化批次大小（根据CPU内存调整）
IMG_SIZE = 640  # 输入图片尺寸
DEVICE = "cpu"  # CPU训练
PROJECT = "parking_train"
NAME = "yolov8s_parking_optimized"

# 优化后的超参数配置
HYP_PARAMS = {
    "lr0": 0.005,  # 优化初始学习率（略低以提高稳定性）
    "weight_decay": 0.0005,  # 权重衰减
    "momentum": 0.937,  # 动量
    "lrf": 0.001,  # 最终学习率缩放因子（配合余弦退火使用）
    "warmup_epochs": 3.0,  # 预热轮数
    "warmup_momentum": 0.8,  # 预热动量
    "warmup_bias_lr": 0.1,  # 预热偏置学习率
}

# 增强的数据增强策略
AUGMENT_PARAMS = {
    "flipud": 0.0,  # 上下翻转概率（保持不变，车位通常不会上下颠倒）
    "fliplr": 0.7,  # 左右翻转概率（增强至0.7）
    "degrees": 10.0,  # 旋转角度（增强至10度）
    "scale": 0.7,  # 缩放比例（增强至0.7）
    "shear": 5.0,  # 剪切角度（新增5度剪切）
    "translate": 0.15,  # 平移比例（增强至0.15）
    "perspective": 0.001,  # 透视变换概率（新增轻微透视变换）
    "hsv_h": 0.02,  # 色相调整（增强至0.02）
    "hsv_s": 0.8,  # 饱和度调整（增强至0.8）
    "hsv_v": 0.5,  # 亮度调整（增强至0.5）
    "mosaic": 1.0,  # 马赛克增强（新增，值为1.0表示启用）
    "mixup": 0.1,  # MixUp增强（新增，轻微混合图像）
}

# 调整后的目标函数配置
LOSS_PARAMS = {
    "box": 8.0,  # 边界框损失权重（增加至8.0，提高定位精度）
    "cls": 0.75,  # 分类损失权重（增加至0.75，提高分类精度）
    "dfl": 1.5,  # 分布焦点损失权重（保持不变）
}

# 早停配置
EARLY_STOP_PARAMS = {
    "patience": 10,  # 早停耐心值：10轮没有改进则停止
    "min_delta": 0.001  # 最小改进阈值
}

print("开始训练优化后的YOLO8模型...")
# 加载YOLO8模型
model_v8 = YOLO("yolov8s.pt")

# 开始训练
try:
    results_v8 = model_v8.train(
        data=DATA_YAML,
        epochs=EPOCHS,
        batch=BATCH_SIZE,
        imgsz=IMG_SIZE,
        device=DEVICE,
        project=PROJECT,
        name=NAME,
        save=True,  # 保存模型
        val=True,    # 训练中验证
        # 超参数配置
        lr0=HYP_PARAMS["lr0"],
        weight_decay=HYP_PARAMS["weight_decay"],
        momentum=HYP_PARAMS["momentum"],
        lrf=HYP_PARAMS["lrf"],
        warmup_epochs=HYP_PARAMS["warmup_epochs"],
        warmup_momentum=HYP_PARAMS["warmup_momentum"],
        warmup_bias_lr=HYP_PARAMS["warmup_bias_lr"],
        # 余弦退火学习率
        cos_lr=True,  # 启用余弦退火学习率调度器
        # 数据增强策略
        flipud=AUGMENT_PARAMS["flipud"],
        fliplr=AUGMENT_PARAMS["fliplr"],
        degrees=AUGMENT_PARAMS["degrees"],
        scale=AUGMENT_PARAMS["scale"],
        shear=AUGMENT_PARAMS["shear"],
        translate=AUGMENT_PARAMS["translate"],
        perspective=AUGMENT_PARAMS["perspective"],
        hsv_h=AUGMENT_PARAMS["hsv_h"],
        hsv_s=AUGMENT_PARAMS["hsv_s"],
        hsv_v=AUGMENT_PARAMS["hsv_v"],
        mosaic=AUGMENT_PARAMS["mosaic"],
        mixup=AUGMENT_PARAMS["mixup"],
        # 目标函数配置
        box=LOSS_PARAMS["box"],
        cls=LOSS_PARAMS["cls"],
        dfl=LOSS_PARAMS["dfl"],
        # 早停功能
        patience=EARLY_STOP_PARAMS["patience"],
        # 评估指标配置
        conf=0.25,  # 置信度阈值
        iou=0.6,    # IoU阈值
    )
    print("优化后的YOLO8训练完成!")
    
    # 验证模型（输出关键指标）
    print("开始评估优化后的YOLO8模型...")
    metrics_v8 = model_v8.val(data=DATA_YAML, device=DEVICE)
    
    # 保存测试结果
    with open("yolov8_metrics_optimized.txt", "w") as f:
        f.write(f"mAP@0.5: {metrics_v8.box.map50:.4f}\n")
        f.write(f"mAP@0.5:0.95: {metrics_v8.box.map:.4f}\n")
        f.write(f"空缺车位AP@0.5: {metrics_v8.box.ap50[0]:.4f}\n")
        f.write(f"已占用车位AP@0.5: {metrics_v8.box.ap50[1]:.4f}\n")
        f.write(f"空缺车位AP@0.5:0.95: {metrics_v8.box.ap[0]:.4f}\n")
        f.write(f"已占用车位AP@0.5:0.95: {metrics_v8.box.ap[1]:.4f}\n")
        f.write(f"Precision: {metrics_v8.box.mp:.4f}\n")
        f.write(f"Recall: {metrics_v8.box.mr:.4f}\n")
    
    print("优化后的YOLO8评估完成！关键指标：")
    print(f"mAP@0.5: {metrics_v8.box.map50:.4f}")
    print(f"mAP@0.5:0.95: {metrics_v8.box.map:.4f}")
    print(f"空缺车位AP@0.5: {metrics_v8.box.ap50[0]:.4f}")
    print(f"已占用车位AP@0.5: {metrics_v8.box.ap50[1]:.4f}")
    print(f"空缺车位AP@0.5:0.95: {metrics_v8.box.ap[0]:.4f}")
    print(f"已占用车位AP@0.5:0.95: {metrics_v8.box.ap[1]:.4f}")
    print(f"Precision: {metrics_v8.box.mp:.4f}")
    print(f"Recall: {metrics_v8.box.mr:.4f}")
    
    # 复制最佳模型到当前目录
    model_path = os.path.join(PROJECT, NAME, "weights", "best.pt")
    if os.path.exists(model_path):
        new_model_path = "yolov8s_optimized.pt"
        os.system(f"copy {model_path} {new_model_path}")
        print(f"优化后的YOLO8最佳模型已保存为: {new_model_path}")

# 复制最后一次训练的模型到当前目录
    last_model_path = os.path.join(PROJECT, NAME, "weights", "last.pt")
    if os.path.exists(last_model_path):
        new_last_model_path = "yolov8s_optimized_last.pt"
        os.system(f"copy {last_model_path} {new_last_model_path}")
        print(f"优化后的YOLO8最后一次训练模型已保存为: {new_last_model_path}")
    
except Exception as e:
    print(f"训练过程中发生错误: {e}")
    import traceback
    traceback.print_exc()