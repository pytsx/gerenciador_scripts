import flet as ft
from src.components.scripts_table import scripts_table
from engine.route_props import RouteProps

def page(props: RouteProps):
  
  return [
    scripts_table(props).renderer()
  ] 