
from engine.interface import IRouter
import flet as ft

class RouteProps:
  """
  Class to hold route properties for a given route.
  """
  def __init__(
    self, 
    ctx: ft.Page,
    router: IRouter, 
    children: list[ft.Control] = [], 
    props: dict[str, any] = {}
  ) -> None:
    self.ctx: ft.Page = ctx
    self.router: IRouter = router
    self.children: list[ft.Control] = children 
    self.props: dict[str, any] = props