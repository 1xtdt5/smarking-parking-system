# 智慧停车位检测系统运行文档

## 1. 项目概述

智慧停车位检测系统是一个基于YOLOv5/YOLOv8深度学习模型的智能停车解决方案，能够实时检测停车位的占用状态，并提供数据统计与可视化功能。

**主要功能**：

- 单张图像停车位检测
- 视频流停车位检测
- 实时摄像头监测
- 检测结果数据存储
- 数据统计与可视化
- 用户权限管理

## 2. 系统要求

### 2.1 硬件要求

- CPU：至少2核处理器
- 内存：至少4GB RAM
- 存储空间：至少10GB可用空间
- 网络：用于访问Web界面（本地网络即可）
- 可选：摄像头（用于实时检测功能）

### 2.2 软件要求

- Python 3.8或更高版本
- MySQL 5.7或更高版本
- 现代Web浏览器（Chrome、Firefox、Edge等）

## 3. 安装步骤

### 3.1 Windows系统

#### 3.1.1 自动安装（推荐）

1. 双击运行 `install_windows.bat` 文件
2. 按照提示完成安装
3. 安装完成后，按照脚本提示的步骤运行应用

#### 3.1.2 手动安装

1. 确保已安装Python 3.8+和pip
2. 打开命令提示符，进入项目目录
3. 创建虚拟环境：`python -m venv venv`
4. 激活虚拟环境：`venv\Scripts\activate.bat`
5. 安装依赖：`pip install -r requirements.txt`
6. 复制并配置.env文件：
   
   ```bash
   copy .env .env
   ```
   
   然后编辑.env文件配置数据库信息

### 3.2 Linux/macOS系统

#### 3.2.1 自动安装（推荐）

1. 打开终端，进入项目目录
2. 运行安装脚本：`bash install_linux.sh`（Linux）或 `bash install_macos.sh`（macOS）
3. 按照提示完成安装

#### 3.2.2 手动安装

1. 确保已安装Python 3.8+和pip
2. 打开终端，进入项目目录
3. 创建虚拟环境：`python3 -m venv venv`
4. 激活虚拟环境：`source venv/bin/activate`
5. 安装依赖：`pip install -r requirements.txt`
6. 复制并配置.env文件：
   
   ```bash
   cp .env.example .env
   ```
   
   然后编辑.env文件配置数据库信息

## 4. 数据库配置

### 4.1 配置文件设置

编辑项目根目录下的`.env`文件，配置MySQL数据库连接信息：

```ini
# 数据库配置
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=parking_detection
DB_CHARSET=utf8mb4
```

### 4.2 初始化数据库

1. 确保MySQL服务已启动
2. 激活虚拟环境
3. 运行数据库初始化脚本：
   
   ```bash
   python initialize_db.py
   ```

该脚本会自动创建数据库（如果不存在）和所需的表结构，并创建默认管理员账号：

- 用户名：admin
- 密码：admin123

## 5. 运行应用

### 5.1 自动运行（推荐）

#### Windows系统

双击运行 `run_app.bat` 文件

#### Linux/macOS系统

在终端中运行：`bash run_app.sh`

### 5.2 手动运行

1. 激活虚拟环境：
   
   - Windows：`venv\Scripts\activate.bat`
   - Linux/macOS：`source venv/bin/activate`

2. 运行应用程序：
   
   ```bash
   python app.py
   ```

3. 打开Web浏览器，访问：`http://localhost:5000`

### 5.3 查看运行日志

所有运行输出都会保存到 `app_output.log` 文件中，可通过以下方式查看：

- Windows：使用记事本或其他文本编辑器打开
- Linux/macOS：`tail -f app_output.log`

## 6. 功能使用指南

### 6.1 用户登录

1. 访问 `http://localhost:5000`
2. 使用管理员账号登录（默认：admin/admin123）
3. 登录后进入系统仪表盘

### 6.2 图像检测

1. 点击左侧菜单的"图像检测"或访问 `http://localhost:5000/detect`
2. 上传包含停车位的图片
3. 选择检测模型（YOLOv5或YOLOv8）
4. 点击"开始检测"按钮
5. 查看检测结果和统计数据

### 6.3 视频检测

1. 点击左侧菜单的"视频检测"或访问 `http://localhost:5000/video-detect`
2. 上传视频文件
3. 选择检测模型和参数
4. 点击"开始检测"按钮
5. 查看检测结果统计

### 6.4 实时监测

1. 点击左侧菜单的"实时监测"或访问 `http://localhost:5000/realtime-detect`
2. 选择摄像头设备
3. 点击"开始监测"按钮
4. 查看实时检测结果
5. 点击"停止监测"按钮结束

### 6.5 数据统计

1. 点击左侧菜单的"模型数据"或访问 `http://localhost:5000/model-data`
2. 查看停车位检测统计图表
3. 可按日期筛选数据

### 6.6 用户管理

1. 点击左侧菜单的"用户管理"或访问 `http://localhost:5000/user-management`
2. 管理员可以查看、添加和删除用户
3. 可设置用户角色（管理员或操作员）

## 7. API接口说明

### 7.1 认证接口

- `POST /api/login` - 用户登录
- `POST /api/register` - 用户注册
- `POST /api/logout` - 用户登出

### 7.2 检测接口

- `POST /api/detect/image` - 图像检测
- `POST /api/detect/video` - 视频检测
- `POST /api/detect/realtime/start` - 开始实时检测
- `POST /api/detect/realtime/stop` - 停止实时检测

### 7.3 数据接口

- `GET /api/detection-results` - 获取检测结果列表
- `GET /api/detection-boxes/<result_id>` - 获取特定检测结果的详细信息
- `GET /api/stats` - 获取统计数据

### 7.4 用户管理接口

- `GET /api/get-users` - 获取用户列表
- `POST /api/add-user` - 添加用户
- `POST /api/delete-user` - 删除用户

## 8. 项目结构

```
parking_system/
├── app.py              # Flask应用主程序
├── db_manager.py       # 数据库管理类
├── initialize_db.py    # 数据库初始化脚本
├── config.py           # 系统配置
├── requirements.txt    # 依赖列表
├── .env                # 环境变量配置
├── templates/          # HTML模板文件
├── static/             # 静态资源（CSS、JS）
├── uploads/            # 文件上传目录
├── parking_train/      # 训练好的模型
├── dataset/            # 数据集目录
├── install_windows.bat # Windows安装脚本
├── install_linux.sh    # Linux安装脚本
├── install_macos.sh    # macOS安装脚本
└── run_app.bat/sh      # 运行脚本
```

## 9. 常见问题与解决方案

### 9.1 数据库连接失败

**问题**：应用无法连接到MySQL数据库
**解决方案**：

- 确保MySQL服务已启动
- 检查.env文件中的数据库配置信息是否正确
- 确保数据库用户有足够的权限

### 9.2 依赖安装失败

**问题**：pip install -r requirements.txt失败
**解决方案**：

- 确保已激活虚拟环境
- 升级pip：`pip install --upgrade pip`
- 尝试单独安装失败的包

### 9.3 端口被占用

**问题**：应用无法启动，提示端口5000已被占用
**解决方案**：

- 修改.env文件中的PORT配置，使用其他端口
- 或关闭占用5000端口的其他程序

### 9.4 检测速度慢

**问题**：检测过程耗时较长
**解决方案**：

- 降低视频/摄像头的分辨率
- 增加系统内存
- 考虑使用GPU加速（需额外配置）

## 10. 联系方式

如果您在使用过程中遇到问题，请联系系统管理员或开发团队。

---

**文档版本**：v1.0
**更新日期**：2025-12-18
**适用项目**：智慧停车位检测系统
