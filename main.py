import dearpygui.dearpygui as dpg

from app import create_app
from modules import scan_modules_dir

modules = scan_modules_dir(dir="modules", funcs=["execute"])
app = create_app("Gerenciador de Projetos", 800, 800)

# Callback de executar módulo
def executar_modulo(sender, app_data, user_data):
  print(f"Executando módulo: {user_data}")
  win_tag = f"win_{user_data}"
  # cria janela para o módulo
  with app.window(tag=win_tag, pos=[100, 100], no_move=False, minus_width=500, minus_height=650, no_close=False):
    try:
      modules[user_data]['execute']()
    except Exception as e:
      print(f"Erro ao executar o módulo {user_data}: {e}")


# Callback para ações rápidas (menu suspenso)
def abrir_acoes_rapidas(sender, app_data, user_data):
  print(f"Ações rápidas para: {user_data}")
  # Aqui você pode abrir um popup/menu


# Janela principal
with app.window():
  # app.menu({
  #   "settings": [
  #     {"label": "Toggle Fullscreen", "callback": lambda: dpg.toggle_viewport_fullscreen()},
  #   ],
  # })

  app.display_items(
    data=[i for i in modules], 
    execute=executar_modulo, 
    actions=abrir_acoes_rapidas
  )

app.run()
