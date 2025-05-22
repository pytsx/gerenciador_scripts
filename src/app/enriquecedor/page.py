"""
FLUXO:
  - selecionar arquivo
    - autodetectar a coluna de CNPJ [sugestão: CNPJ, cnpj, CNPJ_CPF]
  - selecionar coluna de CNPJ
  - selecionar template de enriquecimento
    - tipo de disparo é uma lista customizável: tipo de disparo é um template que define com quais colunas a base selecionada será enriquecida e com e a respectiva formatação
  - previa do arquivo enriquecido
  - download do arquivo enriquecido
"""

from engine import BaseRouteProps, join, get_downloads_path, open_downloads, Table
import flet as ft
from pathlib import Path
import polars as pl 

from src.components.dataframe_table import dataframe_table
from src.lib.file_picker import FilePicker

templates ={
  "hsm": ["CNPJ", "E-mail"],
  "sms": ["CNPJ", "Telefone"],
  "asc": ["CNPJ", "Telefone"],
}

# Helper function to load the base contact data
def load_base(max_cnpj:int):
  """
  Load the base contact data from an Excel file and return a unique, non-null DataFrame
  containing CNPJ, Telefone, and E-mail columns.
  """
  _base_df = pl.read_excel(Path("./src/data/carteiras.xlsx").absolute())
  return _base_df["CNPJ", "Telefone", "E-mail"].unique("Telefone").drop_nulls().filter(pl.col("CNPJ").cast(pl.Int64) < int(max_cnpj))

# Enrichment page class
class EnrichFile:
  """
  Represents the enrichment page where users can upload files, select templates,
  preview enriched data, and export the results.
  """
  def __init__(self, route_props: BaseRouteProps):
    # Initialize route properties and UI components
    self.route_props: BaseRouteProps = route_props
    self.route_props.ctx.scroll = True
    # File picker for selecting files
    self.file_picker = FilePicker(self.route_props)
    # Table container for displaying data previews
    self.table_container = ft.Column([Table(self.route_props.ctx, "preview-table", ["CNPJ"], []).renderer()])
    self.joined_df: pl.DataFrame = pl.DataFrame()

    # File picker dialog
    self.pick_files_dialog = ft.FilePicker(on_result=self.on_file_picked)
    # Export table button
    self.export_table_btn = ft.Button("exportar tabela", on_click=lambda _: self.export_files())
    # Template selection card
    self.template_type = ft.Card(
      content=ft.Container(
        padding=10,
        content=ft.Column([
          ft.Text("Escolha o template de enriquecimento"),
          ft.RadioGroup(
            on_change=self.on_template_type_change,
            content=ft.Column([ft.CupertinoRadio(value=template, label=template) for template in templates.keys()])
          ),
        ])
      )
    )
    # Button to trigger file picking
    self.pick_files_btn = ft.ElevatedButton(
      "Escola o arquivo",
      icon=ft.icons.UPLOAD_FILE,
      on_click=lambda _: self.pick_files(),
    )
    # Loader for indicating progress
    self.loader = ft.ProgressBar(width=self.route_props.ctx.width, height=5)
    # Main content layout
    self.content = [
      ft.Container(
        expand=True,
        content=ft.Row([
          ft.Container(
            content=ft.Column([
              self.pick_files_dialog,
              self.pick_files_btn,
              self.file_picker.message,
              self.file_picker.children,
              ft.Container(expand=True)
            ],
            width=self.route_props.ctx.width / 2,
            expand=True,
            height=self.route_props.ctx.height - 100)
          ),
          ft.Container(
            content=self.table_container,
            width=self.route_props.ctx.width / 2,
            expand=True,
            height=self.route_props.ctx.height - 100,
          )
        ])
      )
    ]

  def on_file_picked(self, e: ft.FilePickerResultEvent):
    """
    Handle the event when a file is picked.
    """
    self.file_picker.pick_files_result(e)
    self.file_picker.children.controls.append(self.template_type)
    self.file_picker.children.update()
    self.file_picker.message.value = f"{len(self.file_picker.files[0].stem)}"
    self.file_picker.message.update()
    
    # Load the contact base
    contact_base = self.load_contact_base(self.file_picker.dataframe["CNPJ"].max())

    # Join the dataframes
    self.joined_df = join(self.file_picker.dataframe, contact_base, keys=["CNPJ"], how="inner")

  def load_contact_base(self, max_cnpj: int):
    """
    Load the contact base data and update the UI accordingly.
    """
    body = list(self.content)
    self.route_props.ctx.remove(*self.content)
    self.route_props.ctx.add(self.loader)
    self.route_props.ctx.update()

    contact_base = load_base(max_cnpj)

    self.route_props.ctx.remove(self.loader)
    self.route_props.ctx.add(*body)

    return contact_base

  def export_files(self):
    """
    Export the enriched data to an Excel file.
    """
    if self.file_picker.dataframe.is_empty():
      self.file_picker.message.value = "Nenhum arquivo selecionado"
      self.file_picker.message.update()
      return

    # Check if the required column exists
    required_columns = ["CNPJ", "cnpj", "CNPJ_CPF", "CNPJCPF", "NUMCGCCPECPFCLI", "NUMCGCCPF", "NUMCGCCPFCLI"]
    existing_columns = set(self.file_picker.dataframe.columns)
    matching_columns = [col for col in required_columns if col in existing_columns]

    if not matching_columns:
      self.file_picker.message.value = "Coluna de CNPJ não encontrada no arquivo"
      self.file_picker.message.update()
      return

    # Normalize the CNPJ column name
    self.file_picker.dataframe = self.file_picker.dataframe.rename({col: "CNPJ" for col in matching_columns})
 
    # Export the enriched data
    self.joined_df.write_excel(get_downloads_path() / f"{self.file_picker.files[0].stem}_enriquecido.xlsx")
    open_downloads()
    self.file_picker.children.update()

  def on_template_type_change(self, e: ft.ControlEvent):
    """
    Handle changes in the selected enrichment template.
    """
    self.table_container.controls.clear()
    
    columns = templates[e.data]
    if columns:
      _tab = dataframe_table(self.file_picker.route_props, self.file_picker.dataframe[columns].head(15))

    self.table_container.controls.append(_tab.renderer())
    self.table_container.update()

    self.file_picker.children.controls.append(self.export_table_btn)
    self.file_picker.children.update()

  def pick_files(self):
    """
    Open the file picker dialog to select files.
    """
    self.pick_files_dialog.pick_files(
      allow_multiple=False,
      allowed_extensions=["csv", "xlsx", "xls"],
    )

# Page entry point
def page(props: BaseRouteProps):
  """
  Return the content for the enrichment page.
  """
  return EnrichFile(props).content