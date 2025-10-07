import os
import time
from typing import Any, Dict, Optional

import httpx
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()


class JDYClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        auth_header: Optional[str] = None,
        auth_scheme: Optional[str] = None,
        timeout_seconds: Optional[float] = None,
        retry_times: Optional[int] = None,
        retry_backoff_seconds: Optional[float] = None,
        path_query: Optional[str] = None,
        path_create: Optional[str] = None,
        path_update: Optional[str] = None,
        path_delete: Optional[str] = None,
    ):
        self.base_url = (base_url or os.getenv("BASE_URL") or "https://api.jiandaoyun.com").rstrip("/")
        self.token = token or os.getenv("JDY_API_TOKEN") or ""
        self.auth_header = auth_header or os.getenv("JDY_AUTH_HEADER") or "Authorization"
        self.auth_scheme = auth_scheme or os.getenv("JDY_AUTH_SCHEME") or "Bearer"
        self.timeout_seconds = float(timeout_seconds or os.getenv("HTTP_TIMEOUT_SECONDS") or 30)
        self.retry_times = int(retry_times or os.getenv("RETRY_TIMES") or 2)
        self.retry_backoff_seconds = float(retry_backoff_seconds or os.getenv("RETRY_BACKOFF_SECONDS") or 1.0)
        


        self.path_query = path_query or os.getenv("JDY_PATH_QUERY") or "/api/v1/app/{app_id}/entry/{entry_id}/data"
        self.path_create = path_create or os.getenv("JDY_PATH_CREATE") or "/api/v1/app/{app_id}/entry/{entry_id}/data"
        self.path_update = path_update or os.getenv("JDY_PATH_UPDATE") or "/api/v1/app/{app_id}/entry/{entry_id}/data_update"
        self.path_delete = path_delete or os.getenv("JDY_PATH_DELETE") or "/api/v1/app/{app_id}/entry/{entry_id}/data_delete"

        self._client = httpx.Client(timeout=self.timeout_seconds)

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
        }
        if self.token:
            headers[self.auth_header] = f"{self.auth_scheme} {self.token}".strip()
        return headers

    def _url(self, path_template: str, app_id: str, entry_id: str) -> str:
        path = path_template.format(app_id=app_id, entry_id=entry_id)
        if not path.startswith("/"):
            path = "/" + path
        return f"{self.base_url}{path}"

    def _request_with_retry(self, method: str, url: str, json: Optional[Dict[str, Any]] = None) -> httpx.Response:
        last_exc: Optional[Exception] = None
        for attempt in range(self.retry_times + 1):
            try:
                resp = self._client.request(method, url, headers=self._headers(), json=json)
                # 认为 2xx/3xx 正常，其它根据需要在这里扩展
                if resp.status_code >= 200 and resp.status_code < 400:
                    return resp
                # 临时错误重试（如 429/5xx）
                if resp.status_code in (429, 500, 502, 503, 504) and attempt < self.retry_times:
                    time.sleep(self.retry_backoff_seconds * (2 ** attempt))
                    continue
                resp.raise_for_status()
                return resp
            except Exception as e:
                last_exc = e
                if attempt < self.retry_times:
                    time.sleep(self.retry_backoff_seconds * (2 ** attempt))
                    continue
                raise e
        # 理论不会到达
        if last_exc:
            raise last_exc
        raise RuntimeError("Unknown request failure")

    # 查询数据
    def query_records(
        self,
        app_id: str,
        entry_id: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        payload 示例（需按官方文档组装）：
        {
          "filter": {...},
          "fields": ["_id","字段A",...],
          "page": 1,
          "per_page": 50,
          "order_by": ...
        }
        """
        url = self._url(self.path_query, app_id, entry_id)
        resp = self._request_with_retry("POST", url, json=payload or {})
        return resp.json()

    # 新增数据（使用v5版本API）
    def create_record(
        self,
        app_id: str,
        entry_id: str,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        使用v5版本API创建单条记录
        data 示例：
        {
            "_widget_字段ID": {"value": "字段值"}
        }
        """
        # 使用v5版本API
        url = f"{self.base_url}/api/v5/app/entry/data/create"
        body = {
            "app_id": app_id,
            "entry_id": entry_id,
            "data": data
        }
        resp = self._request_with_retry("POST", url, json=body)
        return resp.json()

    # 更新数据（使用v5版本API）
    def update_record(
        self,
        app_id: str,
        entry_id: str,
        record_id: str,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        使用v5版本API更新单条记录
        data 示例：
        {
            "_widget_字段ID": {"value": "字段值"}
        }
        """
        # 使用v5版本API
        url = f"{self.base_url}/api/v5/app/entry/data/update"
        body = {
            "app_id": app_id,
            "entry_id": entry_id,
            "data_id": record_id,
            "data": data
        }
        resp = self._request_with_retry("POST", url, json=body)
        return resp.json()

    # 删除数据（使用v5版本API）
    def delete_record(
        self,
        app_id: str,
        entry_id: str,
        record_id: str,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        使用v5版本API删除单条记录
        """
        # 使用v5版本API
        url = f"{self.base_url}/api/v5/app/entry/data/delete"
        body = {
            "app_id": app_id,
            "entry_id": entry_id,
            "data_id": record_id
        }
        # 合并额外参数
        if extra:
            body.update(extra)
        resp = self._request_with_retry("POST", url, json=body)
        return resp.json()