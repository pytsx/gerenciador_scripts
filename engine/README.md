# DearGUI Engine

Uma engine modular para construção de interfaces gráficas dinâmicas utilizando o framework Flet.

## Visão Geral

A DearGUI Engine fornece uma estrutura para criar aplicações Flet com carregamento dinâmico de módulos, sistema de páginas e componentes reutilizáveis. A engine foi projetada para:

- Carregar dinamicamente módulos Python em tempo de execução
- Gerenciar o ciclo de vida de páginas e componentes
- Simplificar a criação de interfaces consistentes
- Facilitar a reutilização de código UI

## Componentes da Engine

### 1. `app.py`

Gerencia o ciclo de vida da aplicação:

- `App`: Classe principal que inicia a aplicação
- `Page`: Gerencia o carregamento e renderização de uma página
- Funções de layout e página padrão

### 2. `modules.py`

Fornece mecanismos para carregamento dinâmico de módulos:

- `Module`: Carrega um único arquivo `.py` como módulo dinâmico
- `Modules`: Escaneia um diretório e carrega todos os arquivos `.py`

### 3. `interface.py`

Define interfaces abstratas para implementação:

- `IApp`: Interface para classe de aplicação
- `IPage`: Interface para classe de página

### 4. `component.py`

Define a base para componentes UI reutilizáveis:

- `Component`: Classe base para criar componentes compostos

## Como Usar a Engine

Veja como implementar sua própria aplicação:

### 1. Estrutura de Diretórios

```
myapp/
├── __main__.py          # Ponto de entrada
├── engine/              # Engine (este diretório)
├── src/                 # Sua implementação
│   ├── app/             # Definições de páginas
│   │   ├── page.py      # Conteúdo principal
│   │   ├── layout.py    # Layout da página
│   │   └── not_found.py # Tratamento de erros
│   └── components/      # Componentes da aplicação
├── scripts/             # Scripts executáveis dinamicamente
└── env.py               # Configurações do ambiente
```

### 2. Inicializando a Aplicação

```python
# __main__.py
from engine.app import App
from env import APP_DIR

app = App(APP_DIR)
app.initialize()
```

### 3. Configurando o Ambiente

```python
# env.py
from engine.modules import Modules
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "src" / "app"

# Carregue scripts dinâmicos
scripts = Modules(dir=BASE_DIR / "scripts", main="execute")
```

### 4. Criando uma Página

```python
# src/app/page.py
import flet as ft
from src.components.my_component import MyComponent

def page(ctx: ft.Page):
    return [
        ft.Text("Hello DearGUI", size=30),
        MyComponent(ctx).renderer()
    ]
```

### 5. Definindo o Layout

```python
# src/app/layout.py
import flet as ft

def layout(page: ft.Page, *children: ft.Control) -> ft.Page:
    page.title = "Minha Aplicação"
    page.appbar = ft.AppBar(
        title=ft.Text("Minha Aplicação"),
        bgcolor=ft.colors.SURFACE_VARIANT,
    )
    page.add(*children)
    return page
```

### 6. Tratando Erros

```python
# src/app/not_found.py
import flet as ft

def not_found(error):
    return [
        ft.Text(f"Erro: {error}", color=ft.colors.RED),
    ]
```

### 7. Criando um Componente

```python
# src/components/my_component.py
import flet as ft
from engine.component import Component

class MyComponent(Component):
    def __init__(self, ctx: ft.Page):
        self.ctx = ctx
        super().__init__(
            ft.Text("Componente Personalizado"),
            ft.ElevatedButton("Clique", on_click=self.on_click)
        )
    
    def on_click(self, e):
        print("Botão clicado!")
    
    def renderer(self) -> ft.Control:
        return super().renderer(self.ctx)
```

## API de Referência

### App

```python
App(root: Path)
```
- `root`: Caminho do diretório da página raiz
- `initialize()`: Inicia a aplicação

### Page

```python
Page(dir: Path)
```
- `dir`: Diretório contendo arquivos page.py, layout.py, not_found.py
- `run(page: ft.Page)`: Renderiza a página no contexto Flet

### Module

```python
Module(path: Path, main: str, funcs: list[str])
```
- `path`: Caminho para arquivo .py
- `main`: Nome da função principal a expor
- `funcs`: Lista de nomes de funções auxiliares

### Modules

```python
Modules(dir: Path, main: str, funcs: list[str] = [])
```
- `dir`: Diretório com arquivos .py
- `main`: Nome da função principal em cada módulo
- `funcs`: Lista de nomes de funções auxiliares

### Component

```python
Component(*controls: ft.Control)
```
- `controls`: Controles Flet que compõem o componente
- `renderer(ctx: ft.Page)`: Renderiza o componente

## Melhores Práticas

1. **Organização de Diretórios**:
   - Mantenha componentes reutilizáveis em `/src/components/`
   - Agrupe componentes relacionados em subdiretórios

2. **Componentização**:
   - Crie componentes reutilizáveis para elementos de UI comuns
   - Prefira composição de componentes à duplicação de código

3. **Carregamento Dinâmico**:
   - Use `Modules` para carregar scripts dinamicamente
   - Defina uma estrutura consistente para scripts executáveis

4. **Tratamento de Erros**:
   - Sempre implemente `not_found.py` para lidar com erros
   - Use try/except em callbacks para evitar travamentos

## Exemplo em `src/`

O diretório `src/` em seu projeto demonstra:

- Estrutura de diretórios recomendada
- Implementação de uma tabela de scripts executáveis
- Criação de componentes reutilizáveis (Table)
- Definição de layout com AppBar
- Tratamento de erros com not_found

## Licença

[Sua licença aqui]
