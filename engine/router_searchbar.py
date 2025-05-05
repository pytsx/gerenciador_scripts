from engine.interface import IRouter
import flet as ft

class RouterSearchbar(ft.SearchBar):
  def __init__(self, page: ft.Page, router: IRouter, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.on_tap = lambda e: self.open_view()
    self.on_submit = lambda e: self.close_view()
    self.on_click = lambda e: self.open_view()
    self.width = page.width - 20
    
    def go_to(e: ft.ControlEvent, data: str):
      router.navigate(data, page)
      self.close_view()
    
    def on_click(e: ft.ControlEvent, data):
      go_to(e, data)
  
    self.controls = [
      ft.ListTile(title=ft.Text(route), data=route, on_click=lambda e, data=route:on_click(e, data))
      for route 
      in router.routes.keys()
    ]
    
    def on_submit(e: ft.ControlEvent):
      if self.value:
        go_to(e, self.value)
    
    self.on_tap=lambda e, sb=self: sb.open_view()
    self.on_submit=on_submit
