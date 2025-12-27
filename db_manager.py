import pymysql
import bcrypt
import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 数据库配置
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'yolo_db'),
    'charset': os.environ.get('DB_CHARSET', 'utf8mb4')
}

class DBManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.config = db_config
    
    def connect(self):
        """连接到数据库"""
        try:
            self.connection = pymysql.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def commit(self):
        """提交事务"""
        if self.connection:
            self.connection.commit()
    
    def rollback(self):
        """回滚事务"""
        if self.connection:
            self.connection.rollback()
    
    def hash_password(self, password):
        """密码加密"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password, hashed_password):
        """验证密码"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def get_user_by_username(self, username):
        """根据用户名获取用户信息"""
        try:
            self.connect()
            sql = "SELECT * FROM users WHERE username = %s AND status = 'active'"
            self.cursor.execute(sql, (username,))
            user = self.cursor.fetchone()
            return user
        except Exception as e:
            print(f"获取用户信息失败: {e}")
            return None
        finally:
            self.disconnect()
    
    def register_user(self, username, password, role='operator'):
        """注册新用户"""
        try:
            # 检查用户名是否已存在
            existing_user = self.get_user_by_username(username)
            if existing_user:
                return False, "用户名已存在"
            
            # 密码加密
            hashed_password = self.hash_password(password)
            
            # 插入新用户
            self.connect()
            sql = """
            INSERT INTO users (username, password, role)
            VALUES (%s, %s, %s)
            """
            self.cursor.execute(sql, (username, hashed_password, role))
            self.commit()
            return True, "注册成功"
            
        except Exception as e:
            print(f"注册用户失败: {e}")
            return False, f"注册失败: {str(e)}"
        finally:
            self.disconnect()
    
    def get_all_users(self):
        """获取所有用户列表"""
        try:
            self.connect()
            sql = "SELECT * FROM users ORDER BY created_at DESC"
            self.cursor.execute(sql)
            users = self.cursor.fetchall()
            return users
        except Exception as e:
            print(f"获取用户列表失败: {e}")
            return []
        finally:
            self.disconnect()
    
    def delete_user(self, user_id):
        """删除用户"""
        try:
            self.connect()
            # 不能删除admin用户
            sql_check_admin = "SELECT role FROM users WHERE id = %s"
            self.cursor.execute(sql_check_admin, (user_id,))
            user = self.cursor.fetchone()
            if user and user['role'] == 'admin':
                return False, "不能删除管理员用户"
            
            # 软删除用户（设置状态为inactive）
            sql = "UPDATE users SET status = 'inactive' WHERE id = %s"
            self.cursor.execute(sql, (user_id,))
            self.commit()
            
            if self.cursor.rowcount == 0:
                return False, "用户不存在"
                
            return True, "用户删除成功"
            
        except Exception as e:
            print(f"删除用户失败: {e}")
            return False, f"删除失败: {str(e)}"
        finally:
            self.disconnect()
    
    def save_detection_result(self, image_path, vehicle_count, model_version, created_by, boxes):
        """保存检测结果"""
        try:
            self.connect()
            
            # 获取空车位和已占用车位数
            empty_count = 0
            occupied_count = 0
            
            for box in boxes:
                if box['class_id'] == 0:
                    empty_count += 1
                elif box['class_id'] == 1:
                    occupied_count += 1
            
            # 保存检测结果主表
            sql_result = """
            INSERT INTO detection_results (
                image_path, vehicle_count, empty_count, occupied_count, total_boxes, 
                model_version, created_by
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            total_boxes = len(boxes)
            
            self.cursor.execute(sql_result, (
                image_path, 
                vehicle_count, 
                empty_count, 
                occupied_count, 
                total_boxes,
                model_version, 
                created_by
            ))
            result_id = self.cursor.lastrowid
            
            # 保存检测框详情
            if boxes:
                sql_box = """
                INSERT INTO detection_boxes (
                    result_id, class_id, class_name, x1, y1, x2, y2, confidence
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                box_data = []
                for box in boxes:
                    box_data.append((
                        result_id,
                        box['class_id'],
                        box['class_name'],
                        box['x1'],
                        box['y1'],
                        box['x2'],
                        box['y2'],
                        box['confidence']
                    ))
                
                if box_data:
                    self.cursor.executemany(sql_box, box_data)
            
            # 提交事务
            self.commit()
            return True, result_id
            
        except Exception as e:
            print(f"保存检测结果失败: {e}")
            self.rollback()
            return False, None
        finally:
            self.disconnect()
    
    def get_detection_results(self, limit=100, offset=0):
        """获取检测结果列表"""
        try:
            self.connect()
            sql = """
            SELECT dr.*, u.username as created_by_username
            FROM detection_results dr
            JOIN users u ON dr.created_by = u.id
            ORDER BY dr.detection_time DESC
            LIMIT %s OFFSET %s
            """
            self.cursor.execute(sql, (limit, offset))
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(f"获取检测结果列表失败: {e}")
            return []
        finally:
            self.disconnect()
    
    def get_detection_boxes_by_result_id(self, result_id):
        """根据检测结果ID获取检测框信息"""
        try:
            self.connect()
            sql = """
            SELECT * FROM detection_boxes 
            WHERE result_id = %s
            ORDER BY id
            """
            self.cursor.execute(sql, (result_id,))
            boxes = self.cursor.fetchall()
            return boxes
        except Exception as e:
            print(f"获取检测框信息失败: {e}")
            return []
        finally:
            self.disconnect()
    
    def create_database_and_tables(self):
        """创建数据库和表结构"""
        try:
            # 先连接到MySQL服务器
            self.connection = pymysql.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            
            # 创建数据库
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            
            # 切换到创建的数据库
            self.cursor.execute(f"USE {self.config['database']}")
            
            # 创建用户表
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
                password VARCHAR(255) NOT NULL COMMENT '加密后的密码',
                role ENUM('admin', 'operator') NOT NULL DEFAULT 'operator' COMMENT '角色：admin超级管理员，operator操作员',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                status ENUM('active', 'inactive') NOT NULL DEFAULT 'active' COMMENT '状态：active激活，inactive禁用'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            
            # 创建检测结果表
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS detection_results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                image_path VARCHAR(255) NOT NULL COMMENT '检测图片路径',
                vehicle_count INT NOT NULL COMMENT '检测到的车辆数量',
                empty_count INT NOT NULL COMMENT '空车位数',
                occupied_count INT NOT NULL COMMENT '已占用车位数',
                total_boxes INT NOT NULL COMMENT '总检测框数',
                model_version VARCHAR(20) NOT NULL COMMENT '使用的模型版本：yolov5或yolov8',
                detection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '检测时间',
                created_by INT NOT NULL COMMENT '创建者ID，关联users表',
                FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_image_path (image_path),
                INDEX idx_detection_time (detection_time),
                INDEX idx_model_version (model_version)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            
            # 创建检测框表
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS detection_boxes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                result_id INT NOT NULL COMMENT '关联detection_results表的ID',
                class_id INT NOT NULL COMMENT '类别ID：0=空缺车位，1=已占用车位',
                class_name VARCHAR(50) NOT NULL COMMENT '类别名称',
                x1 FLOAT NOT NULL COMMENT '检测框左上角x坐标',
                y1 FLOAT NOT NULL COMMENT '检测框左上角y坐标',
                x2 FLOAT NOT NULL COMMENT '检测框右下角x坐标',
                y2 FLOAT NOT NULL COMMENT '检测框右下角y坐标',
                confidence FLOAT NOT NULL COMMENT '检测置信度',
                FOREIGN KEY (result_id) REFERENCES detection_results(id) ON DELETE CASCADE,
                INDEX idx_result_id (result_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            
            # 检查是否有默认的管理员账号
            self.cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            admin_user = self.cursor.fetchone()
            
            if not admin_user:
                # 创建默认管理员账号
                hashed_password = self.hash_password('admin123')
                self.cursor.execute("""
                INSERT INTO users (username, password, role)
                VALUES (%s, %s, 'admin')
                """, ('admin', hashed_password))
            
            self.commit()
            print("数据库和表结构创建成功")
            return True
            
        except Exception as e:
            print(f"创建数据库和表结构失败: {e}")
            self.rollback()
            return False
        finally:
            self.disconnect()
