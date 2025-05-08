import flet as ft

from env import scripts
from engine.route_props import RouteProps

def generate_static_params():
  return [[script, {}] for script in scripts.keys()]
  
def page(props: RouteProps):
  script_name = (props.props["script"] or "").split("/")[-1]
  
  script = scripts[script_name]
  
  if script is None:
    return [ft.Text(f"route {props.props["script"] } - Script <{script_name}> não encontrado", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.RED_900)]
  
  return [
    ft.Card(content=ft.Container(
        content=ft.Column([ft.Text(f"{script_name}")], scroll=True),
        width=props.ctx.width,
        height=props.ctx.height - 100,
        expand=True,
        padding=10
      )
     ),
  ] 