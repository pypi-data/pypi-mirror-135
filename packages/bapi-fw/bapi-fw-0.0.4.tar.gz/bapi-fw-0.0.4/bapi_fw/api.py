from http.server import HTTPServer
from typing import Callable, Dict, Optional

from .routes import Route
from .request_handler import ReqHandler


class API():
    def __init__(self) -> None:
        self.server: HTTPServer
        self.serverinfo: Dict = {}
        self.routes = {}

    def get(self, path: str, status_code: int = 200):  # , name: Optional[str]):
        def decorated(func: Callable):
            route = Route(
                path=path,
                endpoint=func,
                # name=name,
                method='GET',
                status_code=status_code
            )
            self.routes[route.path] = route
            return func
        return decorated

    def run(self, host: str, port: int = 8000):
        ReqHandler.add_routes(self.routes)
        self.server = HTTPServer(
            server_address=(host, port),
            RequestHandlerClass=ReqHandler
        )
        self.serverinfo["host"] = host
        self.serverinfo["port"] = port
        try:
            self.server.serve_forever()
        except KeyboardInterrupt as e:
            print("\nShutting down server.")
            self.server.shutdown()
