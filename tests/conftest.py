import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
praktikum = types.ModuleType("praktikum")
praktikum.__path__ = [str(ROOT)]
sys.modules.setdefault("praktikum", praktikum)
