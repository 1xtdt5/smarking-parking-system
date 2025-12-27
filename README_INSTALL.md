**安装指南 (README_INSTALL)**

- **目标**: 本文档说明如何在另一台电脑上安装并运行此停车位检测项目（跨平台：Windows / macOS / Linux）。

**先决条件**:
- **Python**: 推荐 Python 3.10+（项目在开发环境中使用 Python 3.13，但 3.10–3.13 均可）。
- **系统依赖**: 若需使用相机或处理视频，建议安装系统级的媒体库（例如在 Linux 上安装 `libgl1`, `ffmpeg` 等）。
- **数据库**: 项目使用 MySQL（通过 `pymysql` 连接）。可用 MySQL 本地安装或通过 Docker 运行。
- **GPU (可选)**: 若要使用 GPU 加速，需安装合适的 CUDA/cuDNN 并使用与之兼容的 PyTorch/Ultralytics 构建。

**仓库中重要文件**:
- 应用入口与模板: [app.py](app.py)
- 启动脚本: [start_app.py](start_app.py)、[run_app.bat](run_app.bat)
- 依赖列表: [requirements.txt](requirements.txt)
- 数据库 SQL: [yolo_db/create_database.sql](yolo_db/create_database.sql)
- 数据库配置: [yolo_db/db_config.py](yolo_db/db_config.py) 与 [db_config.json](db_config.json)

**快速安装（Windows，PowerShell）**
1. 打开 PowerShell，切换到项目目录：
```powershell
Push-Location 'C:\Path\To\parking_system'
```
2. 创建虚拟环境并激活（此处使用 `.venv` 目录）：
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
3. 升级 pip 并安装依赖：
```powershell
.\.venv\Scripts\pip.exe install --upgrade pip
.\.venv\Scripts\pip.exe install -r requirements.txt
```
4. 配置数据库：
   - 若本机已有 MySQL，使用 MySQL 客户端执行建表脚本：
```powershell
mysql -u root -p < yolo_db\create_database.sql
```
   - 或使用 Docker 启动 MySQL（示例）：
```powershell
docker run -d --name parking-mysql -e MYSQL_ROOT_PASSWORD=123456 -e MYSQL_DATABASE=parking_detection -p 3306:3306 mysql:8
sleep 5
docker exec -i parking-mysql mysql -u root -p123456 parking_detection < yolo_db/create_database.sql
```
5. 更新数据库配置（如需）：编辑 [yolo_db/db_config.py](yolo_db/db_config.py) 或 [db_config.json](db_config.json) 以匹配你的 MySQL 用户名/密码/主机。
6. 准备模型：
   - 项目默认从环境变量 `YOLOV8_MODEL_PATH` / `YOLOV5_MODEL_PATH` 指定模型路径，或者使用项目内的模型文件（例如 `yolov8s.pt`、`yolov8n.pt`）。将模型文件放在项目中的可访问路径，并在 .env 中设置对应变量（见下）。
7. 创建 `.env`（可选但推荐），示例内容：
```
SECRET_KEY=change_me
PORT=5000
DEBUG=True
UPLOAD_FOLDER=uploads
YOLOV8_MODEL_PATH=runs/detect/train/weights/best.pt
YOLOV5_MODEL_PATH=yolov5/runs/detect/train/weights/best.pt
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=123456
DB_NAME=parking_detection
```
8. 启动应用（推荐使用 `start_app.py` 捕获日志）：
```powershell
.\.venv\Scripts\python.exe start_app.py
```
9. 后台运行（示例）：
```powershell
Start-Process -FilePath .\.venv\Scripts\python.exe -ArgumentList 'start_app.py'
```

**快速安装（macOS / Linux，bash）**
1. 切换到项目目录：
```bash
cd /path/to/parking_system
```
2. 创建虚拟环境并激活：
```bash
python3 -m venv .venv
source .venv/bin/activate
```
3. 升级 pip 并安装依赖：
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
4. 配置数据库（本机 MySQL 或 Docker）：
```bash
mysql -u root -p < yolo_db/create_database.sql
# 或
docker run -d --name parking-mysql -e MYSQL_ROOT_PASSWORD=123456 -e MYSQL_DATABASE=parking_detection -p 3306:3306 mysql:8
sleep 5
docker exec -i parking-mysql mysql -u root -p123456 parking_detection < yolo_db/create_database.sql
```
5. 创建 `.env`（参照上文）。
6. 启动应用：
```bash
python start_app.py
# 或后台运行
nohup python start_app.py > app_output.log 2>&1 &
```

**环境变量说明（可放在 `.env`）**
- `SECRET_KEY`: Flask secret key。
- `PORT`: 应用监听端口（默认 5000）。
- `DEBUG`: 是否开启调试模式（True/False）。
- `UPLOAD_FOLDER`: 上传文件保存目录（默认 `uploads`）。
- `YOLOV8_MODEL_PATH` / `YOLOV5_MODEL_PATH`: YOLO 模型文件路径。

**日志与调试**
- 启动脚本 `start_app.py` 会将运行输出写入 `app_output.log`（见项目根目录）。
- 检查日志：
```powershell
Get-Content app_output.log -Tail 200 -Wait
```
或在 Linux/macOS：
```bash
tail -n 200 -f app_output.log
```
- 健康检查（服务启动并监听 5000 端口后）：
```bash
curl http://127.0.0.1:5000/api/health
```

**数据库说明**
- 默认数据库配置位于 [yolo_db/db_config.py](yolo_db/db_config.py)，以及根目录的 [db_config.json](db_config.json)。根据需要修改为你的数据库凭据。
- 初始化数据库：执行 [yolo_db/create_database.sql](yolo_db/create_database.sql) 创建表结构。

**模型文件**
- 项目未包含所有训练后模型（或可能包含多个示例权重文件）。你可以：
  - 使用已有的 `yolov8s.pt` / `yolov8n.pt` 等文件并在 `.env` 中设置 `YOLOV8_MODEL_PATH`，或
  - 将模型路径指向训练输出目录（项目中常见路径如 `runs/detect/train/weights/best.pt`）。

**常见问题与排查**
- 如果遇到 `ModuleNotFoundError`：确认虚拟环境已激活并已安装 `requirements.txt` 中所有依赖。
- 如果 `ultralytics` 或 `torch` 报错：检查 Python 版本与平台是否兼容；若需 GPU，请安装与 CUDA 兼容的 `torch` 版本（非 `pip install -r requirements.txt` 的默认版本）。
- 若无法连接数据库：检查 MySQL 是否运行、`yolo_db/db_config.py` 的连接信息是否正确，以及防火墙/端口是否被阻塞。
- 若模型加载失败：确认 `YOLOV8_MODEL_PATH` 指向存在的 `.pt` 文件，且文件可读。

**可选：使用 Docker 运行（简要说明）**
- 可以通过 Docker 把应用与数据库容器化，简化部署。基本思路：
  - 编写 `Dockerfile` 以安装 Python、复制代码并安装 `requirements.txt`。
  - 使用 `docker-compose.yml` 编排应用与 MySQL 服务，并挂载模型文件与 `uploads` 卷。

**测试与验证**
- 启动后，确认以下命令返回成功：
```bash
curl http://127.0.0.1:5000/api/health
```
- 访问浏览器界面：打开 `http://127.0.0.1:5000`（默认登录页）。

**下一步建议**
- 若需要，我可以：
  - 为你生成一个 `docker-compose.yml` 和 `Dockerfile` 的示例，或
  - 在仓库内添加一个 `INSTALL_WINDOWS.md` 与 `INSTALL_LINUX.md` 的更详细分步指南，或
  - 帮你调试 `app_output.log` 中的具体错误（你可以把日志贴上来，或允许我读取该文件）。

---
文件更新于项目根目录，帮助在新机器上快速部署并运行服务。
