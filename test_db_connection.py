import pymysql
import json

# 加载数据库配置
with open('db_config.json') as f:
    db_config = json.load(f)

try:
    # 连接到MySQL服务器
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    
    print("数据库连接成功")
    
    # 检查数据库是否存在
    cursor.execute(f"SHOW DATABASES LIKE '{db_config['database']}'")
    if cursor.fetchone():
        print(f"数据库 {db_config['database']} 存在")
        
        # 切换到该数据库
        cursor.execute(f"USE {db_config['database']}")
        print(f"已切换到数据库 {db_config['database']}")
        
        # 检查检测结果表是否存在
        cursor.execute("SHOW TABLES LIKE 'detection_results'")
        if cursor.fetchone():
            print("detection_results 表存在")
            
            # 查询检测结果表结构
            cursor.execute("DESCRIBE detection_results")
            print("\ndetection_results 表结构：")
            for row in cursor.fetchall():
                print(f"{row['Field']}: {row['Type']} {row['Null']} {row['Key']} {row['Default']} {row['Extra']}")
            
            # 检查是否有数据
            cursor.execute("SELECT COUNT(*) as count FROM detection_results")
            count = cursor.fetchone()['count']
            print(f"\ndetection_results 表中有 {count} 条数据")
            
            if count > 0:
                # 查询最新的10条数据
                cursor.execute("SELECT * FROM detection_results ORDER BY detection_time DESC LIMIT 10")
                results = cursor.fetchall()
                print("\n最新10条检测结果：")
                for result in results:
                    print(f"ID: {result['id']}, 图片路径: {result['image_path']}, 车辆数: {result['vehicle_count']}, \
                          空车位: {result['empty_count']}, 已占用: {result['occupied_count']}, \
                          检测时间: {result['detection_time']}")
        else:
            print("detection_results 表不存在")
        
        # 检查users表
        cursor.execute("SHOW TABLES LIKE 'users'")
        if cursor.fetchone():
            print("\nusers 表存在")
            
            # 查询用户数据
            cursor.execute("SELECT id, username, role, status FROM users")
            users = cursor.fetchall()
            print("\n用户列表：")
            for user in users:
                print(f"ID: {user['id']}, 用户名: {user['username']}, 角色: {user['role']}, 状态: {user['status']}")
        else:
            print("\nusers 表不存在")
    else:
        print(f"数据库 {db_config['database']} 不存在")
        print("尝试创建数据库和表结构...")
        from db_manager import DBManager
        
        db_manager = DBManager()
        success = db_manager.create_database_and_tables()
        if success:
            print("数据库和表结构创建成功")
        else:
            print("数据库和表结构创建失败")
            
except Exception as e:
    print(f"数据库操作失败: {e}")
finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'connection' in locals() and connection:
        connection.close()
    print("数据库连接已关闭")
