import flet as ft
from src.components.scripts_table import scripts_table
from engine import BaseRouteProps

def page(props: BaseRouteProps):
  
  return [
    scripts_table(props).renderer()
  ] 