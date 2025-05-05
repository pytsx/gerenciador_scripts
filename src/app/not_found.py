import flet as ft
from engine.route_props import RouteProps

def not_found(props: RouteProps):
  return [
    ft.Text(f"{props.props["error"]}", size=20, color=ft.colors.RED),
  ] 