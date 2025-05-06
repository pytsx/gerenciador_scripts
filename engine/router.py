from engine.route import Route
from engine.interface import IRouter
from engine.route_props import RouteProps
from engine.route_builder import RouteBuilder

import flet as ft
from pathlib import Path
from typing import Callable
import re

blacklist = [
  "__pycache__",
  "__"
]

class Router(IRouter): 
  def __init__(self, root: Route) -> None:
    self.root: Route = root
    self.routes: dict[str, Route] = { "/": self.root }
    self.dynamic_routes: list[tuple[re.Pattern, Route, str, Callable[[], list[str]]]] = []
    self.url: str = "/"
    self._build_route_structure(root)

  def error(self, route: Route, ctx: ft.Page, error_message: str) -> list[ft.Control]:
    """
    Retorna uma página de erro personalizada.
    """
    return [
      *RouteBuilder.error(route, RouteProps(ctx, self, props={"error": f"{error_message}"}))
    ]
  
  def try_build_route(self, ctx: ft.Page, error_message: str, route: Route, props: dict = {}) -> list[ft.Control]:
    try: 
      return [*RouteBuilder.build(route, RouteProps(ctx, self, props=props))]
    except Exception as e:
      return self.error(route, ctx, f"{error_message} > {route.name} - {e}")
    
  def navigate(self, ctx: ft.Page, _path: str) -> None:
    """
    Navega para a página correspondente ao caminho fornecido.
    Se o caminho não existir, tenta corresponder a uma rota dinâmica.
    Se ainda não existir, navega para a página de erro (not_found).
    """
    ctx.update()
    self.url = _path
    
    first = ctx.controls[0]
    first.bar_hint_text = self.url
    ctx.controls.clear()
    ctx.add(first)
    
    if _path in self.routes:
      dynamic_route = self.routes[self.url] if not self.routes[self.url].isDynamic else self.routes[self.url].dynamic_route
      route = self.routes[self.url]
      
      if route.isDynamic:
        dynamic_name = dynamic_route.name.split("/")[-1].strip('[]')
        ctx.add(*self.try_build_route(ctx, "Erro ao renderizar o caminho dinâmico", route, props={f"{dynamic_name}": self.url}))
      else:
        ctx.add(*self.try_build_route(ctx, "Erro ao renderizar o caminho estático", route))
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
      
    # Then check dynamic routes
    for pattern, route, _ in self.dynamic_routes:
      if match := pattern.match(path):
        # rota dinâmica encontrada, retorna ela
        return route
        
    return None
  
  def check_path(self, path: Path) -> bool:
    """
    Verifica se o caminho existe nas rotas.
    """
    return path.is_dir() and path.name not in blacklist
  
  def _build_dynamic_route(self, route: Route, path: Path, parent_path: str = "/") -> None:
    if route.isDynamic or route.isDynamic:
      # Extract parameter name from the directory name (e.g., [id] -> id)
      param_name = path.name.strip('[]')
      # Create a regex pattern for this route
      pattern = re.compile(f"^{re.escape(parent_path)}([^/]+)(/.*)?$")

      # Add to dynamic routes
      self.dynamic_routes.append((pattern, route, param_name, route.generate_static_params))
      params = route.generate_static_params()
      
      print(f"Rota dinâmica: {route.name} -> {params}")
      
      for param in params:
        static_path = f"{parent_path}{param}"
        param_route = Route(path.parent / param, route)
        param_route.dynamic_route = route
        param_route.isDynamic = True
        self.routes[static_path] = param_route
        
        
  def _build_route_structure(self, route: Route, parent_path: str = "/") -> None:
    """
    Carrega todos os diretórios de páginas e módulos disponíveis.
    """
    print(f"Carregando rotas: {route.name} -> {parent_path}")
    if not route.dir.is_dir() or not self.check_path(route.dir):
      return
    
    for child in route.dir.iterdir():
      if not self.check_path(child):
        continue
      
      child_route = Route(child, route)
      route_path = f"{parent_path.rstrip('/')}/{child.name}".replace("//", "/")
      
      if child_route.isDynamic or route.isDynamic:
        self._build_dynamic_route(child_route, child, parent_path)
        # # Extract parameter name from the directory name (e.g., [id] -> id)
        # param_name = child.name.strip('[]')
        # # Create a regex pattern for this route
        # pattern = re.compile(f"^{re.escape(parent_path)}([^/]+)(/.*)?$")

        # # Add to dynamic routes
        # self.dynamic_routes.append((pattern, child_route, param_name, child_route.generate_static_params))
        # params = child_route.generate_static_params()
        
        # print(f"Rota dinâmica: {child_route.name} -> {params}")
        
        # for param in params:
        #   static_path = f"{parent_path}{param}"
        #   param_route = Route(child.parent / param, route)
        #   param_route.dynamic_route = child_route
        #   param_route.isDynamic = True
        #   self.routes[static_path] = param_route
      else:
        # Handle static routes
        self.routes[route_path] = child_route
      # Recursively process child directories
      if child.is_dir():
        self._build_route_structure(child_route, route_path)
        
  def __getitem__(self, path: str) -> Route:
    """
    Permite acessar as páginas diretamente pelo caminho.
    """
    return self.get_route(path)
