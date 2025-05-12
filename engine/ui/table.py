"""
Módulo table: componente UI reutilizável para exibição de tabelas Flet.
Define classe Table que estende Component, combinando um botão
de refresh e um DataTable com colunas e linhas personalizadas.
"""
# importa flet para construção de controles UI
import flet as ft
# importa classe base Component para composição de controles
from engine import Component

class Table(Component):
    """
    Componente de tabela com botão de recarregar.
    Recebe contexto da página, chave única, colunas e linhas de dados.
    """
    def __init__(
        self,
        ctx: ft.Page,
        key: str,
        columns: list[ft.DataColumn | str],
        rows: list[ft.DataRow]
    ) -> None:
        # filtra colunas já definidas como ft.DataColumn
        cols = [col for col in columns if isinstance(col, ft.DataColumn)]
        # converte strings em DataColumn com ft.Text
        cols.extend([
            ft.DataColumn(ft.Text(col))
            for col in columns
            if isinstance(col, str)
        ])
        # armazena contexto da página para uso em callbacks
        self.ctx = ctx

        # chama construtor da classe base com controles:
        # - ícone de refresh que chama self.refresh()
        # - DataTable com propriedades customizadas
        super().__init__(
            ft.IconButton(
                icon=ft.icons.REFRESH,
                tooltip="Recarregar",
                on_click=lambda e, c=ctx: self.refresh(c),
            ),
            ft.DataTable(
                key=key,
                bgcolor="#2d2d2d",
                width=ctx.width,
                border=ft.border.all(2, "#3d3d3d"),
                border_radius=10,
                vertical_lines=ft.border.BorderSide(3, "#2d2d2d"),
                horizontal_lines=ft.border.BorderSide(1, "#5d5d5d"),
                heading_row_color=ft.Colors.BLACK12,
                columns=cols,
                rows=rows,
            )
        )
    
    def renderer(self) -> ft.Control:
        """
        Retorna o wrapper (Column) contendo os controles.
        Recebe ctx apenas para manter assinatura compatível.
        """
        return super().renderer(self.ctx)