import flet as ft
from engine import BaseRouteProps

def not_found(props: BaseRouteProps):
  return [
    ft.Text(f"{props.props["error"]}", size=20, color=ft.colors.RED),
  ] 