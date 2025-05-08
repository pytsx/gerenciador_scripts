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
  def __init__(
    self, 
    name: str, 
    dir: Path, 
    parent: "IRoute" = None,
    curent_path_node: str = None,
    page: Module = None,
    layout: Module = None,
    not_found: Module = None,
  ):
    # define diretório da página
    self.dir: Path =dir
    # define o diretório pai (opcional)
    self.parent: "IRoute" | None =parent
    # define o nome do diretório
    self.name:str =name
    
    self.curent_path_node:str =curent_path_node
    
    self.static_params: list[tuple[str, dict]] = []

    self.router: IRouter
    # Carrega módulos se os arquivos existirem
    self.page:Module  = page
    self.layout:Module = layout
    self.not_found:Module = not_found
        
class IRouter: 
  def __init__(self, root: IRoute) -> None:
    self.root: IRoute = root
    self.routes: dict[str, IRoute] = { "/": self.root }
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
  def _construct_route_hierarchy(self, page: IRoute, parent_path: str = "/") -> None:
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
  