from env import scripts
from engine import BaseRouteProps, GenerateStaticParams
import flet as ft 

def generate_static_params():
  """
  Gera parâmetros estáticos para a página de scripts.
  """
  return BaseRouteProps.create_static_list(scripts.keys())

def page(props: BaseRouteProps) -> ft.Column:
  """
    Renderiza a página de scripts.
  """
  return [
    ft.Text(f"{props.to_dict()}")
  ]