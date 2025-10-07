import json
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from fastmcp import FastMCP

from src.jdy_client import JDYClient

# 加载环境变量
load_dotenv()

app = FastMCP("jdy-mcp")
client = JDYClient()


def _ok(data: Any) -> Dict[str, Any]:
    return {"ok": True, "data": data}


def _err(message: str, detail: Optional[Any] = None) -> Dict[str, Any]:
    return {"ok": False, "error": {"message": message, "detail": detail}}


@app.tool(
    name="query_records",
    description="查询简道云表单数据。参数：app_id、entry_id、payload_json(JSON字符串，按官方文档组织过滤/分页/字段)。",
)
def query_records(
    app_id: str,
    entry_id: str,
    payload_json: Optional[str] = None,
) -> str:
    try:
        payload = json.loads(payload_json) if payload_json else {}
        res = client.query_records(app_id, entry_id, payload)
        return json.dumps(_ok(res), ensure_ascii=False)
    except Exception as e:
        return json.dumps(_err("query_records failed", str(e)), ensure_ascii=False)


@app.tool(
    name="create_record",
    description="在简道云表单新增数据。参数：app_id、entry_id、data_json（JSON字符串，包含 data 字段）。",
)
def create_record(
    app_id: str,
    entry_id: str,
    data_json: str,
) -> str:
    try:
        data = json.loads(data_json) if data_json else {}
        res = client.create_record(app_id, entry_id, data)
        return json.dumps(_ok(res), ensure_ascii=False)
    except Exception as e:
        return json.dumps(_err("create_record failed", str(e)), ensure_ascii=False)


@app.tool(
    name="update_record",
    description="更新简道云表单数据。参数：app_id、entry_id、record_id、data_json（JSON字符串，包含 data 字段，使用批量更新接口）。",
)
def update_record(
    app_id: str,
    entry_id: str,
    record_id: str,
    data_json: str,
) -> str:
    try:
        data = json.loads(data_json) if data_json else {}
        res = client.update_record(app_id, entry_id, record_id, data)
        return json.dumps(_ok(res), ensure_ascii=False)
    except Exception as e:
        return json.dumps(_err("update_record failed", str(e)), ensure_ascii=False)


@app.tool(
    name="delete_record",
    description="删除简道云表单数据。参数：app_id、entry_id、record_id、extra_json（可选JSON字符串，如需附加参数则传）。",
)
def delete_record(
    app_id: str,
    entry_id: str,
    record_id: str,
    extra_json: Optional[str] = None,
) -> str:
    try:
        extra = json.loads(extra_json) if extra_json else {}
        res = client.delete_record(app_id, entry_id, record_id, extra)
        return json.dumps(_ok(res), ensure_ascii=False)
    except Exception as e:
        return json.dumps(_err("delete_record failed", str(e)), ensure_ascii=False)


if __name__ == "__main__":
    # 运行 MCP Server（stdio）
    app.run()