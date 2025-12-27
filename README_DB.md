# YOLO parking detection data management system

## 项目概述
基于MySQL数据库的YOLOv5/YOLOv8检测数据管理系统，实现了完整的"模型检测-权限验证-数据存储-查询管理"闭环。

## 已完成的功能

### 1. 数据库结构设计
- **用户表(users)**: 存储管理员和操作员信息，支持密码加密存储
- **检测结果表(detection_results)**: 存储YOLO模型检测结果的基本信息
- **检测框表(detection_boxes)**: 存储每个检测框的详细坐标和置信度

### 2. 权限管理机制
- 超级管理员(admin): 拥有全量管控权限
- 操作员(operator): 仅授权写入检测数据
- 密码使用bcrypt加密存储，确保安全

### 3. 数据库操作类
- `DBManager`类封装了所有数据库操作
- 支持用户注册、登录、权限验证
- 实现检测数据的写入、查询、批量导入
- 内置异常处理和事务管理，确保数据完整性

### 4. YOLO模型整合
- 无缝集成YOLOv5/YOLOv8模型输出
- 结构化存储检测结果：图片路径、车辆数量、检测框坐标、模型版本
- 支持单张图片实时检测和批量历史数据导入

### 5. 自动标注功能
- 可以使用训练好的模型对图像进行自动标注
- 输出YOLO格式的标注文件和可视化检测结果

## 快速开始

### 1. 环境准备

#### 1.1 安装依赖
```bash
# 安装MySQL相关依赖
pip install pymysql bcrypt
```

#### 1.2 配置MySQL连接
编辑`db_config.py`文件，设置你的MySQL连接信息：

```python
# 数据库配置文件
DB_CONFIG = {
    'host': 'localhost',      # 数据库主机地址
    'port': 3306,             # 数据库端口
    'user': 'root',           # 数据库用户名
    'password': 'your_password',  # 你的MySQL密码
    'database': 'parking_detection',  # 数据库名称
    'charset': 'utf8mb4',     # 字符集
    'autocommit': False       # 关闭自动提交，使用事务管理
}
```

#### 1.3 创建数据库和表
运行数据库连接测试脚本，它会自动创建数据库和表结构：

```bash
python test_db_connection.py
```

### 2. 功能使用

#### 2.1 自动标注功能

使用训练好的模型对图像进行自动标注：

```bash
# 自动标注单个图像
python auto_annotate.py

# 标注结果会保存在 auto_annotations 目录中
```

#### 2.2 YOLO检测与数据库存储

##### 2.2.1 单张图像检测与存储

```bash
# 使用YOLOv8模型检测并存储结果
python yolo_db_integration.py --image dataset/images/test/0.png

# 使用YOLOv5模型检测并存储结果
python yolo_db_integration.py --image dataset/images/test/0.png --model parking_train/yolov5s_parking/weights/best.pt --version yolov5
```

##### 2.2.2 批量图像检测与存储

```bash
# 批量处理目录中的所有图像
python yolo_db_integration.py --dir dataset/images/test
```

#### 2.3 数据库操作示例

```python
from yolo_db.db_manager import DBManager

# 初始化数据库管理器
db = DBManager()

# 用户登录
login_success, user_info = db.login('admin', 'admin123')
if login_success:
    print(f"登录成功！用户ID: {user_info['id']}")

# 查询检测结果
success, results = db.get_detection_results(limit=10)
if success:
    print(f"查询到 {len(results)} 条检测结果")
    for result in results:
        print(f"- {result['image_path']}: {result['vehicle_count']} 辆车")
```

## 文件说明

| 文件名 | 功能描述 |
|-------|---------|
| `create_database.sql` | 数据库结构定义脚本 |
| `db_config.py` | 数据库连接配置文件 |
| `db_manager.py` | 数据库操作类 |
| `yolo_db_integration.py` | YOLO检测与数据库整合脚本 |
| `auto_annotate.py` | 自动标注功能脚本 |
| `test_db_connection.py` | 数据库连接测试工具 |

## 系统架构

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  YOLO Model     │     │  DB Manager     │     │  MySQL Database │
│  (v5/v8)        │────▶│  - 权限验证     │────▶│  - users        │
│                 │     │  - 数据处理     │     │  - detection_   │
│                 │     │  - 事务管理     │     │    results      │
└─────────────────┘     └─────────────────┘     │  - detection_   │
                                                │    boxes        │
                                                └─────────────────┘
```

## 使用注意事项

1. **MySQL配置**：
   - 确保MySQL服务正在运行
   - 正确配置`db_config.py`中的用户名和密码
   - 首次使用时需要创建数据库和表结构

2. **权限管理**：
   - 默认超级管理员账户：用户名`admin`，密码`admin123`
   - 请及时修改默认密码

3. **模型使用**：
   - 使用`parking_train/`目录下的`best.pt`模型文件获得最佳效果
   - 可以根据需要切换YOLOv5或YOLOv8模型

4. **批量处理**：
   - 批量导入大量数据时建议分批次处理
   - 系统会自动处理异常并保持数据一致性

## 扩展功能

系统设计支持以下扩展功能：

- Web界面开发
- 实时视频流处理
- 数据分析和可视化
- API接口开发
- 多模型比较功能

## 技术栈

- Python 3.9
- MySQL 8.0
- PyTorch 2.0+
- Ultralytics YOLO
- pymysql
- bcrypt
