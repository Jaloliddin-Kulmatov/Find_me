"""Vercel function: GET /api/sites - the list of platforms that get checked."""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _core import list_sites  # noqa: E402


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps(list_sites()).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "public, s-maxage=3600")
        self.end_headers()
        self.wfile.write(body)
