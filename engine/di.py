from typing import Any, Dict, Optional, TypeVar, Type
import inspect
from functools import wraps

T = TypeVar('T')

class ServiceContainer:
  """
    Container central para serviços com suporte a singleton e transient.
    
    Uso básico:

    container = ServiceContainer()
    container.register("theme_service", ThemeService())
    
    # Resolver manualmente
    theme_service = container.resolve("theme_service")
    
    # Usar com decorador de injeção
    @container.inject("theme_service", "script_service")
    class MyComponent:
        def __init__(self, ctx):
            self.ctx = ctx
            # self.theme_service e self.script_service já estão disponíveis
  
  """
  def __init__(self):
      self._services: Dict[str, Dict[str, Any]] = {}
      self._scopes: Dict[str, Dict[str, Any]] = {}
      self._current_scope: Optional[str] = None
      
  def register(self, key: str, service_or_factory: Any, singleton: bool = True, scope: Optional[str] = None) -> None:
      """
      Registra um serviço no container.
      
      Args:
          key: Identificador único do serviço
          service_or_factory: Instância do serviço ou factory function
          singleton: Se True, mantém a mesma instância, do contrário cria nova a cada resolução
          scope: Opcional, nome do escopo para serviços com escopo definido
      """
      is_factory = callable(service_or_factory) and not isinstance(service_or_factory, type)
      
      self._services[key] = {
          # Se é singleton e não factory, usa a própria instância, caso contrário None
          "instance": None if is_factory or not singleton else service_or_factory,
          # Se é factory ou é classe (para instanciação lazy)
          "factory": service_or_factory if is_factory or isinstance(service_or_factory, type) else None,
          "singleton": singleton,
          "scope": scope
      }
      
  def resolve(self, key: str) -> Any:
      """
      Resolve um serviço pelo seu identificador.
      
      Args:
          key: Identificador do serviço
          
      Returns:
          A instância do serviço
          
      Raises:
          KeyError: Se o serviço não estiver registrado
      """
      if key not in self._services:
          raise KeyError(f"Serviço '{key}' não está registrado no container")
          
      service_def = self._services[key]
      
      # Se tem escopo e o escopo está ativo
      if service_def["scope"] and self._current_scope:
          scope_key = f"{service_def['scope']}:{self._current_scope}"
          
          # Se o escopo existe e tem o serviço
          if scope_key in self._scopes and key in self._scopes[scope_key]:
              return self._scopes[scope_key][key]
      
      # Se é singleton e já tem instância
      if service_def["singleton"] and service_def["instance"] is not None:
          return service_def["instance"]
          
      # Se não tem instância mas tem factory
      if service_def["factory"] is not None:
          factory = service_def["factory"]
          
          # Se é uma classe, instancia
          if isinstance(factory, type):
              instance = self._instantiate(factory)
          else:
              # Caso contrário chama a factory function
              instance = factory()
              
          # Se é singleton, guarda a instância
          if service_def["singleton"]:
              service_def["instance"] = instance
              
          # Se tem escopo e o escopo está ativo
          if service_def["scope"] and self._current_scope:
              scope_key = f"{service_def['scope']}:{self._current_scope}"
              
              if scope_key not in self._scopes:
                  self._scopes[scope_key] = {}
                  
              self._scopes[scope_key][key] = instance
              
          return instance
          
      return service_def["instance"]
  
  def _instantiate(self, cls: Type[T]) -> T:
      """
      Instancia uma classe injetando suas dependências.
      
      Args:
          cls: Classe a ser instanciada
          
      Returns:
          Instância da classe com dependências injetadas
      """
      # Inspeciona os parâmetros do construtor
      signature = inspect.signature(cls.__init__)
      params = {}
      
      # Para cada parâmetro (exceto self)
      for name, param in signature.parameters.items():
          if name == 'self':
              continue
              
          # Se o parâmetro tem uma anotação de tipo
          if param.annotation != inspect.Parameter.empty:
              # Procura um serviço registrado com o nome do parâmetro
              if name in self._services:
                  params[name] = self.resolve(name)
                  
      # Instancia a classe com os parâmetros injetados
      return cls(**params)
  
  def begin_scope(self, name: str) -> None:
      """Inicia um novo escopo para serviços scoped"""
      self._current_scope = name
      
  def end_scope(self) -> None:
      """Finaliza o escopo atual e libera os serviços"""
      if self._current_scope:
          for scope_key in list(self._scopes.keys()):
              if scope_key.endswith(f":{self._current_scope}"):
                  del self._scopes[scope_key]
                  
      self._current_scope = None
      
  def inject(self, *service_keys: str):
    """
      Decorador para injetar serviços em uma classe.
      
      Args:
          *service_keys: Nomes dos serviços a serem injetados
          
      Returns:
          Decorador que injeta os serviços na classe
      
      Exemplo:

      @container.inject("theme_service", "script_service")
      class MyComponent:
          def __init__(self, ctx):
              self.ctx = ctx
              # self.theme_service e self.script_service já estão disponíveis
      
    """
    def decorator(cls):
      original_init = cls.__init__
      
      @wraps(original_init)
      def __init__(_self, *args, **kwargs):
          # Injeta os serviços como atributos
          for key in service_keys:
              setattr(_self, key, _self.resolve(key))
              
          # Chama o construtor original
          original_init(_self, *args, **kwargs)
          
      # Adiciona método de resolução na instância
      cls.resolve = lambda self, key, _c = self: _c.resolve(key)
      
      # Substitui o construtor
      cls.__init__ = __init__
      return cls
        
    return decorator


# Instância global do container
container = ServiceContainer()

# Decorador de injeção para uso simplificado
def inject(*service_keys: str):
  """
  Decorador para injetar serviços em uma classe.
  
  Args:
      *service_keys: Nomes dos serviços a serem injetados
      
  Returns:
      Classe com as dependências injetadas automaticamente
  """
  return container.inject(*service_keys)