# Converters for common toolchains

Optional adapters that let existing toolchains read and write the Portable Wiki Markdown profile and the Portable Wiki Bundle. None of them is required by the guidelines; each is one direction an engine or a site generator *may* take ([17 · Roadmap](../guidelines/17-Roadmap_and_Open_Questions.md)).

| Directory | Toolchain | What it does |
|---|---|---|
| [`remark/`](remark/) | JavaScript, unified/remark (Docusaurus, Astro, Gatsby, custom pipelines) | A remark plugin that turns `[[free links]]`, `![[embeds]]`, `^block-ids`, and `> [!NOTE]` callouts into mdast nodes that render to the HTML conventions of chapter 08 and stringify back to the same syntax. |
| [`markdown-it/`](markdown-it/) | JavaScript, markdown-it (VitePress, Eleventy, many editors and previewers) | A markdown-it plugin with an inline rule for free links, embeds, fragments, and interwiki prefixes, and core rules for `^block-ids` and `> [!NOTE]` callouts, rendering to the same HTML conventions (MKUP-12) as the remark plugin. |
| [`pandoc/`](pandoc/) | Pandoc 3 (any of its 40-odd output formats) | A Lua filter that resolves free links read with Pandoc's `wikilinks_title_after_pipe` extension, maps separators and interwiki prefixes, turns `^block-id` tokens into identified blocks and `> [!NOTE]` quotes into callout divs, and keeps the wikilink form when writing MediaWiki or DokuWiki. |
| [`../tools/`](../tools/) | Python | The reference tooling: scanner, dialect converters (Obsidian, Foam, Dendron, Logseq, Gollum, static sites), bundle build and unbundle with git history, Open Knowledge Format, BookStack Portable ZIP, and MediaWiki XML dump import and export, with import and export reports. |

Each converter has its own README with usage and tests. Contributions for other toolchains (Python-Markdown, goldmark, comrak, Marked) are welcome; the [conformance corpus](../corpus/README.md) is the shared test material.
