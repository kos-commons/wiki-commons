# 08 · Markup and Syntax

> **Part III — Interoperability Guidelines** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [07 · Collaboration, Awareness and Governance](07-Collaboration_Awareness_and_Governance.md) · Next: [09 · Metadata and Frontmatter](09-Metadata_and_Frontmatter.md)

**In one sentence:** No engine needs to change its native markup; every engine is encouraged to be able to read and write one shared Markdown profile that carries the things Markdown alone cannot: free links, anchors, block identifiers, transclusion, tags, callouts, and a graceful way to carry everything else.

Recommendations in this chapter carry the prefix `MKUP-`.

---

## 1. The lesson of the markup wars

Two things are true at once. Every attempt to make all wikis share one native markup has failed, and most wikis have nonetheless converged on Markdown as the thing they import, export, paste, and increasingly write. WikiCreole, conceived at the 2006 wiki symposium and released as version 1.0 in 2007, was designed as a neutral common markup by comparing existing engines; a handful adopted it, the largest engines kept their own syntax, and the specification has been frozen since. Meanwhile CommonMark gave Markdown an unambiguous specification, GitHub Flavored Markdown added the tables and task lists everyone wanted, and a generation of note tools (Obsidian, Logseq, Foam, Dendron, Silverbullet, and many more) made `[[wikilinks]]` inside Markdown an ordinary thing.

Markdown is therefore the practical common tongue, with one well-known gap: it has no native syntax for the features that make a wiki a wiki. Each tool fills the gap slightly differently.

This chapter responds to both truths:

- **Native markup is not the target.** Wikitext, DokuWiki syntax, TiddlyWiki WikiText, PukiWiki syntax, Org-mode, AsciiDoc, Scrapbox notation, and block JSON are all legitimate. Nothing here asks an engine to abandon its syntax.
- **One portable profile is the target for interchange.** The *Portable Wiki Markdown* profile below is a small, layered set of conventions that an engine is encouraged to **read** on import and **write** on export, and that new Markdown-based engines are encouraged to adopt natively because it costs nothing to do so.

## 2. The Portable Wiki Markdown profile

The profile is layered. Each layer is a superset of the one below; an engine declares which layer it reads and writes.

| Layer | Name | Content |
|---|---|---|
| 0 | **CommonMark core** | Everything in the CommonMark specification: paragraphs, ATX and setext headings, emphasis, lists, fenced and indented code, block quotes, inline links and images, autolinks, thematic breaks, HTML blocks and inline HTML, entity references. |
| 1 | **Shared extensions** | The GFM specification's extensions (tables, task lists, strikethrough, extended autolinks); footnotes (not in the GFM specification but implemented almost everywhere); a YAML frontmatter block ([Chapter 09](09-Metadata_and_Frontmatter.md)). |
| 2 | **Wiki extensions** | Free links, labelled links, heading and block anchors, block identifiers, embeds and transclusion, tags, callouts, hidden comments, the interwiki prefix form, and a generic directive syntax for declared extensions. |
| 3 | **Declared engine extensions** | Anything else, carried in a form that degrades to readable text and is declared in the bundle manifest ([Chapter 12](12-Extensibility_Macros_and_Dynamic_Content.md)). |

A page written in the profile looks like this:

```markdown
---
id: 018f6c3e-9d2b-7c4a-8e1f-2b3c4d5e6f70
title: Edit Conflicts
aliases: [Edit conflict, Editing collisions]
tags: [history, collaboration]
created: 2024-03-02T10:15:00+09:00
updated: 2026-09-30T18:42:11Z
status: stable
license: CC-BY-SA-4.0
lang: en
---

An **edit conflict** happens when two people save changes to the same
page based on the same earlier revision. See [[Revision History]] and
[[Revision History#Merging|how merging works]].

> [!NOTE]
> Most engines merge non-overlapping changes automatically.

The resolution screen shows both versions side by side. ^conflict-ui

![[Glossary#^optimistic-concurrency]]

Related: [[wikipedia:Edit conflict]] · #collaboration
```

Everything in that example renders acceptably in a plain CommonMark renderer: the links become literal `[[...]]` text (still legible), the callout becomes a block quote starting with `[!NOTE]`, the `^conflict-ui` identifier is a harmless token, the embed becomes a literal line. That is the design goal of Layer 2: **every construct degrades to something a reader can still understand.**

## 3. Recommendations

### Declaring what you speak

#### MKUP-1 · Declare your flavour

Every engine **should** document its native markup and the Markdown profile layer it reads and writes. When serving Markdown over HTTP, engines **should** use the `text/markdown` media type (RFC 7763) with its required `charset` parameter and its `variant` parameter naming a registered Markdown variant (for example `text/markdown; charset=UTF-8; variant=CommonMark` or `variant=GFM`), and **should** name the profile layer in the bundle manifest (`markup.profile: portable-wiki-markdown/2`), since no registered variant describes wiki extensions. Native formats **should** be served with their own declared media type (for example `text/x-wiki` for wikitext) and named in the manifest.

#### MKUP-2 · Parse with a CommonMark-conformant parser

Importers **should** use a parser that passes the CommonMark test suite and layers the extensions on top, rather than a hand-written approximation. Exporters **should** produce output that a CommonMark parser interprets as intended: blank lines around blocks, consistent list markers, escaped characters where ambiguous. Engines **may** choose a stricter or more lenient native dialect, but the *exported* form **should** be conservative.

#### MKUP-3 · Support the shared extensions

Layer 1 is **recommended** in full for any Markdown-based engine. For engines whose native format is not Markdown, exporters **should** map tables to GFM tables, checklists to task lists, and notes to footnotes where the native format has them. Fenced code blocks **should** keep their info string (the language name); that is where diagrams and other declared extensions live ([MKUP-15](#mkup-15--callouts-math-and-diagrams)).

### Free links

#### MKUP-4 · The free link forms

Engines **should** read, and **should** write on export, the following forms:

| Form | Meaning |
|---|---|
| `[[Title]]` | Link to the page whose title (or alias) is *Title*; shown text is *Title*. |
| `[[Title\|Shown text]]` | Same target, custom label. |
| `[[Title#Heading text]]` | Link to the heading whose text is *Heading text* in *Title*. The anchor is the heading's text, not a slug ([MKUP-8](#mkup-8--headings-and-anchors)). |
| `[[Title#^block-id]]` | Link to the block carrying identifier *block-id* ([MKUP-9](#mkup-9--block-identifiers)). |
| `[[#Heading text]]`, `[[#^block-id]]` | Within the current page. |
| `[[Namespace/Title]]` | Link into a hierarchy, using `/` ([MKUP-7](#mkup-7--hierarchy-separator)). |
| `[[prefix:Title]]` | Interwiki link when *prefix* is declared in the manifest's interwiki map ([MKUP-13](#mkup-13--interwiki-prefix-form)); otherwise an ordinary title containing a colon. |

Inside code spans and fenced code, `[[...]]` **should not** be parsed. A literal double bracket outside code **may** be escaped as `\[\[`. The characters `|`, `#`, and `]]` cannot appear unescaped in a title.

#### MKUP-5 · Resolution should be tolerant and documented

Engines **should** resolve a link target in a documented order, for example: exact title match; alias match ([META-4](09-Metadata_and_Frontmatter.md)); case-insensitive match; match after normalization (Unicode NFC, collapsing runs of spaces, underscores and hyphens into one separator, trimming); then hierarchy fallback (same namespace first, then unique match anywhere, then declared disambiguation). When a bare title matches several pages in a hierarchy, the engine **should** prefer the nearest and **should** report the ambiguity in health views ([NAV-15](04-Discovery_Navigation_and_Topology.md#nav-15--health-views-orphans-wanted-dead-ends)). Resolution rules **should** be stated in the manifest so that importers can reproduce them.

#### MKUP-6 · Target first, label second; declare otherwise

The order `[[Target|Label]]` is **recommended**. It is the convention of MediaWiki, DokuWiki, MoinMoin, PmWiki (pipe form), Trac, Redmine, Zim, Wikidot, WikiCreole, Tiki, Obsidian, Quartz, Foam, Silverbullet, and most Markdown wikilink libraries; TWiki and Foswiki use the same order with a different delimiter (`[[Target][Label]]`). The reverse order (`[[Label|Target]]`) is native to TiddlyWiki, ikiwiki, Gollum, GitLab wikis, JSPWiki, Hiki, and Dendron, and appears with other delimiters in PukiWiki and GROWI (`[[Label>Target]]`), XWiki (`[[Label>>Target]]`), Confluence's legacy wiki markup (`[Label|Target]`), Logseq's Markdown-link form (`[Label]([[Target]])`), and PmWiki's arrow form (`[[Label -> Target]]`). The split is old enough that Gitea's renderer guesses the order heuristically, and GitHub's documentation and Gollum's disagree about which order the GitHub wiki uses. Engines using label-first order **should** declare `markup.link_label_order: label-first` in exports so that converters can flip it, and all engines are **encouraged** to accept both on import when the target can be identified unambiguously (for example, when exactly one side matches an existing title). Delimiter variants are mapped by converters ([Appendix B](appendices/B-Syntax_Crosswalk.md)).

#### MKUP-7 · Hierarchy separator

`/` is **recommended** as the portable separator in link targets and page paths. Engines whose native separator is `:` (DokuWiki namespaces) or `.` (Dendron, PmWiki's alternate form) **should** map it to `/` on export and back on import, and **should** record the native separator in the manifest. MediaWiki-style namespace prefixes (`Talk:Title`, `User:Name`) are not hierarchy; they **should** be preserved in titles and declared in the manifest's namespace list so that importers can distinguish them from interwiki prefixes.

### Structure and addressing

#### MKUP-8 · Headings and anchors

ATX headings (`## Heading`) are **recommended** for export. The page title **should** live in frontmatter; body headings **should** then begin at level 2. A leading level-1 heading identical to the title **may** be present and importers **should** treat it as the title rather than duplicating it. Engines **should** derive heading anchors deterministically from heading text and document the algorithm; the widely implemented "GitHub style" (lower-case, punctuation removed, spaces to hyphens, duplicates suffixed `-1`, `-2`) is **recommended** for Markdown engines. In portable links, the fragment is the **heading text** (`[[Page#Heading text]]`), so that each engine computes its own anchor and the link survives differing algorithms.

#### MKUP-9 · Block identifiers

A block (paragraph, list item, block quote, table, code block) **may** carry an identifier written as a trailing `^id` token on its last line, separated by a space, where `id` matches `[A-Za-z0-9][A-Za-z0-9_-]*`. Identifiers **should** be unique within a page and stable over time; UUIDs or short random strings are both acceptable. `[[Page#^id]]` links to the block; `![[Page#^id]]` transcludes it. Engines whose native model gives every block an identifier (Logseq, Roam, Notion, Scrapbox / Cosense, Federated Wiki) **should** export those identifiers in this form; engines without a block model **should** preserve the token on import (as text or metadata) rather than discarding it, so that references remain resolvable later. Logseq and Roam `((uuid))` references map to `[[Page#^uuid]]` when the containing page is known, and to a bundle-wide block index otherwise ([XFER-3](10-Interchange_and_Portability.md)).

#### MKUP-10 · Embeds and transclusion

`![[Page]]`, `![[Page#Heading text]]`, and `![[Page#^id]]` are **recommended** for transcluding another page, section, or block. Images and attachments **should** use the standard Markdown image syntax, `![alt text](attachments/diagram.png)`, with a relative path and non-empty alternative text; engines that natively write `![[image.png]]` **should** convert on export. Parameterized transclusion (templates with arguments) is engine-specific and **should** be snapshotted on export using the envelope in [Chapter 12](12-Extensibility_Macros_and_Dynamic_Content.md). Transclusion **should** be depth-limited and cycle-safe.

#### MKUP-11 · Hidden comments

HTML comments (`<!-- ... -->`) are **recommended** as the portable form for editorial notes that readers should not see; every Markdown renderer hides them and every text editor shows them. Engines with their own hidden-comment syntax (Obsidian `%% ... %%`, wikitext `<!-- -->`, Org `# ...`) **should** map it to HTML comments on export. Comments that begin with `wiki:` are reserved for the declared-extension envelopes of [Chapter 12](12-Extensibility_Macros_and_Dynamic_Content.md).

#### MKUP-12 · Rendered HTML conventions

When rendering to HTML, engines **should** emit semantic elements (`<article>`, `<section>`, `<nav>`, `<h1>`–`<h6>`, `<time datetime>`), `id` attributes on headings and identified blocks, and a distinguishable class on internal links; `class="wikilink"` with `class="wikilink wikilink-missing"` for dangling links is **recommended** so that themes and tools can recognize them regardless of engine. A `data-wiki-target` attribute carrying the unresolved title is **encouraged**. Links to external sites on open wikis **should** carry `rel="nofollow ugc"` or the engine's documented equivalent. Pages **should** declare their language (`lang`) and **should** expose metadata machine-readably ([META-12](09-Metadata_and_Frontmatter.md)).

### Wiki vocabulary

#### MKUP-13 · Interwiki prefix form

`[[prefix:Title]]` is **recommended** for links into other wikis, with the prefix declared in the manifest's `interwiki` map (prefix → URL template). Importers lacking interwiki support **should** expand the link to a plain URL using the map rather than dropping it. The native DokuWiki form `[[prefix>Title]]` **should** be converted on export.

#### MKUP-14 · Tags

`tags:` in frontmatter is the **recommended** canonical location for a page's tags ([META-5](09-Metadata_and_Frontmatter.md)). Inline hashtags (`#tag`, with no space after `#` and not at the start of a line, where `#` means a heading) **may** additionally be supported; exporters **should** also list inline tags in frontmatter so that importers without inline-tag support lose nothing. Engines in which a tag *is* a page (Logseq, Scrapbox / Cosense, TiddlyWiki) **should** export the tag pages themselves as pages of `kind: category`.

#### MKUP-15 · Callouts, math, and diagrams

- *Callouts.* The block-quote form `> [!TYPE]` followed by an optional title and body is **recommended**; it is shared by GitHub alerts and Obsidian callouts and degrades to a labelled block quote. The five shared types `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION` (GitHub's set, introduced in 2023, all of which Obsidian also accepts) **should** be recognized; other types **may** be used and **should** be rendered as a generic callout when unknown, as Obsidian does by falling back to its note style. Container forms such as `:::note` **should** be converted to the block-quote form on export.
- *Math.* `$...$` and `$$...$$` with TeX syntax **may** be supported; engines **should** declare it. Degradation is to literal text, which remains readable to those who read TeX.
- *Diagrams.* Fenced code blocks with an info string (` ```mermaid `, ` ```plantuml `, ` ```graphviz `) **are recommended** for diagrams written as text; they degrade perfectly to a code block showing the source. Rendered images **should** carry alternative text.

#### MKUP-16 · Generic directives for declared extensions

When an engine's macros, queries, or widgets must appear in Markdown source, the generic directive syntax is **recommended**: a container form

```markdown
::: name key="value" other=1
Fallback or snapshot content shown by renderers that do not know *name*.
:::
```

and an inline form `:name[fallback text]{key="value"}`. Both come from the long-running CommonMark community proposal and have multiple implementations. Renderers that do not recognize the directive **should** render the fallback content. The HTML-comment envelope in [Chapter 12](12-Extensibility_Macros_and_Dynamic_Content.md) is the alternative when invisibility in unknown renderers is preferable. Engines **should** declare every directive name they emit in the manifest.

### Everything else

#### MKUP-17 · Raw HTML

Inline and block HTML is part of CommonMark and **may** appear in the profile. Exporters **should** minimize it, preferring Markdown constructs, because HTML is what importers sanitize most aggressively ([SEC-1](14-Security_Privacy_and_Trust.md)). Where native markup has no Markdown equivalent (complex tables with spans, definition lists, underlines), a small HTML subset is acceptable and **should** be listed in the manifest.

#### MKUP-18 · Native syntaxes: provide a path, not a replacement

Engines whose native markup is not Markdown **should**: (a) publish a grammar, a reference parser, or a canonical HTML rendering that others can parse (MediaWiki's Parsoid HTML is an example of the third); (b) provide an exporter to the portable profile that declares its fidelity ([XFER-2](10-Interchange_and_Portability.md)); and (c) ideally an importer from it. Pandoc already reads or writes several wiki markups and is a reasonable bridge; engines are **encouraged** to contribute readers and writers for their syntax to shared converters rather than maintaining private ones.

#### MKUP-19 · Text conventions

UTF-8 without a byte-order mark, `LF` line endings, a trailing newline, and Unicode NFC normalization of titles and link targets are **recommended** for exported files. Tabs **should** be avoided in Markdown except inside code.

#### MKUP-20 · Publish a test corpus

Engines **should** publish sample pages exercising every construct they emit, in native form and in the portable profile, so that converter authors can test against reality. A shared cross-engine corpus is a goal of this project ([17 · Roadmap](17-Roadmap_and_Open_Questions.md)).

## 4. The degradation ladder

Graceful degradation is the profile's organizing idea. The table shows what each Layer 2 construct becomes in a renderer that knows only Layer 0 or 1. If the degraded form is still understandable, the construct is portable.

| Construct | In a plain CommonMark/GFM renderer | Readable? |
|---|---|---|
| `[[Title]]` | Literal text `[[Title]]` | Yes: the target is visible. |
| `[[Title\|Label]]` | Literal text | Yes. Converters **may** rewrite to `[Label](Title.md)` for static sites. |
| `[[Title#Heading]]` | Literal text | Yes. |
| `^block-id` | A short token at the end of a paragraph | Yes, slightly noisy. |
| `![[Page]]` | Literal text | Yes, as a visible reference; content not shown. Exporters **should** snapshot when the target is not in the bundle. |
| `#tag` inline | Literal text | Yes. |
| `> [!NOTE]` | Block quote beginning with `[!NOTE]` | Yes. |
| `$x^2$` | Literal TeX | Yes, for those who read TeX. |
| ` ```mermaid ` | Code block showing the diagram source | Yes. |
| `::: name` directive | Fallback content as paragraphs, surrounded by `:::` lines | Yes. |
| `<!-- wiki:... -->` envelope | Hidden; enclosed snapshot shown | Yes, invisibly. |
| `[[prefix:Title]]` | Literal text | Yes; converters **should** expand using the map. |

## 5. Bridging the document and block paradigms

Markdown is linear text; many modern engines store trees of blocks. The profile bridges them with three conventions, none of which requires the other side to change its model:

1. **Outliner pages are nested lists.** An outliner page exports as a Markdown document whose body is a nested bullet list, one bullet per block, preserving depth. Logseq already stores pages this way. Document engines render nested lists natively.
2. **Blocks keep their identity through `^id`.** Block identifiers travel as trailing tokens ([MKUP-9](#mkup-9--block-identifiers)); references and embeds use `#^id`. A document engine can ignore them and still show a correct page.
3. **Block properties stay with the block.** Properties on a block (`key:: value` in Logseq) **should** be exported either as the same `key:: value` line (which degrades to visible text) or inside an HTML-comment envelope immediately following the block ([Chapter 12](12-Extensibility_Macros_and_Dynamic_Content.md)). Page-level properties go to frontmatter ([Chapter 09](09-Metadata_and_Frontmatter.md)).

Line-based engines (Scrapbox / Cosense) fit the same bridge: each line is a block, indentation is depth, and bracket notation maps to Markdown emphasis and links ([Appendix B](appendices/B-Syntax_Crosswalk.md)).

Conversely, a document imported into a block engine **should** be split at paragraph and list-item boundaries into blocks, with any `^id` tokens becoming block identifiers and headings becoming heading blocks, so that the round trip back to Markdown reproduces the original structure.

## 6. What this chapter does not do

- It does not specify a grammar for the profile beyond the forms above; the CommonMark specification plus the listed extensions is the grammar, and a conformance corpus is future work.
- It does not standardize any engine's native syntax.
- It does not define how macros execute, only how they appear and degrade ([Chapter 12](12-Extensibility_Macros_and_Dynamic_Content.md)).

---

Previous: [07 · Collaboration, Awareness and Governance](07-Collaboration_Awareness_and_Governance.md) · Next: [09 · Metadata and Frontmatter](09-Metadata_and_Frontmatter.md)
