"""
Módulo utils.modules
Fornece classes para carregar módulos Python de forma dinâmica:
- Module: representa e carrega um único arquivo .py, expõe função principal e auxiliares.
- Modules: escaneia um diretório, carrega todos os .py e expõe um dicionário de Module.
"""

from pathlib import Path    # Path: manipula caminhos de arquivo e diretório
import importlib.util       # importlib.util: cria specs para imports dinâmicos
import sys                  # sys: registra módulos carregados em cache
from typing import Callable # Callable: tipagem para funções carregadas

class Module:
    """
    Representa e carrega um único módulo Python a partir de arquivo.
    path: Path para arquivo .py
    main: nome da função principal a expor
    funcs: lista de nomes de funções auxiliares a expor
    """
    def __init__(self, path: Path, main: str, funcs: list[str]):
        # Carrega o arquivo e obtém o objeto módulo
        self.module = self.load(path)
        # Junta nome da função principal com auxiliares
        self.funcs_names = [main, *funcs]
        # Função principal dummy até ser substituída
        self.main = lambda: None
        # Dicionário para mapear funções auxiliares existentes
        res: dict[str, Callable] = {}

        if self.module is None:
            # Se não carregou, levanta ImportError
            raise ImportError(f"Não foi possível carregar o módulo {path}")

        # Para cada nome esperado, vincula se existir no módulo
        for func_name in self.funcs_names:
            if hasattr(self.module, func_name):
                func = getattr(self.module, func_name)  # busca o atributo
                if callable(func):
                    if func_name == main:
                        # substitui função dummy pela função real principal
                        self.main = func
                    else:
                        # adiciona a função auxiliar ao dicionário
                        res[func_name] = func
            else:
                # se não existir, cria stub inofensivo
                res[func_name] = lambda: None
        # expõe dicionário de funções auxiliares
        self.funcs = res

    def load(self, path: Path) -> object:
        """
        Carrega arquivo .py como um módulo Python dinâmico.
        Retorna o módulo carregado ou lança erro.
        """
        if not path.exists():
            # arquivo deve existir
            raise FileNotFoundError(f"Arquivo {path} não encontrado.")
        # define o nome do módulo com base no nome do arquivo
        module_name = path.stem
        # cria um spec a partir do arquivo físico
        spec = importlib.util.spec_from_file_location(module_name, str(path))
        if spec is None:
            # falha no spec
            raise ImportError(f"Não foi possível criar o spec para {path}")
        # cria o módulo vazio a partir do spec
        module = importlib.util.module_from_spec(spec)
        # executa o módulo (popula atributos)
        spec.loader.exec_module(module)
        # registra no cache de importação para permitir reload ou introspecção
        sys.modules[module_name] = module
        # retorna o objeto módulo
        return module

class Modules:
    """
    Gerencia vários módulos em um diretório:
    - Escaneia todos .py em dir
    - Cria um Module para cada arquivo encontrado
    - Exibe interface similar a dict para acesso
    """
    def __init__(self, dir: Path, main: str, funcs: list[str] = []):
        self.dir = dir            # Path do diretório a escanear
        self.main = main          # nome da função principal de cada módulo
        self.funcs = funcs        # nomes das funções auxiliares

        if not self.dir.exists():
            raise FileNotFoundError(f"Diretório {self.dir} não encontrado.")
        if not self.dir.is_dir():
            raise NotADirectoryError(f"{self.dir} não é um diretório.")
        if not self.main:
            raise ValueError("O nome do módulo principal não pode ser vazio.")

        # itera sobre arquivos .py e cria Module para cada um
        self.modules = {
            file.stem: Module(file, self.main, self.funcs)
            for file in self.dir.iterdir()
            if file.is_file() and file.suffix == ".py"
        }

    def keys(self) -> list[str]:
        """Retorna lista de nomes de módulos carregados."""
        return list(self.modules.keys())

    def __getitem__(self, key: str):
        """Permite acesso via modules[key], retorna Module ou None."""
        return self.modules.get(key, None)

    def __iter__(self):
        """Iterador para percorrer pares (nome, Module)."""
        return iter(self.modules.items())

    def __len__(self):
        """Quantidade de módulos carregados no diretório."""
        return len(self.modules)
