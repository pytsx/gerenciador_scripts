import platform
from pathlib import Path
import os 
import subprocess

blacklist = [
  "__pycache__",
  "__",
  "__ignore__"
]


def get_downloads_path() -> Path:
  if platform.system() == "Windows":
      import ctypes.wintypes

      buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
      ctypes.windll.shell32.SHGetFolderPathW(None, 0x0005, None, 0, buf)

      downloads = Path(buf.value).parent / "Downloads"
  else:
      downloads = Path.home() / "Downloads"

  return downloads


def open_file_explorer(path: Path) -> None:
  if platform.system() == "Windows":
    os.startfile(path)
  elif platform.system() == "Darwin":  # macOS
    subprocess.run(["open", path])
  else:  # Linux
    subprocess.run(["xdg-open", path])
    

def open_downloads() -> None:
  downloads = get_downloads_path()
  open_file_explorer(downloads)