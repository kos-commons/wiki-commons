# 12 · Extensibility, Macros and Dynamic Content

> **Part III — Interoperability Guidelines** · **Status:** Working Draft 0.4 (October 2026)
> Previous: [11 · APIs and Discovery](11-APIs_and_Discovery.md) · Next: [13 · Accessibility, Internationalization and Web Standards](13-Accessibility_Internationalization_and_Web_Standards.md)

**In one sentence:** Macros, templates, queries, scripts, and plugins are where wikis get their power and where portability goes to die; these guidelines do not try to standardize what extensions *do*, only how they *announce themselves*, how they *degrade*, and how their output *travels*.

Recommendations in this chapter carry the prefix `EXT-`. The numbered recommendations are the guidance of this chapter ([00 §4](00-Overview_and_Vision.md#4-guidance-language)); the surrounding sections explain, give evidence, and add no obligations.

---

## 1. The problem, stated honestly

Every mature wiki engine has an escape hatch from plain markup: a way to insert a table of contents, list the subpages, pull in another page, run a query over structured data, render a chart, call a script. The source report counted this as one of the three hardest obstacles to any wiki standard, for two reasons that remain true:

- **The syntax is wildly different.** The classic engines alone use at least a dozen shapes for "call a macro": `{{Template|arg}}` and `{{#if:...}}` in MediaWiki, `~~NOCACHE~~` and `<plugin>` tags in DokuWiki, `<<Macro(args)>>` in MoinMoin (and Gollum, and TiddlyWiki), `[[Macro(args)]]` and `{{{#!processor}}}` in Trac, `[[!directive]]` in ikiwiki, `(:directive:)` in PmWiki, `%MACRO{...}%` in TWiki and Foswiki, `{{macro/}}` in XWiki, `{PLUGIN()}...{PLUGIN}` in Tiki, `[{INSERT ...}]` in JSPWiki, `#plugin()` and `&plugin(){...};` in PukiWiki. The same characters mean different things: `{{...}}` is a template in MediaWiki, an image in DokuWiki, MoinMoin, and Zim, a transclusion in TiddlyWiki, and a macro in XWiki and Redmine.
- **The semantics are bound to a runtime.** A MediaWiki template with Lua modules, an XWiki Velocity script, a Dataview query in Obsidian, a Notion database view, a Confluence Jira macro: each depends on a host language, a data model, and often a live service. Executing them elsewhere is impossible, and standardizing their execution would be a security problem as much as an engineering one.

The report's conclusion is adopted here: execution is out of scope ([00 §7.2](00-Overview_and_Vision.md#72-explicitly-out-of-scope)). What remains is a tractable and valuable problem: making sure that a page full of macros is still a readable, honest page when it arrives somewhere the macros do not run.

## 2. A taxonomy of extensions

Different kinds of extension need different treatment.

| Kind | Examples | What must travel |
|---|---|---|
| **Inline and block macros** | TOC, date, page count, recent changes list, children list, backlinks list | Their *output* at export time, plus the fact that it was generated. |
| **Templates and parameterized transclusion** | MediaWiki templates, Confluence excerpt include, Logseq templates | The *expanded* content, the parameter values, and the template page itself. |
| **Queries and dynamic lists** | Semantic MediaWiki `#ask`, Dataview, Obsidian Bases, Logseq queries, Notion database views, DokuWiki struct, Foswiki `%SEARCH%` | The result set at export time, the query source, and the schema of the data queried. |
| **External embeds** | Video players, maps, iframes, oEmbed cards, Jira issues | A link, a title, and ideally a static preview. |
| **Scripts** | Lua (Scribunto), Velocity and Groovy (XWiki), JavaScript widgets, TiddlyWiki widgets, Silverbullet Lua | The source as a code block and the output as a snapshot. Never execution. |
| **Structured data** | XWiki classes, Semantic MediaWiki properties, Foswiki DataForms, Tiki trackers, Notion properties | Values in `properties`, schemas in the bundle ([XFER-11](10-Interchange_and_Portability.md)). |
| **Editor plugins** | Toolbars, autocompletion, slash commands, paste handlers | Nothing, unless they introduce syntax, in which case they are syntax extensions. |
| **Themes and skins** | Visual appearance, layout | Nothing. Content never depends on them. |
| **Backends and integrations** | Storage, authentication, search, webhooks | Nothing in content; declared in documentation and APIs ([Chapter 11](11-APIs_and_Discovery.md)). |

## 3. Recommendations

### Announcing

#### EXT-1 · Declare every extension

Each extension (plugin, macro package, template library) **should** ship a small manifest, and engines **should** be able to list the extensions active on a wiki:

```yaml
name: examplewiki-struct
version: "2.1.0"
license: GPL-2.0-or-later
homepage: https://example.org/plugins/struct
kind: [syntax, structured-data, query]
syntax:
  directives: [query, schema]        # names introduced, in the generic directive form
  native: ["{{query ...}}"]          # native forms, for documentation
fallback: snapshot                    # snapshot | hide | text | none
permissions: [read-pages, read-structured]
```

Bundles list active extensions under `extensions_used` ([XFER-1](10-Interchange_and_Portability.md)) so that importers know which directive names to expect.

#### EXT-2 · Never repurpose core constructs

Extensions **should not** change the meaning of CommonMark or Layer 1 constructs (headings, emphasis, links, code fences, block quotes, tables). New meaning **should** come through new syntax: the generic directive form ([MKUP-16](08-Markup_and_Syntax.md)), a fenced code block with a distinctive info string, the `> [!TYPE]` callout form, or the engine's native macro syntax. Fenced code with an info string is the safest home for anything written as text (diagrams, queries, scripts), because it degrades to a visible code block everywhere.

#### EXT-3 · Every extension has a fallback, in source and in output

- In **source**, a construct **should** be readable by a person who does not know the extension: the directive form's fallback body, a code block's content, a template call's name and parameters.
- In **rendered output**, an unknown or disabled extension **should** render as something visible (its fallback body, or a labelled placeholder "unknown macro: name") rather than nothing. Silence is the worst failure mode because nobody notices the loss.

### Travelling

#### EXT-4 · Snapshot envelopes

On export, dynamic output **should** be materialized into static content in the portable profile and wrapped in an HTML-comment envelope that records where it came from:

```markdown
<!-- wiki:snapshot kind="macro" name="children" engine="examplewiki" src="{{children depth=1}}" at="2026-10-04T02:00:00Z" -->
- [[Guides/Getting Started]]
- [[Guides/Advanced Topics]]
<!-- /wiki:snapshot -->
```

Envelope attributes:

| Attribute | Meaning |
|---|---|
| `kind` | `macro`, `template`, `query`, `embed`, `script`, `transclusion`, `unknown`. |
| `name` | The macro, template, or directive name. |
| `engine` | The engine or extension that produced the snapshot. |
| `src` | The original source text, with `"` escaped as `&quot;` and `-->` never appearing (escape `>` as `&gt;` if needed). |
| `params` | Optional JSON object of resolved parameters. |
| `at` | RFC 3339 time of the snapshot. |
| `target` | For transclusion: the source page and revision. |
| `id` | Optional stable identifier for the construct within the page. |

The body between the markers is ordinary Markdown: the rendered result converted to the profile. The markers are invisible in every Markdown renderer, so a reader of the exported page sees the content as it looked. An importer that recognizes `engine` and `name` **may** replace the snapshot with a live construct; one that does not **should** keep the body, and **may** keep the envelope so that a later export can round-trip. Envelopes **may** nest. Inline macros use the same markers inline: `<!-- wiki:snapshot kind="macro" name="pagecount" -->1,248<!-- /wiki:snapshot -->`.

Snapshots **should** be marked as generated in the importing engine's editor if it keeps the envelope, so that nobody hand-edits content that will be regenerated.

#### EXT-5 · Block property envelopes

Metadata attached to a block (as opposed to a page) **should** travel either as a visible `key:: value` line following the block, or as an envelope immediately after it:

```markdown
The resolution screen shows both versions side by side. ^conflict-ui
<!-- wiki:props {"status": "needs-screenshot", "owner": "aiko"} -->
```

The visible form is preferred when the properties are meaningful to readers; the envelope when they are machinery.

#### EXT-6 · Templates: export the expansion and the template

Parameterized templates **should** be expanded in place on export, wrapped in a `kind="template"` envelope with `name` and `params`, and the template pages themselves **should** be exported with `kind: template`. Importers with a compatible template system **may** reconstruct the call from `name` and `params`; others keep the expansion. Unexpanded template syntax **should not** be exported bare, since it degrades to meaningless braces.

#### EXT-7 · Queries: snapshot the result, keep the question

Query results **should** be exported as static tables or lists in a `kind="query"` envelope whose `src` holds the query and whose `params` **may** hold the query language (`lang: "dataview"`, `"smw-ask"`, `"sql"`). The data queried **should** itself be in the bundle ([XFER-11](10-Interchange_and_Portability.md)) so that an importer with a query capability can re-run an equivalent. Engines are **encouraged** to make query results visually distinct from hand-written content in their own interface too; it is the same honesty.

#### EXT-8 · External embeds: a link first

Embedded external content **should** export as a link with a title, in a `kind="embed"` envelope, optionally with a static preview image included in `attachments/`. Engines **should not** auto-load third-party content on import without the operator's consent ([PRIV-4](14-Security_Privacy_and_Trust.md)). Where the provider supports oEmbed, the oEmbed response **may** be recorded in `params` to help re-embedding.

#### EXT-9 · Scripts: source as code, output as snapshot

Script bodies **should** export as fenced code blocks with the language as info string, and their rendered output as a `kind="script"` snapshot. Importers **should never** execute imported scripts automatically. Engines that run scripts **should** sandbox them, document the sandbox, and declare required permissions ([SEC-6](14-Security_Privacy_and_Trust.md)).

### Interoperating

#### EXT-10 · A small common directive vocabulary

Many macros do the same thing under different names. Engines and converters are **encouraged** to recognize the following directive names in the generic form as a shared vocabulary, mapping their native equivalents to and from them on import and export. Each has an obvious degradation.

| Directive | Meaning | Native equivalents (examples) | Degrades to |
|---|---|---|---|
| `::: toc` | Table of contents of the current page | `__TOC__`, `~~TOC~~`, `(:toc:)`, `%TOC%`, `[[!toc]]`, `{{toc}}`, `{{toc/}}`, `#contents`, `<<TableOfContents>>`, `[[_TOC_]]` | Omitted, or a snapshot list of headings |
| `::: children` | List of subpages or child pages | `{{Special:PrefixIndex}}`, `{{child_pages}}`, `[[!map]]`, `%SEARCH{...}%`, `#ls` | Snapshot list of links |
| `::: backlinks` | Pages linking here | Special:WhatLinksHere, backlink actions, `<<Backlinks>>` | Snapshot list of links |
| `::: recent-changes` | Recent changes, optionally scoped | `<<RecentChanges>>`, `#recent`, `[[RecentChanges()]]` | Snapshot list |
| `::: tag-list` | Pages carrying a tag | Category pages, `{{tag>name}}`, `#related` | Snapshot list |
| `::: include` | Transclude a page or section (unparameterized) | `{{:Page}}`, `(:include:)`, `%INCLUDE{}%`, `{{include}}`, `<<Include()>>`, `![[Page]]` | `![[Page]]` or a snapshot |
| `::: query` | A query over structured data | `{{#ask:}}`, Dataview, Bases, `{{query}}`, `%SEARCH%` | Snapshot table |
| `::: embed` | External content | `{{youtube>id}}`, `{{iframe}}`, oEmbed URLs | A link |
| `::: math` | Display mathematics (when `$$` is unavailable) | `<math>`, `$$` | Literal TeX |

Attributes are written as `key=value` pairs (`::: children depth=2 sort=title`). A registry of directive names with their meanings and attributes is proposed as future work ([17 · Roadmap](17-Roadmap_and_Open_Questions.md)).

#### EXT-11 · Themes stay out of the content

Themes and skins **should** rely on the semantic hooks of [MKUP-12](08-Markup_and_Syntax.md) (semantic elements, `wikilink` classes, heading identifiers) rather than requiring markup changes; **should** respect `prefers-color-scheme` and `prefers-reduced-motion`; **should** keep print styles; and **should not** reduce accessibility below the engine's baseline ([Chapter 13](13-Accessibility_Internationalization_and_Web_Standards.md)).

#### EXT-12 · Plugin APIs: documented, versioned, hookable

Engines are **encouraged** to expose stable, documented, semantically versioned extension points: parser extension (register a directive or syntax), link resolution (custom targets, interwiki handlers), rendering (post-process HTML), storage events (page saved, renamed, deleted; useful for webhooks and search indexing), authentication providers, and export hooks (so that extensions can write their own snapshot envelopes). A plugin that can participate in export is a plugin whose content survives.

#### EXT-13 · Least privilege for extensions

Extensions **should** declare the permissions they need (read pages, write pages, network access, user data) and engines **should** show operators that list before enabling. Content produced by extensions **should** pass through the same sanitization as user content ([SEC-1](14-Security_Privacy_and_Trust.md)). Extension marketplaces and directories are **encouraged** to show license, maintenance status, and permission requirements prominently.

## 4. Worked example: a page before and after export

Native source in an imaginary engine:

```
{{children depth=1}}

== Status ==
{{query lang=struct}} SELECT title, status FROM decisions WHERE status = "open" {{/query}}

{{Template:Warning|text=This page is being restructured.}}
```

Exported in the portable profile:

```markdown
<!-- wiki:snapshot kind="macro" name="children" engine="examplewiki" src="{{children depth=1}}" at="2026-10-04T02:00:00Z" -->
- [[Decisions/ADR-001 Use Markdown]]
- [[Decisions/ADR-002 Bundle Layout]]
<!-- /wiki:snapshot -->

## Status

<!-- wiki:snapshot kind="query" name="query" engine="examplewiki-struct" params='{"lang":"struct"}' src="SELECT title, status FROM decisions WHERE status = &quot;open&quot;" at="2026-10-04T02:00:00Z" -->
| Title | Status |
|---|---|
| [[Decisions/ADR-002 Bundle Layout]] | open |
<!-- /wiki:snapshot -->

<!-- wiki:snapshot kind="template" name="Warning" engine="examplewiki" params='{"text":"This page is being restructured."}' -->
> [!WARNING]
> This page is being restructured.
<!-- /wiki:snapshot -->
```

A reader of the exported file sees a list, a table, and a warning. An importer that knows the engine can rebuild all three dynamically. An importer that knows none of it loses nothing visible. That is the whole design.

## 5. Observed in

The envelope idea is not new; several engines already use HTML comments to carry machinery invisibly through Markdown. SilverBullet's "baked sections" freeze the output of a Lua expression into the page between `<!--#lua ... -->` and `<!--/lua-->` markers, so that the rendered result is plain Markdown while the source expression survives. Nuclino's API represents engine-specific metadata and inline comments as HTML comments inside otherwise standard CommonMark. MediaWiki's Parsoid HTML records the original template call for every expanded template as RDFa so that the visual editor can round-trip it. SiYuan lets the exporter choose how block references degrade (anchor text or footnotes) and keeps a lossless JSON form beside the Markdown. Obsidian's Bases keep a query as a small YAML file rather than in page text, which is another way of keeping the question separate from the answer. On the macro-syntax side, the classic engines' dozen shapes listed in §1 are all still in production use, which is the strongest argument for standardizing the envelope rather than the macro.

---

Previous: [11 · APIs and Discovery](11-APIs_and_Discovery.md) · Next: [13 · Accessibility, Internationalization and Web Standards](13-Accessibility_Internationalization_and_Web_Standards.md)
