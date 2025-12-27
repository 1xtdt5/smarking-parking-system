from yolo_db.db_manager import DBManager

def verify_database_results():
    """验证数据库中的检测结果"""
    print("\n" + "="*60)
    print("验证数据库检测结果")
    print("="*60)
    
    # 初始化数据库管理器
    db = DBManager()
    
    try:
        # 查询最近的检测结果
        success, results = db.get_detection_results(limit=10, offset=0)
        
        if success and results:
            print(f"✅ 查询到 {len(results)} 条检测结果")
            print("\n最近的检测结果：")
            print(f"{'ID':<5} {'图像路径':<60} {'车辆数':<6} {'模型版本':<8} {'创建人':<8} {'创建时间':<20}")
            print("-" * 120)
            
            for result in results:
                # 获取检测框
                box_success, boxes = db.get_detection_boxes(result['id'])
                
                print(f"{result['id']:<5} {result['image_path']:<60} {result['vehicle_count']:<6} {result['model_version']:<8} {result['username']:<8} {result['detection_time']:<20}")
                
                if box_success and boxes:
                    print(f"      检测框: {len(boxes)} 个")
                    # 打印前3个检测框示例
                    for i, box in enumerate(boxes[:3], 1):
                        print(f"        [{i}] {box['class_name']} ({box['confidence']:.2f}) - [{box['x1']:.0f},{box['y1']:.0f},{box['x2']:.0f},{box['y2']:.0f}]")
                    if len(boxes) > 3:
                        print(f"        ... 等 {len(boxes)-3} 个检测框")
        else:
            print("❌ 未查询到检测结果")
            
    except Exception as e:
        print(f"❌ 验证过程中发生错误: {e}")

if __name__ == "__main__":
    verify_database_results()