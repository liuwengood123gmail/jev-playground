# Jev Playground

TypeSafe Jev（System One 模型）的本地测试台：原理讲解、三种问题类型、自由 Playground，以及三个场景演示（新闻情绪打分 / 实时家居控制 / 五子棋自动判断）。

## 运行

```bash
python server.py        # 默认 http://localhost:8787
python server.py 9000   # 自定义端口
```

API key 放在 `.env`（`TYPESAFE_API_KEY=...`）或环境变量里；`server.py` 负责加 Bearer 头转发到 `https://api.typesafe.ai/v1`，浏览器永远看不到 key。

## 文件

- `server.py` — 零依赖代理（标准库）：`/` 静态页、`POST /api/systemone`、`GET /api/models`、`GET /api/health`；429/529 自动指数退避重试。
- `index.html` — 单文件页面，原生 JS，无构建。
- `.env` — API key（不要提交到 git）。
