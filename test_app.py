import os
import sys
import logging

# 配置日志，将输出写入文件
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app_test.log'),
        logging.StreamHandler()
    ]
)

def test_model_loading():
    """测试模型加载功能"""
    print("=== 测试模型加载 ===")
    logging.info("=== 测试模型加载 ===")
    
    # 打印当前目录和文件列表
    print(f"当前工作目录: {os.getcwd()}")
    logging.info(f"当前工作目录: {os.getcwd()}")
    
    print("当前目录文件:")
    logging.info("当前目录文件:")
    for file in os.listdir('.'):
        print(f"  {file}")
        logging.info(f"  {file}")
    
    # 检查模型文件是否存在
    print("\n=== 检查模型文件 ===")
    logging.info("\n=== 检查模型文件 ===")
    
    yolo5_model_path = 'parking_train/yolov5s_parking/weights/best.pt'
    yolo8_model_path = 'parking_train/yolov8s_parking/weights/best.pt'
    
    print(f"YOLO5模型路径: {yolo5_model_path}")
    print(f"YOLO5模型是否存在: {os.path.exists(yolo5_model_path)}")
    logging.info(f"YOLO5模型路径: {yolo5_model_path}")
    logging.info(f"YOLO5模型是否存在: {os.path.exists(yolo5_model_path)}")
    
    print(f"YOLO8模型路径: {yolo8_model_path}")
    print(f"YOLO8模型是否存在: {os.path.exists(yolo8_model_path)}")
    logging.info(f"YOLO8模型路径: {yolo8_model_path}")
    logging.info(f"YOLO8模型是否存在: {os.path.exists(yolo8_model_path)}")
    
    # 测试模型加载
    try:
        print("\n=== 尝试加载YOLO8模型 ===")
        logging.info("\n=== 尝试加载YOLO8模型 ===")
        
        from ultralytics import YOLO
        model = YOLO(yolo8_model_path)
        print(f"✅ YOLO8模型加载成功: {model}")
        logging.info(f"✅ YOLO8模型加载成功: {model}")
        
        # 打印模型信息
        print(f"模型类型: {type(model).__name__}")
        logging.info(f"模型类型: {type(model).__name__}")
        
        return True
    except Exception as e:
        print(f"❌ YOLO8模型加载失败: {str(e)}")
        logging.error(f"❌ YOLO8模型加载失败: {str(e)}")
        import traceback
        traceback.print_exc()
        logging.error(traceback.format_exc())
        return False

def test_app_import():
    """测试导入应用程序模块"""
    print("\n=== 测试导入应用程序模块 ===")
    logging.info("\n=== 测试导入应用程序模块 ===")
    
    try:
        import config
        print(f"✅ config模块导入成功")
        logging.info(f"✅ config模块导入成功")
        print(f"默认模型: {config.DEFAULT_MODEL}")
        logging.info(f"默认模型: {config.DEFAULT_MODEL}")
        print(f"模型路径: {config.MODEL_PATHS}")
        logging.info(f"模型路径: {config.MODEL_PATHS}")
        
        return True
    except Exception as e:
        print(f"❌ config模块导入失败: {str(e)}")
        logging.error(f"❌ config模块导入失败: {str(e)}")
        import traceback
        traceback.print_exc()
        logging.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("=== 开始测试YOLO_parking_car项目 ===")
    logging.info("=== 开始测试YOLO_parking_car项目 ===")
    
    model_ok = test_model_loading()
    app_ok = test_app_import()
    
    print("\n=== 测试结果汇总 ===")
    logging.info("\n=== 测试结果汇总 ===")
    
    if model_ok and app_ok:
        print("✅ 所有测试通过！")
        logging.info("✅ 所有测试通过！")
        sys.exit(0)
    else:
        print("❌ 测试失败！")
        logging.error("❌ 测试失败！")
        sys.exit(1)