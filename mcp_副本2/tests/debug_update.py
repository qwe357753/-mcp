import os
import json
import httpx

BASE_URL = (os.getenv("BASE_URL") or "https://api.jiandaoyun.com").rstrip("/")
APP_ID = os.getenv("APP_ID") or "64e8652b291f1d0007936647"
ENTRY_ID = os.getenv("ENTRY_ID") or "68ca20c2ba18d1bac9c10173"
TOKEN = os.getenv("JDY_API_TOKEN") or "请输入APIkey"
RECORD_ID = os.getenv("RECORD_ID") or "68e1f82a6a630beffded9b42"
FIELD_KEY = os.getenv("FIELD_KEY") or "_widget_1758077118701"
NEW_VALUE = os.getenv("NEW_VALUE") or "你好，是的（更新探测）"

headers = {"Content-Type": "application/json"}
if TOKEN:
    headers["Authorization"] = f"Bearer {TOKEN}"

def url(path):
    if not path.startswith("/"):
        path = "/" + path
    return f"{BASE_URL}{path.format(app_id=APP_ID, entry_id=ENTRY_ID, record_id=RECORD_ID)}"

payloads = [
    ("POST", "/api/v1/app/{app_id}/entry/{entry_id}/data_update", {"_id": RECORD_ID, "data": {FIELD_KEY: {"value": NEW_VALUE}}}, "A data_update + _id"),
    ("POST", "/api/v1/app/{app_id}/entry/{entry_id}/data_update", {"ids": [RECORD_ID], "data": {FIELD_KEY: {"value": NEW_VALUE}}}, "B data_update + ids"),
    ("POST", "/api/v1/app/{app_id}/entry/{entry_id}/data_update", {"record_id": RECORD_ID, "data": {FIELD_KEY: {"value": NEW_VALUE}}}, "C data_update + record_id"),
    ("POST", "/api/v1/app/{app_id}/entry/{entry_id}/data_update", {"updates": [{"_id": RECORD_ID, "data": {FIELD_KEY: {"value": NEW_VALUE}}}]}, "D data_update + updates[]"),
    ("POST", "/api/v1/app/{app_id}/entry/{entry_id}/data/update", {"_id": RECORD_ID, "data": {FIELD_KEY: {"value": NEW_VALUE}}}, "E data/update + _id"),
    ("POST", "/api/v1/app/{app_id}/entry/{entry_id}/data/update", {"ids": [RECORD_ID], "data": {FIELD_KEY: {"value": NEW_VALUE}}}, "F data/update + ids"),
    ("POST", "/api/v1/app/{app_id}/entry/{entry_id}/data/{record_id}", {"data": {FIELD_KEY: {"value": NEW_VALUE}}}, "G data/{id} POST + data"),
    ("PUT",  "/api/v1/app/{app_id}/entry/{entry_id}/data/{record_id}", {"data": {FIELD_KEY: {"value": NEW_VALUE}}}, "H data/{id} PUT + data"),
]

out = []
with httpx.Client(timeout=30.0) as client:
    for method, path, body, label in payloads:
        try:
            if method == "GET":
                resp = client.get(url(path), headers=headers)
            elif method == "PUT":
                resp = client.put(url(path), headers=headers, json=body)
            else:
                resp = client.post(url(path), headers=headers, json=body)
            out.append({
                "label": label,
                "method": method,
                "path": path,
                "status": resp.status_code,
                "text": resp.text[:500]
            })
        except Exception as e:
            out.append({
                "label": label,
                "error": str(e)
            })

print(json.dumps(out, ensure_ascii=False, indent=2))