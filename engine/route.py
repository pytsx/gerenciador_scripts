
from pathlib import Path                
from engine.modules import Module     
from engine.interface import IRoute, IRouter
from engine.route_builder import RouteBuilder
        
class RouteLevel:
    def __init__(self, level: int = 0) -> None:
        self.level: int = level
        
class RoutePath:
    def __init__(self, path: str = "") -> None:
        self.path: str = path
        self.segments: list[str] = path.split("/")

class Route(IRoute):
    """
    Implementa IPage para carregar e renderizar:
    - Subdiretórios contendo page.py, layout.py, not_found.py
    - Fallback em caso de erro de renderização
    """
    def __init__(self, dir: Path, parent: "Route" = None) -> None:
        super().__init__(dir, parent)  # inicializa children a partir de subdirs
        # Localiza possíveis arquivos de customização:

    def generate_static_params(self) -> list[str]:
        """
        Gera parâmetros estáticos a partir da hierarquia de páginas.
        - Retorna um dicionário com os parâmetros estáticos.
        """
        func = self.page.funcs["generate_static_params"]
        if func is None:
            return []
        result = func()
        if not isinstance(result, list) or not all(isinstance(k, str) for k in result) or not all(isinstance(v, str) for v in result):
            return []
        return [*result]
    

    