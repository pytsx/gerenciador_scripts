
from engine.interface import IRouter
import flet as ft

class BaseRouteProps:
    """
    Class to hold route properties for a given route.
    """
    def __init__(
        self, 
        ctx: ft.Page = None,
        router: IRouter = None, 
        children: list[ft.Control] = [], 
        props: dict[str, any] = {}
    ) -> None:
        self.ctx: ft.Page = ctx
        self.router: IRouter = router
        self.children: list[ft.Control] = children 
        self.props: dict[str, any] = props

    def to_dict(self) -> dict[str, any]:
        """
        Converts the BaseRouteProps instance to a dictionary.
        
        Returns:
            Dictionary representation of the BaseRouteProps instance
        """
        return {
            "ctx": self.ctx,
            "router": self.router,
            "children": self.children,
            "props": self.props
        }

    @staticmethod
    def create_static(segment: str, params: dict[str, any] = None) -> 'BaseRouteProps':
        """
        Cria um BaseRouteProps para uso em parâmetros estáticos.
        
        Args:
            segment: Segmento da rota (por exemplo, 'carteiras', 'users')
            params: Parâmetros específicos da rota

        Returns:
            BaseRouteProps com o segmento e parâmetros configurados
        """
        return BaseRouteProps(props={"segment": segment, **(params or {})})
        
    @staticmethod
    def create_static_list(items: list[str]) -> list['BaseRouteProps']:
        """
        Cria uma lista de BaseRouteProps a partir de uma lista de strings.
        
        Args:
            items: Lista de segmentos de rota

        Returns:
            Lista de BaseRouteProps
        """
        return [BaseRouteProps.create_static(item) for item in items]