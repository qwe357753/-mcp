import os
import json
import sys
import httpx

BASE_URL = (os.getenv("BASE_URL") or "https://api.jiandaoyun.com").rstrip("/")
PATH_QUERY = os.getenv("JDY_PATH_QUERY") or "/api/v1/app/{app_id}/entry/{entry_id}/data"
METHOD = (os.getenv("METHOD") or "POST").upper()

APP_ID = os.getenv("APP_ID")
ENTRY_ID = os.getenv("ENTRY_ID")
TOKEN = os.getenv("JDY_API_TOKEN") or "请输入APIkey"
AUTH_HEADER = os.getenv("JDY_AUTH_HEADER") or "Authorization"
AUTH_SCHEME = os.getenv("JDY_AUTH_SCHEME") or "Bearer"

if not APP_ID or not ENTRY_ID:
    print(json.dumps({"ok": False, "error": "APP_ID or ENTRY_ID not set"}))
    sys.exit(0)

url = f"{BASE_URL}{PATH_QUERY.format(app_id=APP_ID, entry_id=ENTRY_ID)}"
headers = {"Content-Type": "application/json"}
if TOKEN:
    scheme = (AUTH_SCHEME or "").strip()
    if scheme:
        headers[AUTH_HEADER] = f"{scheme} {TOKEN}"
    else:
        headers[AUTH_HEADER] = TOKEN

payload = {"page": 1, "per_page": 1}

try:
    with httpx.Client(timeout=30.0) as client:
        if METHOD == "GET":
            resp = client.get(url, headers=headers, params=payload)
        else:
            resp = client.post(url, headers=headers, json=payload)
        out = {
            "ok": resp.status_code >= 200 and resp.status_code < 400,
            "status": resp.status_code,
            "url": url,
            "method": METHOD,
            "req_headers": headers,
            "resp_text": resp.text,
        }
        print(json.dumps(out, ensure_ascii=False))
except Exception as e:
    print(json.dumps({"ok": False, "error": str(e)}))