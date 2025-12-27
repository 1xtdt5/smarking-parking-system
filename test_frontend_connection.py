import requests
import json

# 测试登录API
def test_login():
    print("测试登录API...")
    url = "http://100.95.145.222:5000/api/login"
    headers = {"Content-Type": "application/json"}
    data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()
        print(f"登录结果: {result}")
        return result
    except Exception as e:
        print(f"登录API测试失败: {e}")
        return None

# 测试健康检查API
def test_health_check():
    print("\n测试健康检查API...")
    url = "http://100.95.145.222:5000/api/health"
    
    try:
        response = requests.get(url)
        result = response.json()
        print(f"健康检查结果: {result}")
        return result
    except Exception as e:
        print(f"健康检查API测试失败: {e}")
        return None

if __name__ == "__main__":
    print("开始测试前后端连接...")
    test_health_check()
    test_login()