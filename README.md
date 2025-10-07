# 简道云 MCP（Python）

一个基于 Python 的 MCP 服务端，封装简道云开放接口，实现数据增删改查，并以 MCP 工具形式暴露。

## 功能
- query_records：条件查询（使用简道云官方 `/api/v1/app/{app_id}/entry/{entry_id}/data` 接口）
- create_record：新增记录（使用简道云官方 `/api/v1/app/{app_id}/entry/{entry_id}/data` 接口）
- update_record：更新记录（使用简道云官方 `/api/v1/app/{app_id}/entry/{entry_id}/data_update` 接口）
- delete_record：删除记录（使用简道云官方 `/api/v1/app/{app_id}/entry/{entry_id}/data_delete` 接口）

## 安装与运行

1) 克隆或进入本目录后，复制环境变量示例：
```
cp .env.example .env
```
编辑 .env，填写：
- BASE_URL：API 基础域名（默认 https://api.jiandaoyun.com）
- JDY_API_TOKEN：你的简道云开放平台 API Token
- 如官方文档与默认端点不同，请覆盖 JDY_PATH_QUERY/CREATE/UPDATE/DELETE

2) 安装依赖（建议使用 Python 3.10+）：
```
pip install -r requirements.txt
```

3) 运行 MCP Server：
```
python -m src.server
```
或：
```
python src/server.py
```

## 在 MCP 客户端中使用

将该服务注册为命令（stdio）：
- command: python
- args: ["src/server.py"]
- cwd: 本项目目录

随后可调用以下工具：
- query_records(app_id, entry_id, payload_json)
  - payload_json 例如：
    ```
    {
      "filter": {},
      "fields": ["_id","字段A"],
      "page": 1,
      "per_page": 50
    }
    ```
- create_record(app_id, entry_id, data_json)
  - data_json 例如：
    ```
    {
      "data": {
        "字段A": "值",
        "字段B": 123
      }
    }
    ```
- update_record(app_id, entry_id, record_id, data_json)
  - data_json 例如：
    ```
    {
      "data": {
        "字段A": "新值"
      }
    }
    ```
  - 注意：record_id 会自动转换为简道云官方使用的 `_id` 字段
- delete_record(app_id, entry_id, record_id, extra_json?)
  - extra_json 通常可省略；如官方文档需要附加参数可传入
  - 注意：record_id 会自动转换为简道云官方使用的 `_id` 字段

所有工具返回值均为 JSON 字符串：
```
{ "ok": true, "data": ... }
或
{ "ok": false, "error": { "message": "...", "detail": "..." } }
```

## 自定义端点与鉴权
- 若官方文档端点路径不同，修改 .env 中 JDY_PATH_QUERY/CREATE/UPDATE/DELETE。
- 默认使用 Authorization: Bearer 请输入APIkey；可通过 JDY_AUTH_HEADER 与 JDY_AUTH_SCHEME 调整。

## 注意
- 各 API 的 payload 字段格式请以官方文档为准。本项目提供可配置端点与直传 payload 的方式以降低对齐成本。
- 如需 AppId+AppSecret 的签名鉴权，可在 jdy_client.py 中扩展 _headers() 和/或在请求体中加入签名参数逻辑。
