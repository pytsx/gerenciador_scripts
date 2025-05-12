# Script Management System

O **Script Management System** é uma aplicação modular e extensível construída com a biblioteca [Flet](https://flet.dev/), projetada para gerenciar scripts Python, interfaces dinâmicas e navegação entre páginas. Este sistema utiliza uma arquitetura baseada em rotas, injeção de dependências e carregamento dinâmico de módulos, permitindo alta flexibilidade e desacoplamento.

## Funcionalidades Principais

### 1. **Sistema de Navegação**
- Navegação entre múltiplas páginas utilizando rotas dinâmicas e estáticas.
- Suporte a parâmetros dinâmicos em rotas, como `[script]`.
- Fallback para páginas de erro personalizadas (`not_found`).

### 2. **Carregamento Dinâmico de Módulos**
- Carregamento automático de scripts Python a partir de um diretório específico.
- Cada script pode definir um ponto de entrada (`execute`) para ser executado dinamicamente.
- Gerenciamento de módulos com a classe `Modules`.

### 3. **Tabela de Scripts**
- Exibição de scripts disponíveis em uma tabela interativa.
- Ações rápidas, como executar ou navegar para um script, diretamente da interface.

### 4. **Injeção de Dependências**
- Sistema de injeção de dependências utilizando o `ServiceContainer`.
- Suporte a escopos e singletons para maior controle sobre o ciclo de vida dos serviços.

### 5. **Manipulação de DataFrames**
- Integração com a biblioteca [Polars](https://pola-rs.github.io/polars/) para manipulação de DataFrames.
- Funções como `join` para combinar tabelas de dados com base em chaves.

### 6. **Gerador de Formulários**
- Geração dinâmica de formulários com suporte a múltiplos tipos de campos (texto, número, radio, dropdown, etc.).
- Callback para manipulação dos dados submetidos.

### 7. **Interface Personalizável**
- Componentes reutilizáveis, como tabelas e formulários.
- Suporte inicial para temas personalizados.

## Estrutura do Projeto

```
script management system/
├── engine/                 # Núcleo da aplicação
│   ├── ui/                 # Componentes de interface (tabela, gerador de formulários)
│   ├── router/             # Sistema de roteamento
│   ├── route/              # Gerenciamento de rotas e layouts
│   ├── dataframe/          # Manipulação de DataFrames
│   ├── env/                # Configurações e utilitários do sistema
│   ├── di.py               # Injeção de dependências
│   ├── modules.py          # Carregamento dinâmico de módulos
│   └── component.py        # Classe base para componentes de UI
├── src/                    # Código da aplicação
│   ├── app/                # Páginas e layouts
│   ├── components/         # Componentes reutilizáveis
│   └── lib/                # Bibliotecas auxiliares
├── scripts/                # Diretório de scripts Python gerenciados
├── VERSIONS.md             # Histórico de versões
├── README.md               # Documentação do projeto
└── __main__.py             # Ponto de entrada da aplicação
```

## Como Funciona

1. **Inicialização**:
   - O sistema é iniciado pelo arquivo `__main__.py`, que configura o roteador e o gerador de rotas.

2. **Navegação**:
   - As rotas são geradas dinamicamente a partir da estrutura de diretórios em `src/app`.
   - Cada página pode ter um layout (`layout.py`), uma página principal (`page.py`) e uma página de erro (`not_found.py`).

3. **Carregamento de Scripts**:
   - Os scripts no diretório `scripts/` são carregados dinamicamente pela classe `Modules`.
   - Cada script deve implementar uma função `execute` como ponto de entrada.

4. **Interface**:
   - Componentes como tabelas e formulários são renderizados dinamicamente com base nos dados fornecidos.

5. **Injeção de Dependências**:
   - Serviços são registrados no `ServiceContainer` e podem ser injetados em componentes ou classes.

## Requisitos

- Python 3.9 ou superior
- Dependências:
  - [Flet](https://flet.dev/)
  - [Polars](https://pola-rs.github.io/polars/)

## Como Executar

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd script-management-system
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```bash
   python __main__.py
   ```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
