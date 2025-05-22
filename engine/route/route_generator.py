from engine.interface import IRouteGenerator
from engine.route import Route
from pathlib import Path
from engine.route.route_props import BaseRouteProps
from engine.env import blacklist


def expand_static_params(param_groups: list[BaseRouteProps]) -> list[str]:
  """
  Extrai os segmentos de rota de uma lista de listas de BaseRouteProps.
  
  Args:
      param_groups: Lista de listas de BaseRouteProps com segmentos definidos
      
  Returns:
      Lista de strings representando os segmentos de rota
  """
  segments = []
  for group in param_groups:
    if isinstance(group, list):
      for props in group:
        if hasattr(props, 'props') and props.props.get("segment"):
          segments.append(props.props.get("segment", ""))
    elif hasattr(group, 'props') and group.props.get("segment"):
      segments.append(group.props.get("segment", ""))
  return segments

class RouteGenerator(IRouteGenerator):
  def __init__(self, root: Route):
    super().__init__(root)
    self.routes = {}
    self.initialize_route_structure(self.root.dir)
    self.establish_route_hierarchy()
    self.process_all_static_params()

  def process_all_static_params(self):
    routes_copy = list(self.routes.values())
    
    for route in routes_copy:
      self.resolve_static_params(route)

  def resolve_static_params(self, route: Route):
    param_groups = self.collect_static_param_groups(route)
    print(f"[resolve_static_params] {route.name} -> {param_groups}")
    if param_groups:
      paths = expand_static_params(param_groups)
      print(f"[resolve_static_params] {route.name} -> {paths}")
      self.replace_route_with_expanded_paths(route, paths)

  def collect_static_param_groups(self, route: Route) -> list[list]:
    """Coleta grupos de parâmetros estáticos da hierarquia de rotas"""
    param_groups = []
    current = route
    stack: list[Route] = []

    while current.parent:
      current = current.parent
      stack.append(current)

    for parent in reversed(stack):
      if parent.static_params:
        # Adiciona cada BaseRouteProps individualmente à lista plana
        if isinstance(parent.static_params, list):
          param_groups.extend(parent.static_params)
        else:
          param_groups.append(parent.static_params)

    if route.static_params:
      # Adiciona os parâmetros da rota atual
      if isinstance(route.static_params, list):
        param_groups.extend(route.static_params)
      else:
        param_groups.append(route.static_params)

    return param_groups

  def replace_route_with_expanded_paths(self, route: Route, paths: list[str]):
    """
    Substitui uma rota com parâmetros por rotas expandidas.
    
    Args:
        route: A rota original 
        paths: Os caminhos expandidos
    """
    # Remove a rota original
    self.routes.pop(route.name, None)
    
    # Adiciona uma rota para cada caminho expandido
    for path in paths:
        final_path = self.build_final_path(route.name, path)
        new_route = Route(route.dir, name=final_path)
        new_route.page = route.page
        new_route.layout = route.layout
        new_route.not_found = route.not_found
        new_route.parent = route.parent
        
        # Encontra o BaseRouteProps correspondente a este path
        matching_props = next(
            (props for props in route.static_params if props.props.get("segment") == path),
            BaseRouteProps(props={"segment": path})  # fallback
        )
        
        # Guarda os parâmetros originais para quando a rota for construída
        new_route.original_props = matching_props
        self.routes[final_path] = new_route
        print(f"[resolve_static_params] {route.name} -> {final_path}")

  def build_final_path(self, base_name: str, path: str) -> str:
    base_parts = base_name.strip("/").split("/")
    value_parts = path.strip("/").split("/")
    final_parts = []

    vi = 0
    for part in base_parts:
      if part.startswith("[") and part.endswith("]") and vi < len(value_parts):
        final_parts.append(value_parts[vi])
        vi += 1
      else:
        final_parts.append(part)

    final_parts.extend(value_parts[vi:])
    return "/" + "/".join(final_parts)

  def initialize_route_structure(self, path: Path, parent: Route = None):
    if not self.is_valid_directory(path):
      return

    name = self.normalize_name(path)
    self.routes[name] = type(self.root)(path, name=name)
    if parent:
      self.routes[name].parent = parent

    for sub_route in path.iterdir():
      if self.is_valid_directory(sub_route):
        self.initialize_route_structure(sub_route, self.routes[name])

  def establish_route_hierarchy(self):
    for route in self.routes.values():
      route.parent = self.routes.get(self.normalize_name(route.dir.parent), None)

  def is_valid_directory(self, path: Path) -> bool:
    return path.is_dir() and path.name not in blacklist

  def normalize_name(self, path: Path) -> str:
    return str(path.absolute()).replace(str(self.root.dir.absolute()), "/").replace("\\", "/").replace("//", "/")
