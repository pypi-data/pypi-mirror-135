import json
from http.server import BaseHTTPRequestHandler
from socketserver import BaseServer
from typing import Dict

from .routes import Route


class ReqHandler(BaseHTTPRequestHandler):
    routes: Dict[str, Route]

    def __init__(
        self, request,
        client_address,
        server,
        # routes: Dict[str, Route]
    ):
        super().__init__(request, client_address, server)
        # self.routes = routes

    def do_GET(self):
        self.send_response(200, message=json.loads('{"status": "all good"}'))
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # get correct function
        foo = self.routes.get(self.path)
        print(self.routes)
        if foo is not None:
            content = foo.endpoint()
            self.wfile.write(json.dumps(content).encode())
        else:
            print("Nothing found")

    @classmethod
    def add_routes(cls, routes: Dict[str, Route]):
        cls.routes = routes
