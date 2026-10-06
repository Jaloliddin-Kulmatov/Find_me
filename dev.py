#!/usr/bin/env python3
"""Run Find_me locally, the same way Vercel serves it.

    python3 dev.py        then open http://localhost:8765

Static files come from public/, and /api/<name> runs the handler in api/<name>.py,
exactly like Vercel's Python functions.
"""
import importlib.util
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", 8765))
_functions = {}


def load_function(name):
    if name not in _functions:
        path = os.path.join(ROOT, "api", f"{name}.py")
        if name.startswith("_") or not os.path.isfile(path):
            return None
        spec = importlib.util.spec_from_file_location(f"api_{name}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _functions[name] = module.handler
    return _functions[name]


class DevHandler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=os.path.join(ROOT, "public"), **kw)

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        path = urlparse(self.path).path
        if path.startswith("/api/"):
            fn = load_function(path[len("/api/"):].strip("/"))
            if fn is None:
                return self.send_error(404, "No such API function")
            return fn.do_GET(self)
        return super().do_GET()


if __name__ == "__main__":
    print(f"Find_me running at http://localhost:{PORT}")
    ThreadingHTTPServer(("127.0.0.1", PORT), DevHandler).serve_forever()
