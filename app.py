from dearpygui import dearpygui
from typing import Callable

class App: 
  def __init__(self, title: str, width: int = 600, height: int = 400):
    self.width = width
    self.height = height
    self.title = title
    self.engine = dearpygui
    self.engine.create_context()

  def window(self, 
    tag: str = "window",
    no_move=True, 
    no_title_bar=True,
    no_close=True,
    no_resize=True,
    pos: list[int] = [0, 0],
    minus_width: int = 0,
    minus_height: int = 0,
  ): 
    if self.engine.does_item_exist(tag):
      self.engine.delete_item(tag)
    return self.engine.window(
      tag=tag,
      pos=pos, 
      no_move=no_move, 
      no_title_bar=no_title_bar,
      no_close=no_close,
      no_resize=no_resize,
      width=self.width - minus_width,
      height=self.height - minus_height,
    )
  
  def child_window(self, tag: str, width: int = 600, height: int = 400, parent: str = "window"):
    if self.engine.does_item_exist(tag):
      self.engine.delete_item(tag)
    return self.engine.child_window(
      tag=tag,
      parent=parent,
      width=self.width ,
      height=self.height ,
      autosize_x=True,
      autosize_y=True,
      no_scrollbar=True,
      pos=[0, 0],
    )

  def run(self): 
    self.engine.create_viewport(title=self.title, width=self.width, height=self.height,resizable=False )
    self.engine.setup_dearpygui()
    self.engine.show_viewport()
    self.engine.start_dearpygui()
    self.engine.destroy_context()

  def display_items(self, data: list,  execute: Callable, actions: Callable):
    for item in data:
      with self.engine.group(horizontal=True):
        self.list_item( item, execute, actions)

  def list_item(self, modulo: str, execute: Callable, actions: Callable): 
    self.engine.add_text(modulo, )
    self.engine.add_spacer(width=20)
    self.engine.add_button(label="Executar", width=100, callback=execute, user_data=modulo)
    self.engine.add_button(label="+", width=30, callback=actions, user_data=modulo)
  
  def menu(self, items: dict[str, list[dict]]):
    with self.engine.menu_bar():
      with self.engine.menu(label="Menu"):
        for key in items: 
          with self.engine.menu(label=key):
            for item in items[key]:
              self.engine.add_menu_item(**item)

def create_app(title: str, width: int = 600, height: int = 400) -> App:
  return App(title, width, height)