import flet as ft
from engine import Component, BaseRouteProps

def ${name}(props: BaseRouteProps):
  """
  Componente ${name}
  """
  return ft.Column([
      ft.Text("${class_name} Component", size=20)
  ])