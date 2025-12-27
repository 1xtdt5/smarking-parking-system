import requests
import json
import os

# 测试后端API的完整功能
def test_full_api():
    print("=== 测试完整API功能 ===")
    
    # 1. 测试健康检查接口
    try:
        response = requests.get('http://localhost:5000/api/health')
        if response.status_code == 200:
            result = response.json()
            print("✅ 健康检查接口测试成功")
            print(f"   状态: {result['data']['status']}")
            print(f"   版本: {result['data']['version']}")
        else:
            print(f"❌ 健康检查接口测试失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查接口测试异常: {e}")
        return False
    
    # 2. 测试登录接口
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post('http://localhost:5000/api/login', json=login_data)
        if response.status_code == 200:
            login_result = response.json()
            if login_result['success']:
                print("✅ 登录接口测试成功")
                print(f"   用户名: {login_result['data']['username']}")
                print(f"   角色: {login_result['data']['role']}")
            else:
                print(f"❌ 登录接口测试失败: {login_result['message']}")
                return False
        else:
            print(f"❌ 登录接口测试失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 登录接口测试异常: {e}")
        return False
    
    # 3. 测试检测接口（如果有测试图片）
    test_image_path = "images/0.png"
    if os.path.exists(test_image_path):
        try:
            with open(test_image_path, 'rb') as f:
                files = {'image': f}
                data = {
                    'username': 'admin',
                    'password': 'admin123',
                    'model_version': 'yolov8',
                    'conf_threshold': 0.5
                }
                response = requests.post('http://localhost:5000/api/detect', files=files, data=data)
                if response.status_code == 200:
                    detect_result = response.json()
                    if detect_result['success']:
                        print("✅ 检测接口测试成功")
                        print(f"   模型版本: {detect_result['data']['model_version']}")
                        print(f"   检测总数: {detect_result['data']['summary']['total_boxes']}")
                        print(f"   空闲车位: {detect_result['data']['summary']['empty_count']}")
                        print(f"   占用车位: {detect_result['data']['summary']['occupied_count']}")
                    else:
                        print(f"❌ 检测接口测试失败: {detect_result['message']}")
                else:
                    print(f"❌ 检测接口测试失败，状态码: {response.status_code}")
                    print(f"   响应内容: {response.text}")
        except Exception as e:
            print(f"❌ 检测接口测试异常: {e}")
    else:
        print("ℹ️  未找到测试图片，跳过检测接口测试")
    
    return True

if __name__ == "__main__":
    test_full_api()
