#!/usr/bin/env python3
"""
测试简道云批量更新功能
根据官方文档：https://hc.jiandaoyun.com/open/14225
"""

import json
import os
import sys

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.jdy_client import JDYClient

def test_batch_update():
    """测试批量更新功能"""
    client = JDYClient()
    
    # 使用调试脚本中的实际参数
    app_id = "64e8652b291f1d0007936647"
    entry_id = "68ca20c2ba18d1bac9c10173"
    
    # 先查询数据
    print("=== 查询现有数据 ===")
    try:
        query_result = client.query_records(app_id, entry_id, {
            "fields": ["_id", "_widget_1758077118701", "_widget_1758077118702"],
            "per_page": 10
        })
        print(f"查询结果: {json.dumps(query_result, ensure_ascii=False, indent=2)}")
        
        # 获取第一条记录的ID用于测试
        if query_result.get("data") and len(query_result["data"]) > 0:
            record_id = query_result["data"][0]["_id"]
            print(f"找到记录ID: {record_id}")
            
            # 测试更新
            print("\n=== 测试更新数据 ===")
            update_data = {
                "_widget_1758077118701": {"value": "山东高速"},
                "_widget_1758077118702": {"value": "济宁发展"}
            }
            
            update_result = client.update_record(app_id, entry_id, record_id, update_data)
            print(f"更新结果: {json.dumps(update_result, ensure_ascii=False, indent=2)}")
            
        else:
            print("没有找到数据记录")
            
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    test_batch_update()