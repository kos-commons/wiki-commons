#!/usr/bin/env python3
"""Entry point for the Wiki Commons reference tooling (see tools/README.md).

    python3 tools/wikicommons.py --help
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pwb.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
