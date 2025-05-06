# -*- coding: utf-8 -*-
import flet as ft
from engine.route_props import RouteProps

from env import scripts

def generate_static_params():
  return scripts.keys()
  

def Page(props: RouteProps) -> list[ft.Control]:
  """
  Página de execução do módulo.
  """

  # Retorna a página de execução
  return [
    ft.Text(f"Módulo executado com sucesso!")
  ]