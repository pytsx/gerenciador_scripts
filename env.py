from engine.modules import Modules
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "src" / "app"

scripts = Modules(dir=BASE_DIR / "scripts", main="execute")