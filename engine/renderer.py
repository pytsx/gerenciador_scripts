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
from engine.route import Route
from engine.route import BaseRouteProps, RouteBuilder
from engine.router import RouterSearchbar

def match_dynamic_segments(path_template: str, resolved_path: str) -> dict:
    keys = path_template.strip("/").split("/")
    values = resolved_path.strip("/").split("/")

    return {
      f"{k.strip("[]")}": v for k, v in zip(keys, values)
      if k.startswith("[") and k.endswith("]")
    }
    
class Renderer(IRenderer): 
    def __init__(self, searchbar: RouterSearchbar) -> None:
        super().__init__()
        self._searchbar = searchbar
        self.ctx: ft.Page = None
        
    
    def ensure_ctx(self) -> bool:
        if self.ctx is None:
            raise Exception("Context not initialized. Please run the app first.")
        return True
    
    def clear(self) -> None:
        if self.ensure_ctx():
            self.ctx.controls.clear()
    
    def mount_default_layout(self, router: Router) -> None:
        if self.ensure_ctx():
            searchbar = self._searchbar.mount(self.ctx, router, bar_hint_text=router.url)
            self.ctx.add(searchbar)  # Adiciona o RouterSearchbar antes de qualquer operação
            searchbar.update()  # Garante que o controle seja atualizado corretamente
        
    def render_route(self, router: Router, route: Route) -> None:
        if self.ensure_ctx():
            self.ctx.add(*RouteBuilder.build(
                    route, 
                    BaseRouteProps(
                        ctx=self.ctx, 
                        router=router, 
                        props=match_dynamic_segments(route.name, router.url)
                    )
                )
            )
    
    def _render(self, ctx: ft.Page, router: Router) -> ft.Page:
        self.ctx = ctx
        
        self.clear()
        self.mount_default_layout(router)
        
        route = router.get_route(router.url)
        self.render_route(router, route)
        
    def run(self, router: Router):
        ft.app(lambda ctx, rt=router:self._render(ctx, rt), host="localhost", port=8080)

