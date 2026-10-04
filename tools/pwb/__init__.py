"""Reference tooling for the Wiki Commons guidelines.

Modules:
  markup   scan Portable Wiki Markdown constructs and convert between dialects
  resolve  title normalization and free-link resolution (MKUP-5)
  bundle   assemble a Portable Wiki Bundle from a folder of Markdown, and back
  history  revision history from a git repository as portable history records
  okf      Open Knowledge Format (OKF) interchange
  corpus   run the conformance corpus
  cli      command-line interface (see tools/wikicommons.py)

Standard library only, plus PyYAML for YAML files.
"""
__version__ = "0.2.0"
