#!/usr/bin/env python3
"""
全面测试所有API端点和页面的可访问性
"""

import requests
import os
import sys

BASE_URL = 'http://localhost:5000'

# 测试用例：API端点
test_cases_api = [
    ('GET', '/api/health', {}, 200),
    ('POST', '/api/login', {'username': 'test', 'password': 'test'}, 401),  # 预期失败登录
]

# 测试用例：页面
test_cases_pages = [
    ('GET', '/', {}, 200),
    ('GET', '/index.html', {}, 200),
    ('GET', '/dashboard.html', {}, 200),
    ('GET', '/test.html', {}, 200),
]

# 测试用例：静态资源
test_cases_static = [
    ('GET', '/css/style.css', {}, 200),
    ('GET', '/js/api.js', {}, 200),
    ('GET', '/js/auth.js', {}, 200),
    ('GET', '/js/dashboard.js', {}, 200),
]

# 测试用例：可能的错误路径（预期404）
test_cases_error = [
    ('GET', '/nonexistent.html', {}, 404),
    ('GET', '/api/nonexistent', {}, 404),
    ('GET', '/css/nonexistent.css', {}, 404),
    ('GET', '/js/nonexistent.js', {}, 404),
]

def run_test(method, endpoint, data, expected_status):
    """运行单个测试用例"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == 'GET':
            response = requests.get(url, params=data)
        elif method == 'POST':
            response = requests.post(url, json=data)
        else:
            print(f"\n❌ 不支持的请求方法: {method}")
            return False
        
        actual_status = response.status_code
        success = actual_status == expected_status
        
        status_icon = "✅" if success else "❌"
        status_color = "\033[92m" if success else "\033[91m"
        reset_color = "\033[0m"
        
        print(f"\n{status_icon} {method} {url}")
        print(f"   {status_color}预期状态: {expected_status}, 实际状态: {actual_status}{reset_color}")
        
        if not success:
            print(f"   响应内容: {response.text[:100]}...")
        
        return success
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ {method} {url}")
        print(f"   请求失败: {e}")
        return False

def main():
    """主函数，运行所有测试用例"""
    print("🚀 开始全面测试所有API端点和页面...")
    print("=" * 60)
    
    total_success = 0
    total_tests = 0
    
    # 测试API端点
    print("\n📡 测试API端点:")
    print("-" * 40)
    for method, endpoint, data, expected_status in test_cases_api:
        total_tests += 1
        if run_test(method, endpoint, data, expected_status):
            total_success += 1
    
    # 测试页面
    print("\n📄 测试页面:")
    print("-" * 40)
    for method, endpoint, data, expected_status in test_cases_pages:
        total_tests += 1
        if run_test(method, endpoint, data, expected_status):
            total_success += 1
    
    # 测试静态资源
    print("\n📦 测试静态资源:")
    print("-" * 40)
    for method, endpoint, data, expected_status in test_cases_static:
        total_tests += 1
        if run_test(method, endpoint, data, expected_status):
            total_success += 1
    
    # 测试错误路径
    print("\n❌ 测试错误路径（预期404）:")
    print("-" * 40)
    for method, endpoint, data, expected_status in test_cases_error:
        total_tests += 1
        if run_test(method, endpoint, data, expected_status):
            total_success += 1
    
    # 打印测试结果摘要
    print("\n" + "=" * 60)
    print("📊 测试结果摘要:")
    print(f"   总测试用例: {total_tests}")
    print(f"   成功: {total_success}")
    print(f"   失败: {total_tests - total_success}")
    print(f"   成功率: {total_success/total_tests*100:.1f}%")
    print("=" * 60)
    
    if total_success == total_tests:
        print("🎉 所有测试通过！系统运行正常。")
        return 0
    else:
        print("⚠️  部分测试失败，请检查系统配置。")
        return 1

if __name__ == "__main__":
    # 检查是否已安装requests库
    try:
        import requests
    except ImportError:
        print("❌ 未安装requests库，请先运行: pip install requests")
        sys.exit(1)
    
    sys.exit(main())
