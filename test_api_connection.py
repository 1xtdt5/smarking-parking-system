import requests

# 测试后端API连接
def test_api_connection():
    print("=== 测试前后端通信 ===")
    
    # 测试健康检查接口
    try:
        response = requests.get('http://localhost:5000/api/health')
        if response.status_code == 200:
            result = response.json()
            print("✅ 健康检查接口测试成功")
            print(f"   状态: {result['data']['status']}")
            print(f"   版本: {result['data']['version']}")
            return True
        else:
            print(f"❌ 健康检查接口测试失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查接口测试异常: {e}")
        return False

if __name__ == "__main__":
    test_api_connection()
