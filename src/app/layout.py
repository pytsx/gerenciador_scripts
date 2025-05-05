import flet as ft
from engine.route_props import RouteProps

def layout(props: RouteProps) -> ft.Page:
  print("Layout", props.children)
  props.ctx.title = "Gerenciador de Projetos"
  props.ctx.vertical_alignment = ft.MainAxisAlignment.CENTER
  
  props.ctx.appbar = ft.AppBar(
    title=ft.Text("Gerenciador de Projetos"),
    bgcolor=ft.colors.BACKGROUND,
    actions=[
      # ft.IconButton(ft.icons.NOTIFICATIONS, tooltip="Notificações"),
    ],
  )

  return [
    *props.children,
    ft.Container(expand=True)
  ]