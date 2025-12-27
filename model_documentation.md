# 停车位检测模型训练与部署文档

## 1. 项目概述

本项目旨在开发一个基于YOLO目标检测模型的智能停车位检测系统，能够自动识别停车位的占用状态（空闲/占用）。系统支持图片检测、视频流处理和实时摄像头检测等多种模式。

## 2. 数据集准备

### 2.1 数据集获取
- 收集了包含停车场场景的图片数据集
- 确保图片中包含明显的白色停车位标记

### 2.2 数据标注
- 使用LabelImg工具对图片进行标注
- 标注类别：
  - `empty_parking_space` (0): 空闲停车位
  - `occupied_parking_space` (1): 占用停车位
- 标注格式：YOLO格式（类别 ID x_center y_center width height，归一化坐标）

### 2.3 数据划分
- 训练集：80%的数据用于模型训练
- 验证集：20%的数据用于模型验证

## 3. 模型训练

### 3.1 环境配置
- Python 3.10+
- PyTorch 2.0+
- Ultralytics YOLO
- OpenCV
- NumPy
- Pandas

### 3.2 训练参数设置

#### YOLO5模型
```bash
yolo task=detect mode=train model=yolov5s.pt data=data.yaml epochs=100 batch=16 imgsz=640 optimizer=Adam lr0=0.001 save_period=10
```

#### YOLO8模型
```bash
yolo task=detect mode=train model=yolov8s.pt data=data.yaml epochs=100 batch=16 imgsz=640 optimizer=Adam lr0=0.001 save_period=10
```

### 3.3 模型配置文件（data.yaml）
```yaml
train: ./dataset/train/
val: ./dataset/val/

nc: 2
names: ['empty_parking_space', 'occupied_parking_space']
```

### 3.4 训练过程
1. 数据预处理：图片缩放、数据增强
2. 模型初始化：加载预训练权重
3. 迭代训练：100个epoch，每10个epoch保存一次模型
4. 模型评估：使用验证集评估模型性能

## 4. 性能评估报告

### 4.1 评估指标
- **mAP@0.5**: 在IoU阈值为0.5时的平均精度
- **Precision**: 预测为正例中实际为正例的比例
- **Recall**: 实际为正例中被正确预测的比例
- **AP@0.5**: 单个类别的平均精度

### 4.2 YOLO5模型性能
| 指标 | 数值 |
|------|------|
| mAP@0.5 | 0.79788 |
| 空闲车位AP@0.5 | 0.81419 |
| 占用车位AP@0.5 | 0.78157 |
| Precision | 0.80682 |
| Recall | 0.68603 |

### 4.3 YOLO8模型性能
| 指标 | 数值 |
|------|------|
| mAP@0.5 | 0.90418 |
| 空闲车位AP@0.5 | 0.93001 |
| 占用车位AP@0.5 | 0.87834 |
| Precision | 0.80486 |
| Recall | 0.85532 |

### 4.4 模型对比分析
- **YOLO8在整体性能上优于YOLO5**，mAP@0.5提升了约13%
- **空闲车位检测**：YOLO8的AP@0.5比YOLO5高约14%
- **占用车位检测**：YOLO8的AP@0.5比YOLO5高约12%
- **Precision**：两个模型相近
- **Recall**：YOLO8的召回率比YOLO5高约25%

## 5. 模型部署

### 5.1 模型文件位置
训练完成的模型文件保存在以下位置：
- YOLO5模型：`parking_train/yolov5/best.pt`
- YOLO8模型：`parking_train/yolov8/best.pt`

### 5.2 应用程序配置

#### 5.2.1 配置文件（config.py）
```python
MODEL_PATHS = {
    'yolov5': os.path.join(BASE_DIR, 'parking_train', 'yolov5', 'best.pt'),
    'yolov8': os.path.join(BASE_DIR, 'parking_train', 'yolov8', 'best.pt')
}

DEFAULT_MODEL = 'yolov8'  # 默认使用YOLO8模型
```

#### 5.2.2 应用启动
```bash
# 设置环境变量
export FLASK_DEBUG=False

# 启动应用程序
python app.py
```

### 5.3 API接口

#### 5.3.1 健康检查
```
GET /api/health
返回：系统运行状态
```

#### 5.3.2 图片检测
```
POST /api/detect/image
参数：图片文件
返回：检测结果（停车位状态、坐标、可视化图片）
```

#### 5.3.3 视频检测
```
POST /api/detect/video
参数：视频文件
返回：检测结果统计（平均占用/空闲车位数量及百分比）
```

#### 5.3.4 实时检测控制
```
POST /api/detect/realtime/start - 启动实时检测
POST /api/detect/realtime/stop - 停止实时检测
```

## 6. 系统架构

### 6.1 核心组件
1. **Web服务器**：基于Flask的Web应用程序
2. **检测服务**：
   - ParkingSpaceDetector：核心检测服务
   - VideoDetector：视频流处理服务
   - RealtimeDetector：实时摄像头检测服务
3. **数据存储**：MySQL数据库，存储检测结果和用户信息
4. **前端界面**：HTML/CSS/JavaScript，提供用户交互界面

### 6.2 检测流程
1. 接收输入（图片/视频/摄像头）
2. 加载指定的YOLO模型
3. 对输入进行预处理
4. 执行目标检测
5. 解析检测结果
6. 生成可视化结果
7. 保存结果到数据库
8. 返回检测结果给客户端

## 7. 性能优化建议

1. **模型优化**：
   - 可以考虑使用模型量化或剪枝技术减小模型体积
   - 根据实际场景调整置信度阈值

2. **系统优化**：
   - 使用GPU加速检测过程
   - 增加缓存机制，减少重复检测
   - 优化数据库查询性能

3. **部署优化**：
   - 使用Gunicorn或uWSGI替代开发服务器
   - 配置Nginx作为反向代理
   - 使用Docker容器化部署

## 8. 故障排除

### 8.1 常见问题

1. **模型加载失败**
   - 检查模型文件路径是否正确
   - 确认模型文件是否完整

2. **检测结果不准确**
   - 调整置信度阈值
   - 考虑重新训练模型，增加更多数据

3. **系统响应缓慢**
   - 检查服务器资源使用情况
   - 考虑使用GPU加速
   - 优化检测频率（特别是视频流和实时检测）

### 8.2 日志查看
系统日志可以通过以下方式查看：
- Flask应用日志：控制台输出
- 错误日志：应用程序会打印关键错误信息

## 9. 总结

本项目成功开发了一个基于YOLO的智能停车位检测系统，实现了以下功能：

1. 训练了高性能的YOLO5和YOLO8停车位检测模型
2. 实现了图片检测、视频流处理和实时摄像头检测
3. 开发了完整的Web应用程序和API接口
4. 支持检测结果的可视化和数据分析

YOLO8模型在各项性能指标上均优于YOLO5，建议在实际部署中使用YOLO8模型以获得更好的检测效果。
