import flet as ft
from engine import Component, BaseRouteProps

def tabela(props: BaseRouteProps):
  """
  Componente tabela
  """
  return ft.Column([
      ft.Text("Tabela Component", size=20)
  ])