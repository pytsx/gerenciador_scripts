from pathlib import Path
from engine.router.router import Router
from engine.route.route import Route
from engine.router.router_searchbar import RouterSearchbar
from engine.route.route_generator import RouteGenerator
from engine.renderer import Renderer
from engine.cli import initialize_with_cli

class App:
  def __init__(self, name: str, app_path: Path) -> None:
    self.name:str=name
    self.app_path:Path=app_path
    
  def initialize_application(self):
    searchbar = RouterSearchbar()
    
    self.renderer:Renderer=Renderer(searchbar=searchbar)
    
    self.app_route:Route=Route(self.app_path, "/")
    
    self.router_generator:RouteGenerator=RouteGenerator(self.app_route)
    self.router:Router=Router(self.router_generator, self.renderer)
    
    self.renderer.run(self.router)
    
  def run(self):
    """
    Run the app with the given parameters.
    Args:
        when_started (callable, optional): Function to call when the app starts.
        when_stopped (callable, optional): Function to call when the app stops.
        before_render (callable, optional): Function to call before rendering.
        after_render (callable, optional): Function to call after rendering.
    """
    initialize_with_cli(self.initialize_application)
    
    
__all__ = ["App"]