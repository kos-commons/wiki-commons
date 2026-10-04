# wiki-commons.lua (Pandoc filter)

A [Pandoc](https://pandoc.org/) Lua filter for the Portable Wiki Markdown profile of the [Wiki Commons guidelines](https://kos-commons.github.io/wiki-commons/guidelines/08-Markup_and_Syntax.html). Optional tooling: it lets any of Pandoc's output formats consume the profile, and it keeps the free-link form when writing MediaWiki or DokuWiki markup.

Pandoc 3 parses `[[Target|Label]]` with its `wikilinks_title_after_pipe` extension (or `wikilinks_title_before_pipe` for label-first sources); the filter then resolves targets, maps fragments, handles `![[embeds]]`, `^block-id` tokens, and `> [!NOTE]` callouts.

```sh
# HTML with resolved links (index.json maps lowercased titles to hrefs)
pandoc -f commonmark_x+wikilinks_title_after_pipe --lua-filter converters/pandoc/wiki-commons.lua \
       -M wiki-commons-index=index.json -M wiki-commons-interwiki=interwiki.json page.md -t html

# Convert a portable page to MediaWiki or DokuWiki markup, keeping [[free links]]
pandoc -f commonmark_x+wikilinks_title_after_pipe --lua-filter converters/pandoc/wiki-commons.lua page.md -t mediawiki
pandoc -f commonmark_x+wikilinks_title_after_pipe --lua-filter converters/pandoc/wiki-commons.lua page.md -t dokuwiki
```

Options are passed as metadata: `wiki-commons-index` (JSON file, lowercased title → href), `wiki-commons-interwiki` (JSON file, prefix → URL template with `{title}`), `wiki-commons-separator` (default `/`), `wiki-commons-extension` (appended to unresolved targets when no index is given; default `.html`).

HTML output follows [MKUP-12](https://kos-commons.github.io/wiki-commons/guidelines/08-Markup_and_Syntax.html#mkup-12--rendered-html-conventions): links carry `class="wikilink"` and `data-wiki-target`; unknown targets become a `span.wikilink-missing` with an accessible label; identified blocks become `div.wiki-block` with the block id; callouts become `div.callout.callout-<type>`.

Test: `sh converters/pandoc/test.sh` (needs `pandoc` on the PATH, or `WIKI_COMMONS_PANDOC=/path/to/pandoc`).
