import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# 设置工作目录
os.chdir(r'c:\Users\25031\Desktop\parking_system')

# 获取最新的训练结果目录
train_dirs = glob.glob('parking_train/yolov8s_parking*')
train_dirs.sort(key=lambda x: os.path.getmtime(x), reverse=True)

if not train_dirs:
    print("错误：未找到训练结果目录！请先运行训练脚本。")
    exit()

latest_train_dir = train_dirs[0]
print(f"使用最新的训练结果目录: {latest_train_dir}")

# 读取训练结果
results_path = os.path.join(latest_train_dir, 'results.csv')
if not os.path.exists(results_path):
    print(f"错误：训练结果文件 {results_path} 不存在！")
    exit()

results = pd.read_csv(results_path)

# 创建图表
plt.figure(figsize=(15, 12))

# 1. 绘制训练损失曲线
plt.subplot(3, 2, 1)
plt.plot(results['epoch'], results['train/box_loss'], label='Box Loss', color='red', linewidth=2)
plt.plot(results['epoch'], results['train/cls_loss'], label='Class Loss', color='green', linewidth=2)
plt.plot(results['epoch'], results['train/dfl_loss'], label='DFL Loss', color='blue', linewidth=2)
plt.xlabel('Epoch', fontsize=12)
plt.ylabel('Loss', fontsize=12)
plt.title('Training Loss Curves', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# 2. 绘制验证损失曲线
plt.subplot(3, 2, 2)
plt.plot(results['epoch'], results['val/box_loss'], label='Val Box Loss', color='red', linewidth=2)
plt.plot(results['epoch'], results['val/cls_loss'], label='Val Class Loss', color='green', linewidth=2)
plt.plot(results['epoch'], results['val/dfl_loss'], label='Val DFL Loss', color='blue', linewidth=2)
plt.xlabel('Epoch', fontsize=12)
plt.ylabel('Loss', fontsize=12)
plt.title('Validation Loss Curves', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# 3. 绘制mAP曲线
plt.subplot(3, 2, 3)
plt.plot(results['epoch'], results['metrics/mAP50(B)'], label='mAP@0.5', color='purple', linewidth=2)
plt.plot(results['epoch'], results['metrics/mAP50-95(B)'], label='mAP@0.5:0.95', color='orange', linewidth=2)
plt.xlabel('Epoch', fontsize=12)
plt.ylabel('mAP', fontsize=12)
plt.title('Validation mAP Curves', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# 4. 绘制精确率曲线
plt.subplot(3, 2, 4)
plt.plot(results['epoch'], results['metrics/precision(B)'], label='Precision', color='cyan', linewidth=2)
plt.xlabel('Epoch', fontsize=12)
plt.ylabel('Precision', fontsize=12)
plt.title('Validation Precision Curve', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# 5. 绘制召回率曲线
plt.subplot(3, 2, 5)
plt.plot(results['epoch'], results['metrics/recall(B)'], label='Recall', color='magenta', linewidth=2)
plt.xlabel('Epoch', fontsize=12)
plt.ylabel('Recall', fontsize=12)
plt.title('Validation Recall Curve', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# 6. 绘制学习率曲线
plt.subplot(3, 2, 6)
plt.plot(results['epoch'], results['lr/pg0'], label='Learning Rate (PG0)', color='black', linewidth=2)
plt.plot(results['epoch'], results['lr/pg1'], label='Learning Rate (PG1)', color='gray', linewidth=2, linestyle='--')
plt.plot(results['epoch'], results['lr/pg2'], label='Learning Rate (PG2)', color='lightgray', linewidth=2, linestyle=':')
plt.xlabel('Epoch', fontsize=12)
plt.ylabel('Learning Rate', fontsize=12)
plt.title('Learning Rate Curves', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# 保存图表
plt.tight_layout()
output_path = os.path.join(latest_train_dir, 'training_curves.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"训练过程可视化完成！")
print(f"图表已保存至: {output_path}")

# 打印关键训练信息
print("\n训练关键信息总结：")
print(f"总训练轮数: {results['epoch'].max() + 1}")
print(f"最佳mAP@0.5: {results['metrics/mAP50(B)'].max():.4f} (第{results['metrics/mAP50(B)'].idxmax() + 1}轮)")
print(f"最佳mAP@0.5:0.95: {results['metrics/mAP50-95(B)'].max():.4f} (第{results['metrics/mAP50-95(B)'].idxmax() + 1}轮)")
print(f"最终训练Box Loss: {results['train/box_loss'].iloc[-1]:.4f}")
print(f"最终验证Box Loss: {results['val/box_loss'].iloc[-1]:.4f}")

# 检查是否生成了评估指标文件
metrics_file = 'yolov8_metrics.txt'
if os.path.exists(metrics_file):
    print(f"\n评估指标文件 {metrics_file} 内容：")
    with open(metrics_file, 'r') as f:
        print(f.read())