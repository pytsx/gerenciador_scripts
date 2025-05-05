import flet as ft 
from engine.interface import IRoute, IRouter
from engine.route_props import RouteProps

def default_layout(props: RouteProps) -> list[ft.Control]:
    """
    Layout padrão (sem AppBar):
    - Recebe page do Flet e controles a serem renderizados.
    - Adiciona os controles e retorna a própria page.
    """
    return [*props.children]          # devolve objeto page para Flet processar

def default_page(props: RouteProps) -> list[ft.Control]:
    """
    Page padrão vazia (fallback quando não há page.py):
    - Recebe contexto Flet (ctx) e retorna tupla vazia de controles.
    """
    return [] 

class RouteBuilder:
    def __init__(self,  route: "IRoute") -> None:
        self.route: "IRoute"  = route
    
    def _retrieve_page(self, route: "IRoute"):
        if route.dynamic_route is not None and route.dynamic_route.page is not None:
            return route.dynamic_route.page.main
        elif route.page is not None:
            return route.page.main
        return default_page
        
    def _retrieve_layout(self, route: "IRoute"):
        if route.layout is not None:
            return route.layout.main
        return default_layout
        
    def _retrieve_parent_layout(self, route: "IRoute"):
        if route.parent is not None and route.parent.layout is not None:
            return route.parent.layout.main
        return default_layout
    
    def _retrieve_structure(self, route: "IRoute"):
        parent_layout = self._retrieve_parent_layout(route)
        layout_fn = self._retrieve_layout(route)
        page_fn = self._retrieve_page(route)
        return parent_layout, layout_fn, page_fn
    
    
    def build(self, ctx: ft.Page, router: "IRouter", props: dict = {}) -> list[ft.Control]:
        # Escolhe funções de acordo com disponibilidade
        parent_layout, layout_fn, page_fn = self._retrieve_structure(self.route)
        print("[debug] RouteBuilder.build()")
        print("exist", parent_layout, layout_fn, page_fn )
        try:
            controls = page_fn(RouteProps(ctx, router, [], props=props))
            print("[debug] RouteBuilder.build() - page_fn:", controls)
                
            if controls is None:
                controls = self.route.not_found.main(RouteProps(ctx, router, props={"error": "Page not found"}))
            
            print("[debug] RouteBuilder.build() - controls:", controls)
            
            result = parent_layout(RouteProps(ctx, router, [*layout_fn(RouteProps(ctx, router, [*controls]))]))
            
            print("[debug] RouteBuilder.build() - result:", result)
            
            if not result: 
                result = parent_layout(RouteProps(ctx, router, *layout_fn(RouteProps(ctx, router, [*controls]))))
            
            print("[debug] RouteBuilder.build() - result:", result)
            
            return [*result]
        except Exception as e:
            return [*parent_layout(RouteProps(ctx, router, [*layout_fn(RouteProps(ctx, router, [*self.route.not_found.main(RouteProps(ctx,router, props={"error build": str(e)}))]))] ))]
                
     
        