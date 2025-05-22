"""
Módulo component: define classe base Component para composição de controles UI.
Component encapsula controles originais em um Column e fornece método de refresh.
"""
# importa flet para tipagem de controles e atualização de UI
import flet as ft
# importa sleep para simular atraso de carregamento
from time import sleep

class Component:
    """
    Classe base para componentes compostos de múltiplos controles.
    Armazena controles originais e fornece wrapper em ft.Column.
    """
    def __init__(self, *control: list[ft.Control]):
        # armazena controles originais para possível recarregamento
        self.origin = [*control]
        # cria coluna que agrupa os controles
        self.wrapper = ft.Column(control)

    def renderer(self, ctx: ft.Page) -> ft.Control:
        """
        Retorna o controle wrapper (Column) para renderização.
        ctx: contexto da página, não usado diretamente aqui.
        """
        return self.wrapper

    def refresh(self, ctx: ft.Page):
        """
        Recarrega os controles simulando delay.
        1. Limpa controles atuais.
        2. Atualiza UI.
        3. Aguarda 0.2s.
        4. Repõe controles originais.
        5. Atualiza UI novamente.
        """

        # remove todos os controles do wrapper
        self.wrapper.controls.clear()
        # notifica Flet para atualizar a UI
        ctx.update()

        # pausa para simular operação de IO ou processamento
        sleep(0.2)

        # limpa novamente (caso necessário) e restaura controles originais
        self.wrapper.controls.clear()
        self.wrapper.controls.extend(self.origin)
        # notifica Flet para renderizar a lista restaurada
        ctx.update()


__all__ = ["Component"]