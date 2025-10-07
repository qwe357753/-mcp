import os
import json
import sys

# 允许从项目根目录直接运行：python tests/smoke_query.py
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from jdy_client import JDYClient  # noqa: E402


def main():
    app_id = os.getenv("APP_ID")
    entry_id = os.getenv("ENTRY_ID")
    if not app_id or not entry_id:
        print(json.dumps({"ok": False, "error": "APP_ID or ENTRY_ID not set"}))
        return

    client = JDYClient()
    payload = {
        "page": 1,
        "per_page": 1,
        # 如需过滤可在此添加 filter、fields 等，保持与官方文档一致
        # "filter": {},
        # "fields": ["_id"]
    }
    try:
        res = client.query_records(app_id, entry_id, payload)
        print(json.dumps({"ok": True, "data": res}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}))


if __name__ == "__main__":
    main()