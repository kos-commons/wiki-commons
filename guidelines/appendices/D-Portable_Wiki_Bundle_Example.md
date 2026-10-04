# Appendix D · Portable Wiki Bundle Example

> **Appendices** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [C · Portable Page Metadata Reference](C-Portable_Page_Metadata_Reference.md) · Next: [E · Glossary](E-Glossary.md)

**In one sentence:** A walk through the small but complete bundle in [`examples/portable-wiki-bundle/`](../../examples/portable-wiki-bundle/), file by file, showing what each part carries, how it degrades, and how an importer would read it.

The bundle describes an imaginary eight-page wiki exported from an imaginary engine. It exercises every optional part of the layout at fidelity level 5: pages with full metadata, a redirect, a category page, a template, a translated page, a dangling link, an interwiki link, a block identifier and a block embed, a snapshot envelope for a macro and one for a template, an attachment with a sidecar, a history with a patch, a rename, a bot edit, a suppressed revision and a revert, a discussion with an anchored comment, a contributor directory, structured data with schemas, a block index, a link graph, and checksums.

---

## 1. The tree

```
examples/portable-wiki-bundle/
├── wiki-bundle.yaml                        manifest (XFER-1)
├── pages/
│   ├── Home.md                             entry page; callout, dangling link, interwiki link, children snapshot
│   ├── Edit Conflicts.md                   full metadata; block id ^conflict-ui; embed; footnote; attachment
│   ├── Editing Collisions.md               redirect page (kind: redirect)
│   ├── Glossary.md                         status: wip; three identified blocks
│   ├── 編集の競合.md                        Japanese translation (lang: ja, translations)
│   ├── Category/Collaboration.md           kind: category
│   ├── Templates/Decision Record.md        kind: template; schema reference
│   └── Decisions/ADR-001 Use Markdown.md   properties with a schema; template snapshot
├── attachments/
│   ├── conflict-diagram.svg                a script-free SVG with <title> and <desc>
│   └── conflict-diagram.svg.meta.yaml      sidecar: media type, hash, size, alt, license, attribution
├── history/
│   ├── 018f6c3e-9d2b-7c4a-8e1f-2b3c4d5e6f70.jsonl   six records for Edit Conflicts
│   └── 018f6c3e-0000-7c4a-8e1f-2b3c4d5e6f00.jsonl   two records for Home
├── discussions/
│   └── 018f6c3e-9d2b-7c4a-8e1f-2b3c4d5e6f70.jsonl   a resolved thread and an anchored comment
├── users.yaml                              contributor directory (no email addresses)
├── structured/
│   ├── schemas/decision-record.schema.json shape of properties on decision pages
│   └── tables/decisions.csv + decisions.schema.json   a table and its column types
├── blocks.json                             block id → page path
├── links.json                              advisory link graph
└── sha256sums.txt                          checksums of every file except the manifest
```

## 2. The manifest

[`wiki-bundle.yaml`](../../examples/portable-wiki-bundle/wiki-bundle.yaml) says who made the bundle and when, where the content came from, the default language and license, and, most usefully for an importer, the **conventions**: the profile layer (`portable-wiki-markdown/2`), the link label order (`target-first`), the separator written in this bundle (`/`) and the one the source engine used natively (`:`), the heading anchor algorithm, the directive names that may appear (`toc`, `children`), the small HTML subset used (`sub`, `sup`), the MediaWiki-style title prefixes present (`Talk`, `User`), and the interwiki map (`wikipedia`, `wp`, `jawp`).

The `contents` block tells the importer what to expect (eight pages, one attachment, history, discussions as JSON Lines, users, structured data). The `fidelity` block declares level 5 and lists exactly what was degraded (one `children` macro snapshotted, one template expanded) and dropped (access control lists, replaced by `visibility`). `conformance` is the exporter's self-declared profiles.

## 3. Pages

**`Home.md`** is an ordinary page with a `> [!TIP]` callout, a list of free links including a labelled one (`[[Decisions/ADR-001 Use Markdown|Our first decision record]]`), a link to a page that does not exist (`[[Merge Strategies]]`, which an importer should keep dangling), an interwiki link (`[[wikipedia:Wiki|...]]`), a link to a category page, an inline `#meta` tag that is also in `tags:`, and a **snapshot envelope** around the output of the `children` macro:

```markdown
<!-- wiki:snapshot kind="macro" name="children" engine="examplewiki" src="{{children path=&quot;Decisions&quot; depth=1}}" at="2026-10-04T02:00:00Z" -->
- [[Decisions/ADR-001 Use Markdown]]
<!-- /wiki:snapshot -->
```

A plain Markdown viewer shows the list. An importer that knows `examplewiki`'s `children` macro may replace it with a live one.

**`Edit Conflicts.md`** carries the fullest frontmatter: `id`, `aliases` (including the former title), `tags`, `lang` and `translations`, dates, `contributors` including an anonymous and a bot contributor, `status`, a `review` object, `license`, `description`, `source`, and engine-specific data under `ext.examplewiki`. The body has a footnote, a same-page heading link (`[[#Merging|how merging works]]`), a dangling link (`[[Revision History]]`), an image with alternative text referenced relative to the page (`../attachments/conflict-diagram.svg`), a paragraph ending in a block identifier (`^conflict-ui`), and a block embed (`![[Glossary#^optimistic-concurrency]]`).

**`Editing Collisions.md`** is a redirect: `kind: redirect`, `redirect: Edit Conflicts`, no body. The target page lists the old title in `aliases`, so an importer without redirects can fold the two.

**`Glossary.md`** has `status: wip` and a callout saying so; three definitions end in block identifiers (`^base-revision`, `^optimistic-concurrency`, `^revision`) so other pages can embed them.

**`編集の競合.md`** is the Japanese page: `lang: ja`, `translations: {en: Edit Conflicts}`, a non-Latin title and file name, and `properties` recording which English revision it translates. It links to the English page and to the Japanese Wikipedia through the `jawp` prefix.

**`Category/Collaboration.md`** is a category page (`kind: category`) with a short description; engines in which tags are pages import it as a tag page, others as an ordinary page.

**`Templates/Decision Record.md`** is a template (`kind: template`) with headings and a `schema` reference. **`Decisions/ADR-001 Use Markdown.md`** was created from it: its `properties` follow the schema, and the expanded template header is wrapped in a `kind="template"` envelope with `name` and `params`.

## 4. Attachment and sidecar

The SVG is hand-written, has no scripts, and carries `<title>` and `<desc>` for accessibility. The sidecar records its media type, SHA-256, size, default alternative text, license (`CC-BY-4.0`, different from the wiki's `CC-BY-SA-4.0` default), attribution, source URL, uploader, and upload time.

## 5. History

The six records for *Edit Conflicts* show the record types in [XFER-7](../10-Interchange_and_Portability.md):

1. `create` with full `content` (the first stub, misspelled "conflct").
2. `edit`, `minor: true`, by an anonymous editor shown under a temporary-account label, with a `patch` instead of full content and the `sha256` of the resulting content.
3. `rename` from "Editing Collisions" to "Edit Conflicts", with a summary.
4. `edit` by a bot (`kind: bot`, `automated: true`) with full content.
5. `edit` by a user whose content and summary were **suppressed** (`suppressed: [content, summary]`, `reason: personal-data`), leaving a tombstone that preserves the chain.
6. `revert` that `reverts` r0005 and `restores` r0004, with the restored content.

The two records for *Home* show a `create` followed by an `edit` carried as a patch that introduces the `children` macro in its native form; the snapshot in `pages/Home.md` is what that macro produced at export time.

## 6. Discussions

Three records: a question and its reply (both `resolved: true`), and an unresolved comment anchored to a sentence with a Web Annotation `TextQuoteSelector` (`exact`, `prefix`, `suffix`) against revision `r0004`. An importer with inline comments re-anchors it; one without lists the quote under the page.

## 7. Users, structured data, indexes, checksums

`users.yaml` maps the identifiers used in history and frontmatter to display names, kinds (`person`, `bot`, `group`), and profile URLs, and deliberately contains no email addresses.

`structured/schemas/decision-record.schema.json` describes the `properties` of decision pages; `structured/tables/decisions.csv` is a one-row table indexing them, with `decisions.schema.json` typing its columns and marking `page` as a page reference.

`blocks.json` lets an importer resolve `#^id` references without scanning every page; `links.json` is an advisory edge list that marks the two dangling targets with `resolved: false`. `sha256sums.txt` lists a hash for every file except the manifest that names it.

## 8. What a plain Markdown viewer shows

Open any page in a viewer that knows only CommonMark and GFM:

- Free links appear as literal `[[Edit Conflicts]]`: visible, understandable, not clickable.
- The callouts appear as block quotes beginning with `[!TIP]`.
- `^conflict-ui` appears as a short token at the end of a paragraph.
- The embed appears as the literal line `![[Glossary#^optimistic-concurrency]]`.
- The snapshot envelopes are invisible; their contents (a list, a status box) show as ordinary Markdown.
- The image renders, because its path is relative to the page.
- The frontmatter may render as a table or as text, depending on the viewer.

Nothing is lost that a reader needs. That is the point of the profile's degradation ladder ([Chapter 08 §4](../08-Markup_and_Syntax.md#4-the-degradation-ladder)).

## 9. What an importer does

1. Read the manifest. Note the label order, separators, directives, namespaces, interwiki map, default license, and fidelity declaration. Warn if the license is incompatible with the destination ([LIC-5](../15-Licensing_and_Attribution.md)).
2. Treat the bundle as untrusted ([SEC-7](../14-Security_Privacy_and_Trust.md)): check paths, sizes, media types, and checksums; sanitize Markdown and the SVG.
3. Create pages from `pages/`, keeping `title` and `id`, folding `aliases`, honouring `kind` and `visibility`, preserving unknown keys and `ext` ([META-11](../09-Metadata_and_Frontmatter.md)).
4. Rewrite links as needed: flip label order if the destination is label-first; map `/` to the native separator; expand or keep interwiki prefixes; leave dangling links dangling.
5. Import attachments with their metadata; rewrite relative image paths to wherever attachments live.
6. Replay `history/` into native revisions, mapping authors through `users.yaml`, keeping tombstones as tombstones, and preserving revision identifiers for permalinks.
7. Import discussions, re-anchoring where possible.
8. Resolve `#^id` references through `blocks.json` or by scanning; keep identifiers the destination cannot use as text.
9. Decide what to do with snapshot envelopes: replace with live constructs when the extension is known, otherwise keep the content (and optionally the envelope).
10. Write an **import report** listing everything that was degraded, dropped, or left dangling ([XFER-13](../10-Interchange_and_Portability.md)).

## 10. Validating the bundle

The repository ships a dependency-free validator (Python 3; PyYAML needed for the YAML files):

```sh
python3 tools/validate_bundle.py examples/portable-wiki-bundle
```

It checks the manifest, every page's frontmatter, every history and discussion record, and every attachment sidecar against the schemas in [`schemas/`](../../schemas/), verifies the checksums, resolves the targets in `links.json` and `blocks.json`, confirms that relative attachment paths exist, and reports dangling links as information rather than errors. Any full JSON Schema validator can be used instead ([schemas/README.md](../../schemas/README.md)).

## 11. Making your own

1. Write the manifest first, truthfully: the profile layer you reach, your native label order and separator, the directives you emit, what you drop.
2. One page, one file, title in frontmatter, path as hierarchy. Keep Unicode in file names.
3. Export links in the portable forms; expand nothing you do not have to; snapshot everything dynamic with an envelope.
4. Attach sidecars to attachments; reference them relatively.
5. Export history as JSON Lines, oldest first, with full content at least at checkpoints.
6. Validate, import into another engine, export again, and compare ([XFER-15](../10-Interchange_and_Portability.md)). Then tell this project what was hard.

---

Previous: [C · Portable Page Metadata Reference](C-Portable_Page_Metadata_Reference.md) · Next: [E · Glossary](E-Glossary.md)
