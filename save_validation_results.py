from ultralytics import YOLO

# 加载优化后的模型
model = YOLO('parking_train/yolov8s_parking_optimized/weights/best.pt')

# 进行验证
results = model.val(data='parking.yaml', device='cpu')

# 保存验证结果到文件
with open('yolov8_metrics_optimized.txt', 'w') as f:
    f.write(f'mAP@0.5: {results.box.map50:.4f}\n')
    f.write(f'mAP@0.5:0.95: {results.box.map:.4f}\n')
    f.write(f'Precision: {results.box.mp:.4f}\n')
    f.write(f'Recall: {results.box.mr:.4f}\n')
    f.write(f'空缺车位AP@0.5: {results.box.ap50[0]:.4f}\n')
    f.write(f'已占用车位AP@0.5: {results.box.ap50[1]:.4f}\n')
    f.write(f'空缺车位AP@0.5:0.95: {results.box.ap[0]:.4f}\n')
    f.write(f'已占用车位AP@0.5:0.95: {results.box.ap[1]:.4f}\n')

print('验证结果已保存到yolov8_metrics_optimized.txt')
print('\n验证结果概览:')
print(f'mAP@0.5: {results.box.map50:.4f}')
print(f'mAP@0.5:0.95: {results.box.map:.4f}')
print(f'Precision: {results.box.mp:.4f}')
print(f'Recall: {results.box.mr:.4f}')
print(f'空缺车位AP@0.5: {results.box.ap50[0]:.4f}')
print(f'已占用车位AP@0.5: {results.box.ap50[1]:.4f}')