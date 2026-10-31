"""Tiny example service used to exercise the pipeline templates."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer


def greeting(name):
    name = (name or "world").strip()[:64]
    return {"message": f"hello, {name}"}


class Handler(BaseHTTPRequestHandler):
    server_version = "example"
    sys_version = ""

    def do_GET(self):  # noqa: N802
        body = json.dumps(greeting(self.path.strip("/"))).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
