#!/bin/sh
# Smoke test for wiki-commons.lua. Requires Pandoc 3.
set -eu
PANDOC="${WIKI_COMMONS_PANDOC:-pandoc}"
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
printf '{"edit conflicts": "edit-conflicts.html", "guides/getting started": "guides/getting-started.html"}' > "$TMP/index.json"
printf '{"wp": "https://en.wikipedia.org/wiki/{title}"}' > "$TMP/interwiki.json"
cat > "$TMP/page.md" <<'MD'
See [[Edit Conflicts|the page]], [[Guides/Getting Started#Install]], [[Missing]], [[wp:Wiki]] and ![[Edit Conflicts#^b1]] and ![[diagram.png|200]].

A paragraph. ^para-1

> [!NOTE]- Title here
> body
MD
HTML="$($PANDOC -f commonmark_x+wikilinks_title_after_pipe --lua-filter "$HERE/wiki-commons.lua" -M wiki-commons-index="$TMP/index.json" -M wiki-commons-interwiki="$TMP/interwiki.json" "$TMP/page.md" -t html)"
check() { printf '%s' "$HTML" | grep -qF -- "$1" || { echo "MISSING in HTML: $1"; printf '%s\n' "$HTML"; exit 1; }; }
HTML="$(printf '%s' "$HTML" | tr '\n' ' ')"
check 'href="edit-conflicts.html"'
check 'data-wiki-target="Edit Conflicts">the page</a>'
check 'href="guides/getting-started.html#install"'
check 'class="wikilink wikilink-missing"'
check 'aria-label="page does not exist yet">Missing</span>'
check 'href="https://en.wikipedia.org/wiki/Wiki"'
check 'class="wikilink wikilink-interwiki"'
check 'href="edit-conflicts.html#b1"'
check 'class="wiki-embed"'
check '<img src="diagram.png"'
check 'alt="diagram.png"'
check 'id="para-1" class="wiki-block"'
check 'class="callout callout-note"'
check 'data-callout="note"'
check 'data-callout-fold="-"'
check '<strong>Title here</strong>'
MW="$($PANDOC -f commonmark_x+wikilinks_title_after_pipe --lua-filter "$HERE/wiki-commons.lua" "$TMP/page.md" -t mediawiki)"
printf '%s' "$MW" | grep -qF '[[Edit Conflicts|the page]]' || { echo "mediawiki output lost the wikilink"; printf '%s\n' "$MW"; exit 1; }
printf '%s' "$MW" | grep -qF '[[Missing]]' || { echo "mediawiki output lost [[Missing]]"; exit 1; }
DW="$($PANDOC -f commonmark_x+wikilinks_title_after_pipe --lua-filter "$HERE/wiki-commons.lua" "$TMP/page.md" -t dokuwiki)"
printf '%s' "$DW" | grep -qF '[[Missing]]' || { echo "dokuwiki output lost [[Missing]]"; printf '%s\n' "$DW"; exit 1; }
echo "wiki-commons.lua: all checks passed"
