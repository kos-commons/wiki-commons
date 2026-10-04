# Conformance Corpus

> **Status:** Working Draft 0.2 (October 2026). The corpus grows from implementers' failures; additions and corrections are welcome ([CONTRIBUTING](../CONTRIBUTING.md)).

**In one sentence:** Small, reviewable test cases for the parts of the guidelines that can be tested: how Portable Wiki Markdown constructs parse and convert, how free links resolve, and which bundles a validator should accept or reject.

The corpus is what [17 · Roadmap](../guidelines/17-Roadmap_and_Open_Questions.md) calls the single most valuable next artifact. It is also honest about its limits: every expectation here was produced by the repository's reference implementation (`tools/pwb`) from a hand-written input and then reviewed by a person. The expectations therefore encode *one careful reading* of the guidelines, not a ruling. Where an engine disagrees, the right response is a discussion and, if the guidelines were unclear, a change to the guidelines and the corpus together.

## Layout

```
corpus/
  markup/<case>/            Portable Wiki Markdown constructs (chapter 08)
    input.md                the page under test
    case.yaml               optional options (see below)
    expected.scan.json      constructs found by the scanner
    expected.<dialect>.md   the page converted to another dialect, when case.yaml asks for it
  resolution/<case>/        free-link resolution (MKUP-5, NAV-6)
    case.yaml               the page index, the linking page's path, interwiki map, namespaces
    input.md                links to resolve
    expected.json           where each link resolves and by which rule
  bundles/
    valid/<name>/           Portable Wiki Bundles that validate without errors (one per fidelity level 0 to 3)
    invalid/<name>/         bundles the validator should reject, each with expected-errors.txt
```

The repository's example bundle (`examples/portable-wiki-bundle/`) covers fidelity levels 4 and 5 and is validated separately by the tests.

## Running

```sh
python3 tools/wikicommons.py corpus check          # compare against the expectations
python3 tools/wikicommons.py corpus check -v       # list every check
python3 tools/wikicommons.py corpus update         # regenerate expectations from the reference implementation
```

`update` overwrites expectations; review the diff before committing, because a wrong expectation is worse than a missing one. The test suite (`python3 -m unittest discover -s tests`) runs the corpus as one of its tests, and the CI workflow runs both.

## Markup cases

`input.md` is a page in some dialect (the portable profile unless `case.yaml` says otherwise). `case.yaml` may contain:

| Key | Meaning |
|---|---|
| `dialect` | The input's dialect: `portable` (default), `obsidian`, `foam`, `logseq`, `dendron`, `gollum`. |
| `label_order` | `target-first` (default) or `label-first`, for scanning the input. |
| `convert` | List of dialects to convert to; each produces `expected.<dialect>.md`. `static` means plain CommonMark with relative Markdown links. |
| `pages` | A page index for resolution during conversion: list of `{path, title, aliases}`. |
| `from_path` | The path of the page under test within that index (for relative links and hierarchy fallback). |
| `interwiki`, `namespaces`, `pages_prefix` | As in a bundle manifest. |
| `block_index` | Map of block identifiers to page titles (Logseq `((uuid))` references). |

`expected.scan.json` has these top-level keys: `frontmatter` (parsed YAML; values YAML coerced into dates appear as `{"$type": "date", "iso": ...}` so that the pitfall is visible), `headings` (with GitHub-style `anchor`), `links` (each with `raw`, `target`, `label`, `fragment`, `fragment_kind` of `heading` or `block`, `prefix`, `embed`, `line`), `block_ids`, `tags` (`frontmatter` and `inline`), `callouts`, `directives`, `envelopes` (snapshot envelopes with `kind`, `name`, `depth`, `body`), and `props`.

Converted outputs end with an HTML comment listing the degradation notes the converter recorded (dangling links turned into text, block identifiers removed, embeds turned into links), because declaring loss is part of what is being tested ([PR-17](../guidelines/02-Guiding_Principles.md)).

What the markup cases cover: every free-link form; label order in both directions; code spans, fences, and escapes; interwiki and namespace prefixes; embeds of pages, headings, blocks, and images; block identifiers in every position where they are and are not valid; heading anchors including duplicates, punctuation, and Japanese; inline and frontmatter tags; callouts with folding and titles; container and inline directives; snapshot and property envelopes including nesting and an unclosed one; frontmatter pitfalls; non-Latin and Unicode-decomposed titles; Logseq, Obsidian, and Dendron source dialects; conversion to Dendron, Gollum, Logseq, and static Markdown; dangling and same-page links; hidden HTML comments; standard Markdown links left untouched; and link edge cases such as empty labels and stray delimiters.

## Resolution cases

`case.yaml` defines the index (`pages`, each `{path, title, aliases, kind}`), the `from_path` of the linking page, and optionally `interwiki`, `namespaces`, and `pages_prefix`. Every link in `input.md` is resolved; `expected.json` records, per link, the resolved `path` (or `null`), the rule that resolved it (`via`: `exact`, `alias`, `case`, `normalized`, `hierarchy`, `relative`, `self`, `interwiki`, `ambiguous`, or `dangling`), the `url` for interwiki links, and the `candidates` when a bare title is ambiguous.

The cases cover the MKUP-5 order (exact, alias, case-insensitive, normalized, hierarchy fallback), same-directory preference and ambiguity reporting, unique-basename matching, relative paths, interwiki and namespace prefixes, Unicode normalization and separator collapsing, a `pages/` prefix, self links, and redirect pages.

## Bundle cases

Each valid bundle is a complete directory with `wiki-bundle.yaml`, pages, and checksums, at a declared fidelity level: level 0 (text only, no frontmatter), 1 (structure and an attachment with a sidecar), 2 (full metadata, a redirect, a category, a discussion page, interwiki and namespaces), 3 (history records and a contributor directory). `tools/validate_bundle.py` is expected to exit 0 on each.

Each invalid bundle breaks exactly one rule: a manifest without `format`, a checksum mismatch, a block reference to an identifier that does not exist, a suppressed history record that still carries content, frontmatter with wrong types, an attachment whose sidecar hash is wrong, a page referencing a missing attachment, a redirect page without a target. `expected-errors.txt` lists substrings that must appear in the validator's output.

## Adding a case

1. Create a directory with a numbered, descriptive name and write `input.md` by hand; keep it small and about one thing.
2. Add `case.yaml` if the case needs options, conversions, or an index.
3. Run `python3 tools/wikicommons.py corpus update`, then read the generated expectations line by line. If they are wrong, the reference implementation has a bug or the guidelines are ambiguous; fix the cause, not the expectation.
4. Mention the case in the relevant list above and open a pull request.

Cases that reproduce a disagreement between two real engines are the most valuable kind.

## What the corpus is not

It is not a certification: passing it means an implementation agrees with the reference reading of the testable parts of the guidelines, nothing more. It does not test rendering (how a construct looks), user experience patterns, APIs, or accessibility, all of which need other kinds of evidence. And it is deliberately small so that every expectation can be read by a person.
