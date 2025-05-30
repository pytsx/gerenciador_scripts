import flet as ft
from engine import BaseRouteProps

def layout(props: BaseRouteProps) -> ft.Page:
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
    ft.Container(expand=True),
  ]