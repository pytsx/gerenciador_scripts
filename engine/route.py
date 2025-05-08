
from pathlib import Path                
from engine.modules import Module     
from engine.interface import IRoute
import re

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
    def __init__(self, dir: Path, parent: "Route" = None, name:str=None) -> None:
        page_py=dir / "page.py"            # script principal da página
        layout_py=dir / "layout.py"        # define layout custom
        not_found_py=dir / "not_found.py"  # define página de erro
        _name=dir.name.replace("app/", "/")

        super().__init__(
            name=_name,
            dir=dir, 
            parent=parent,
            curent_path_node=_name.split("/")[-1],
            page=Module(path=page_py, main="page", funcs=["generate_static_params", "generate_metadata"]) if page_py.exists() else None,
            layout=Module(path=layout_py, main="layout", funcs=[]) if layout_py.exists() else None,
            not_found=Module(path=not_found_py, main="not_found", funcs=[]) if not_found_py.exists() else None,
            
        ) 
        self.generate_static_params()


    def generate_static_params(self) -> list[tuple[str, dict]]:
        """
        Gera parâmetros estáticos a partir da hierarquia de páginas.
        - Retorna um dicionário com os parâmetros estáticos.
        """
        func = self.page.funcs["generate_static_params"]
        if func is None:
            return []
        result = func()
        if not isinstance(result, list):
            return []
        self.static_params = result
        return [*result]