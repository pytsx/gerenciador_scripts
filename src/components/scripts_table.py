import flet as ft
from env import scripts
from src.components.ui import Table
from engine.route_props import RouteProps

def executar_modulo(key, page: ft.Page = None):
  print(f"Executando módulo: {key}")
  module = scripts[key]
  if not module:
    print(f"Módulo {key} não encontrado.")
    return
  
  try: module.main()
  except Exception as e:
    print(f"Erro ao executar o módulo {key}: {e}")

# Callback para ações rápidas (menu suspenso)
def abrir_acoes_rapidas( key: str):
  print(f"Ações rápidas para: {key}")
  # Aqui você pode abrir um popup/menu

    
def scripts_table(props: RouteProps):
  return Table(
      key="tabela_scripts",
      ctx=props.ctx,
      columns=["Scripts", ""],
      rows=[
        ft.DataRow(
          cells=[
            ft.DataCell(ft.Text(module)),
            ft.DataCell(
              content=ft.Row(
                  
                  controls=[
                    ft.IconButton(ft.icons.ARROW_OUTWARD_SHARP, tooltip="ir para", on_click=lambda e, m=module, p=props: p.router.navigate(p.ctx, "/" + m)),
                    ft.PopupMenuButton(
                      icon=ft.icons.MORE_VERT,
                      tooltip="Ações rápidas",
                      items=[
                        ft.PopupMenuItem(text="Executar", on_click=lambda e, m=module: executar_modulo(m)),
                        ft.PopupMenuItem(text="ir para", on_click=lambda e, m=module, p=props: p.router.navigate(p.ctx, "/" + m)),
                      ]
                    )
                  ],
                  alignment=ft.MainAxisAlignment.END,
                  
              ),
            ),
          ]
        )
        for module in scripts.keys()
      ],
    )
  