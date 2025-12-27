# 数据库初始化脚本
from db_manager import DBManager

def initialize_database():
    print("正在初始化数据库...")
    
    try:
        db = DBManager()
        success = db.create_database_and_tables()
        
        if success:
            print("数据库初始化成功！")
            return True
        else:
            print("数据库初始化失败！")
            return False
            
    except Exception as e:
        print(f"数据库初始化出错: {str(e)}")
        return False

if __name__ == "__main__":
    initialize_database()