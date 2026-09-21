"""Jev Playground local server.

Serves index.html and proxies requests to api.typesafe.ai so the API key never
reaches the browser and CORS is not an issue.  Standard library only.

    python server.py            # http://localhost:8787
    python server.py 9000       # custom port
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
API_BASE = "https://api.typesafe.ai/v1"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8787


def load_key():
    key = os.environ.get("TYPESAFE_API_KEY")
    if key:
        return key
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("TYPESAFE_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


API_KEY = load_key()


def upstream(method, path, body=None, retries=2):
    """Call TypeSafe; retry 429/529 with exponential backoff. Returns (status, bytes, elapsed_ms)."""
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        API_BASE + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "jev-playground/0.1",
        },
    )
    attempt = 0
    while True:
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read(), (time.perf_counter() - t0) * 1000
        except urllib.error.HTTPError as e:
            elapsed = (time.perf_counter() - t0) * 1000
            payload = e.read()
            if e.code in (429, 529) and attempt < retries:
                time.sleep(0.5 * (2 ** attempt))
                attempt += 1
                continue
            return e.code, payload, elapsed
        except (urllib.error.URLError, TimeoutError) as e:
            elapsed = (time.perf_counter() - t0) * 1000
            return 502, json.dumps({"error": f"upstream unreachable: {e}"}).encode(), elapsed


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (time.strftime("%H:%M:%S"), fmt % args))

    def _send(self, status, body, ctype="application/json", extra=None):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            html = (ROOT / "index.html").read_bytes()
            return self._send(200, html, "text/html; charset=utf-8")
        if self.path == "/api/health":
            return self._send(200, json.dumps({"ok": True, "key_present": bool(API_KEY)}).encode())
        if self.path == "/api/models":
            if not API_KEY:
                return self._send(401, b'{"error":"TYPESAFE_API_KEY not set"}')
            status, body, ms = upstream("GET", "/models")
            return self._send(status, body, extra={"X-Proxy-Elapsed-Ms": f"{ms:.0f}"})
        self._send(404, b'{"error":"not found"}')

    def do_POST(self):
        if self.path != "/api/systemone":
            return self._send(404, b'{"error":"not found"}')
        if not API_KEY:
            return self._send(401, b'{"error":"TYPESAFE_API_KEY not set (put it in .env)"}')
        length = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError as e:
            return self._send(400, json.dumps({"error": f"bad JSON: {e}"}).encode())
        status, payload, ms = upstream("POST", "/systemone", body)
        self._send(status, payload, extra={"X-Proxy-Elapsed-Ms": f"{ms:.0f}"})


if __name__ == "__main__":
    if not API_KEY:
        print("WARNING: TYPESAFE_API_KEY not found in env or .env — requests will fail with 401")
    print(f"Jev Playground  ->  http://localhost:{PORT}")
    try:
        ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        pass
