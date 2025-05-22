import flet as ft
from engine import BaseRouteProps

def page(props: BaseRouteProps):
    """
    ${title} page
    """
    return [
        ft.Text("${title}", size=30),
        ft.Text("Esta é a página ${name}")
    ]