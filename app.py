from flask import Flask, request, jsonify, render_template, flash, redirect
from flask_cors import CORS
import os
import base64
from datetime import datetime
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 导入数据库操作模�?
from db_manager import DBManager

# 导入YOLO模型和检测相关函�?
from ultralytics import YOLO
import cv2
import numpy as np

# 配置应用
app = Flask(__name__, template_folder='templates')
CORS(app)  # 允许跨域请求
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-me')  # 添加密钥用于flash消息

# 添加路由来提供HTML文件
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/index.html')
def index_html():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard.html')
def dashboard_html():
    return render_template('dashboard.html')

@app.route('/test.html')
def test_html():
    return render_template('login.html')

# 图像检测页面路�?
@app.route('/detect')
def detect_page():
    return render_template('image_detection.html')

# 视频检测页面路�?
@app.route('/video-detect')
def video_detect_page():
    return render_template('video_detection.html')

# 实时监测页面路由
@app.route('/realtime-detect')
def realtime_detect_page():
    return render_template('realtime_detection.html')

# 模型数据页面路由
@app.route('/model-data')
def model_data_page():
    from datetime import datetime
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('model_data.html', current_date=current_date)

# 用户管理页面路由
@app.route('/user-management')
def user_management_page():
    # 检查是否为管理�?
    username = request.args.get('username')
    password = request.args.get('password')
    
    try:
        db = DBManager()
        user = db.get_user_by_username(username)
        
        if not user or not db.verify_password(password, user['password']):
            return jsonify({'success': False, 'message': '用户验证失败'}), 401
        
        if user['role'] != 'admin':
            return jsonify({'success': False, 'message': '只有管理员可以访问此页面'}), 403
        
        # 获取所有用户列�?
        users = db.get_all_users()
        
        return render_template('user_management.html', users=users, current_user=username)
        
    except Exception as e:
        print(f"访问用户管理页面失败: {e}")
        return jsonify({'success': False, 'message': '访问失败，请稍后重试'}), 500

# 注册页面路由
@app.route('/register')
def register_page():
    return render_template('register.html')

# 注册表单处理路由
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    
    # 基本验证
    if not username or not password or not confirm_password:
        flash('请填写所有必填字段', 'danger')
        return redirect('/register')
    
    if password != confirm_password:
        flash('两次输入的密码不一致', 'danger')
        return redirect('/register')
    
    if len(username) < 3 or len(username) > 20:
        flash('用户名长度应在3-20个字符之间', 'danger')
        return redirect('/register')
    
    if len(password) < 8:
        flash('密码长度至少8个字符', 'danger')
        return redirect('/register')
    
    # 检查密码是否包含字母和数字
    if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        flash('密码必须包含字母和数字', 'danger')
        return redirect('/register')
    
    # 调用数据库方法注册用户
    try:
        db = DBManager()
        success, message = db.register_user(username, password)
        
        if success:
            flash('注册成功，请登录', 'success')
            return redirect('/')
        else:
            flash(message, 'danger')
            return redirect('/register')
    except Exception as e:
        flash(f'注册失败: {str(e)}', 'danger')
        return redirect('/register')

# 文件上传配置
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff', 'webp'}  # 添加更多图像格式支持
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 33554432))  # 增加�?2MB

# 创建上传目录（如果不存在�?
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 辅助函数：检查文件扩展名是否允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 辅助函数：自适应图像尺寸处理
def preprocess_image(image_path, max_size=1920):
    """
    预处理图像，自适应调整大尺寸图�?
    
    参数:
        image_path: 图像路径
        max_size: 最大尺寸（宽度或高度）
        
    返回:
        处理后的图像路径（如果调整了尺寸，返回临时文件路径）
    """
    import cv2
    import os
    import tempfile
    
    try:
        img = cv2.imread(image_path)
        if img is None:
            return image_path
        
        h, w = img.shape[:2]
        scale = min(max_size/w, max_size/h)
        
        # 如果需要调整尺�?
        if scale < 1:
            new_w = int(w * scale)
            new_h = int(h * scale)
            # 使用INTER_LINEAR插值保持图像质�?
            resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
            
            # 保存到临时文�?
            base_name = os.path.basename(image_path)
            temp_file = tempfile.NamedTemporaryFile(suffix=os.path.splitext(base_name)[1], delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            cv2.imwrite(temp_path, resized_img)
            return temp_path
        
        return image_path
    except Exception as e:
        print(f"图像预处理失�? {e}")
        return image_path

# 模型配置
MODEL_PATHS = {
    'yolov5su': os.environ.get('YOLOV5SU_MODEL_PATH', 'yolov5su.pt'),
    'yolov8s': os.environ.get('YOLOV8S_MODEL_PATH', 'yolov8s.pt'),
    'yolov8n': os.environ.get('YOLOV8N_MODEL_PATH', 'yolov8n.pt'),
    'custom': os.environ.get('CUSTOM_MODEL_PATH', 'yolov8s_new.pt'),  # 更新默认自定义模型为优化后的版本
    'yolo11n-obb': os.environ.get('YOLO11N_OBB_MODEL_PATH', 'yolo11n-obb.pt'),
    'yolov8n-obb': os.environ.get('YOLOV8N_OBB_MODEL_PATH', 'yolov8n.pt')
}

# 类别名称
CLASS_NAMES = {
    0: 'empty_parking_space',
    1: 'occupied_parking_space'
}

# 全局模型变量
global_models = {}

# 辅助函数：检查文件扩展名是否允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 辅助函数：加载YOLO模型
def load_model(model_version):
    model_path = MODEL_PATHS.get(model_version)
    if not model_path or not os.path.exists(model_path):
        return None
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        print(f"加载模型失败: {e}")
        return None

# 系统启动时预加载默认模型
def preload_models():
    """
    系统启动时预加载常用模型，提高检测速度
    """
    global global_models
    default_models = ['custom', 'yolov8s']  # 预加载优化后的自定义模型和yolov8s
    
    for model_version in default_models:
        if model_version not in global_models or global_models[model_version] is None:
            model = load_model(model_version)
            if model:
                global_models[model_version] = model
                print(f"�?预加载模型成�? {model_version}")
            else:
                print(f"�?预加载模型失�? {model_version}")

# 在应用启动时预加载模�?
preload_models()

# 辅助函数：解析YOLO模型输出
def parse_yolo_output(results, image_path):
    detection = results[0]
    boxes = detection.boxes
    
    detection_boxes = []
    empty_count = 0
    occupied_count = 0
    vehicle_count = 0
    
    # 只读取一次图像尺寸，避免重复IO操作
    img_height, img_width = detection.orig_shape[:2]
    
    # 批量处理边界框，减少循环开销
    for i in range(len(boxes)):
        box = boxes[i]
        class_id = int(box.cls.item())
        class_name = CLASS_NAMES.get(class_id, f'class_{class_id}')
        
        # 直接获取边界框坐标，避免多次调用item()
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        confidence = float(box.conf.item())
        
        # 边界框有效性检�?
        if x1 >= x2 or y1 >= y2:
            continue
            
        # 坐标范围检�?
        x1 = max(0, min(x1, img_width))
        y1 = max(0, min(y1, img_height))
        x2 = max(0, min(x2, img_width))
        y2 = max(0, min(y2, img_height))
        
        detection_box = {
            'class_id': class_id,
            'class_name': class_name,
            'x1': x1,  # 减少不必要的精度，提高传输速度
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'confidence': round(confidence, 3),  # 减少精度，提高传输速度
            'width': x2 - x1,
            'height': y2 - y1
        }
        
        detection_boxes.append(detection_box)
        
        # 更新计数�?
        if class_id == 0:
            empty_count += 1
        elif class_id == 1:
            occupied_count += 1
            vehicle_count += 1
    
    detection_summary = {
        'total_boxes': len(detection_boxes),
        'empty_count': empty_count,
        'occupied_count': occupied_count,
        'vehicle_count': vehicle_count,
        'image_width': img_width,
        'image_height': img_height,
        # 添加前端期望的字段名称以解决显示问题
        'vacant_count': empty_count,
        'total_spaces': len(detection_boxes)
    }
    
    return detection_boxes, detection_summary

# API路由

# 健康检查API
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'success': True,
        'message': '系统运行正常',
        'timestamp': datetime.now().isoformat()
    })

# 用户注册API
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    
    # 基本验证
    if not username or not password or not confirm_password:
        return jsonify({'success': False, 'message': '请填写所有必填字段'}), 400
    
    if password != confirm_password:
        return jsonify({'success': False, 'message': '两次输入的密码不一致'}), 400
    
    if len(username) < 3 or len(username) > 20:
        return jsonify({'success': False, 'message': '用户名长度应在3-20个字符之间'}), 400
    
    if len(password) < 8:
        return jsonify({'success': False, 'message': '密码长度至少8个字符'}), 400
    
    # 检查密码是否包含字母和数字
    if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        return jsonify({'success': False, 'message': '密码必须包含字母和数字'}), 400
    
    # 调用数据库方法注册用户
    try:
        db = DBManager()
        success, message = db.register_user(username, password)
        
        if success:
            return jsonify({'success': True, 'message': '注册成功，请登录'})
        else:
            return jsonify({'success': False, 'message': message}), 400
    except Exception as e:
        print(f'注册失败: {str(e)}')
        return jsonify({'success': False, 'message': f'注册失败: {str(e)}'}), 500

# 用户登录API
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400
    
    try:
        db = DBManager()
        user = db.get_user_by_username(username)
        
        if not user or not db.verify_password(password, user['password']):
            return jsonify({'success': False, 'message': '密码错误'}), 401
        
        # 返回用户信息（不包含密码�?
        user_info = {
            'id': user['id'],
            'username': user['username'],
            'role': user['role']
        }
        
        return jsonify({'success': True, 'user': user_info})
        
    except Exception as e:
        print(f"登录失败: {e}")
        return jsonify({'success': False, 'message': '登录失败，请稍后重试'}), 500

# 获取仪表盘数据API
@app.route('/api/get-dashboard-data', methods=['GET'])
def get_dashboard_data():
    try:
        db = DBManager()
        
        # 获取最新的检测结�?
        latest_results = db.get_detection_results(limit=1, offset=0)
        latest_detection = latest_results[0] if latest_results else None
        
        # 获取最新的检测框
        if latest_detection:
            detection_boxes = db.get_detection_boxes_by_result_id(latest_detection['id'])
        else:
            detection_boxes = []
        
        # 计算统计数据
        if latest_detection:
            total_spaces = latest_detection.get('total_boxes', 0)
            occupied_spaces = latest_detection.get('occupied_count', 0)
            vacant_spaces = latest_detection.get('empty_count', 0)
            occupancy_rate = round((occupied_spaces / total_spaces * 100) if total_spaces > 0 else 0, 2)
        else:
            total_spaces = 0
            occupied_spaces = 0
            vacant_spaces = 0
            occupancy_rate = 0
        
        # 获取系统状态数�?
        model_precision = 95.8  # 模拟数据，实际应从模型中获取
        fps = 12  # 模拟数据
        system_load = 45  # 模拟数据
        
        # 获取最新检测时�?
        latest_detection_time = '暂无数据'
        if latest_detection and 'created_at' in latest_detection:
            try:
                if hasattr(latest_detection['created_at'], 'strftime'):
                    latest_detection_time = latest_detection['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                else:
                    latest_detection_time = str(latest_detection['created_at'])
            except Exception as e:
                print(f"格式化日期失�? {e}")
        
        # 构造仪表盘数据
        dashboard_data = {
            'total_spaces': total_spaces,
            'occupied_spaces': occupied_spaces,
            'vacant_spaces': vacant_spaces,
            'occupancy_rate': occupancy_rate,
            'latest_occupied': occupied_spaces,
            'latest_vacant': vacant_spaces,
            'latest_detection_time': latest_detection_time,
            'model_precision': model_precision,
            'fps': fps,
            'system_load': system_load
        }
        
        return jsonify(dashboard_data)
        
    except Exception as e:
        print(f"获取仪表盘数据失�? {e}")
        # 返回默认数据
        return jsonify({
            'total_spaces': 0,
            'occupied_spaces': 0,
            'vacant_spaces': 0,
            'occupancy_rate': 0,
            'latest_occupied': 0,
            'latest_vacant': 0,
            'latest_detection_time': '暂无数据',
            'model_precision': 95.8,
            'fps': 12,
            'system_load': 45
        })

# 用户登出API
@app.route('/api/logout', methods=['POST'])
def logout_api():
    # 由于当前没有使用会话或令牌机制，登出只需返回成功响应
    return jsonify({'success': True, 'message': '登出成功'})

# Web界面登出路由
@app.route('/logout')
def logout():
    # 重定向到登录页面
    return redirect('/')

# 添加用户API
@app.route('/api/add-user', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    admin_username = data.get('admin_username')
    admin_password = data.get('admin_password')
    
    try:
        db = DBManager()
        
        # 验证管理员身份
        admin = db.get_user_by_username(admin_username)
        if not admin or not db.verify_password(admin_password, admin['password']):
            return jsonify({'success': False, 'message': '管理员验证失败'}), 401
        
        if admin['role'] != 'admin':
            return jsonify({'success': False, 'message': '只有管理员可以添加用户'}), 403
        
        # 验证用户输入
        if not username or not password or not confirm_password:
            return jsonify({'success': False, 'message': '请填写所有必填字段'}), 400
        
        if password != confirm_password:
            return jsonify({'success': False, 'message': '两次输入的密码不一致'}), 400
        
        if len(username) < 3 or len(username) > 20:
            return jsonify({'success': False, 'message': '用户名长度应在3-20个字符之间'}), 400
        
        if len(password) < 8:
            return jsonify({'success': False, 'message': '密码长度至少8个字符'}), 400
        
        # 检查密码是否包含字母和数字
        if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            return jsonify({'success': False, 'message': '密码必须包含字母和数字'}), 400
        
        # 添加新用户（默认角色为operator）
        success, message = db.register_user(username, password, role='operator')
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'message': message}), 400
            
    except Exception as e:
        print(f"添加用户失败: {e}")
        return jsonify({'success': False, 'message': '添加用户失败，请稍后重试'}), 500

# 删除用户API
@app.route('/api/delete-user', methods=['POST'])
def delete_user():
    data = request.get_json()
    user_id = data.get('user_id')
    admin_username = data.get('admin_username')
    admin_password = data.get('admin_password')
    
    try:
        db = DBManager()
        
        # 验证管理员身份
        admin = db.get_user_by_username(admin_username)
        if not admin or not db.verify_password(admin_password, admin['password']):
            return jsonify({'success': False, 'message': '管理员验证失败'}), 401
        
        if admin['role'] != 'admin':
            return jsonify({'success': False, 'message': '只有管理员可以删除用户'}), 403
        
        # 删除用户
        success, message = db.delete_user(user_id)
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'message': message}), 400
            
    except Exception as e:
        print(f"删除用户失败: {e}")
        return jsonify({'success': False, 'message': '删除用户失败，请稍后重试'}), 500

# 获取用户列表API
@app.route('/api/get-users', methods=['GET'])
def get_users():
    admin_username = request.args.get('admin_username')
    admin_password = request.args.get('admin_password')
    
    try:
        db = DBManager()
        
        # 验证管理员身份
        admin = db.get_user_by_username(admin_username)
        if not admin or not db.verify_password(admin_password, admin['password']):
            return jsonify({'success': False, 'message': '管理员验证失败'}), 401
        
        if admin['role'] != 'admin':
            return jsonify({'success': False, 'message': '只有管理员可以访问此接口'}), 403
        
        # 获取所有用户列表
        users = db.get_all_users()
        
        # 转换日期格式
        for user in users:
            if hasattr(user['created_at'], 'strftime'):
                user['created_at'] = user['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            
        return jsonify({'success': True, 'users': users})
            
    except Exception as e:
        print(f"获取用户列表失败: {e}")
        return jsonify({'success': False, 'message': '获取用户列表失败，请稍后重试'}), 500

# 获取当前用户信息API
@app.route('/api/user', methods=['GET'])
def get_current_user():
    username = request.args.get('username')
    password = request.args.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400
    
    try:
        db = DBManager()
        user = db.get_user_by_username(username)
        
        if not user or not db.verify_password(password, user['password']):
            return jsonify({'success': False, 'message': '用户验证失败'}), 401
        
        # 返回用户信息（不包含密码�?
        user_info = {
            'id': user['id'],
            'username': user['username'],
            'role': user['role']
        }
        
        return jsonify({'success': True, 'user': user_info})
        
    except Exception as e:
        print(f"获取用户信息失败: {e}")
        return jsonify({'success': False, 'message': '获取用户信息失败，请稍后重试'}), 500

# 获取停车统计信息API
@app.route('/api/stats', methods=['GET'])
def get_parking_stats():
    username = request.args.get('username')
    password = request.args.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400
    
    try:
        db = DBManager()
        user = db.get_user_by_username(username)
        
        if not user or not db.verify_password(user['password']):
            return jsonify({'success': False, 'message': '用户验证失败'}), 401
        
        # 获取统计数据
        # 由于目前没有专门的停车位表，我们从检测结果中获取最新的统计信息
        try:
            # 获取最新的检测结�?
            latest_results = db.get_detection_results(limit=1, offset=0)
            
            if latest_results:
                latest_result = latest_results[0]
                total_spaces = latest_result['total_boxes']
                empty_count = latest_result['empty_count']
                occupied_count = latest_result['occupied_count']
                vehicle_count = latest_result['vehicle_count']
            else:
                # 如果没有检测结果，返回默认�?
                total_spaces = 0
                empty_count = 0
                occupied_count = 0
                vehicle_count = 0
            
            # 计算占用�?
            occupancy_rate = round((occupied_count / total_spaces * 100) if total_spaces > 0 else 0, 2)
            
            # 构造统计数�?
            stats = {
                'total_spaces': total_spaces,
                'empty_count': empty_count,
                'occupied_count': occupied_count,
                'vehicle_count': vehicle_count,
                'occupancy_rate': occupancy_rate,
                'last_updated': latest_result['created_at'] if latest_results else None
            }
            
            return jsonify({'success': True, 'data': stats})
            
        except Exception as stats_error:
            print(f"获取统计数据失败: {stats_error}")
            # 如果获取统计数据失败，返回默认统计信�?
            return jsonify({
                'success': True,
                'data': {
                    'total_spaces': 0,
                    'empty_count': 0,
                    'occupied_count': 0,
                    'vehicle_count': 0,
                    'occupancy_rate': 0,
                    'last_updated': None
                }
            })
            
    except Exception as e:
        print(f"获取停车统计信息失败: {e}")
        return jsonify({'success': False, 'message': '获取停车统计信息失败，请稍后重试'}), 500

# 获取所有停车位信息API
@app.route('/api/spaces', methods=['GET'])
def get_parking_spaces():
    username = request.args.get('username')
    password = request.args.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400
    
    try:
        db = DBManager()
        user = db.get_user_by_username(username)
        
        if not user or not db.verify_password(password, user['password']):
            return jsonify({'success': False, 'message': '用户验证失败'}), 401
        
        # 获取最新的检测结果中的停车位信息
        try:
            # 获取最新的检测结�?
            latest_results = db.get_detection_results(limit=1, offset=0)
            
            if latest_results:
                latest_result = latest_results[0]
                # 获取该检测结果的所有检测框（停车位�?
                detection_boxes = db.get_detection_boxes_by_result_id(latest_result['id'])
                
                # 转换为停车位格式
                parking_spaces = []
                for i, box in enumerate(detection_boxes):
                    space_status = 'available' if box['class_id'] == 0 else 'occupied'
                    parking_spaces.append({
                        'id': i + 1,  # 使用索引作为临时ID
                        'space_id': i + 1,
                        'status': space_status,
                        'coordinates': {
                            'x1': box['x1'],
                            'y1': box['y1'],
                            'x2': box['x2'],
                            'y2': box['y2']
                        },
                        'confidence': box['confidence'],
                        'last_updated': latest_result['created_at']
                    })
            else:
                # 如果没有检测结果，返回空列�?
                parking_spaces = []
            
            return jsonify({'success': True, 'data': parking_spaces})
            
        except Exception as spaces_error:
            print(f"获取停车位信息失败: {spaces_error}")
            return jsonify({'success': True, 'data': []})
            
    except Exception as e:
        print(f"获取停车位信息失败: {e}")
        return jsonify({'success': False, 'message': '获取停车位信息失败，请稍后重试'}), 500

# 更新停车位信息API
@app.route('/api/spaces/<int:space_id>', methods=['PUT'])
def update_parking_space(space_id):
    username = request.args.get('username')
    password = request.args.get('password')
    data = request.get_json()
    
    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400
    
    if not data:
        return jsonify({'success': False, 'message': '更新数据不能为空'}), 400
    
    try:
        db = DBManager()
        user = db.get_user_by_username(username)
        
        if not user or not db.verify_password(password, user['password']):
            return jsonify({'success': False, 'message': '用户验证失败'}), 401
        
        # 由于目前没有专门的停车位表，更新功能暂时不可�?
        # 这里只做简单的响应
        return jsonify({'success': True, 'message': '停车位信息更新功能正在开发中'})
        
    except Exception as e:
        print(f"更新停车位信息失败: {e}")
        return jsonify({'success': False, 'message': '更新停车位信息失败，请稍后重试'}), 500

# 停车检测API
@app.route('/api/detect', methods=['POST'])
def detect():
    # 获取请求参数
    username = request.form.get('username')
    password = request.form.get('password')
    model_version = request.form.get('model_version', 'yolov8s')  # 将默认模型改为yolov8s
    conf_threshold = float(request.form.get('conf_threshold', 0.5))
    
    # 验证用户身份
    try:
        db = DBManager()
        user = db.get_user_by_username(username)
        
        if not user or not db.verify_password(password, user['password']):
            return jsonify({'success': False, 'message': '用户验证失败'}), 401
    except Exception as e:
        print(f"用户验证失败: {e}")
        return jsonify({'success': False, 'message': '用户验证失败'}), 500
    
    # 检查是否有图片上传
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': '没有上传图片'}), 400
    
    image = request.files['image']
    
    if image.filename == '':
        return jsonify({'success': False, 'message': '没有选择图片'}), 400
    
    if not allowed_file(image.filename):
        return jsonify({'success': False, 'message': '不支持的图片格式'}), 400
    
    # 保存上传的图�?
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{image.filename}"
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)
    
    # 预处理图像，自适应调整大尺寸图�?
    processed_image_path = preprocess_image(image_path)
    is_temp_file = processed_image_path != image_path
    
    # 加载YOLO模型
    global global_models
    if model_version in global_models and global_models[model_version] is not None:
        model = global_models[model_version]
        print(f"�?使用预加载模�? {model_version}")
    else:
        model = load_model(model_version)
        if model:
            global_models[model_version] = model
            print(f"�?动态加载模�? {model_version}")
        else:
            # 清理上传的图片和临时文件
            if os.path.exists(image_path):
                os.remove(image_path)
            if is_temp_file and os.path.exists(processed_image_path):
                os.remove(processed_image_path)
            return jsonify({'success': False, 'message': f'加载{model_version}模型失败'}), 500
    
    try:
        # 执行检测，添加优化参数提高推理速度
        results = model(processed_image_path, 
                       conf=conf_threshold, 
                       verbose=False, 
                       iou=0.45,  # 设置IOU阈值，减少重复检�?
                       max_det=1000,  # 限制最大检测框数量
                       agnostic_nms=True,  # 使用类别无关的NMS，提高速度
                       device='cpu')  # 根据实际硬件配置选择
        
        # 解析检测结�?
        detection_boxes, detection_summary = parse_yolo_output(results, processed_image_path)
        
        # 可视化检测结�?
        result_image = results[0].plot()
        
        # 保存可视化结�?
        result_filename = f"result_{filename}"
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
        cv2.imwrite(result_path, result_image)
        
        # 将可视化结果转换为base64编码
        _, buffer = cv2.imencode('.jpg', result_image)
        result_base64 = base64.b64encode(buffer).decode('utf-8')
        visualization = f"data:image/jpeg;base64,{result_base64}"
        
        # 保存检测结果到数据库
        db = DBManager()
        success, result_id = db.save_detection_result(
            image_path,  # 保存原始图像路径
            detection_summary['vehicle_count'],
            model_version,
            user['id'],
            detection_boxes
        )
        
        if not success:
            return jsonify({'success': False, 'message': '保存检测结果失败'}), 500
        
        # 返回检测结果
        return jsonify({
            'success': True,
            'data': {
                'result_id': result_id,
                'image_path': image_path,
                'model_version': model_version,
                'summary': detection_summary,
                'boxes': detection_boxes,
                'visualization': visualization
            }
        })
        
    except Exception as e:
        print(f"检测失败: {e}")
        # 清理上传的图片和临时文件
        if os.path.exists(image_path):
            os.remove(image_path)
        if is_temp_file and os.path.exists(processed_image_path):
            os.remove(processed_image_path)
        return jsonify({'success': False, 'message': '检测失败，请稍后重试'}), 500
    finally:
        # 清理临时文件
        if is_temp_file and os.path.exists(processed_image_path):
            os.remove(processed_image_path)

# 获取检测结果列表API
@app.route('/api/detection-results', methods=['GET'])
def get_detection_results():
    username = request.args.get('username')
    password = request.args.get('password')
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))
    
    # 验证用户身份
    try:
        db = DBManager()
        user = db.get_user_by_username(username)
        
        if not user or not db.verify_password(password, user['password']):
            return jsonify({'success': False, 'message': '用户验证失败'}), 401
    except Exception as e:
        print(f"用户验证失败: {e}")
        return jsonify({'success': False, 'message': '用户验证失败'}), 500
    
    try:
        db = DBManager()
        results = db.get_detection_results(limit, offset)
        
        # 处理结果，添加可视化数据
        for result in results:
            result['summary'] = {
                'total_boxes': result['total_boxes'],
                'empty_count': result['empty_count'],
                'occupied_count': result['occupied_count'],
                'vehicle_count': result['vehicle_count'],
                # 添加前端期望的字段名称以解决显示问题
                'vacant_count': result['empty_count'],
                'total_spaces': result['total_boxes']
            }
        
        return jsonify({'success': True, 'data': results})
        
    except Exception as e:
        print(f"获取检测结果失�? {e}")
        return jsonify({'success': False, 'message': '获取检测结果失败，请稍后重试'}), 500

# 图片检测API（兼容前�?api/detect/image调用�?
@app.route('/api/detect/image', methods=['POST'])
def detect_image():
    # 直接调用现有的detect函数处理请求
    return detect()

# 获取检测框信息API
@app.route('/api/detection-boxes/<int:result_id>', methods=['GET'])
def get_detection_boxes(result_id):
    username = request.args.get('username')
    password = request.args.get('password')
    
    # 验证用户身份
    try:
        db = DBManager()
        user = db.get_user_by_username(username)
        
        if not user or not db.verify_password(password, user['password']):
            return jsonify({'success': False, 'message': '用户验证失败'}), 401
    except Exception as e:
        print(f"用户验证失败: {e}")
        return jsonify({'success': False, 'message': '用户验证失败'}), 500
    
    try:
        db = DBManager()
        boxes = db.get_detection_boxes_by_result_id(result_id)
        
        return jsonify({'success': True, 'data': boxes})
        
    except Exception as e:
        print(f"获取检测框信息失败: {e}")
        return jsonify({'success': False, 'message': '获取检测框信息失败，请稍后重试'}), 500

# 实时检测相关API端点
# 启动实时检测API
@app.route('/api/detect/realtime/start', methods=['POST'])
def start_realtime_detection():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400
    
    try:
        db = DBManager()
        user = db.get_user_by_username(username)
        
        if not user or not db.verify_password(password, user['password']):
            return jsonify({'success': False, 'message': '用户验证失败'}), 401
        
        # 由于当前没有实现真正的实时检测功能（需要WebSocket或其他长连接技术）
        # 这里只返回功能正在开发中的响应
        return jsonify({'success': True, 'message': '实时检测功能正在开发中'})
        
    except Exception as e:
        print(f"启动实时检测失败: {e}")
        return jsonify({'success': False, 'message': '启动实时检测失败，请稍后重试'}), 500

# 停止实时检测API
@app.route('/api/detect/realtime/stop', methods=['POST'])
def stop_realtime_detection():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400
    
    try:
        db = DBManager()
        user = db.get_user_by_username(username)
        
        if not user or not db.verify_password(password, user['password']):
            return jsonify({'success': False, 'message': '用户验证失败'}), 401
        
        # 由于当前没有实现真正的实时检测功能（需要WebSocket或其他长连接技术）
        # 这里只返回功能正在开发中的响�?
        return jsonify({'success': True, 'message': '实时检测功能正在开发中'})
        
    except Exception as e:
        print(f"停止实时检测失败: {e}")
        return jsonify({'success': False, 'message': '停止实时检测失败，请稍后重试'}), 500

# 视频检测API
@app.route('/api/detect/video', methods=['POST'])
def detect_video():
    # 获取请求参数
    username = request.form.get('username')
    password = request.form.get('password')
    model_version = request.form.get('model_version', 'yolov8s')  # 将默认模型改为yolov8s
    conf_threshold = float(request.form.get('conf_threshold', 0.5))
    
    # 验证用户身份
    try:
        db = DBManager()
        user = db.get_user_by_username(username)
        
        if not user or not db.verify_password(password, user['password']):
            return jsonify({'success': False, 'message': '用户验证失败'}), 401
    except Exception as e:
        print(f"用户验证失败: {e}")
        return jsonify({'success': False, 'message': '用户验证失败'}), 500
    
    # 检查是否有视频上传
    if 'video' not in request.files:
        return jsonify({'success': False, 'message': '没有上传视频'}), 400
    
    video = request.files['video']
    
    if video.filename == '':
        return jsonify({'success': False, 'message': '没有选择视频'}), 400
    
    # 检查视频文件类型（这里简单检查扩展名，实际应用中应该检查MIME类型�?
    allowed_video_extensions = {'mp4', 'avi', 'mov', 'wmv'}
    if '.' not in video.filename or video.filename.rsplit('.', 1)[1].lower() not in allowed_video_extensions:
        return jsonify({'success': False, 'message': '不支持的视频格式'}), 400
    
    # 保存上传的视�?
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{video.filename}"
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video.save(video_path)
    
    # 加载YOLO模型
    global global_models
    if model_version in global_models and global_models[model_version] is not None:
        model = global_models[model_version]
        print(f"�?使用预加载模�? {model_version}")
    else:
        model = load_model(model_version)
        if model:
            global_models[model_version] = model
            print(f"�?动态加载模�? {model_version}")
        else:
            # 清理上传的视�?
            if os.path.exists(video_path):
                os.remove(video_path)
            return jsonify({'success': False, 'message': f'加载{model_version}模型失败'}), 500
    
    try:
        # 处理视频帧并进行检�?
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("无法打开视频文件")
        
        # 获取视频信息
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0
        
        # 初始化统计变�?
        total_occupied = 0
        total_empty = 0
        frame_count = 0
        key_frames = []
        avg_occupied_count = 0
        avg_vacant_count = 0
        
        # 处理视频�?
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # 每隔几帧处理一次（可以根据需要调整）
            if frame_count % 10 == 0:
                # 预处理图像，调整大尺寸图�?
                h, w = frame.shape[:2]
                max_size = 1920
                scale = min(max_size/w, max_size/h)
                
                # 如果需要调整尺�?
                if scale < 1:
                    new_w = int(w * scale)
                    new_h = int(h * scale)
                    # 使用INTER_LINEAR插值保持图像质�?
                    processed_frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
                else:
                    processed_frame = frame
                
                # 直接在内存中执行检测，使用优化参数
                results = model(processed_frame, 
                               conf=conf_threshold, 
                               verbose=False,
                               iou=0.45,  # 设置IOU阈值，减少重复检�?
                               max_det=1000,  # 限制最大检测框数量
                               agnostic_nms=True,  # 使用类别无关的NMS，提高速度
                               device='cpu')  # 根据实际硬件配置选择
                
                # 解析检测结�?
                # 对于视频帧，我们需要手动处理图像路径相关的逻辑
                # 从结果中获取边界框信�?
                boxes = results[0].boxes
                detection_boxes = []
                empty_count = 0
                occupied_count = 0
                vehicle_count = 0
                
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = float(box.conf[0])
                        cls_id = int(box.cls[0])
                        
                        detection_boxes.append({
                            'x1': x1,
                            'y1': y1,
                            'x2': x2,
                            'y2': y2,
                            'confidence': conf,
                            'class_id': cls_id,
                            'class_name': CLASS_NAMES.get(cls_id, f'class_{cls_id}')
                        })
                        
                        if cls_id == 0:  # 空车�?
                            empty_count += 1
                        elif cls_id == 1:  # 已占用车�?
                            occupied_count += 1
                            vehicle_count += 1
                
                detection_summary = {
                    'total_boxes': len(detection_boxes),
                    'empty_count': empty_count,
                    'occupied_count': occupied_count,
                    'vehicle_count': vehicle_count,
                    'vacant_count': empty_count,  # 兼容前端使用
                    'total_spaces': occupied_count + empty_count  # 总车位数�?
                }
                
                # 更新统计数据
                total_occupied += detection_summary['occupied_count']
                total_empty += detection_summary['empty_count']
                
                # 保存关键帧信息（�?0帧保存一次）
                if frame_count % 50 == 0:
                    # 可视化检测结�?
                    result_image = results[0].plot()
                    
                    # 将结果转换为base64
                    _, buffer = cv2.imencode('.jpg', result_image)
                    result_base64 = base64.b64encode(buffer).decode('utf-8')
                    visualization = f"data:image/jpeg;base64,{result_base64}"
                    
                    key_frames.append({
                        'frame_index': frame_count,
                        'timestamp': f"{int(frame_count/fps):02d}:{int((frame_count % fps)/fps*60):02d}",
                        'occupied': detection_summary['occupied_count'],
                        'vacant': detection_summary['empty_count'],
                        'image_data': visualization
                    })
            
            frame_count += 1
        
        # 计算平均�?
        if frame_count > 0:
            avg_occupied_count = round(total_occupied / (frame_count / 10))  # 除以处理的帧数
            avg_vacant_count = round(total_empty / (frame_count / 10))
        
        # 释放视频捕获
        cap.release()
        
        # 构建响应数据
        response_data = {
            'success': True,
            'message': '视频检测完成',
            'data': {
                'video_path': video_path,
                'model_version': model_version,
                'total_frames': total_frames,
                'fps': round(fps, 2),
                'duration': round(duration, 2),
                'avg_occupied_count': avg_occupied_count,
                'avg_vacant_count': avg_vacant_count,
                'key_frames': key_frames
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"视频检测失败 {e}")
        # 清理上传的视频
        if os.path.exists(video_path):
            os.remove(video_path)
        return jsonify({'success': False, 'message': '视频检测失败，请稍后重试'}), 500

# 模型数据API
@app.route('/api/model-data', methods=['GET'])
def api_model_data():
    try:
        from datetime import datetime
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # 返回更新后的模型数据，突出显示YOLO8和YOLO5
        model_data = {
            'models': [
                {
                    'name': 'YOLOv8n-OBB',
                    'version': 'v8.0',
                    'created_at': '2025-12-18',
                    'detection_type': 'OBB检测',
                    'accuracy': 90.418,
                    'status': 'enabled',
                    'is_main': True,  # 标记为主要模�?
                    'rank': 1  # 性能排名
                },
                {
                    'name': 'YOLOv5n-OBB',
                    'version': 'v5.0',
                    'created_at': '2025-12-18',
                    'detection_type': 'OBB检测',
                    'accuracy': 79.788,
                    'status': 'enabled',  # 设置为已启用
                    'is_main': True,  # 标记为主要模�?
                    'rank': 2  # 性能排名
                },
                {
                    'name': 'YOLO11n-OBB',
                    'version': 'v11.0',
                    'created_at': '2025-12-19',
                    'detection_type': 'OBB检测',
                    'accuracy': 91.2,
                    'status': 'loaded',
                    'rank': 3  # 性能排名
                }
            ],
            'performance': {
                'yolov8n_obb': {'accuracy': 90.418, 'inference_time': 140, 'recall': 0.925, 'precision': 0.918},
                'yolov5n_obb': {'accuracy': 79.788, 'inference_time': 125, 'recall': 0.674, 'precision': 0.752},
                'yolo11n_obb': {'accuracy': 91.2, 'inference_time': 135, 'recall': 0.932, 'precision': 0.924}
            },
            'usage': {
                'yolov8n_obb': 65,  # 主要使用YOLO8
                'yolov5n_obb': 30,  # 其次是YOLO5
                'yolo11n_obb': 5    # YOLO11使用率较�?
            }
        }
        
        return jsonify({
            'status': 'success',
            'data': model_data
        })
    except Exception as e:
        print(f"获取模型数据失败: {e}")
        return jsonify({
            'status': 'error',
            'message': '获取模型数据失败'
        }), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=False
    )





















