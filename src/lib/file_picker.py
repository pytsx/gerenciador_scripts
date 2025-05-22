from engine import BaseRouteProps, Table, join, get_downloads_path
import flet as ft
from pathlib import Path
from src.components.dataframe_table import dataframe_table
import polars as pl 


class FilePicker: 
  def __init__(self, route_props: BaseRouteProps):
    self.children: ft.Column = ft.Column()
    self.files: list[Path] = []
    self.dataframe: pl.DataFrame = pl.DataFrame()
    self.message:ft.Text = ft.Text()
    self.route_props:BaseRouteProps = route_props

  def pick_files_result(self, e: ft.FilePickerResultEvent):
    self.files.clear()
    self.dataframe.clear()
    self.children.controls.clear()
    self.message.clean()
    self.files.extend([Path(file.path).absolute() for file in e.files if file.path.endswith((".csv", ".xlsx", ".xls"))])
    
    self.dataframe = pl.read_csv(self.files[0], truncate_ragged_lines=True,infer_schema_length=1000) if self.files[0].name.endswith(".csv") else pl.read_excel(self.files[0])
    
    self.message.value = (
      ", ".join(map(lambda f: f.stem, self.files)) if self.files else "Cancelled!"
    )
    self.message.update()
    self.children.update()