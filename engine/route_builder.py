import flet as ft 
from engine.interface import IRoute
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


def default_error(props: RouteProps) -> list[ft.Control]:
    return [
        ft.Text(f"Erro: Página não encontrada ou rota mal configurada. Detalhes: {props.props.get('error', 'Sem detalhes')}")
    ]

class RouteBuilder:
    @staticmethod
    def _retrieve_page(route: "IRoute"):
        if route.page is not None:
            return route.page.main
        return default_page
    
    @staticmethod   
    def _retrieve_layout(route: "IRoute"):
        if route.layout is not None:
            return route.layout.main
        return default_layout

    @staticmethod
    def _assemble_layout_stack(route: "IRoute", props: RouteProps) -> list[ft.Control]:
        """
        Aplica layouts em ordem correta: mais externo envolve mais interno.
        Começa do route atual e caminha até a raiz, montando a hierarquia.
        """
        layouts = []
        current = route

        # Subir até o topo e empilhar os layouts
        while current:
            layouts.append(RouteBuilder._retrieve_layout(current))
            current = current.parent

        # Agora, aplicar os layouts de fora para dentro
        result = props.children
        for layout_fn in layouts:
            result = layout_fn(RouteProps(props.ctx, props.router, children=result, props=props.props))

        return result

    @staticmethod
    def build(route: "IRoute", props: RouteProps) -> list[ft.Control]:
        ctx = props.ctx
        router = props.router
        print(f"[build] page {route.dir}")
        
        # Escolhe funções de acordo com disponibilidade
        page_fn = RouteBuilder._retrieve_page(route)
        
        
        print(f"[build] page exist? {page_fn}")
        
        try:
            controls = [*page_fn(props)]
            print(f"[build] contorls: {controls}")
                
            if controls is None:
                controls = route.not_found.main(RouteProps(ctx, router, props={"error": "Page not found"}))
            result = RouteBuilder._assemble_layout_stack(route, RouteProps(ctx, router, controls))
            
            print(f"[build] result: {result}")
            if not result: 
                result = route.not_found.main(RouteProps(ctx, router, props={"error": "Page not found"}))
            
            return [*result]
        except Exception as e:
            # return [*parent_layout(RouteProps(ctx, router, [*layout_fn(RouteProps(ctx, router, [*route.not_found.main(RouteProps(ctx,router, props={"error build": str(e)}))]))] ))]
            return [*RouteBuilder.error(route, RouteProps(ctx, router, props={"error": "erro no build: " + str(e)}))]
                
    
    @staticmethod
    def error(route: "IRoute", props: RouteProps) -> list[ft.Control]:
        """
        Retorna uma página de erro personalizada.
        """
        return [
            *RouteBuilder._assemble_layout_stack(
                route,
                RouteProps(
                    ctx=props.ctx,
                    router=props.router,
                    children=[*(
                        route.not_found.main(props) 
                        if route.not_found
                        else default_error(props)
                    )]
                )
            )
        ]