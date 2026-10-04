# Tools

Small, dependency-light helpers that accompany the guidelines. They are reference tooling in the sense of [17 · Roadmap](../guidelines/17-Roadmap_and_Open_Questions.md): useful today, and a starting point for better tools.

| Tool | Purpose |
|---|---|
| `validate_bundle.py` | Validates a Portable Wiki Bundle directory against the schemas in `schemas/`, verifies checksums, resolves block references and link-graph entries, and reports dangling links. Python 3 only; PyYAML is needed to check the YAML files. |
| `check_links.py` | Checks that every relative Markdown link and heading anchor inside this repository's own documents resolves. Used before releases. |

```sh
python3 tools/validate_bundle.py examples/portable-wiki-bundle
python3 tools/check_links.py
```
