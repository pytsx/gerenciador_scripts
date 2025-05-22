from engine.interface import IRouter
import flet as ft

class RouterSearchbar(ft.SearchBar):
  def __init__(self,  *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.on_tap = lambda e: self.open_view()
    self.on_submit = lambda e: self._safe_close_view()
    self.on_click = lambda e: self.open_view()
   

  def _safe_close_view(self):
    """Fecha a visualização de forma segura, verificando se o controle foi adicionado à página."""
    if self.page:  # Verifica se o controle foi adicionado à página
      self.close_view()

  def mount(self, ctx: ft.Page, router: IRouter, bar_hint_text: str):
    """Renderiza o controle na página."""
    self.width = ctx.width - 20
    self.bar_hint_text = bar_hint_text
    self.autofocus = True
    
    def go_to(e: ft.ControlEvent, data: str):
      if self.page:  # Verifica se o controle foi adicionado à página
        router.navigate(data)
        self._safe_close_view()
    
    def on_click(e: ft.ControlEvent, data):
      go_to(e, data)

    routes = [
      route for route in router.routes.keys()
    ]
  
    self.controls = [
      ft.ListTile(title=ft.Text(route), data=route, on_click=lambda e, data=route:on_click(e, data))
      for route 
      in routes
    ]
    
    def on_submit(e: ft.ControlEvent):
      if self.value and self.page:  # Verifica se o controle foi adicionado à página
        go_to(e, self.value)
    
    self.on_tap = lambda e, sb=self: sb.open_view()
    self.on_submit = on_submit
    
    return self