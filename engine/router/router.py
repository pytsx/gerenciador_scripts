from engine.route import Route, BaseRouteProps, RouteBuilder, RouteGenerator
from engine.interface import IRouter, IRenderer

import flet as ft
from pathlib import Path

from engine.env import blacklist

def extract_name_from_path(remove: Path, from_path: Path) -> str: 
  return f"{from_path.absolute()}".replace(f"{remove.absolute()}", "/").replace("\\", "/").replace("//", "/")

class Router(IRouter): 
  def __init__(self, route_generator: RouteGenerator, renderer: IRenderer) -> None:
    super().__init__(route_generator, renderer)
    self.routes = route_generator.routes
    self.url: str = "/"

  def error(self, route: Route, ctx: ft.Page, error_message: str):
    return [
      *RouteBuilder.error(route, BaseRouteProps(ctx, self, props={"error": f"{error_message}"}))
    ]
    
  def remount_default_layout(self, ctx: ft.Page) -> None:
    ctx.update()
    first: ft.SearchBar = ctx.controls[0]
    first.bar_hint_text = self.url
    ctx.controls.clear()
    ctx.add(first)

  def navigate(self, _path: str) -> None:
    self.url = _path
    # self.remount_default_layout(ctx)
    
    self.renderer.clear()
    self.renderer.mount_default_layout(self)
    
    if _path in self.routes:
      route = self.routes[self.url]
      self.renderer.ctx.add(*RouteBuilder.build(
        route, 
        BaseRouteProps(
            ctx=self.renderer.ctx, 
            router=self, 
            props=self.match_dynamic_segments(route.name, self.url)
          )
        )
      )
    else:
      # Handle 404 or not found page
      self.error(self.route_generator.root, self.renderer.ctx, "Página não encontrada")

  
  def match_dynamic_segments(self, path_template: str, resolved_path: str) -> dict:
    keys = path_template.strip("/").split("/")
    values = resolved_path.strip("/").split("/")

    return {
      f"{k.strip("[]")}": v for k, v in zip(keys, values)
      if k.startswith("[") and k.endswith("]")
    }
    
  def get_route(self, path: str) -> Route:
    if path in self.routes:
      return self.routes[path]
    
    return None
  
  def check_path(self, path: Path) -> bool:
    return path.is_dir() and path.name not in blacklist
  
  def __getitem__(self, path: str) -> Route:
    return self.get_route(path)
