from engine import Renderer, Router, RouteGenerator, Route
from env import APP_DIR
from pathlib import Path

class App:
  def __init__(self, name: str, app_path: Path) -> None:
    self.name: str = name
    self.app_path: Path = app_path
    self.renderer: Renderer = Renderer()
    self.app_route: Route = Route(self.app_path, "/")
    self.router_generator: RouteGenerator = RouteGenerator(self.app_route)
    self.router: Router = Router(self.router_generator, self.renderer)
  
  def run(self):
    self.renderer.run(self.router)


app = App("Inteligência Comercial", APP_DIR)


app.run()