import flet as ft
from engine import BaseRouteProps

"""
    Componentes:
        - sidebar 
        - header
        - children:
            - orquestrador
                - criar fluxo de atualização
                - executar fluxo de atualização
                
                # fluxo de atualização
                    - agedar
                    - executar paralelamente ou sequencialmente
                    
            - tabelas
                - baixar tabela em excel
                - enviar tabela por e-mail
"""

def page(props: BaseRouteProps):
    """
    Tableau page
    """
    return [
        ft.Text("Tableau", size=30),
        ft.Text("Esta é a página tableau")
    ]