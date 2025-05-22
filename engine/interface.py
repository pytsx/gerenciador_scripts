"""
Módulo interface: define as interfaces abstratas para Páginas (IPage) e Aplicações (IApp).
IPage: representa contrato para carregamento e renderização de páginas.
"""
# importa Path para manipular diretórios de páginas
from pathlib import Path
# importa ABC e abstractmethod para definição de interfaces
from abc import ABC, abstractmethod
from engine.modules import Module
import flet as ft

class IRoute(ABC):
  """
  Interface abstrata para páginas hierárquicas.
  Cada página deve implementar run(), que recebe um objeto ft.Page
  e retorna um ft.Page configurado.
  """
  def __init__(
    self, 
    name: str, 
    dir: Path, 
    parent: "IRoute" = None,
    
    page: Module = None,
    layout: Module = None,
    not_found: Module = None,
  ):
    # define diretório da página
    self.dir: Path =dir
    self.parent: "IRoute" | None =parent
    # define o nome do diretório
    self.name:str =name
    # define os parâmetros dinâmicos da página
    self.static_params: list[tuple[str, dict]] = []
    
    # Carrega módulos
    self.page:Module  = page
    self.layout:Module = layout
    self.not_found:Module = not_found
  
  @abstractmethod
  def generate_static_params(self) -> list[tuple[str, dict]]:...
  
"""
  [IRouteGenerator]
"""  
class IRouteGenerator(ABC):
  def __init__(self, root: IRoute):
    self.root: IRoute = root
    self.routes: dict[str, IRoute] = {}
  
  @abstractmethod
  def initialize_route_structure(self, path: Path):
    ...
    
  @abstractmethod      
  def establish_route_hierarchy(self):
    ...
    
    
  @abstractmethod
  def normalize_name(self, path: Path) -> str:
    ...
  
class IRenderer(ABC): 
  
  def __init__(self) -> None:
    self.ctx: ft.Page
    ...
    
  @abstractmethod
  def _render(self, ctx: ft.Page, router: "IRouter") -> ft.Page:
    ...
      
  @abstractmethod
  def run(self):
    ...
  
  @abstractmethod
  def clear(self) -> None:
    ...

  @abstractmethod  
  def mount_default_layout(self, router: "IRouter") -> None:
    ...
  
  @abstractmethod
  def render_route(self, router: "IRouter", route: "IRoute") -> None:
    ...
    
  @abstractmethod
  def ensure_ctx(self) -> bool:
    """
    Verifica se o contexto (ctx) está inicializado.
    Se não estiver, lança uma exceção.
    """
    ...
  
"""
  [IRouter]
"""  
      
class IRouter: 
  def __init__(self, route_generator: IRouteGenerator, renderer: IRenderer) -> None:
    self.route_generator: IRouteGenerator = route_generator
    self.renderer: IRenderer = renderer
    self.routes: dict[str, IRoute] = { }
    self.url: str = "/"


  @abstractmethod
  def navigate(self, ctx: ft.Page, _path: str) -> None:
    """
    Navega para a página correspondente ao caminho fornecido.
    Se o caminho não existir, tenta corresponder a uma rota dinâmica.
    Se ainda não existir, navega para a página de erro (not_found).
    """
    ...
  
  @abstractmethod
  def error(self, route: "IRoute", ctx: ft.Page, error_message: str) -> list[ft.Control]:
    """
    Retorna uma página de erro personalizada.
    """
    ...
  
  @abstractmethod
  def get_route(self, path: str) -> IRoute:
    """
    Retorna a página correspondente ao caminho fornecido.
    Se o caminho não existir, tenta corresponder a uma rota dinâmica.
    Se ainda não existir, retorna None.
    """
    ...
  
  @abstractmethod
  def check_path(self, path: Path) -> bool:
    """
    Verifica se o caminho existe nas rotas.
    """
    ...
  
  @abstractmethod
  def __getitem__(self, path: str) -> IRoute:
    """
    Permite acessar as páginas diretamente pelo caminho.
    """
    ...



class GenerateStaticParams(list):
  """Define parâmetros estáticos para uma rota."""
  pass