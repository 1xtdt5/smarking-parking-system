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
        database=db_config['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()
    
    print("数据库连接成功")
    
    # 检查并添加缺失的字段
    cursor.execute("DESCRIBE detection_results")
    columns = {row['Field'] for row in cursor.fetchall()}
    
    print(f"当前表结构包含字段: {columns}")
    
    # 需要的字段列表
    required_columns = {
        'empty_count': 'INT NOT NULL DEFAULT 0',
        'occupied_count': 'INT NOT NULL DEFAULT 0',
        'total_boxes': 'INT NOT NULL DEFAULT 0'
    }
    
    # 检查并添加缺失的字段
    for field, definition in required_columns.items():
        if field not in columns:
            print(f"添加缺失字段: {field}")
            cursor.execute(f"ALTER TABLE detection_results ADD COLUMN {field} {definition}")
    
    # 提交更改
    connection.commit()
    print("表结构修复成功")
    
    # 再次检查表结构
    cursor.execute("DESCRIBE detection_results")
    print("\n修复后的表结构：")
    for row in cursor.fetchall():
        print(f"{row['Field']}: {row['Type']} {row['Null']} {row['Key']} {row['Default']} {row['Extra']}")
    
    # 检查是否还有其他表需要修复
    cursor.execute("SHOW TABLES")
    tables = [row[f'Tables_in_{db_config['database']}'] for row in cursor.fetchall()]
    print(f"\n数据库中的表：{tables}")
    
    if 'detection_boxes' in tables:
        cursor.execute("DESCRIBE detection_boxes")
        print("\ndetection_boxes 表结构：")
        for row in cursor.fetchall():
            print(f"{row['Field']}: {row['Type']} {row['Null']} {row['Key']} {row['Default']} {row['Extra']}")
    
    if 'users' in tables:
        cursor.execute("DESCRIBE users")
        print("\nusers 表结构：")
        for row in cursor.fetchall():
            print(f"{row['Field']}: {row['Type']} {row['Null']} {row['Key']} {row['Default']} {row['Extra']}")

except Exception as e:
    print(f"操作失败: {e}")
    if 'connection' in locals():
        connection.rollback()
finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'connection' in locals() and connection:
        connection.close()
    print("数据库连接已关闭")
