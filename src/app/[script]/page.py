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
        content=ft.Column([ft.Row(
          [
            ft.Text(script_name, size=20, weight=ft.FontWeight.BOLD),
            ft.IconButton(ft.icons.PLAY_ARROW, tooltip="Executar", on_click=lambda e: script.main()),
          ],
          alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        ft.Container(expand=True),                  
        ], scroll=True),
        width=props.ctx.width,
        height=props.ctx.height - 100,
        expand=True,
        padding=10
      )
     ),
  ] 