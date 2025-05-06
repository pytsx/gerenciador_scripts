"""
Módulo interface: define as interfaces abstratas para Páginas (IPage) e Aplicações (IApp).
IPage: representa contrato para carregamento e renderização de páginas.
"""
# importa Path para manipular diretórios de páginas
from pathlib import Path
# importa ABC e abstractmethod para definição de interfaces
from abc import ABC, abstractmethod
from engine.modules import Module
import re
import flet as ft

class IRoute(ABC):
  """
  Interface abstrata para páginas hierárquicas.
  Cada página deve implementar run(), que recebe um objeto ft.Page
  e retorna um ft.Page configurado.
  """
  def __init__(self, dir: Path, parent: "IRoute" = None):
    # define o diretório pai (opcional)
    self.parent: "IRoute" | None = parent
    # define diretório da página
    self.dir: Path = dir
    # define o nome do diretório
    self.name: str = "/" + ("" if not self.parent else dir.parent.name + "/" + dir.name).replace("app/", "")
    
    self.dynamic_route: "IRoute" = None
    self.curent_path_node = self.name.split("/")[-1]
    
    # verifica se possui algum item entre parentes []
    self.isDynamic: bool = bool(re.search(r"\[(.*?)\]", self.name))

    page_py = dir / "page.py"            # script principal da página
    layout_py = dir / "layout.py"        # define layout custom
    not_found_py = dir / "not_found.py"  # define página de erro
    self.router: IRouter

    # Carrega módulos se os arquivos existirem
    self.page = Module(path=page_py, main="page", funcs=["generate_static_params"]) if page_py.exists() else None 
    self.layout = Module(path=layout_py, main="layout", funcs=[]) if layout_py.exists() else None 
    self.not_found = Module(path=not_found_py, main="not_found", funcs=[]) if not_found_py.exists() else None
        
class IRouter: 
  def __init__(self, root: IRoute) -> None:
    self.root: IRoute = root
    self.routes: dict[str, IRoute] = { "/": self.root }
    self.dynamic_routes: list[tuple[re.Pattern, IRoute, str]] = []
    self.url: str = "/"

  @abstractmethod
  def searchbar(self, page: ft.Page) -> ft.Page:
    """
    Adiciona uma barra de pesquisa à página.
    """
    pass
  
  @abstractmethod
  def navigate(self, ctx: ft.Page, _path: str) -> None:
    """
    Navega para a página correspondente ao caminho fornecido.
    Se o caminho não existir, tenta corresponder a uma rota dinâmica.
    Se ainda não existir, navega para a página de erro (not_found).
    """
    pass
  
  @abstractmethod
  def get_route(self, path: str) -> IRoute:
    """
    Retorna a página correspondente ao caminho fornecido.
    Se o caminho não existir, tenta corresponder a uma rota dinâmica.
    Se ainda não existir, retorna None.
    """
    pass
  
  @abstractmethod
  def check_path(self, path: Path) -> bool:
    """
    Verifica se o caminho existe nas rotas.
    """
    pass
  
  @abstractmethod
  def _build_route_structure(self, page: IRoute, parent_path: str = "/") -> None:
    """
    Carrega todos os diretórios de páginas e módulos disponíveis.
    """
    pass
  
  @abstractmethod
  def __getitem__(self, path: str) -> IRoute:
    """
    Permite acessar as páginas diretamente pelo caminho.
    """
    pass
  