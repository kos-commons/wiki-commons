# Appendix A · Wiki Engine Landscape

> **Appendices** · **Status:** Working Draft 0.1 (October 2026) · Facts checked against primary sources in early October 2026; items marked *(unverified)* could not be confirmed against a primary source and are offered with that caveat.
> Index: [README](../../README.md) · Next: [B · Syntax Crosswalk](B-Syntax_Crosswalk.md)

**In one sentence:** A survey of fifty-odd wiki engines and wiki-like knowledge tools across three generations, written to show what they share, where they diverge, and which ideas each contributed, so that no single engine is mistaken for "the wiki".

This appendix is descriptive. Inclusion is not endorsement; omission is not judgement. Corrections and additions from maintainers are the most welcome kind of contribution ([CONTRIBUTING](../../CONTRIBUTING.md)).

---

## 1. How to read this appendix

Each engine gets a compact profile: origin and status, license, implementation and storage, content model, markup and link syntax (with the order of target and label in a labelled link), history, collaboration, API, export, and what is distinctive about it. Section 5 condenses the profiles into a matrix; Section 6 draws cross-cutting observations.

Abbreviations: *T|L* = labelled links are written target first (`[[Target|Label]]`); *L|T* = label first (`[[Label|Target]]`); *RT* = real-time co-editing.

## 2. Classic engines

### 2.1 WikiWikiWeb and UseModWiki (historical)

- **WikiWikiWeb** (Ward Cunningham, launched 25 March 1995, Perl). The first wiki, created to host the Portland Pattern Repository. CamelCase WikiWords as links; a trailing `?` for pages not yet written; RecentChanges as the social hub; "edit this page" on every page. Made read-only in 2015. Its design principles are quoted in [02 · Guiding Principles](../02-Guiding_Principles.md#8-relationship-to-cunninghams-original-design-principles).
- **UseModWiki** (Clifford Adams, 1999, Perl, GPL). Flat-file. Introduced and named **free links** (`[[Free Link]]`) in 2001 so that page names need not be CamelCase. Ran the English Wikipedia from January 2001 to January 2002, which is how `[[...]]`, RecentChanges, interwiki prefixes, and the question-mark-turned-red-link lineage entered MediaWiki. Still receives occasional releases *(latest release date unverified)*.

### 2.2 MediaWiki

- **Origin/status:** Wikimedia Foundation; live on Wikipedia since 2002. Active. Stable 1.46 (June 2026); LTS 1.43 (December 2024, supported to December 2027); 1.47 LTS planned for November 2026. **License:** GPL-2.0-or-later. **Stack:** PHP; MariaDB/MySQL (PostgreSQL, SQLite supported).
- **Model:** linear wikitext document with sections. **Markup:** Wikitext; Parsoid converts between wikitext and a specified HTML/RDFa form (MediaWiki DOM spec 2.8) and is planned to become the default parser; VisualEditor for WYSIWYG. **Links:** `[[Page]]`, `[[Page|label]]` (**T|L**), namespaces `Help:Page`, optional subpages `Parent/Child`, sections `[[Page#Section]]`, interwiki `[[wikipedia:Page]]`, interlanguage `[[fr:Page]]`; missing pages render as **red links**. **Transclusion/macros:** templates `{{Name|param}}`, page transclusion `{{:Page}}`, parser functions `{{#if:...}}`, Lua via Scribunto, tag extensions `<ref>`.
- **Metadata:** categories (`[[Category:X]]`), page properties, structured data via extensions (Semantic MediaWiki, Cargo, Wikibase). **History:** full text of every revision; diff; undo and rollback; summaries; minor flag; patrolling; revision deletion and suppression; move with redirect. **Collaboration:** talk namespaces with modern discussion tools; Recent changes with rich filters and Atom/RSS; watchlists; notifications; no core RT.
- **API:** Action API (`api.php`) and REST API (`rest.php/v1`) with a served OpenAPI description; OAuth via extension. **Export:** XML dumps (`export-0.11` schema) with full history; Pandoc reads and writes `mediawiki`. **Distinctive:** the de facto reference for free links, namespaces, templates, red links, watchlists, and the XML dump; the largest deployment of soft security in existence; temporary accounts replacing public IPs (English Wikipedia, November 2025).

### 2.3 DokuWiki

- **Origin/status:** Andreas Gohr, 2004. Active; releases "Kaos" (February 2024), "Librarian" (May 2025), "Mort" (July 2026). **License:** GPL-2.0. **Stack:** PHP; **flat files**, no database.
- **Model:** linear document. **Markup:** DokuWiki syntax; Markdown via plugins. **Links:** `[[page]]`, `[[page|text]]` (**T|L**), namespaces with `:` mapped to directories, sections `[[page#section]]`, interwiki `[[wp>Page]]`; page names are lower-cased; missing pages styled distinctly (red). **Embeds/macros:** `{{image.png?200}}`, footnotes `((text))`, `~~NOCACHE~~`, `<code>`, plugin tags.
- **History:** attic of old revisions with changelog; diff (side-by-side and inline); revert; summaries; minor flag; visible timed page locks. **Collaboration:** Recent changes with feed; page and namespace subscriptions with digests; discussion via plugin. **API:** XML-RPC and, since 2024, **JSON-RPC with a generated OpenAPI 3.1 document** and token authentication; its XML-RPC API still implements the early WikiRPCInterface methods. **Export:** raw and XHTML exports per page; PDF/ODT via plugins; Pandoc reads and writes `dokuwiki`. **Distinctive:** the reference flat-file wiki; a configurable license selector that places the license in footer and HTML head; namespace syntax inherited by Zim.

### 2.4 MoinMoin

- **Origin/status:** Jürgen Hermann, 2000, Python. 1.9 line (Python 2) dormant since 1.9.11 (2020); **moin2** in beta (2.0.0b5, March 2026). **License:** GPL-2.0-or-later. **Stack:** Python; file store or SQLAlchemy backends in moin2.
- **Markup:** MoinWiki; moin2 renders MoinWiki, Creole, reStructuredText, DocBook, MediaWiki, and Markdown. **Links:** CamelCase or `[[Page]]`, `[[Page|label]]` (**T|L**), subpages `/`, interwiki `MeatBall:Page`, attachments `[[attachment:file]]`. **Macros:** `<<MacroName(args)>>`; parsers `{{{#!highlight python ...}}}`; includes `<<Include(Page)>>`. **History:** revisions, diff, revert, comment, "trivial change" flag. **Collaboration:** RecentChanges, subscriptions; clicking the page title lists backlinks, as on the first wiki. **API:** XML-RPC (1.9). **Export:** moin2 serialization; no Pandoc support. **Distinctive:** `<<Macro>>` and `{{{#!parser}}}` forms influenced Trac; multi-markup items in moin2; a cautionary tale about long rewrites.

### 2.5 PmWiki

- **Origin/status:** Patrick Michaud, 2002; maintained by Petko Yotov. Active (2.7.6, September 2026). **License:** GPL-2.0-or-later. **Stack:** PHP; flat files holding text, metadata, and history in one file per page.
- **Links:** `[[page]]`, `[[Page|label]]` (**T|L**) **and** `[[label -> Page]]` (the only mainstream engine offering both orders); groups `Group/Page` or `Group.Page`; anchors `[[Page#name]]`; InterMap `Wikipedia:Page`; missing pages displayed specially "to invite others to create the page". **Directives:** `(:toc:)`, `(:include Page:)`, `(:if ...:)`, `(:title Text:)`. **History:** per-page diffs, restore, summary, minor flag. **Collaboration:** RecentChanges per group and site-wide; email notification. **API:** none official. **Export:** `?action=source`; no Pandoc. **Distinctive:** two-level group hierarchy; the `(:directive:)` shape; both label orders.

### 2.6 TWiki and Foswiki

- **TWiki** (Peter Thoeny, 1998, Perl, GPL-2.0-or-later): dormant; last release 6.1.0 (2018). **Foswiki** (community fork, 2008, Perl, GPL): maintained; 2.1.11 (March 2026). Flat-file topics in "webs" with RCS or plain-file history.
- **Markup:** TML (Topic Markup Language); TinyMCE-based WYSIWYG. **Links:** WikiWords; `[[Target][Label]]` (**T|L** with a `][` delimiter); other web `Web.Topic`; missing topics show a red question-mark link. **Macros:** `%MACRO{param="value"}%`, `%INCLUDE{}%`, `%SEARCH{}%`, `%TOC%`; macros expand before formatting. **Metadata:** **DataForms**: typed name–value fields per topic defined by a form, stored as `%META:` lines. **History:** full revisions, rdiff, restore, quiet save. **Collaboration:** WebChanges, WebNotify subscriptions. **API:** REST handlers for plugins. **Export:** raw, static publishing; Pandoc reads `twiki`. **Distinctive:** the "structured wiki" and wiki-application idea that XWiki and Tiki developed further.

### 2.7 XWiki

- **Origin/status:** Ludovic Dubost / XWiki SAS, 2004, Java. Active: LTS 17.10.x, stable 18.8 (September 2026). **License:** LGPL-2.1. **Stack:** Java; Hibernate over an RDBMS.
- **Model:** document plus typed **objects** (XClass/XObject) attached to pages; nested pages; "applications" built from class, sheet, template, and live table. **Markup:** XWiki Syntax 2.1 (also renders Markdown, Confluence, MediaWiki, Creole); CKEditor WYSIWYG; **real-time WYSIWYG editing enabled by default since 16.9** (Netflux and ChainPad). **Links:** `[[Page]]`, `[[label>>Page]]` (**L|T** with `>>`), `[[Space.Page]]`, anchors by parameter, `interwiki:prefix:Page`, attachments `attach:`. **Macros:** `{{macro param="x"}}...{{/macro}}`, `{{toc/}}`, `{{include reference="..."/}}`, scripting `{{velocity}}`, `{{groovy}}`. **History:** major/minor versions, diff, rollback, comments, minor flag. **Collaboration:** comments and annotations, activity stream, watch, RT editing. **API:** REST over wikis, spaces, pages, objects, classes, with a downloadable **OpenAPI** description; scripting APIs. **Export:** XAR packages, HTML, PDF; Pandoc writes `xwiki`. **Distinctive:** the second-generation structured wiki; unique `>>` label syntax; RT editing in a classic engine.

### 2.8 Tiki Wiki CMS Groupware

- Community project since 2002; active with five-year LTS releases (Tiki 30 LTS, July 2026). LGPL-2.1. PHP and MySQL/MariaDB. Wiki plus trackers (user-defined database forms), forums, blogs, calendars. **Links:** `((page))`, `((page|label))` (**T|L**), external wikis `Prefix:Page`. **Plugins:** `{PLUGIN(params)}body{PLUGIN}`. History, diff, rollback, comments, minor flag; feeds and search. Pandoc reads `tikiwiki`. **Distinctive:** the all-in-one model and trackers as structured data in wiki text.

### 2.9 Apache JSPWiki

- Janne Jalkanen, early 2000s; Apache project. Active (2.12.5 and 3.0.0, August 2026). Apache-2.0. Java; file-based versioning providers. **Links:** single brackets `[Page]`, `[label|Page]` (**L|T**), interwiki `[Wikipedia:Page]`, footnotes `[1]`. **Plugins:** `[{INSERT plugin WHERE param=value}]`, `[{TableOfContents}]`, variables `[{$pagename}]`. History, diff, restore, change notes; RSS; Lucene search. Legacy XML-RPC. **Distinctive:** the origin of the WikiRPCInterface specification; the `[{...}]` plugin form.

### 2.10 Trac

- Edgewall Software, 2004, Python, BSD-3-Clause. Maintenance (1.6, September 2023). Wiki alongside tickets and changesets in one RDBMS environment. **Links:** CamelCase; TracLinks `wiki:Page` and `[wiki:Page label]`; Creole-style `[[Page]]` and `[[wiki:Page|label]]` (**T|L**); InterTrac and InterWiki prefixes; missing pages carry class `missing`. **Processors/macros:** `{{{#!python ...}}}`, `[[Macro(args)]]`, `[[TOC]]`. History, diff, revert; timeline across wiki and tickets; XML-RPC via plugin. **Distinctive:** popularized `{{{#!processor}}}` blocks; dual link syntaxes.

### 2.11 ikiwiki

- Joey Hess, 2006, Perl, GPL-2.0-or-later. Active (3.20260201). A **wiki compiler**: pages live in git (or another VCS) and compile to static HTML, with a CGI for editing. Markdown default, other markups via plugins. **Links:** `[[Page]]`, `[[label|Page]]` (**L|T**), subpages with `/`, anchors `[[Page#foo]]`. **Directives:** `[[!directive param="value"]]` (`[[!meta title="..."]]`, `[[!inline pages="blog/*"]]`, `[[!tag x]]`), deliberately distinguished from links by `!`. History is git history; commit messages are summaries; RecentChanges is generated; comments plugin. **Distinctive:** the origin of the git-backed static wiki pattern.

### 2.12 Gollum and the forge wikis

- **Gollum** (GitHub, around 2010; now community-maintained; 6.1.0, December 2024; MIT; Ruby). Pages are files in a **git repository**; format by extension (Markdown, RDoc, AsciiDoc, Creole, MediaWiki, Org, reST, Textile). **Links:** `[[Page]]`, `[[link text|Page]]` (**L|T**), spaces become `-` in file names; macros `<<Macro()>>`; `[[_TOC_]]`. History is git; no API beyond the library.
- **GitHub wiki**: a `.wiki.git` repository per project. GitHub's own documentation describes the labelled form as `[[Page|Link Text]]` while Gollum's and GitLab's documentation describe `[[Link Text|Page]]`; implementations differ, and **Gitea's** renderer resolves the ambiguity with a heuristic (its source comment: "MediaWiki uses [[link|text]], while GitHub uses [[text|link]]"). **GitLab wiki**: a git repository per project or group; `[[Page]]` and `[[label|slug]]` (**L|T**); page history; REST API. **Gitea / Forgejo wiki**: `.wiki.git`; short links `[[Name]]`, `[[Name|Text]]`. **Azure DevOps wiki**: a git repository with a `.order` file per folder, an `.attachments` folder, standard Markdown links, and `[[_TOC_]]`. **Bitbucket wiki**: a git repository; Creole by default (`[[target|label]]`, **T|L**), also Markdown, reST, Textile.
- **Distinctive:** the forge wikis made "a wiki is a git repository of Markdown files" ordinary, and preserved the label-order split in the process.

### 2.13 Gitit

- John MacFarlane (author of Pandoc), 2008, Haskell, GPL-2.0. Maintained (0.16.0.2, September 2026). Backed by git, darcs, or mercurial. Pandoc Markdown by default; also reST, LaTeX, HTML, DocBook, Org per page. **Links:** Markdown links with an empty URL, `[Front Page]()`, so no wiki-specific syntax; categories in a metadata block. History from the VCS; Atom feeds; export to anything Pandoc writes. **Distinctive:** the first wiki built directly on Pandoc; demonstrates format pluralism through a converter.

### 2.14 PukiWiki, YukiWiki, FreeStyleWiki, Hiki (Japan)

- **YukiWiki** (Hiroshi Yuki, Perl, early 2000s; distribution ended 2018). Introduced the `[[BracketName]]` convention for Japanese text, in which CamelCase cannot express links; also supported WikiNames.
- **PukiWiki** (PHP port of YukiWiki, 2001; PukiWiki Development Team; 1.5.4, March 2022; GPL-2.0-or-later). Flat files. **Markup:** headings `*`, lists `-`/`+`, definitions `: term | desc`. **Links:** `[[ページ名]]`, alias `[[エイリアス>ページ名]]` (**L|T** with `>`), InterWiki `[[InterWikiName:Page]]`; missing pages get a trailing `?`. **Plugins:** block `#contents`, `#ref(image.png)`, `#comment`, `#pcomment`; inline `&ref(file);`, `&size(20){text};`. **History:** time-windowed backups with diff; no edit summaries; a "do not update timestamp" option plays the minor-edit role. **Collaboration:** RecentChanges maintained as an actual page; in-page comment forms; RSS. **Distinctive:** the most influential Japanese wiki; related pages listed in the footer; comment forms inside pages.
- **FreeStyleWiki** (Perl; 3.6.5, 2018; GPL) and **Hiki** (Ruby; 1.0.0, 2013; GPL; links `[[Page]]`, `[[label|URL]]` **L|T**) are dormant but formative in the Japanese community.

### 2.15 TiddlyWiki

- Jeremy Ruston, 2004; TiddlyWiki 5 since 2013; 5.4.1 (July 2026). BSD-3-Clause. JavaScript. **A single self-contained HTML file** that saves itself, or a Node.js server storing one `.tid` file per tiddler.
- **Model:** many small titled units ("tiddlers"), a non-linear notebook; tags are tiddlers and drive structure; `$:/` system tiddlers hold configuration and interface. **Markup:** TiddlyWiki WikiText; Markdown via plugin. **Links:** `[[Tiddler Title]]`, `[[Displayed Title|Tiddler Title]]` (**L|T**); no namespaces; missing tiddlers are styled distinctly and created on click. **Transclusion:** `{{Tiddler}}`, with templates `{{Tiddler||Template}}`, fields `{{Tiddler!!field}}`; macros `<<name param>>`; widgets `<$list filter="...">`; **filters** `[tag[Example]sort[title]]` as the query language. **Metadata:** fields (`title`, `tags`, `created`, `modified`, `type`, custom). **History:** none in single-file form (`modified`/`modifier` fields only); external versioning in Node mode. **Export:** `.tid` files (name:value header lines, blank line, text), JSON tiddler arrays, static HTML, CSV. **Distinctive:** single-file portability; "Missing" and "Orphans" views built in; the documentation site is itself a TiddlyWiki.

### 2.16 Federated Wiki

- Ward Cunningham, 2011 (Smallest Federated Wiki, founded at an IndieWebCamp); Node.js server published as `wiki` on npm (0.41.0, September 2026). MIT. Pages are **JSON files**: `{title, story, journal}`, where `story` is an array of typed items (paragraph, image, html, code, data, chart; each item type is a plugin) and `journal` is the history of actions (`create`, `add`, `edit`, `move`, `remove`, `fork`).
- **Links:** `[[Page Title]]` resolved by slug across the **neighbourhood** of sites you have visited, forked from, or referenced; `[http://url label]` external. **Collaboration:** no accounts beyond the site owner; **forking** a page from another site is the collaboration primitive, and the journal records provenance; the "lineup" lays visited pages out horizontally; Recent Changes is built from the sites' `sitemap.json`. **API:** `GET /<slug>.json`, `/system/sitemap.json`, owner `PUT` actions. **Distinctive:** history inside the page; plural versions by design ("a chorus of voices"); block-based and federated years before either became fashionable.

### 2.17 Zim and Redmine (brief)

- **Zim** desktop wiki (Jaap Karssenberg; 0.77.2, July 2026; GPL-2.0-or-later; Python/GTK). Plain text files in a folder tree; syntax "inspired by DokuWiki"; `[[page]]`, `[[page|label]]` (**T|L**), `:` hierarchy, `+sub` subpages; version control through a plugin; Pandoc writes `zimwiki`.
- **Redmine** wiki (Jean-Philippe Lang; 7.0.2, October 2026; GPL-2.0; Ruby on Rails). Textile or CommonMark Markdown; `[[Page]]`, `[[Page|label]]` (**T|L**), anchors `[[Page#anchor]]`, cross-project `[[project:Page]]`; macros `{{toc}}`, `{{include(Page)}}`, `{{child_pages}}`; versions, diff, annotate, rollback; REST API for wiki pages.

## 3. Transitional wikis and knowledge bases

### 3.1 Wiki.js

- Nicolas Giard, 2016. AGPL-3.0. Node.js; PostgreSQL (others supported in 2.x). 2.x in maintenance (2.5.315, September 2026); **3.0 in beta since 2021–2022** with no release date. Linear document per locale and path; editors: Markdown, visual (WYSIWYG), raw HTML, AsciiDoc, with a conversion action whose losses are documented (draw.io diagrams become images, tab sets collapse to headings). Path-based links; tags; page history with restore; comments; **GraphQL** API with scoped tokens; git storage module for bidirectional file sync. **Distinctive:** the 2017–2020 "wiki as an application" generation; honest documentation of lossy conversion; a long major rewrite.

### 3.2 BookStack

- Dan Brown, 2015. MIT. PHP/Laravel; MySQL/MariaDB. Active (26.09, September 2026); moved from GitHub to Codeberg in 2026. Fixed hierarchy **Shelves → Books → Chapters → Pages** (a book can sit on several shelves). WYSIWYG (a new Lexical-based editor replacing TinyMCE) and a CommonMark-based Markdown editor with callouts; pages keep their original Markdown when written that way. Tags as name–value pairs; page templates; revisions with changelog messages, restore, audit log, recycle bin; comments; REST API self-documented at `/api/docs` with tokens. **Export:** contained HTML, PDF, plain text, Markdown, and a documented, re-importable **Portable ZIP**. **Distinctive:** the book metaphor; a documented portable archive.

### 3.3 Outline

- 2017; Business Source License 1.1 converting each release to Apache-2.0 after four years. Node/TypeScript; PostgreSQL and Redis; **ProseMirror** editor with **Yjs** and Hocuspocus for RT editing. Collections of nested documents; mentions of users, documents, and dates; comments and threads; revision history with restore; RPC-style JSON API with an **OpenAPI** description, API keys, and OAuth 2.0; webhooks. **Import:** Markdown, JSON, Confluence, Notion, Slab. **Export:** JSON, Markdown ZIP, HTML ZIP, and since September 2026 the **Open Knowledge Format**, a Markdown bundle with per-document YAML frontmatter and a root index. **Distinctive:** a polished open-components answer to Notion; OKF as a sibling of the Portable Wiki Bundle.

### 3.4 Docmost

- 2024. AGPL-3.0 core with enterprise modules under a separate license. NestJS and PostgreSQL; React; **Tiptap** editor with **Yjs** and Hocuspocus. Workspaces → spaces → nested pages; slash commands and Markdown shortcuts; callouts, math, Mermaid, draw.io; page history with comparison; inline comments and mentions; public sharing; an MCP server with OAuth. Import from Markdown, HTML, Notion, Confluence; export Markdown and HTML. **Distinctive:** the fastest-growing open-source Confluence alternative of the mid-2020s.

### 3.5 GROWI and Crowi (Japan)

- **GROWI** (WESEEK / GROWI, Inc., 2017 as a fork of Crowi; MIT; Node.js and MongoDB; 8.0.4, September 2026). **Hierarchical page paths `/parent/child`** are the page's identity; Markdown with YAML frontmatter; **built-in simultaneous editing on Yjs since v7** (replacing an earlier HackMD integration); server-side drafts; three-way conflict resolution. **WIP pages**: new pages left untouched become WIP automatically, are excluded from search, and expire unless published. **Links:** Markdown links plus PukiWiki-style `[[/Sandbox]]` and `[[Label>./Page]]` (**L|T** with `>`). **Macros:** `$lsx(/path, depth=1:3)` page lists, `$ref()`/`$refs()` attachment lists, draw.io, Mermaid, PlantUML, slides. Tags, bookmarks, templates per hierarchy; revisions with diff; threaded and inline comments; notifications; REST API v3. **Export:** an archive of database collections importable only into the same version; importers for esa.io and Qiita Team. **Crowi** (Sotaro Karasawa, 2013; MIT) is being rebuilt as "Reignite" (v2 alpha, 2026) with Yjs-based RT editing.

### 3.6 Otter Wiki, Silverbullet, Trilium, and the code-editor wikis

- **An Otter Wiki** (MIT; Python/Flask; 2.25.0, October 2026): Markdown files in a **git repository**; full git history and diffs; `{{include|src=/Page|section=...}}` transclusion with cycle protection; `{{DataTable}}`, `{{PageIndex}}`, `{{InfoBox}}`; `[[Page]]` links.
- **Silverbullet** (Zef Hemel; MIT; 2.11.1, September 2026): a "space" is a folder of Markdown pages; TypeScript client with a Rust backend after rewrites from Deno and Go; **Space Lua** scripting with inline `${expr}` and **SLIQ** queries over indexed frontmatter and tags; **"baked sections"** freeze Lua output into `<!--#lua ... --> ... <!--/lua-->` Markdown; links `[[page]]`, `[[page|alias]]` (**T|L**), `[[page#header]]`, `[[page@pos]]`; linked mentions. **Distinctive:** a working precedent for snapshot envelopes.
- **Trilium Notes** (zadam, 2017; now a community continuation; AGPL-3.0; 0.106.0, September 2026): a **tree with cloning** (one note under several parents); typed notes (text via CKEditor 5, code, canvas, mind map, relation map); inheritable attributes (labels and relations) driving templates and scripts; revisions; self-hosted sync; **ETAPI** REST interface with an OpenAPI description; export subtrees as HTML or Markdown ZIP.
- **Foam** (MIT; VS Code; 0.46.0, September 2026): `[[note]]`, block anchors `[[note#^id]]`, backlinks, templates. **Dendron** (Apache-2.0 since 2023, in maintenance mode since February 2023): **dot-delimited hierarchy** in file names (`project.area.topic.md`), stub notes, schemas, required frontmatter (`id`, `title`, `desc`, `updated`, `created`), note references `![[note#header]]`, block anchors `^id`, labelled links `[[Alias|note]]` (**L|T**). **Zettlr** (GPL-3.0; 4.8.0, September 2026): Zettelkasten identifiers, `[[links]]`, Pandoc export, GitHub-style admonitions since 4.8.

### 3.7 Confluence

- Atlassian, 2004; proprietary; Java. Cloud (ADF-native editor) and Data Center. **Storage format:** XHTML with `ac:` and `ri:` namespaces (`<ac:structured-macro ac:name="...">`, `<ac:link><ri:page ri:content-title="..."/></ac:link>`); the Cloud editor uses the **Atlassian Document Format**, a JSON node tree shared with Jira. Legacy wiki markup (`[alias|pagetitle]`, **L|T**) is accepted as input but not stored; wiki markup editing was removed in 2011. Spaces, page trees, folders, labels, templates and blueprints, databases, whiteboards; content states (draft, in progress, verified); optional page owner. Version history, comparison, restore; inline and page comments; watching; RT editing (Synchrony on Data Center). **REST API v2** with an OpenAPI description, cursor pagination, body formats including storage and ADF. **Export:** PDF, Word, CSV, HTML ZIP, XML ZIP (for Data Center import); HTML export omits comments. **Distinctive:** the enterprise wiki; `ac:structured-macro` as the macro container; a well-known portability regression.

### 3.8 Notion

- Notion Labs, 2016; proprietary SaaS. **Everything is a block with a UUID**; pages are blocks; databases with typed properties and views; synced blocks; templates. The public API exposes block objects (about thirty types, limited children per request); comments; mentions; RT editing with a proprietary engine; backlinks since 2020. **Export:** PDF, HTML (optionally with comments), Markdown and CSV (databases as CSV, pages as `.md`); block identifiers and synced-block identity are not represented in Markdown. **Distinctive:** made "the block" the public vocabulary; databases attached to pages; the clearest case of history retention tied to plans.

### 3.9 Scrapbox → Cosense (Japan)

- Nota Inc., now Helpfeel Inc.; launched 2016; **renamed Cosense on 21 May 2024**; proprietary SaaS (free for personal and educational use). The unit is a **project**; pages have **no hierarchy** by design ("recall that Wikipedia has no hierarchy"); tags are pages; editing is **line by line in real time** with per-line identifiers and per-line authorship.
- **Syntax:** `[Page]` single-bracket links; `#tag`; `[/project/page]` cross-project; `[* bold]`, `[/ italic]`, `[- strike]`; external `[URL title]` or `[title URL]` (either order); `[name.icon]`; `code:` and `table:` blocks; `[$ TeX]`. Links to empty pages are shown in a distinct colour, listed under the page, and still count for relations. **Related pages** under every page combine direct links and **two-hop links** (pages sharing a link or hashtag, and pages one hop beyond each link target). Page history snapshots. Internal JSON API; **export and import of project JSON** with per-line `id`, `text`, `userId`, `created`, `updated`; a 2026 agent-oriented command-line tool. **Distinctive:** hierarchy-free, link-only organization; two-hop relations; line-level attribution; the home page as the recency list.

### 3.10 esa.io, Kibela, Qiita Team, DocBase (Japan)

- **esa.io** (esa LLC, 2015): posts are **WIP by default** and "shipped" when ready, under the motto of nurturing information through *share → develop → organize*; categories are slash paths in the title (`日報/2026/10/04`); GFM Markdown; templates; revisions with messages; **three-way merge** on update when the client sends the revision it edited from; REST API with OAuth and personal tokens, backlinks endpoint; export of all posts as Markdown ZIP; import from Qiita Team.
- **Kibela** (Bit Journey, 2017): groups and folders; rich-text, CommonMark (with GFM extensions), and simultaneous-editing modes; has distinguished personal blog-style posts from shared wiki articles; **GraphQL** API; backup export; SCIM.
- **Qiita Team** (Qiita Inc., 2013): a feed of Markdown posts with templates, tags, comments, **edit requests**, and co-editing; positions itself against "wikis with a high posting barrier".
- **DocBase** (kray Inc.): everything is a casual **memo**; Markdown, rich-text, and hybrid editors; simultaneous editing; memos published to several groups; templates with variables; history with restore; export as Markdown and JSON; importers for esa, Qiita Team, and Kibela; MCP integration.

### 3.11 Nuclino, Slab, GitBook (brief)

- **Nuclino**: collections → items (an item in several collections); list, board, table, and graph views; RT editing; REST API and MCP; the API exposes content as **CommonMark plus GFM with engine metadata and inline comments encoded in HTML comments** and native links as item URLs; imports from Markdown, Word, HTML, Confluence, Quip.
- **Slab**: posts organized by topics rather than folders; RT editing; unified search across integrations.
- **GitBook**: spaces of block-based pages with **bidirectional git sync** to Markdown repositories; change requests; PDF export; every page also served as Markdown with a machine-readable index (`llms.txt`) and an MCP server.

### 3.12 Hosted farms and Wikidot (brief)

- **Fandom** (2004 as Wikicities; for-profit, ad-funded) runs a MediaWiki 1.43 fork. **Miraheze** (nonprofit, WikiTide Foundation; no advertising) runs current MediaWiki (1.46 in October 2026) with extensions on request. **Wikidot** (2006): its own markup with triple brackets, `[[[page]]]`, `[[[page | text]]]` (**T|L**), `[[[category: page]]]`; includes, modules, data forms; hosts the SCP Foundation wiki.

### 3.13 Adjacent: HedgeDoc, CodiMD, Etherpad

Collaborative editors, not wikis, but the technology of RT wiki editing came through them. **Etherpad** (2008; Apache-2.0; 3.3.6, September 2026) still uses its Easysync operational-transformation model. **HedgeDoc 1.x** (formerly CodiMD, from HackMD; AGPL-3.0; 1.12.0, August 2026) uses an OT library; **HedgeDoc 2** (pre-release) moves to Yjs. GROWI embedded HackMD/CodiMD for co-editing until replacing it with Yjs in v7; the OT-to-CRDT migration visible here, in GROWI, Crowi 2, Outline, Docmost, AFFiNE, and AppFlowy is the clearest technical convergence in this survey.

## 4. Block-based, outliner, and local-first tools

### 4.1 Obsidian

- Dynalist Inc., 2020; proprietary, free for all use since February 2025. Electron; **plain Markdown files in a local vault**; `.canvas` (JSON Canvas) and `.base` (YAML) files. 1.14.4 (October 2026).
- **Obsidian Flavored Markdown** = CommonMark + GFM + LaTeX + `[[Link]]`, `[[Link|Display]]` (**T|L**), `[[Note#Heading]]`, `[[Note#^id]]`, embeds `![[...]]` (notes, headings, blocks, images with size, PDF pages, canvases), block identifiers ` ^id`, callouts `> [!type]` with foldable `+`/`-` and a dozen types with aliases (unknown types fall back to note), footnotes, `%%comments%%`, `==highlight==`, task lists. Links to nonexistent notes create them on click; links update on rename. **Properties:** YAML frontmatter with typed values; default keys `tags`, `aliases`, `cssclasses` (singular forms dropped in 1.9). **Bases** (1.9, 2025): `.base` YAML files defining filters, formulas, and table/card/list/map/kanban views over frontmatter. **JSON Canvas** 1.0 (2024, MIT): an open format for canvases. **History:** local file-recovery snapshots; version history in the paid sync service. No RT editing or comments natively. Plugin API only. **Distinctive:** the de facto reference for the modern wiki-Markdown dialect; "file over app"; two open vendor formats.

### 4.2 Logseq

- Tienson Qin, 2020; AGPL-3.0; ClojureScript/Electron. **File-based line ended at 0.10.15 (December 2025)**; a **database version** reached 2.0 beta in July 2026, with the project "splitting into two versions". File graphs are **Markdown or Org files**, one per page, every block a list item; blocks receive a UUID (`id:: ...`) when referenced. **Properties** as `key:: value` lines (page properties in the first block; built-ins `title`, `tags`, `alias`, `template`, `public`). **Links:** `[[page]]`, `#tag` (tags are pages), `parent/child` namespaces; **block references `((uuid))`**; labelled form `[label]([[Page]])` (**L|T**). **Embeds:** `{{embed [[page]]}}`, `{{embed ((uuid))}}`. **Queries:** simple `{{query ...}}` and advanced **Datalog** blocks; user macros. No revision history in the file version beyond git or plugins; RT collaboration only in the database version. **Distinctive:** the outliner-as-Markdown-files model; the clearest illustration of the file-first versus database-first fork.

### 4.3 Roam Research (brief)

- 2019; proprietary SaaS. Outliner; `[[page]]`, `#tag`, `attr:: value`, `((block-uid))` references, `{{embed: ((uid))}}`, queries; RT multiplayer. **Export:** JSON, EDN (high fidelity, preserving references), Markdown (one file per page; block references and embeds are lost). **Distinctive:** popularized "networked thought", bidirectional links, and block references for a wide audience.

### 4.4 AFFiNE, AppFlowy, Anytype, SiYuan

- **AFFiNE** (2022; 0.27.4, August 2026): MIT except the backend, which is under an enterprise license; **BlockSuite** editor framework on **Yjs**; Rust CRDT server; docs and whiteboards in one document; databases; import from Markdown, Notion, OneNote; export Markdown, HTML, PDF, snapshots.
- **AppFlowy** (2021; AGPL-3.0; 0.14.6, October 2026): Flutter and Rust; collaboration layer on **yrs** (the Rust port of Yjs); databases, PDF/Word import; self-hosted cloud.
- **Anytype** (Any Source Available License 1.0 for apps, MIT for protocols; 0.57.4, October 2026): local-first with **peer-to-peer, end-to-end-encrypted sync**; objects, types, relations, and composable blocks; export Markdown, **Any-Block** (JSON or Protobuf), PDF; chats are not exportable; gRPC and a JSON API in pre-release.
- **SiYuan** (B3log; AGPL-3.0; 3.8.6, September 2026): Go kernel and TypeScript editor on the Lute Markdown engine; **`.sy` JSON block trees** per document; every block has an identifier; block references `((id "anchor"))` and SQL embeds `{{SELECT ... FROM blocks ...}}`; attributes as Kramdown attribute lists; databases, calendars, mind maps; **export Markdown with configurable degradation of block references** (anchor text or footnotes), plus lossless `.sy.zip`; MCP server with OAuth 2.1.

### 4.5 Tana, Capacities (brief)

- **Tana** (proprietary): an outliner of nodes with **supertags** (a tag that is a type with fields, forming queryable collections); AI agents; MCP server and public API with full export.
- **Capacities** (proprietary): "everything is an object" with typed properties; daily notes; offline operation; full export to Markdown.

### 4.6 Static publishers (brief)

- **Quartz** (MIT): publishes an Obsidian vault as a static site with full dialect support (`[[Page|Custom text]]`, `[[Page#^block-id]]`, `![[...]]`, callouts, `%%comments%%`, tags), case-insensitive link matching, backlinks, graph, and search.
- **Obsidian Publish** (hosted): hover previews, graph, custom domains, and `publish`, `permalink`, `description` frontmatter keys.
- **MkDocs** and **Docusaurus** are documentation generators without native wikilinks; community plugins (`mkdocs-roamlinks-plugin`, `remark-wiki-link`) add `[[Page]]` and `[[Page|label]]`.

## 5. Feature matrix

The matrix condenses the profiles. *T|L* and *L|T* give the labelled-link order; *Sep.* the hierarchy separator; *Missing* how a link to a nonexistent page is shown; *History* the model; *RT* real-time co-editing; *API desc.* whether a machine-readable description (OpenAPI or GraphQL schema) exists; *Pandoc* whether Pandoc reads (R) or writes (W) the native markup.

| Engine | Generation | License | Model | Native markup | Label order | Sep. | Missing | History | RT | API (desc.) | Export | Pandoc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MediaWiki | classic | GPL-2.0+ | document | Wikitext | T\|L | `:` ns, `/` sub | red link | full revisions | no | Action, REST (OpenAPI) | XML dump | R W |
| DokuWiki | classic | GPL-2.0 | document | DokuWiki | T\|L | `:` | red | attic | no | XML-RPC, JSON-RPC (OpenAPI) | raw/XHTML | R W |
| MoinMoin | classic | GPL-2.0+ | document | Moin + others | T\|L | `/` | styled | revisions | no | XML-RPC (1.9) | serialization | — |
| PmWiki | classic | GPL-2.0+ | document | PmWiki | T\|L and `->` | `/` or `.` | marked | per-page | no | — | source | — |
| TWiki / Foswiki | classic | GPL-2.0+ | document (topics) | TML | T][L | `.` | red `?` | RCS revisions | no | REST handlers | raw, static | R (twiki) |
| XWiki | classic→struct. | LGPL-2.1 | document + objects | XWiki 2.1 (+others) | L>>T | `.` | styled | versions | **yes** | REST (OpenAPI) | XAR, HTML, PDF | W |
| Tiki | classic | LGPL-2.1 | document + trackers | Tiki | T\|L | — | `?` | revisions | no | REST-ish | HTML, PDF | R |
| JSPWiki | classic | Apache-2.0 | document | JSPWiki | L\|T (single `[ ]`) | — | `?` | versions | no | XML-RPC | raw | — |
| Trac | classic | BSD-3 | document | Trac/Moin | T\|L | `/` | `missing` class | versions | no | XML-RPC plugin | txt | — |
| ikiwiki | classic (git) | GPL-2.0+ | document | Markdown + others | L\|T | `/` | `?` | git | no | — | static HTML | (Markdown) |
| Gollum / GitHub | git | MIT | document | Markdown + others | L\|T (contested) | `/` | absent style | git | no | — | repo | (Markdown) |
| GitLab wiki | git | — | document | Markdown + others | L\|T | `/` | — | git | no | REST | repo | (Markdown) |
| Gitit | git | GPL-2.0 | document | Pandoc Markdown | Markdown links | `/` | create | VCS | no | — | Pandoc | R W |
| PukiWiki | classic (JP) | GPL-2.0+ | document | PukiWiki | L>T | `/` | `?` | backups | no | — | — | — |
| TiddlyWiki | classic (unique) | BSD-3 | tiddlers | WikiText | L\|T | none | styled, create | none (single file) | no | HTTP (Node) | `.tid`, JSON, HTML | — |
| Federated Wiki | classic (unique) | MIT | story items + journal | minimal + plugins | — | none | ghost/create | journal in page | no | JSON pages | JSON | — |
| Zim | desktop | GPL-2.0+ | document | Zim (DokuWiki-like) | T\|L | `:` | create | VCS plugin | no | — | HTML, MD, reST | W |
| Redmine | classic | GPL-2.0 | document | Textile / CommonMark | T\|L | `:` project | red | versions | no | REST | HTML, PDF, TXT | (Textile) |
| Wiki.js | transitional | AGPL-3.0 | document | Markdown, HTML, AsciiDoc, visual | path links | `/` | — | history | no | GraphQL | git sync | (Markdown) |
| BookStack | transitional | MIT | document | WYSIWYG / Markdown | plain links | shelves/books | — | revisions | no | REST (self-doc) | HTML, PDF, MD, **Portable ZIP** | (Markdown) |
| Outline | transitional | BSL→Apache | document | ProseMirror / Markdown | mentions | collections | — | revisions | **Yjs** | RPC JSON (OpenAPI) | JSON, MD, HTML, **OKF** | (Markdown) |
| Docmost | transitional | AGPL-3.0 + EE | document | Tiptap / Markdown | plain links | spaces | — | history | **Yjs** | REST, MCP | MD, HTML | (Markdown) |
| GROWI | transitional (JP) | MIT | document | Markdown + frontmatter | L>T | `/` paths | — | revisions | **Yjs** | REST v3 | same-version archive | (Markdown) |
| Otter Wiki | git | MIT | document | Markdown | `[[ ]]` | `/` | — | git | no | — | repo | (Markdown) |
| Silverbullet | file-first | MIT | document + Lua | Markdown + Space Lua | T\|L | `/` | — | file/VCS | no | — | folder | (Markdown) |
| Trilium | tree | AGPL-3.0 | tree notes | CKEditor HTML | — | tree w/ clones | — | revisions | sync | ETAPI (OpenAPI) | HTML/MD ZIP | — |
| Dendron | file-first | Apache-2.0 | document | Markdown + frontmatter | L\|T | `.` | stubs | git | no | — | folder | (Markdown) |
| Foam | file-first | MIT | document | Markdown | T\|L | `/` | — | git | no | — | folder | (Markdown) |
| Confluence | enterprise | proprietary | document (ADF/XHTML) | visual (ADF) | L\|T legacy | spaces/tree | — | versions | **yes** | REST v2 (OpenAPI) | PDF, Word, HTML, XML | R (jira markup) |
| Notion | SaaS | proprietary | **blocks** | visual | mentions | tree | n/a | plan-limited | **yes** | REST | MD+CSV, HTML, PDF | (Markdown) |
| Scrapbox / Cosense | SaaS (JP) | proprietary | **lines** | Scrapbox notation | `[Page]` | none | distinct colour | snapshots | **yes** | internal JSON, CLI | JSON | — |
| esa.io | SaaS (JP) | proprietary | document | GFM | Markdown links | `/` in title | — | revisions + messages | partial | REST | MD ZIP | (Markdown) |
| Kibela | SaaS (JP) | proprietary | document | CommonMark / rich | Markdown links | groups/folders | — | history | **yes** | GraphQL | backup | (Markdown) |
| Nuclino | SaaS | proprietary | document | CommonMark+GFM (API) | URLs | collections | — | history | **yes** | REST, MCP | MD, ZIP | (Markdown) |
| GitBook | SaaS | proprietary | blocks | visual / Markdown (git) | Markdown links | spaces | — | change requests | **yes** | REST, MCP | git, PDF, MD | (Markdown) |
| Obsidian | local-first | proprietary (free) | document + `^id` | OFM | T\|L | `/` folders | dimmed, create | snapshots / sync | no | plugin API | files are the export | (Markdown) |
| Logseq (file) | local-first | AGPL-3.0 | **outliner** | Markdown / Org | L\|T (md form) | `/` ns | create | git/plugins | DB only | plugin API | files, MD, OPML | (Markdown) |
| Roam | SaaS | proprietary | outliner | Roam | `[[ ]]` | none | create | yes | **yes** | — | JSON, EDN, MD | — |
| AFFiNE | local-first | MIT + EE | **blocks** (BlockSuite) | visual | — | docs | — | CRDT | **Yjs** | — | MD, HTML, PDF | — |
| AppFlowy | local-first | AGPL-3.0 | blocks | visual | — | tree | — | CRDT | **yrs** | — | MD, PDF | — |
| Anytype | local-first | ASAL / MIT | **objects + blocks** | visual | — | types | — | CRDT | **p2p** | gRPC, JSON (pre) | MD, **Any-Block**, PDF | — |
| SiYuan | local-first | AGPL-3.0 | **blocks** (`.sy`) | Protyle / Markdown | `((id))` | notebooks | — | history | sync | MCP | MD (configurable), `.sy.zip` | — |
| TiddlyWiki (Node) | — | BSD-3 | tiddlers | WikiText | L\|T | none | styled | VCS | no | HTTP | `.tid`/JSON | — |

## 6. Cross-cutting observations

**What everyone kept from 1995.** A flat or shallow page space; a RecentChanges view (down to Gollum's git log and Federated Wiki's sitemap-driven list); per-page history with diff and revert (the exceptions outsource it to files, git, or a sync service); a marker for links whose target does not exist (the original `?` survives in PukiWiki, TWiki/Foswiki, PmWiki, and Trac; MediaWiki's red link became the alternative idiom; modern tools dim, colour, or create); and some escape hatch for macros.

**Free links won, with one unresolved schism.** `[[...]]` is near-universal; only JSPWiki (`[Page]`), Scrapbox / Cosense (`[Page]`), Tiki (`((Page))`), Wikidot (`[[[page]]]`), TWiki/Foswiki (`[[Page][Label]]`), and Gitit (`[Page]()`) deviate. The order of target and label inside a labelled link is split roughly two to one in favour of target-first, but the label-first family (TiddlyWiki, ikiwiki, Gollum and GitLab, JSPWiki, Hiki, Dendron, and with other delimiters PukiWiki, GROWI, XWiki, Confluence's legacy markup, Logseq's Markdown form) includes some of the most-used wikis in the world. Gitea had to encode the split as a heuristic in its renderer; GitHub's and Gollum's documentation disagree with each other. No guideline can wish this away; it can only ask engines to declare their order ([MKUP-6](../08-Markup_and_Syntax.md)).

**Separators and macros diverge even more.** Hierarchy is written with `:`, `/`, `.`, structural containers, or nothing. Macros come in at least a dozen shapes, and `{{...}}` alone means template (MediaWiki), image (DokuWiki, MoinMoin, Zim), tiddler transclusion (TiddlyWiki), macro (XWiki, Redmine), include (Otter Wiki), or embed (Logseq). This is why Chapter 12 standardizes the envelope around a macro's output rather than the macro.

**The document–block divide is real and bridgeable.** Document engines stop stable addressing at headings. Block tools give every unit an identity but export it differently: Obsidian keeps `^id` in the text (so Quartz and Foam can read it); Logseq writes `id::` only when referenced and flattens blocks into nested bullets; Roam's Markdown drops references (hence its EDN backup); Notion emits Markdown without identifiers; SiYuan makes the loss configurable and keeps lossless JSON beside it; Anytype and AFFiNE serialize CRDT state. Scrapbox / Cosense is the odd one: a line model whose JSON carries per-line identifiers and authorship.

**Real-time editing converged on one engine.** Yjs or its Rust port is behind Outline, Docmost, GROWI 7+, Crowi 2, HedgeDoc 2, AFFiNE, AppFlowy, and Logseq's database version; operational transformation survives in the Etherpad and HackMD lineage; Notion, Confluence Cloud, and Scrapbox / Cosense keep proprietary engines; XWiki uses ChainPad. "Local-first" now means two different things: files as the database (Obsidian, Silverbullet, Foam, Dendron) and CRDT state with a Markdown convenience copy (Anytype, AFFiNE, Logseq DB). Logseq's 2026 split between a frozen file-based line and a database-canonical beta is the sharpest illustration of that fork.

**Everyone exports Markdown; almost nobody round-trips.** Documented losses include Wiki.js editor conversions, BookStack's Markdown export "may still use HTML", Confluence's HTML export omitting comments, Notion dropping form views and block identity, Roam losing block references, Logseq's database graphs losing structured properties, Anytype's chats, and GROWI's same-version-only archive. Two 2026 developments point the other way: Outline's Open Knowledge Format and BookStack's documented Portable ZIP; GitBook and others now serve every page as Markdown for machine readers.

**OpenAPI quietly arrived in the classics.** MediaWiki serves a description of its REST API; DokuWiki generates one for its JSON-RPC API; XWiki offers one for download; Trilium, Outline, and Confluence publish theirs. For converter authors, these are the most approachable APIs in the field.

**The Japanese lineage contributed ideas the rest of the field is still catching up with.** Bracket links for languages without capital letters (YukiWiki, PukiWiki); in-page comment forms (PukiWiki); the first-class work-in-progress state (esa.io, now also GROWI's auto-expiring WIP pages); hierarchy-free, link-only organization with two-hop related pages and per-line authorship (Scrapbox / Cosense); hierarchical paths as identity with real-time editing (GROWI). Any guideline that treated wikis as an English-language or MediaWiki-shaped phenomenon would miss them.

**Age is not obsolescence.** New releases in 2026 came from MediaWiki, DokuWiki, PmWiki, Foswiki, ikiwiki, Gitit, JSPWiki (a 3.0), TiddlyWiki, Federated Wiki, Zim, Redmine, Tiki, and XWiki; meanwhile Wiki.js 3 is still in beta after five years, PukiWiki and Trac have gone quiet, and MoinMoin 2 remains in beta. The field is a continuum, not a succession.

---

Index: [README](../../README.md) · Next: [B · Syntax Crosswalk](B-Syntax_Crosswalk.md)
