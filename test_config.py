#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试配置文件读取
"""

import json
import os

def main():
    print("=== 配置文件读取测试 ===")
    
    # 检查文件是否存在
    if not os.path.exists('db_config.json'):
        print("❌ db_config.json 文件不存在")
        return
    
    # 读取配置文件
    try:
        with open('db_config.json', 'r', encoding='utf-8') as f:
            db_config = json.load(f)
        print("✅ 配置文件读取成功")
        print(f"配置内容: {db_config}")
        print(f"  主机: {db_config['host']}")
        print(f"  用户: {db_config['user']}")
        print(f"  密码: '{db_config['password']}'")
        print(f"  数据库: {db_config['database']}")
        print(f"  密码长度: {len(db_config['password'])}")
    except Exception as e:
        print(f"❌ 配置文件读取失败: {e}")

if __name__ == "__main__":
    main()