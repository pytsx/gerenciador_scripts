from engine.route import Route
from engine.interface import IRouter
from engine.route_props import RouteProps

import flet as ft
from pathlib import Path
import re

blacklist = [
  "__pycache__",
  "__"
]


class Router(IRouter): 
  def __init__(self, root: Route) -> None:
    self.root: Route = root
    self.routes: dict[str, Route] = { "/": self.root }
    self.dynamic_routes: list[tuple[re.Pattern, Route, str]] = []
    self.url: str = "/"
    self._load_routes(root)
    print("dynamic_routes", self.dynamic_routes)
    
  
  def error(self, ctx: ft.Page, error_message: str) -> list[ft.Control]:
    """
    Retorna uma página de erro personalizada.
    """
    return [
      *self.root.layout.main(
        RouteProps(
          ctx=ctx, 
          router=self, 
          children=[
            *self.root.not_found.main(
              RouteProps(
                router=self, 
                ctx=ctx,
                props={"error": error_message}
              )
            )
          ] 
        )    
      )
    ]
  
  def try_build_route(self, ctx: ft.Page, error_message: str, route: Route, props: dict = {}) -> list[ft.Control]:
    try: 
      return route.builder.build(ctx, self, props)
    except Exception as e:
      return self.error(ctx, f"{error_message} > {route.name} - {e}")
    
  def navigate(self, _path: str, ctx: ft.Page) -> None:
    """
    Navega para a página correspondente ao caminho fornecido.
    Se o caminho não existir, tenta corresponder a uma rota dinâmica.
    Se ainda não existir, navega para a página de erro (not_found).
    """
    ctx.update()
    first = ctx.controls[0]
    first.bar_hint_text = _path
    ctx.controls.clear()
    ctx.add(first)
    if _path in self.routes:
      self.url = _path
      dynamic_route = self.routes[self.url] if not self.routes[self.url].isDynamic else self.routes[self.url].dynamic_route
      # Clear existing controls before navigating
      # Update current path and run the page
      
      
      
      if dynamic_route.isDynamic:
        dynamic_name = dynamic_route.name.split("/")[-1].strip('[]')
        
        ctx.add(*self.try_build_route(ctx, "Erro ao renderizar o caminho dinâmico", dynamic_route, props={f"{dynamic_name}": self.url}))
      else:
        ctx.add(*self.try_build_route(ctx, "Erro ao renderizar o caminho estático", self.routes[self.url]))

    else:
      # Handle 404 or not found page
      self.error(ctx, "Página não encontrada")
    
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
  
  def _load_routes(self, page: Route, parent_path: str = "/") -> None:
    """
    Carrega todos os diretórios de páginas e módulos disponíveis.
    """
    if not page.dir.is_dir() or not self.check_path(page.dir):
      return
    
    for child in page.dir.iterdir():
      if not self.check_path(child):
        continue
      
      child_route = Route(child, page)
      route_path = f"{parent_path.rstrip('/')}/{child.name}".replace("//", "/")
      
      print(f"Loading route <{route_path}>: {child.name} {child_route.isDynamic} - parent: {parent_path}")
      
      if child_route.isDynamic or page.isDynamic:
        # Extract parameter name from the directory name (e.g., [id] -> id)
        param_name = child.name.strip('[]')
        # Create a regex pattern for this route
        pattern = re.compile(f"^{re.escape(parent_path)}([^/]+)(/.*)?$")

        # Add to dynamic routes
        self.dynamic_routes.append((pattern, child_route, param_name))
        
        params = child_route.generate_static_params()
        for param in params:
          static_path = f"{parent_path}{param}"
          param_route = Route(child.parent / param, page)
          print("param_route", param_route.name)
          param_route.dynamic_route = child_route
          param_route.isDynamic = True
          self.routes[static_path] = param_route
      else:
        # Handle static routes
        self.routes[route_path] = child_route
      # Recursively process child directories
      if child.is_dir():
        self._load_routes(child_route, route_path)
        
  def __getitem__(self, path: str) -> Route:
    """
    Permite acessar as páginas diretamente pelo caminho.
    """
    return self.get_route(path)
