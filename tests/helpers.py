"""Shared test helpers: put tools/ on sys.path and locate the repository."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
EXAMPLE_BUNDLE = ROOT / "examples" / "portable-wiki-bundle"
CORPUS = ROOT / "corpus"
