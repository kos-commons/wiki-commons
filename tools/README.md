# Tools

Small, dependency-light helpers that accompany the guidelines. They are reference tooling in the sense of [17 · Roadmap](../guidelines/17-Roadmap_and_Open_Questions.md): useful today, and a starting point for better tools.

| Tool | Purpose |
|---|---|
| `validate_bundle.py` | Validates a Portable Wiki Bundle directory against the schemas in `schemas/`, verifies checksums, resolves block references and link-graph entries, and reports dangling links. Python 3 only; PyYAML is needed to check the YAML files. |
| `check_links.py` | Checks that every relative Markdown link and heading anchor inside this repository's own documents resolves. Run in CI and before releases. |
| `build_book.py` | Assembles the mdBook source tree in `book/src/` by mirroring the repository layout, adapting the example bundle's pages, and verifying `book/SUMMARY.md`. See [book/README.md](../book/README.md). |
| `check_site.py` | Checks every internal link and anchor in a built site (`book/book/`). Run in CI after `mdbook build`. |
| `wikicommons.py` | Command-line entry point for the reference tooling in `pwb/`: `scan`, `convert`, `resolve`, `bundle`, `unbundle`, `okf export|import`, `validate`, `corpus check|update`. |
| `pwb/` | The library: `markup` (scanner and dialect converter), `resolve` (link resolution), `bundle` (folder ↔ bundle, frontmatter mapping, attachments), `history` (git history replay), `okf` (Open Knowledge Format), `corpus` (corpus runner), `cli`. |
| `wiki-commons.yaml` | The tooling's self-assessment against the conformance profiles of chapter 16. |

```sh
python3 tools/wikicommons.py --help
python3 tools/wikicommons.py bundle ~/vault out/bundle --dialect obsidian --history --name "My vault" --license CC-BY-SA-4.0
python3 tools/wikicommons.py unbundle out/bundle out/site --dialect static
python3 tools/wikicommons.py okf export out/bundle out/okf
python3 -m unittest discover -s tests
```

Dialects understood by `convert`, `bundle`, and `unbundle`: `portable`, `obsidian`, `foam`, `dendron`, `logseq`, `gollum`, `static`. The tools need Python 3 and PyYAML; nothing else.

```sh
python3 tools/validate_bundle.py examples/portable-wiki-bundle
python3 tools/check_links.py
python3 tools/build_book.py && mdbook build book && python3 tools/check_site.py book/book
```
