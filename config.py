# -*- coding: utf-8 -*-
"""
配置文件
"""

import os
import cv2
from pathlib import Path

# 项目根路径
BASE_DIR = Path(__file__).resolve().parent

# 模型路径配置
MODEL_PATHS = {
    'yolov8-obb': os.path.join(BASE_DIR, 'yolov8n-obb.pt'),
    'yolo11-obb': os.path.join(BASE_DIR, 'yolo11n-obb.pt'),
    'yolo11s-obb': os.path.join(BASE_DIR, 'yolo11s-obb.pt'),
    'yolov5': os.path.join(BASE_DIR, 'parking_train/yolov5s_parking/weights/best.pt'),
    'yolov8': os.path.join(BASE_DIR, 'parking_train/yolov8s_parking/weights/best.pt')
}

# 默认模型
DEFAULT_MODEL = 'yolov8'

# 置信度阈值
DEFAULT_CONFIDENCE_THRESHOLD = 0.5

# IOU阈值
DEFAULT_IOU = 0.5

# 类别名称映射
CLASSES = {
    0: 'empty_parking_space',
    1: 'occupied_parking_space'
}

# 中文类别名称映射
CLASSES_CN = {
    0: '空车位',
    1: '已占用车位'
}

# 颜色配置
COLORS = {
    0: (0, 255, 0),  # 绿色 - 空车位
    1: (255, 0, 0)   # 红色 - 已占用车位
}

# 用于可视化的颜色
VIS_COLORS = {
    0: (0, 255, 0),   # 绿色 - 空车位
    1: (255, 0, 0),   # 红色 - 已占用车位
    'text': (255, 255, 255),  # 白色 - 文字
    'background': (0, 0, 0)   # 黑色 - 背景
}

# 字体配置
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
FONT_THICKNESS = 1

# 上传文件配置
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# 数据库配置
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'parking_system',
    'charset': 'utf8mb4'
}

# Flask配置
FLASK_CONFIG = {
    'SECRET_KEY': 'your-secret-key-here',
    'DEBUG': True,
    'TESTING': False,
    'JSON_AS_ASCII': False
}

# 日志配置
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'app.log'),
            'formatter': 'detailed',
            'level': 'DEBUG',
            'encoding': 'utf-8'
        }
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG'
    }
}

def get_color(class_id):
    """
    根据类别ID获取颜色
    :param class_id: 类别ID
    :return: 颜色值 (B, G, R)
    """
    return COLORS.get(class_id, (0, 255, 255))  # 默认黄色
