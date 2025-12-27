import torch
from ultralytics import YOLO

# 配置参数
DATA_YAML = 'parking.yaml'
EPOCHS = 50
BATCH_SIZE = 8
IMG_SIZE = 640
DEVICE = 'cpu'
PROJECT = 'parking_train'
NAME = 'yolov5s_parking'

# 加载YOLOv5小型模型
model = YOLO('yolov5s.pt')

# 开始训练
results = model.train(
    data=DATA_YAML,
    epochs=EPOCHS,
    batch=BATCH_SIZE,
    imgsz=IMG_SIZE,
    device=DEVICE,
    project=PROJECT,
    name=NAME,
    save=True,
    val=True
)

# 验证模型
metrics = model.val(data=DATA_YAML, device=DEVICE)

# 保存测试结果
with open('yolov5_metrics.txt', 'w') as f:
    f.write('mAP@0.5: ' + str(metrics.box.map50) + '\n')
    f.write('空缺车位AP@0.5: ' + str(metrics.box.ap50[0]) + '\n')
    f.write('已占用车位AP@0.5: ' + str(metrics.box.ap50[1]) + '\n')
    f.write('Precision: ' + str(metrics.box.mp) + '\n')
    f.write('Recall: ' + str(metrics.box.mr) + '\n')

print('YOLOv5训练完成！')