# 10 · Interchange and Portability

> **Part III — Interoperability Guidelines** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [09 · Metadata and Frontmatter](09-Metadata_and_Frontmatter.md) · Next: [11 · APIs and Discovery](11-APIs_and_Discovery.md)

**In one sentence:** This chapter describes the *Portable Wiki Bundle*, a plain directory of Markdown pages, attachments, and optional history, discussions, and structured data, with a manifest that declares exactly what was carried and what was dropped, so that a wiki can move between engines without bespoke scripts and without silent loss.

Recommendations in this chapter carry the prefix `XFER-`. Machine-readable schemas: `schemas/bundle-manifest.schema.json`, `schemas/history-record.schema.json`, `schemas/discussion-record.schema.json`, `schemas/attachment-meta.schema.json`. A complete small example lives in `examples/portable-wiki-bundle/` and is walked through in [Appendix D](appendices/D-Portable_Wiki_Bundle_Example.md).

---

## 1. Three channels of portability

Knowledge leaves a wiki through three channels, and all three deserve care:

1. **Per-page raw access.** The smallest unit of portability is a URL that returns one page as plain text in the portable profile. It costs almost nothing and makes every other tool (converters, archivers, other wikis) possible. See [API-2](11-APIs_and_Discovery.md).
2. **Bundles.** A whole wiki, a namespace, or a single page with its history and attachments, exported as files. This chapter.
3. **Live APIs.** Programmatic access to pages, history, search, and changes while the wiki is running. [Chapter 11](11-APIs_and_Discovery.md).

The bundle is the channel that replaces "bespoke conversion scripts" with a shared target. It is deliberately boring: a directory (or an archive of one) that a person can read with a text editor and a file browser, and that a static site generator can publish unchanged.

## 2. Principles

- **Portability over feature parity.** The bundle carries knowledge, not features. An importer does not need to run the exporter's macros; it needs to show what they produced.
- **Declared loss.** Every exporter states its fidelity level and lists what it degraded or dropped; every importer reports what it could not use. Lossy is fine. Silent is not. ([PR-17](02-Guiding_Principles.md))
- **Readable without software.** The bundle is a folder of text files first and a data format second. Anyone can open it.
- **File over app.** Engines that already store content as files in the portable profile (local-first note tools, git-backed wikis) are nearly bundles already and need only a manifest. ([PR-16](02-Guiding_Principles.md))
- **Attribution travels.** History and contributor data are part of the bundle whenever the exporter has them and the license or privacy rules permit. ([PR-18](02-Guiding_Principles.md))

## 3. Bundle layout

```
<bundle-root>/
  wiki-bundle.yaml                 manifest (the only required file besides pages)
  pages/                           one Markdown file per page; directories are hierarchy
    Home.md
    Edit Conflicts.md
    Guides/
      Getting Started.md
    Category/
      Collaboration.md             kind: category
  attachments/                     media and files, referenced relatively from pages
    diagram.png
    diagram.png.meta.yaml          sidecar metadata (alternatively one attachments.yaml index)
  history/                         optional: one JSON Lines file per page
    018f6c3e-9d2b-7c4a-8e1f-2b3c4d5e6f70.jsonl
  discussions/                     optional: one JSON Lines file per page
    018f6c3e-9d2b-7c4a-8e1f-2b3c4d5e6f70.jsonl
  users.yaml                       optional: contributor directory
  structured/                      optional: schemas and tabular data
    schemas/decision-record.schema.json
    tables/releases.csv
    tables/releases.schema.json
  blocks.json                      optional: block-id → page path index
  links.json                       optional: precomputed link graph
```

A bundle **may** be a directory, a ZIP archive, or a tar archive of that directory. When archived, the manifest **should** be the first entry so that tools can inspect a bundle before extracting it.

## 4. Recommendations

### The manifest

#### XFER-1 · Every bundle carries a manifest

`wiki-bundle.yaml` **should** be present and **should** contain:

```yaml
format: portable-wiki-bundle
version: "0.1"
generator:
  name: ExampleWiki
  version: "4.2.0"
  url: https://example.org/examplewiki
exported_at: "2026-10-04T02:00:00Z"
source:
  name: Example Project Wiki
  url: https://wiki.example.org/
  engine: examplewiki
  engine_version: "4.2.0"
lang: en                       # default page language (BCP 47)
license: CC-BY-SA-4.0          # default content license (SPDX) for pages without their own
visibility_default: public
markup:
  profile: portable-wiki-markdown/2        # highest profile layer used
  native_format: text/x-examplewiki        # what the engine stores natively, if different
  link_label_order: target-first           # or label-first
  hierarchy_separator: "/"                 # as written in this bundle (always "/" when conforming)
  native_hierarchy_separator: ":"          # what the source engine used, for round-trip
  heading_anchor_algorithm: github         # or a URL describing it
  directives: [toc, children, query]       # directive names that may appear
  html_subset: [table, details, summary, sub, sup]
namespaces: [Talk, User, Help]             # MediaWiki-style prefixes present in titles
interwiki:
  wikipedia: "https://en.wikipedia.org/wiki/{title}"
  wp: "https://en.wikipedia.org/wiki/{title}"
contents:
  pages: 1248
  attachments: 312
  history: true
  discussions: true
  users: true
  structured: false
fidelity:
  level: 3
  degraded:
    - construct: "dynamic page lists"
      count: 17
      how: "snapshotted with wiki:snapshot envelopes"
    - construct: "parameterized templates"
      count: 203
      how: "expanded in place; template pages included under kind: template"
  dropped:
    - construct: "per-page access control lists"
      how: "replaced by visibility field"
extensions_used:
  - name: examplewiki-struct
    version: "2.1"
    directives: [query]
checksums: sha256sums.txt        # optional: file of "<hash>  <path>" lines
conformance: [portable-content, living-history]   # optional self-declaration, see Chapter 16
```

Unknown manifest keys **should** be preserved by tools that rewrite bundles.

#### XFER-2 · Declare fidelity

Exporters **should** state the highest level they reached and enumerate degraded and dropped constructs; importers **should** state the levels they accept.

| Level | Name | What is carried |
|---|---|---|
| 0 | Text | Readable pages; links may remain as literal `[[...]]`. Any importer can take this. |
| 1 | Structure | Headings, lists, tables, code, images; free links resolvable; attachments present. |
| 2 | Metadata | Portable Page Metadata ([Chapter 09](09-Metadata_and_Frontmatter.md)): identity, aliases, tags, dates, status, license, contributors. |
| 3 | History | Revisions with attribution, summaries, and events ([XFER-7](#xfer-7--history-as-json-lines)). |
| 4 | Conversation | Discussions and annotations ([XFER-10](#xfer-10--discussions-and-annotations)). |
| 5 | Structured data | Properties with schemas; tabular data ([XFER-11](#xfer-11--structured-data)). |

Levels are cumulative in intent but not in enforcement: a bundle **may** carry history without discussions. The manifest's `contents` block says what is present; `fidelity.level` says what the exporter attempted to make faithful.

### Pages

#### XFER-3 · One file per page, path is hierarchy, title is in frontmatter

- Each page is a `.md` file under `pages/` in the portable profile ([Chapter 08](08-Markup_and_Syntax.md)) with Portable Page Metadata ([Chapter 09](09-Metadata_and_Frontmatter.md)).
- The directory path encodes hierarchy with `/`. The file name is derived from the title; the `title` field is authoritative. File names **should** preserve Unicode and spaces. Characters that common file systems forbid (`\ : * ? " < > |` and control characters) **should** be replaced by a documented substitute, and a `/` inside a title (where the source engine allowed one) **should** be replaced likewise, with the true title in frontmatter. When two titles collide on a case-insensitive file system, a numeric suffix **should** be added to the file name only.
- Redirect pages are files with `redirect:` and `kind: redirect`. Category and tag pages carry `kind: category`.
- Block references that name a block without its page (`((uuid))` in outliners) **should** be resolved on export to `[[Page#^uuid]]`; a bundle **may** also include `blocks.json` mapping block identifiers to page paths for importers that keep a global block index.
- Pages **should** end with a newline and be UTF-8 without BOM ([MKUP-19](08-Markup_and_Syntax.md)).

#### XFER-4 · Attachments with sidecar metadata

- Files under `attachments/` keep their original names where possible; exporters **may** use hashed subdirectories for very large collections and **should** then record the original name in metadata.
- Each attachment **should** have metadata, either as a sidecar `<name>.meta.yaml` or as an entry in a single `attachments.yaml` index:

```yaml
filename: diagram.png
media_type: image/png
sha256: 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
size: 48213
alt: "Sequence diagram of an edit conflict between two editors"
license: CC-BY-4.0
attribution: "Aiko Tanaka"
source: https://wiki.example.org/attachments/diagram.png
uploaded_by: aiko
uploaded_at: "2024-03-02T10:20:00+09:00"
```

- Pages **should** reference attachments with paths relative to the page file (`../attachments/diagram.png`), so that any Markdown viewer renders them.
- Exporters **should** deduplicate identical files by hash and **should** include originals rather than only derived thumbnails.
- Attachment history (replaced files) **may** be exported under `history/` as `upload` events.

#### XFER-5 · Visibility and drafts

- Exporters **should** include only what the exporting user may see, and **should** mark every page with `visibility` when the wiki has access restrictions ([COLL-10](07-Collaboration_Awareness_and_Governance.md#coll-10--open-by-default-narrow-with-care)).
- Importers **should** treat `internal` and `restricted` pages as unpublished until an administrator decides otherwise, and **should** treat `status: draft` pages likewise.
- Full access-control models are not expected to transfer; `visibility` is a safety signal, not a permission system.

#### XFER-6 · Interwiki and namespaces travel in the manifest

The `interwiki` map and the `namespaces` list let importers distinguish `[[wikipedia:Topic]]` from `[[Talk:Topic]]` from a title that happens to contain a colon, and let them expand or keep prefixes as they prefer ([MKUP-13](08-Markup_and_Syntax.md), [NAV-13](04-Discovery_Navigation_and_Topology.md#nav-13--interwiki-links)).

### History

#### XFER-7 · History as JSON Lines

History **should** be exported as one JSON Lines file per page under `history/`, named by the page's `id` (or by its path when no identifier exists), with one record per revision or event in chronological order, oldest first:

```json
{"rev":"r0001","parent":null,"type":"create","at":"2024-03-02T10:15:00+09:00","author":{"id":"aiko","name":"Aiko Tanaka"},"summary":"Initial stub","minor":false,"content":"---\ntitle: Edit Conflicts\n---\n\nAn **edit conflict** happens when ...\n","sha256":"..."}
{"rev":"r0002","parent":"r0001","type":"edit","at":"2024-03-05T09:02:11+09:00","author":{"anonymous":true,"label":"~2024-30581-12"},"summary":"typo","minor":true,"patch":"--- r0001\n+++ r0002\n@@ -3,1 +3,1 @@\n-An **edit conflct**\n+An **edit conflict**\n","sha256":"..."}
{"rev":"r0003","parent":"r0002","type":"rename","at":"2025-01-10T12:00:00Z","author":{"id":"aiko","name":"Aiko Tanaka"},"from":"Editing Collisions","to":"Edit Conflicts","summary":"Use the common term"}
{"rev":"r0004","parent":"r0003","type":"edit","at":"2026-06-01T08:30:00Z","author":{"id":"bot-linkfix","name":"LinkFix bot","kind":"bot"},"automated":true,"summary":"Fix double redirect","content":"...","sha256":"..."}
{"rev":"r0005","parent":"r0004","type":"edit","at":"2026-07-14T15:45:00Z","author":{"id":"mallory","name":"mallory"},"suppressed":["content","summary"],"reason":"personal-data","suppressed_by":{"id":"oversight"}}
{"rev":"r0006","parent":"r0005","type":"revert","reverts":"r0005","restores":"r0004","at":"2026-07-14T15:50:00Z","author":{"id":"aiko","name":"Aiko Tanaka"},"summary":"Restored revision r0004","content":"...","sha256":"..."}
```

Record fields:

| Field | Meaning |
|---|---|
| `rev` | Revision identifier, unique within the page (engine-native or sequential). |
| `parent` | Previous revision identifier, or `null` for the first. |
| `type` | `create`, `edit`, `rename`, `delete`, `restore`, `revert`, `upload`, `protect`, `merge`, `fork`, `review`, or an engine-specific value declared in the manifest. |
| `at` | RFC 3339 timestamp. |
| `author` | `{id, name, kind}` referencing `users.yaml`, or `{anonymous: true, label}`. For coalesced real-time revisions, `contributors` (a list of the same shape) **may** be used in addition. |
| `summary` | The edit summary, if any. |
| `minor`, `automated` | Booleans ([HIST-8](06-Temporal_Design_and_Revision_History.md#hist-8--minor-edits-and-noise-control)). |
| `content` | The complete page file (frontmatter and body) at this revision, **or** |
| `patch` | A unified diff from the parent's content. Exporters using patches **should** emit full `content` at least every fifty revisions and whenever `type` is not `edit`. |
| `sha256` | Hash of the full content at this revision, for integrity when `patch` is used. |
| `from`, `to` | For `rename`. |
| `reverts`, `restores` | For `revert`. |
| `suppressed`, `reason`, `suppressed_by` | For tombstoned revisions ([HIST-12](06-Temporal_Design_and_Revision_History.md#hist-12--suppression-without-erasure)); the suppressed fields are omitted. |
| `review` | For `review` events: `{state, by}` ([COLL-14](07-Collaboration_Awareness_and_Governance.md#coll-14--review-as-an-overlay-not-a-gate)). |
| `assistance` | Exploratory: `{kind, tool}` when a machine drafted or suggested the change ([AUTH-14](05-Authoring_and_Participation.md#auth-14--machine-assistance-human-authorship)). |

Engines without per-revision content (journal-based or event-based histories) **should** replay their events into this form; engines with continuous real-time histories **should** export their checkpoints ([HIST-10](06-Temporal_Design_and_Revision_History.md#hist-10--real-time-co-editing-with-durable-history)).

#### XFER-8 · Contributor directory

`users.yaml` **should** list the authors referenced from history and frontmatter:

```yaml
- id: aiko
  name: Aiko Tanaka
  kind: person            # person | bot | group | anonymous
  url: https://wiki.example.org/User:Aiko
- id: bot-linkfix
  name: LinkFix bot
  kind: bot
```

Email addresses and IP addresses **should not** be exported unless the exporting administrator explicitly chooses to and the license and privacy rules permit it ([PRIV-3](14-Security_Privacy_and_Trust.md)). Exporters **should** offer pseudonymization (stable opaque identifiers in place of names) for cases where attribution must be preserved but identities must not travel; the manifest **should** record that it was applied.

#### XFER-9 · Link graph (advisory)

`links.json` **may** list edges `{"from": "pages/Home.md", "to": "pages/Edit Conflicts.md", "kind": "link"}` with `kind` in `link`, `embed`, `redirect`, `interwiki`, `attachment`, and `resolved: false` for dangling targets. It is a convenience for importers and analysts; the content is authoritative.

### Conversation and structure

#### XFER-10 · Discussions and annotations

Discussions **should** be exported under `discussions/` as JSON Lines, one file per page, one record per comment:

```json
{"id":"c1","parent":null,"at":"2026-02-01T10:00:00Z","author":{"id":"aiko","name":"Aiko Tanaka"},"body":"Should we mention three-way merge here?","resolved":true}
{"id":"c2","parent":"c1","at":"2026-02-01T11:30:00Z","author":{"id":"ben","name":"Ben"},"body":"Yes, added in [[Edit Conflicts#Merging]].","resolved":true}
{"id":"c3","parent":null,"at":"2026-03-10T09:00:00Z","author":{"id":"ben","name":"Ben"},"body":"This sentence is unclear.","anchor":{"type":"TextQuoteSelector","exact":"based on the same earlier revision","prefix":"same page ","suffix":".","revision":"r0004"},"resolved":false}
```

The `anchor` object follows the W3C Web Annotation selector vocabulary, so that engines with inline comments can re-anchor and engines without can list the quote. Bodies are Markdown in the portable profile. Talk pages that are themselves wiki pages (MediaWiki) **may** instead be exported as pages with `kind: discussion` and an `about:` field naming the subject page; exporters **should** choose one representation per bundle and declare it.

#### XFER-11 · Structured data

- Per-page structured values live in `properties` ([META-8](09-Metadata_and_Frontmatter.md)).
- Shared shapes (forms, classes, database schemas) **should** be exported as JSON Schema files under `structured/schemas/` and referenced from pages with `properties.schema`.
- Tabular data (database views, tracker tables, query results that are themselves content) **should** be exported as CSV (UTF-8, header row, RFC 4180 quoting) or JSON Lines under `structured/tables/`, each with a sibling schema describing column types and which columns are page references.
- Database rows that are pages in the source engine (Notion-style databases) **should** be exported as pages with `properties`, plus one table file indexing them, so that both document-shaped and table-shaped importers can use them.

#### XFER-12 · Snapshot dynamic content

Macros, queries, dynamic lists, and parameterized templates **should** be materialized on export into static content wrapped in a snapshot envelope that records the original expression ([EXT-4](12-Extensibility_Macros_and_Dynamic_Content.md)). Template pages themselves **should** be exported as pages with `kind: template`. Nothing in a bundle **should** depend on executing code to be read.

### Importing

#### XFER-13 · Produce an import report

Importers **should** produce a human-readable report (a page in the wiki or a file beside the bundle) listing: pages imported, renamed, or skipped; links left dangling; constructs degraded and how; metadata keys not understood but preserved; attachments missing or rejected; the fidelity level achieved. A dry-run mode that produces the report without writing is **encouraged**. The report is the importer's half of "declare what you drop".

#### XFER-14 · Scale gracefully

Bundles **should** be exportable and importable incrementally: a single page with its history, a namespace, or a time range. Archives **should** place the manifest first; large bundles **should** carry checksums; exporters **should** stream rather than build everything in memory. Importers **should** be resumable.

#### XFER-15 · Test the round trip

Export, import into a fresh instance, and export again. The two bundles **should** agree on text, links, metadata, and history; differences **should** be explainable by the manifest's declared degradations. Engines are **encouraged** to run this against `examples/portable-wiki-bundle/` and against bundles from other engines, and to publish the results.

## 5. Relationship to existing export formats

The bundle is designed so that existing formats map onto it rather than compete with it.

| Existing format | Mapping to the bundle |
|---|---|
| **MediaWiki XML dump** (`export-0.11` schema) | One `<page>` → one page file; `<revision>` elements → `history/` records (wikitext converted to the portable profile per revision or, at lower fidelity, latest only, with wikitext preserved under `ext.mediawiki.wikitext`); `<contributor>` → `users.yaml`; categories → `tags`; redirects → `redirect:`. Parsoid HTML or Pandoc as the conversion bridge. |
| **Confluence space export (XML)** | Pages → files with `ext.confluence` for storage-format remnants; labels → `tags`; versions → history; comments → discussions; macros → snapshot envelopes. |
| **Notion export (Markdown + CSV)** | Already close: Markdown pages → `pages/`, CSV databases → `structured/tables/` plus row pages; identifiers from URLs → `id`. |
| **Obsidian vault**, **Foam**, **Dendron**, **Logseq graph** | Already bundles in all but name: add a manifest, normalize link order and separators, map properties ([Chapter 09 §5](09-Metadata_and_Frontmatter.md#5-mapping-from-engines)). |
| **TiddlyWiki JSON / `.tid` files** | Each tiddler → a page; fields → frontmatter; `type` → `format`; tags → `tags`; WikiText converted to the profile with transclusions as `![[...]]` or snapshots. |
| **Federated Wiki JSON** | `story` items → body (one block per item with `^id`); `journal` → `history/` events (`create`, `add`, `edit`, `move`, `remove`, `fork` → `fork` events with `forked_from`). |
| **Scrapbox / Cosense JSON** | `lines` → body with indentation as list depth; line authors → `contributors`; `created`/`updated` → metadata. |
| **DokuWiki data directory** | `pages/` → `pages/` with `:` → `/`; `attic/` + `.changes` → `history/`; `media/` → `attachments/`. |
| **Git-backed wikis** (Gollum, ikiwiki, Otter Wiki, Wiki.js git sync, GitBook git sync) | Commits → history records; the repository is otherwise already a bundle. |
| **Outline's Open Knowledge Format** (2026) | A Markdown bundle with per-document YAML frontmatter and a root index; the closest existing cousin of this layout. Its frontmatter keys map onto Portable Page Metadata, and its index onto `pages/` plus the manifest. Convergence between the two is a stated goal ([17 · Roadmap](17-Roadmap_and_Open_Questions.md)). |
| **BookStack Portable ZIP** | Data plus attachments and images in a documented, re-importable archive; shelves, books, and chapters → directories, pages → files, tags → `tags`. |
| **Anytype Any-Block**, **SiYuan `.sy`**, **AFFiNE snapshots** | Lossless block JSON kept under `ext.<engine>` or as a sidecar, with the Markdown rendering as the portable body and block identifiers as `^id`. |
| **Nuclino API Markdown** | Already CommonMark plus GFM with engine metadata in HTML comments; comments and native links map to `discussions/` and free links. |
| **GROWI archive** | A dump of database collections importable only into the same engine version, which is exactly the situation a bundle is meant to improve on; per-page Markdown with frontmatter maps directly. |

Pandoc is a useful bridge for several native markups ([MKUP-18](08-Markup_and_Syntax.md)); engines are **encouraged** to contribute readers and writers for their syntax to it or to similar shared converters rather than maintaining private ones.

## 6. What the bundle is not

- It is not a backup format. It does not carry configuration, users' credentials, permissions, or plugins. Engines need their own backups.
- It is not a protocol. It has no notion of sessions or incremental sync; see [Chapter 11](11-APIs_and_Discovery.md) for live access and [17 · Roadmap](17-Roadmap_and_Open_Questions.md) for federation ideas.
- It is not mandatory. Engines with excellent native exports lose nothing by also writing a manifest and following the layout; the point is that an importer who has learned one bundle has learned them all.

---

Previous: [09 · Metadata and Frontmatter](09-Metadata_and_Frontmatter.md) · Next: [11 · APIs and Discovery](11-APIs_and_Discovery.md)
