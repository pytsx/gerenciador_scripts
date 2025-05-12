"""
Módulo engine.app
Define classes centrais para execução da aplicação Flet:
- Page: representa e renderiza uma página a partir de diretório.
- App: ponto de entrada que inicializa e dispara ft.app().
Também disponibiliza funções default de layout e page.
"""
import flet as ft
from engine.interface import IRenderer
from engine.router import Router
from engine.route import RouteProps, RouteBuilder
from engine.router import RouterSearchbar

class Renderer(IRenderer): 
    def __init__(self) -> None:
        super().__init__()
        self.searchbar: RouterSearchbar = RouterSearchbar()
    
    def clear(self, ctx: ft.Page, router: Router) -> None:
        ctx.controls.clear()
        searchbar: RouterSearchbar = self.searchbar.mount(ctx, router, bar_hint_text=router.url)
        ctx.add(searchbar)  # Adiciona o RouterSearchbar antes de qualquer operação
        searchbar.update()  # Garante que o controle seja atualizado corretamente
    
    def _render(self, ctx: ft.Page, router: Router) -> ft.Page:
        self.clear(ctx, router)
        
        route = router.get_route(router.url)
        components = RouteBuilder.build(route, RouteProps(ctx, router))
        ctx.add(*components)
        
    def run(self, router: Router):
        ft.app(lambda ctx, rt=router:self._render(ctx, rt))

