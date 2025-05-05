
from pathlib import Path                
from engine.modules import Module     
from engine.interface import IRoute, IRouter
from engine.route_builder import RouteBuilder
        
class Route(IRoute):
    """
    Implementa IPage para carregar e renderizar:
    - Subdiretórios contendo page.py, layout.py, not_found.py
    - Fallback em caso de erro de renderização
    """
    def __init__(self, dir: Path, parent: "Route" = None) -> None:
        super().__init__(dir, parent)  # inicializa children a partir de subdirs
        # Localiza possíveis arquivos de customização:
        page_py = dir / "page.py"            # script principal da página
        layout_py = dir / "layout.py"        # define layout custom
        not_found_py = dir / "not_found.py"  # define página de erro
        self.router: IRouter
        
        self.builder = RouteBuilder(self)  # construtor de rotas

        # Carrega módulos se os arquivos existirem
        self.page = Module(path=page_py, main="page", funcs=["generate_static_params"]) if page_py.exists() else self.page
        self.layout = Module(path=layout_py, main="layout", funcs=[]) if layout_py.exists() else self.layout
        self.not_found = Module(path=not_found_py, main="not_found", funcs=[]) if not_found_py.exists() else self.not_found

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
    

    