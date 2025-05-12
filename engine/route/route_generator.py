from engine.interface import IRouteGenerator
from engine.route import Route
from pathlib import Path
from itertools import product
from engine.env import blacklist


def expand_static_params(nested: list) -> list[str]:
  def extract_group(item):
    if isinstance(item, list) and all(isinstance(i, list) and len(i) > 0 and isinstance(i[0], str) for i in item):
      return [i[0] for i in item]
    if isinstance(item, list) and len(item) == 2 and isinstance(item[0], list) and isinstance(item[1], list):
      prefix = item[0][0] if item[0] and isinstance(item[0][0], str) else ""
      suffixes = expand_static_params(item[1])
      return [f"{prefix}/{s}" for s in suffixes]
    if isinstance(item, list) and len(item) > 0 and isinstance(item[0], str):
      return [item[0]]
    return []

  groups = [extract_group(entry) for entry in nested if extract_group(entry)]
  return ["/".join(p) for p in product(*groups)] if groups else []

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
    if param_groups:
      paths = expand_static_params(param_groups)
      self.replace_route_with_expanded_paths(route, paths)

  def collect_static_param_groups(self, route: Route) -> list[list]:
    param_groups = []
    current = route
    stack: list[Route] = []

    while current.parent:
      current = current.parent
      stack.append(current)

    for parent in reversed(stack):
      if parent.static_params:
        param_groups.append(parent.static_params)

    if route.static_params:
      param_groups.append(route.static_params)

    return param_groups

  def replace_route_with_expanded_paths(self, route: Route, paths: list[str]):
    self.routes.pop(route.name, None)
    for path in paths:
      final_path = self.build_final_path(route.name, path)
      self.routes[final_path] = route
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
