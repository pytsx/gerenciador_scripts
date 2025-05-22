import sys 
import argparse
from pathlib import Path
from engine.scaffold import Scaffold

class CommandArg:
    def __init__(self, name: str, help: str):
        self.name = name
        self.help = help

class Command: 
    def __init__(self, name: str, help: str, action: callable, args: list[CommandArg] = []):
        self.name = name
        self.help = help
        self.args = args
        self.action = action

    def configure_command_parser(self, subparser: argparse._SubParsersAction):
        cmd_parser = subparser.add_parser(self.name, help=self.help)
        for arg in self.args:
            cmd_parser.add_argument(arg.name, help=arg.help)

def create_cli(
    title: str,
    cmds: list[Command] = []    
) -> tuple[argparse.ArgumentParser, argparse.Namespace]:
    parser = argparse.ArgumentParser(description=title)
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")
    
    [cmd.configure_command_parser(subparsers) for cmd in cmds]

    return parser, parser.parse_args()


def run_cli():
    scaffold = Scaffold(Path(__file__).parent / "templates")
    
    cmds = {
        "page": Command(
            name="page",
            help="Cria uma nova página",
            action=lambda name: scaffold.scaffold_page(name, Path("./src")), 
            args=[CommandArg("name", "Nome da página")]
        ),
        "component": Command(
            name="component",
            help="Cria um novo componente",
            action=lambda name: scaffold.scaffold_component(name,Path("./src") ),
            args=[CommandArg("name", "Nome do componente")]
        ),
        "script":  Command(
            name="script",
            help="Cria um novo script",
            action=lambda name: scaffold.scaffold_script(name, Path("./scripts")),
            args=[CommandArg("name", "Nome do script")]
        )
    }
    
    parser, args = create_cli("Gerenciador de scaffolding para scripts e componentes", cmds=cmds.values())
    
    if args.command in cmds:
        cmds[args.command].action(args.name)
        print(f"'{args.name}' criado com sucesso!")
    elif args.command:
        # Handle unknown commands if necessary, or let argparse handle it
        print(f"[ERROR] Comando desconhecido: {args.command}")
        parser.print_help()
    else:
        parser.print_help()

def initialize_with_cli(app: callable):
    if len(sys.argv) > 1 and sys.argv[1] == "new":
        # Remove o primeiro argumento para passar os demais para o CLI
        sys.argv.pop(1)
        run_cli()
        return 
    app()
    
    
__all__ = ["initialize_with_cli"]