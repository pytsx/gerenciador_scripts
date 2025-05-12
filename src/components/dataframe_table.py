import flet as ft
from engine import RouteProps, Table
import polars as pl
    
def dataframe_table(props: RouteProps, dataframe: pl.DataFrame):
  return Table(
    key="dataframe_table",
    ctx=props.ctx,
    columns=[ft.DataColumn(ft.Text(col)) for col in dataframe.columns],
    rows=[
        ft.DataRow(
            cells=[ft.DataCell(ft.Text(str(value))) for value in row]
        )
        for row in dataframe.rows()
    ],
  )
  