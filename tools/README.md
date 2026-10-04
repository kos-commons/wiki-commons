# Tools

Small, dependency-light helpers that accompany the guidelines. They are reference tooling in the sense of [17 · Roadmap](../guidelines/17-Roadmap_and_Open_Questions.md): useful today, and a starting point for better tools.

| Tool | Purpose |
|---|---|
| `validate_bundle.py` | Validates a Portable Wiki Bundle directory against the schemas in `schemas/`, verifies checksums, resolves block references and link-graph entries, and reports dangling links. Python 3 only; PyYAML is needed to check the YAML files. |
| `check_links.py` | Checks that every relative Markdown link and heading anchor inside this repository's own documents resolves. Run in CI and before releases. |
| `build_book.py` | Assembles the mdBook source tree in `book/src/` by mirroring the repository layout, adapting the example bundle's pages, and verifying `book/SUMMARY.md`. See [book/README.md](../book/README.md). |
| `check_site.py` | Checks every internal link and anchor in a built site (`book/book/`). Run in CI after `mdbook build`. |

```sh
python3 tools/validate_bundle.py examples/portable-wiki-bundle
python3 tools/check_links.py
python3 tools/build_book.py && mdbook build book && python3 tools/check_site.py book/book
```
