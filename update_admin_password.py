import pymysql
from yolo_db.db_config import DB_CONFIG
from yolo_db.db_manager import DBManager

# 创建数据库管理器
db = DBManager()

# 尝试连接并更新管理员密码
print("正在更新管理员密码...")

# 新密码
new_password = "admin123"

# 先尝试连接获取连接对象
conn = None
cursor = None

try:
    # 连接到MySQL服务器
    temp_config = DB_CONFIG.copy()
    temp_config.pop('database', None)
    conn = pymysql.connect(**temp_config)
    cursor = conn.cursor()
    
    # 使用数据库
    cursor.execute(f"USE {DB_CONFIG['database']};")
    
    # 创建DBManager实例来生成bcrypt哈希
    db_manager = DBManager()
    hashed_password = db_manager.hash_password(new_password)
    
    # 更新管理员密码
    cursor.execute("UPDATE users SET password = %s WHERE username = 'admin';", (hashed_password,))
    conn.commit()
    
    print(f"✅ 管理员密码已更新为: {new_password}")
    
    # 验证更新是否成功
    cursor.execute("SELECT username FROM users WHERE username = 'admin' AND status = 'active';")
    if cursor.fetchone():
        print("✅ 管理员账户验证成功")
    else:
        print("❌ 管理员账户不存在或已禁用")
    
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
