from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from datetime import datetime
import random
import json
import logging

# 设置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 初始化Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# 确保上传文件夹存在
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 模拟数据库
parking_spaces_data = [
    {'id': 1, 'location': 'A区', 'status': 'available', 'vehicle_type': 'car', 'parking_time': ''},
    {'id': 2, 'location': 'B区', 'status': 'occupied', 'vehicle_type': 'car', 'parking_time': '2023-01-01 10:00:00'},
    {'id': 3, 'location': 'C区', 'status': 'available', 'vehicle_type': 'car', 'parking_time': ''},
    {'id': 4, 'location': 'A区', 'status': 'occupied', 'vehicle_type': 'car', 'parking_time': '2023-01-01 10:30:00'},
    {'id': 5, 'location': 'B区', 'status': 'available', 'vehicle_type': 'car', 'parking_time': ''}
]

detection_results = []

# 检查文件扩展名是否被允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# 主页路由
@app.route('/')
def index():
    return render_template('index.html')

# 仪表盘路由
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# API: 获取仪表盘数据
@app.route('/api/get-dashboard-data', methods=['GET'])
def get_dashboard_data():
    try:
        # 模拟实时数据
        total_spaces = 100
        occupied_spaces = random.randint(40, 60)
        available_spaces = total_spaces - occupied_spaces
        detection_count = len(detection_results)
        success_rate = random.uniform(95.0, 99.0)
        system_status = "正常"
        detection_speed = random.uniform(0.05, 0.15)
        car_count = occupied_spaces
        motorcycle_count = random.randint(5, 15)
        truck_count = random.randint(2, 8)
        bicycle_count = random.randint(1, 5)
        real_time_alert = []
        latest_detections = detection_results[-10:] if detection_results else []
        total_vehicles = car_count + motorcycle_count + truck_count + bicycle_count
        detection_rate = random.uniform(90.0, 95.0)

        return jsonify({
            'total_spaces': total_spaces,
            'occupied_spaces': occupied_spaces,
            'available_spaces': available_spaces,
            'detection_count': detection_count,
            'success_rate': round(success_rate, 2),
            'system_status': system_status,
            'detection_speed': round(detection_speed, 3),
            'car_count': car_count,
            'motorcycle_count': motorcycle_count,
            'truck_count': truck_count,
            'bicycle_count': bicycle_count,
            'real_time_alert': real_time_alert,
            'latest_detections': latest_detections,
            'total_vehicles': total_vehicles,
            'detection_rate': round(detection_rate, 2)
        })
    except Exception as e:
        logger.error(f"Error in get_dashboard_data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# API: 获取模型数据
@app.route('/api/model-data', methods=['GET'])
def api_model_data():
    try:
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        model_data = {
            "models": [
                {
                    "name": "YOLOv8n-OBB",
                    "version": "8.0",
                    "created_date": "2023-09-01",
                    "detection_type": "obb",
                    "accuracy": "90.418%",
                    "status": "enabled",
                    "performance": {
                        "inference_time": 0.012,
                        "recall": 0.925,
                        "precision": 0.945
                    }
                },
                {
                    "name": "YOLOv5n-OBB",
                    "version": "1.0",
                    "created_date": "2023-06-15",
                    "detection_type": "obb",
                    "accuracy": "79.788%",
                    "status": "loaded",
                    "performance": {
                        "inference_time": 0.008,
                        "recall": 0.823,
                        "precision": 0.846
                    }
                },
                {
                    "name": "YOLO11n-OBB",
                    "version": "11.0",
                    "created_date": "2023-12-01",
                    "detection_type": "obb",
                    "accuracy": "91.2%",
                    "status": "loaded",
                    "performance": {
                        "inference_time": 0.015,
                        "recall": 0.938,
                        "precision": 0.952
                    }
                }
            ],
            "performance": {
                "total_detections": 15240,
                "average_confidence": 0.873,
                "total_time": 123.56,
                "fps": 123.3
            },
            "usage": {
                "YOLOv8n-OBB": 65,
                "YOLOv5n-OBB": 20,
                "YOLO11n-OBB": 15
            },
            "timestamp": current_date
        }
        return jsonify(model_data)
    except Exception as e:
        logger.error(f"Error in api_model_data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# API: 获取停车位数据
@app.route('/api/parking-spaces', methods=['GET'])
def get_parking_spaces():
    return jsonify(parking_spaces_data)

# API: 更新停车位状态
@app.route('/api/parking-spaces/<int:space_id>', methods=['PUT'])
def update_parking_space(space_id):
    data = request.get_json()
    for space in parking_spaces_data:
        if space['id'] == space_id:
            space['status'] = data['status']
            space['vehicle_type'] = data['vehicle_type']
            space['parking_time'] = data['parking_time'] if data['status'] == 'occupied' else ''
            return jsonify(space)
    return jsonify({'error': 'Parking space not found'}), 404

# 模型数据路由
@app.route('/model-data')
def model_data():
    return render_template('model_data.html')

# 检测历史路由
@app.route('/history')
def history():
    return render_template('history.html')

# 实时检测路由
@app.route('/realtime')
def realtime():
    return render_template('realtime_detection.html')

# 系统设置路由
@app.route('/settings')
def settings():
    return render_template('system_settings.html')

# 数据统计路由
@app.route('/statistics')
def statistics():
    return render_template('data_statistics.html')

# 健康检查路由
@app.route('/health')
def health():
    return jsonify({
        'status': 'UP',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'version': '1.0.0'
    })

# 主程序入口
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
