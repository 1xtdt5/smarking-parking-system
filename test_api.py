from flask import Flask, jsonify
import os
import random
from datetime import datetime

app = Flask(__name__)

# API: 获取仪表盘数据
@app.route('/api/get-dashboard-data', methods=['GET'])
def get_dashboard_data():
    try:
        # 模拟实时数据
        total_spaces = 100
        occupied_spaces = random.randint(40, 60)
        vacant_spaces = total_spaces - occupied_spaces
        occupancy_rate = (occupied_spaces / total_spaces) * 100
        
        # 模拟检测状态
        latest_occupied = occupied_spaces
        latest_vacant = vacant_spaces
        latest_detection_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 模拟系统状态
        model_precision = 95.8
        fps = 12.5
        system_load = 45.2
        
        return jsonify({
            'total_spaces': total_spaces,
            'occupied_spaces': occupied_spaces,
            'vacant_spaces': vacant_spaces,
            'occupancy_rate': round(occupancy_rate, 2),
            'latest_occupied': latest_occupied,
            'latest_vacant': latest_vacant,
            'latest_detection_time': latest_detection_time,
            'model_precision': model_precision,
            'fps': fps,
            'system_load': system_load
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API: 获取模型数据
@app.route('/api/model-data', methods=['GET'])
def api_model_data():
    try:
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # 返回更新后的模型数据
        model_data = {
            'models': [
                {
                    'name': 'YOLOv8n-OBB',
                    'version': 'v8.0',
                    'created_at': '2025-12-18',
                    'detection_type': 'OBB检测',
                    'accuracy': 90.418,
                    'status': 'enabled'
                },
                {
                    'name': 'YOLOv5n-OBB',
                    'version': 'v5.0',
                    'created_at': '2025-12-18',
                    'detection_type': 'OBB检测',
                    'accuracy': 79.788,
                    'status': 'loaded'
                },
                {
                    'name': 'YOLO11n-OBB',
                    'version': 'v11.0',
                    'created_at': '2025-12-19',
                    'detection_type': 'OBB检测',
                    'accuracy': 91.2,
                    'status': 'loaded'
                }
            ],
            'performance': {
                'yolov8n_obb': {'accuracy': 90.418, 'inference_time': 140, 'recall': 0.925, 'precision': 0.918},
                'yolov5n_obb': {'accuracy': 79.788, 'inference_time': 125, 'recall': 0.674, 'precision': 0.752},
                'yolo11n_obb': {'accuracy': 91.2, 'inference_time': 135, 'recall': 0.932, 'precision': 0.924}
            },
            'usage': {
                'yolov8n_obb': 60,
                'yolov5n_obb': 15,
                'yolo11n_obb': 25
            }
        }
        
        return jsonify({
            'status': 'success',
            'data': model_data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 健康检查
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Service is healthy'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
