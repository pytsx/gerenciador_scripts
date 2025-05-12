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
from engine.route import RouteProps, RouteBuilder
from engine.router import RouterSearchbar

def match_dynamic_segments(path_template: str, resolved_path: str) -> dict:
    keys = path_template.strip("/").split("/")
    values = resolved_path.strip("/").split("/")

    return {
      f"{k.strip("[]")}": v for k, v in zip(keys, values)
      if k.startswith("[") and k.endswith("]")
    }
    
class Renderer(IRenderer): 
    def __init__(self) -> None:
        super().__init__()
        self.searchbar: RouterSearchbar = RouterSearchbar()
    
    def clear(self, ctx: ft.Page) -> None:
        ctx.controls.clear()
    
    def mount_default_layout(self, ctx: ft.Page, router: Router) -> None:
        searchbar: RouterSearchbar = self.searchbar.mount(ctx, router, bar_hint_text=router.url)
        ctx.add(searchbar)  # Adiciona o RouterSearchbar antes de qualquer operação
        searchbar.update()  # Garante que o controle seja atualizado corretamente
        
    def render_route(self, ctx: ft.Page, router: Router, route: Route) -> None:
        ctx.add(*RouteBuilder.build(
                route, 
                RouteProps(
                    ctx=ctx, 
                    router=self, 
                    props=match_dynamic_segments(route.name, router.url)
                )
            )
        )
    
    def _render(self, ctx: ft.Page, router: Router) -> ft.Page:
        self.clear(ctx)
        self.mount_default_layout(ctx, router)
        
        route = router.get_route(router.url)
        self.render_route(ctx, router, route)
        
    def run(self, router: Router):
        ft.app(lambda ctx, rt=router:self._render(ctx, rt))

