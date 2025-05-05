from engine.renderer import Renderer
from engine.router import Router
from engine.route import Route
from env import APP_DIR

Renderer(
  Router(
    Route(APP_DIR)
  )
).run()
