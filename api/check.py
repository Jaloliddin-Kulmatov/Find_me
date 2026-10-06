"""Vercel function: GET /api/check?username=NAME&sites=GitHub,YouTube"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _core import handle_check  # noqa: E402


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, payload = handle_check(urlparse(self.path).query)
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        # Let Vercel's CDN reuse clean answers for 10 minutes; never cache unclear ones.
        settled = status == 200 and all(
            r["status"] not in ("unknown", "error") for r in payload["results"].values())
        self.send_header("Cache-Control", "public, s-maxage=600, stale-while-revalidate=300" if settled else "no-store")
        self.end_headers()
        self.wfile.write(body)
