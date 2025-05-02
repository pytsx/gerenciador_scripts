from pathlib import Path
import importlib.util
import sys


def load_module_from_file(path: Path) -> object:
  if not path.exists():
    raise FileNotFoundError(f"Arquivo {path} não encontrado.")

  module_name = path.stem  # Nome do módulo sem extensão
  spec = importlib.util.spec_from_file_location(module_name, str(path))
  if spec is None:
    raise ImportError(f"Não foi possível criar o spec para {path}")
  module = importlib.util.module_from_spec(spec)  # Cria o módulo a partir do spec
  spec.loader.exec_module(module)  # Carrega o módulo
  sys.modules[module_name] = module
  return module 

def load_functions_from_file(path: Path, funcs: list[str]) -> callable:
  module = load_module_from_file(path)
  res = {}

  for func_name in funcs:
    if hasattr(module, func_name):
      func = getattr(module, func_name)
      if callable(func):
        res[func_name] = func
    else:
      res[func_name] = lambda: None
    
  return res 

def scan_modules_dir(dir: str, funcs: list[str]) -> dict[str, dict[str, callable]]: 
  return {
    file.stem: load_functions_from_file(file, funcs) 
    for file 
    in (Path(__file__).parent / dir).iterdir() 
    if file.is_file() and file.suffix == ".py"
  }