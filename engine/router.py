from engine.route import Route
from engine.interface import IRouter
from engine.route_props import RouteProps
from engine.route_builder import RouteBuilder

import flet as ft
from pathlib import Path
from env import APP_DIR
import re

blacklist = [
  "__pycache__",
  "__"
]

def extract_name_from_path(remove: Path, from_path: Path) -> str: 
  return f"{from_path.absolute()}".replace(f"{remove.absolute()}", "/").replace("\\", "/").replace("//", "/")

class Router(IRouter): 
  def __init__(self, root: Route) -> None:
    self.root: Route = root
    
    root_path = "/"
    self.routes: dict[str, Route] = { f"{root_path}": self.root }
    self.static_params: dict[str, list[str]] = { "/": ["/"]}
    self.url: str = root_path
    
    sub_routes = [Route(sub_route) for sub_route in self.root.dir.rglob("*") if sub_route.is_dir() and self.check_path(sub_route)]
    
    for sub_route in sub_routes:
      sub_route.parent = self.routes[extract_name_from_path(root.dir, sub_route.dir.parent)]
      sub_route_name = extract_name_from_path(root.dir, sub_route.dir)
      self.routes[f"{sub_route_name}"] = sub_route
      self.static_params[sub_route_name] = [*sub_route.parent.static_params, *sub_route.static_params]
    
    for route, static_routes in self.static_params.items():
      last_dynamic = [dynamic_route for dynamic_route in route.split("/") if dynamic_route.startswith("[") and dynamic_route.startswith("]")]
      print("[Router] last_dynamic", last_dynamic)
      if len(last_dynamic) == 0:
        continue
      for static_route in static_routes:
        name = route.replace(f"[{last_dynamic}]", static_route)
        self.routes[name] = route

    print("[Router]")
    print("  root", self.root.dir)
    print("  routes", (self.routes))
    print("  static_params", (self.static_params))
    print("  sub_routes", (sub_routes))
    
  def error(self, route: Route, ctx: ft.Page, error_message: str) -> list[ft.Control]:
    """
    Retorna uma página de erro personalizada.
    """
    return [
      *RouteBuilder.error(route, RouteProps(ctx, self, props={"error": f"{error_message}"}))
    ]
  
  def navigate(self, ctx: ft.Page, _path: str) -> None:
    """
    Navega para a página correspondente ao caminho fornecido.
    Se o caminho não existir, tenta corresponder a uma rota dinâmica.
    Se ainda não existir, navega para a página de erro (not_found).
    """
    ctx.update()
    self.url = _path
    
    print("[navigate]", _path)
    
    first = ctx.controls[0]
    first.bar_hint_text = self.url
    ctx.controls.clear()
    ctx.add(first)
    
    if _path in self.routes:
      route = self.routes[self.url]
      print("[navigate] ### ", route.name)
      ctx.add(*RouteBuilder.build(route, RouteProps(ctx, self, props={"script": "carteiras"})))
    else:
      # Handle 404 or not found page
      self.error(self.root, ctx, "Página não encontrada")

    
  def get_route(self, path: str) -> Route:
    """
    Retorna a página correspondente ao caminho fornecido.
    Se o caminho não existir, tenta corresponder a uma rota dinâmica.
    Se ainda não existir, retorna None.
    """
    # First check static routes
    if path in self.routes:
      return self.routes[path]
    
    return None
  
  def check_path(self, path: Path) -> bool:
    """
    Verifica se o caminho existe nas rotas.
    """
    return path.is_dir() and path.name not in blacklist
  
  def __getitem__(self, path: str) -> Route:
    """
    Permite acessar as páginas diretamente pelo caminho.
    """
    return self.get_route(path)
