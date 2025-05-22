"""
 scaffolding permite à engine injetar arquivos e diretórios preconfigurados em src. 
 Esta abordagem facilita a criação de novos componentes, páginas e scripts com estrutura padronizada.
"""

from pathlib import Path
from string import Template


class Scaffold:
  def __init__(self, templates_dir: Path = None):
    self.templates_dir =  templates_dir or (Path(__file__).parent / "templates")
    print(f"Templates dir: {self.templates_dir}")
    
  def list_templates(self) -> list[str]:
    """Lista todos os templates disponíveis"""
    return [d.name for d in self.templates_dir.iterdir() if d.is_dir()]
  
      
  def scaffold(self, template_name: str, target_dir: Path, variables: dict = {}):
    """
    Gera um scaffold com base em um template.
    
    Args:
      template_name: Nome do template a ser usado
      target_dir: Diretório alvo onde os arquivos serão gerados
      variables: Variáveis para substituição nos templates
    """
    template_dir = self.templates_dir / template_name
    
    if not template_dir.exists():
      raise ValueError(f"Template '{template_name}' não encontrado")
    
    # Cria o diretório alvo se não existir
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Copia e processa os arquivos do template
    for file_path in template_dir.glob("**/*"):
      if file_path.is_file():
        # Caminho relativo ao template
        rel_path = file_path.relative_to(template_dir)
        
        # Processa o nome do arquivo para variáveis
        processed_path = str(rel_path)
        for key, value in variables.items():
          var_pattern = f"__{key}__"
          processed_path = processed_path.replace(var_pattern, value)
        
        # Caminho final do arquivo
        dest_path = target_dir / processed_path
        
        # Cria diretório pai se não existir
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Lê o conteúdo do template
        with open(file_path, 'r', encoding='utf-8') as f:
          content = f.read()
        
        # Substitui variáveis no conteúdo
        template = Template(content)
        processed_content = template.safe_substitute(variables)
        
        # Escreve o arquivo processado
        with open(dest_path, 'w', encoding='utf-8') as f:
          f.write(processed_content)
                
    return target_dir

  def scaffold_page(self, page_name: str, src_dir: Path):
    """
    Cria uma nova página com base no template de página.
    """
    target_dir = src_dir / "app" / page_name
    
    variables = {
      "name": page_name,
      "title": page_name.replace("-", " ").title()
    }
    
    return self.scaffold("page", target_dir, variables)

  def scaffold_component(self, component_name: str, src_dir: Path):
    """
    Cria um novo componente com base no template de componente.
    """
    target_dir = src_dir / "components"
    
    variables = {
      "name": component_name,
      "class_name": "".join(word.title() for word in component_name.split("_"))
    }
    
    return self.scaffold("component", target_dir, variables)

  def scaffold_script(self, script_name: str, scripts_dir: Path):
    """
    Cria um novo script com base no template de script.
    """
    variables = {
      "name": script_name,
      "title": script_name.replace("_", " ").title()
    }
    
    return self.scaffold("script", scripts_dir, variables)
  
__all__ = ["Scaffold"]