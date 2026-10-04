# Building the site

The published site at <https://kos-commons.github.io/wiki-commons/> is built with [mdBook](https://rust-lang.github.io/mdBook/) from the files in this repository.

mdBook needs a single source directory, while the repository keeps its chapters under `guidelines/` with `README.md`, `CONTRIBUTING.md`, `schemas/`, `examples/`, and `tools/` beside them, all joined by relative links. `tools/build_book.py` therefore mirrors the repository layout into `book/src/` (ignored by git), adapts the example bundle's pages (frontmatter shown as a code block, spaces in file names replaced by hyphens), generates an index page for the example bundle directory, copies `book/SUMMARY.md` in, and fails if the summary points at a file that does not exist.

```sh
python3 tools/build_book.py      # assemble book/src/
mdbook build book                # output in book/book/
mdbook serve book --open         # local preview with live reload (rerun build_book.py after edits)
```

Files in this directory:

| File | Purpose |
|---|---|
| `book.toml` | mdBook configuration. `site-url` is the GitHub Pages path of this repository; change it if the site moves to a custom domain. |
| `SUMMARY.md` | The table of contents. Add new chapters here as well as in `guidelines/`. |
| `src/`, `book/` | Generated; not committed. |

The GitHub Actions workflow in `.github/workflows/pages.yml` runs the repository checks (`tools/check_links.py`, `tools/validate_bundle.py`), assembles and builds the book with a pinned mdBook version, verifies the built HTML, and deploys it to GitHub Pages on every push to `main`. Pull requests run the same build without deploying.
