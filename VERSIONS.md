# Histórico de Versões

## v0.0.2

Sistema de Navegação:
  Router.navigate()
  RouteBuilder.build()

Tabela de Scripts:
  executar_modulo()
  abrir_acoes_rapidas()

Carregamento Dinâmico:
  Modules para gerenciar scripts.

Injeção de Dependências:
  ServiceContainer.register()
  ServiceContainer.resolve()
  
---
#### **1. Funcionalidades Adicionadas**
Desde a versão **v0.0.1**, foram implementadas as seguintes funcionalidades:

- **Sistema de Navegação entre Múltiplas Páginas**:
  - Implementado um sistema de roteamento dinâmico e estático utilizando a classe `Router`.
  - Suporte a rotas dinâmicas com parâmetros, como `[script]`, permitindo navegação baseada em contexto.
  - Funções adicionadas:
    - `Router.navigate()`: Navega para uma rota específica.
    - `Router.get_route()`: Retorna a rota correspondente ao caminho.
    - `RouteBuilder.build()`: Constrói a estrutura de layout e página para uma rota.

- **Temas Personalizados de UI**:
  - Adicionado suporte para alternância de temas na interface.
  - Embora o arquivo theme_service.py esteja vazio, a estrutura para gerenciar temas pode ser integrada ao sistema.

- **Tabela de Scripts com Ações Rápidas**:
  - A tabela de scripts foi aprimorada com um menu de ações rápidas, permitindo executar ou editar scripts diretamente.
  - Implementado no componente `scripts_table`.
  - Funções adicionadas:
    - `executar_modulo()`: Executa um módulo específico.
    - `abrir_acoes_rapidas()`: Abre o menu de ações rápidas.

- **Carregamento Dinâmico de Scripts**:
  - O sistema agora carrega scripts dinamicamente do diretório scripts usando a classe `Modules`.
  - Scripts como carteiras.py podem ser executados diretamente.

---

#### **2. Melhorias Técnicas**
- **Refatoração de Componentes**:
  - Componentes como `Table` foram modularizados para maior reutilização.
  - Adicionado suporte a callbacks e atualizações dinâmicas.

- **Sistema de Injeção de Dependências**:
  - Introduzido o container de serviços em `di.py`, permitindo injeção de dependências para maior desacoplamento.
  - Funções adicionadas:
    - `ServiceContainer.register()`: Registra serviços no container.
    - `ServiceContainer.resolve()`: Resolve dependências dinamicamente.

- **Melhorias no Sistema de Roteamento**:
  - Adicionado suporte a rotas dinâmicas com parâmetros, como `[script]`.
  - Implementado fallback para páginas de erro personalizadas em `not_found`.

---

#### **3. Funcionalidades Resolvidas**
- **Sistema de Navegação**:
  - Resolvido o item pendente de navegação entre múltiplas páginas.
  - Implementado suporte a rotas dinâmicas e estáticas.

- **Temas Personalizados**:
  - Adicionado suporte inicial para temas, embora o gerenciamento ainda precise ser implementado.

---

#### **4. Funcionalidades Pendentes**
Apesar das melhorias, algumas pendências ainda permanecem:
- **Persistência de Configurações**:
  - Ainda não há suporte para salvar/restaurar configurações entre sessões.

- **Componentes de Formulário**:
  - Não foram encontrados componentes reutilizáveis para entrada de dados (e.g., campos de texto, botões de envio).

- **Integração com Ferramentas Externas**:
  - Não há evidências de integração com APIs ou serviços externos.

---

### **Resumo das Funcionalidades Adicionadas**
1. **Sistema de Navegação**:
   - `Router.navigate()`
   - `RouteBuilder.build()`

2. **Tabela de Scripts**:
   - `executar_modulo()`
   - `abrir_acoes_rapidas()`

3. **Carregamento Dinâmico**:
   - `Modules` para gerenciar scripts.

4. **Injeção de Dependências**:
   - `ServiceContainer.register()`
   - `ServiceContainer.resolve()`

5. **Temas Personalizados**:
   - Estrutura inicial para gerenciamento de temas.

---

Se precisar de mais detalhes ou ajuda para documentar essas mudanças no VERSIONS.md, é só avisar!

## v0.0.1

Versão inicial do sistema DearGUI com recursos básicos de interface e gerenciamento de scripts.

### Core Engine
- ✅ Sistema de carregamento dinâmico de módulos Python
- ✅ Gerenciamento de ciclo de vida de páginas e componentes
- ✅ Interface abstrata para classes App e Page
- ✅ Classe base Component para UI reutilizável
- ✅ Sistema de tratamento de erros com páginas personalizadas

### Interface de Usuário
- ✅ Layout padrão com AppBar personalizado
- ✅ Componente de tabela reutilizável (Table)
- ✅ Sistema de controle centralizado para scripts
- ✅ Botão de atualização para componentes de tabela

### Funcionalidades
- ✅ Carregamento e listagem automática de scripts Python
- ✅ Execução direta de scripts a partir da interface
- ✅ Menu de ações rápidas para cada script (executar como, editar)
- ✅ Suporte a callbacks para ações de UI

### Estrutura
- ✅ Organização modular em diretórios (engine, src, scripts)
- ✅ Separação entre core e componentes de aplicação
- ✅ Sistema centralizado de configurações (env.py)

### Infraestrutura
- ✅ Arquivo .gitignore básico para arquivos Python
- ✅ Ponto de entrada modular (__main__.py)
- ✅ Documentação inicial (README.md)

### Pendências
- ⬜ Sistema de navegação entre múltiplas páginas
- ⬜ Temas personalizados de UI
- ⬜ Persistência de configurações
- ⬜ Componentes de formulário
- ⬜ Integração com ferramentas externas



