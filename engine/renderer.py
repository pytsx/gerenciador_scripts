"""
Módulo engine.app
Define classes centrais para execução da aplicação Flet:
- Page: representa e renderiza uma página a partir de diretório.
- App: ponto de entrada que inicializa e dispara ft.app().
Também disponibiliza funções default de layout e page.
"""
import flet as ft
from engine.router import Router
from engine.route_props import RouteProps
from engine.router_searchbar import RouterSearchbar
from engine.route_builder import RouteBuilder

class Renderer: 
    def __init__(self, router: Router) -> None:
        self.router: Router = router
    
    def _render(self, ctx: ft.Page) -> ft.Page:
        route = self.router.get_route(self.router.url)
        ctx.add(RouterSearchbar(ctx=ctx, router=self.router, bar_hint_text=self.router.url))
        ctx.add(*[*RouteBuilder.build(route, RouteProps(ctx, self.router))])
    
    def run(self):
        ft.app(self._render)
        
