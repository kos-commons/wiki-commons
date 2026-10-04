# Appendix C · Portable Page Metadata Reference

> **Appendices** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [B · Syntax Crosswalk](B-Syntax_Crosswalk.md) · Next: [D · Portable Wiki Bundle Example](D-Portable_Wiki_Bundle_Example.md)

**In one sentence:** The field-by-field reference for the frontmatter vocabulary introduced in [Chapter 09](../09-Metadata_and_Frontmatter.md), with types, examples, mappings to engines and to established vocabularies, and the YAML pitfalls that bite in practice.

The machine-readable form is [`schemas/page-frontmatter.schema.json`](../../schemas/page-frontmatter.schema.json). The schema is permissive: known keys are type-checked, unknown keys are allowed and should be preserved.

---

## 1. Field reference

Types: `string`, `string[]` (list of strings), `datetime` (RFC 3339 string, or a date `YYYY-MM-DD`), `person` (a string or a mapping with `name`, optional `id`, `url`, `role`, `kind`), `map` (a YAML mapping). "Should" marks fields that are expected in most exports.

| Key | Type | Should | Meaning | Example |
|---|---|---|---|---|
| `title` | string | yes | Human-readable title; the primary address. | `title: Edit Conflicts` |
| `id` | string | encouraged | Stable identifier surviving renames. UUID (v4 or v7) recommended; engine-native identifiers prefixed with a scheme. | `id: 018f6c3e-9d2b-7c4a-8e1f-2b3c4d5e6f70`, `id: "mw:20481"` |
| `aliases` | string[] | when known | Other titles that resolve to this page, including former titles. | `aliases: [Edit conflict, Editing collisions]` |
| `redirect` | string | on redirect pages | Target title or path; the page has no body of its own. | `redirect: Edit Conflicts` |
| `tags` | string[] | when present | Free-form labels; hierarchy flattened as `parent/child`. | `tags: [history, collaboration, meta/needs-review]` |
| `kind` | string | when not `page` | `page`, `category`, `template`, `help`, `system`, `discussion`, `user`, `redirect`; others allowed. | `kind: template` |
| `lang` | string | in multilingual wikis | BCP 47 language tag. | `lang: ja` |
| `translations` | map (lang → path or title) | when known | Other language versions of the same topic. | `translations: {en: "Edit Conflicts", ja: "編集の競合"}` |
| `created` | datetime | yes | First revision time. | `created: "2024-03-02T10:15:00+09:00"` |
| `updated` | datetime | yes | Latest revision time. | `updated: "2026-09-30T18:42:11Z"` |
| `contributors` | person[] | when history is not exported | People who edited the page, in order of first contribution. | see §3 |
| `maintainers` | person[] | optional | Stewards responsible for currency; not owners. | `maintainers: [{name: Docs team, kind: group}]` |
| `status` | string | encouraged | Lifecycle state: `draft`, `wip`, `stable`, `deprecated`, `archived`, `deleted`; others allowed. | `status: wip` |
| `review` | map | when review exists | `state` (`none`, `pending`, `reviewed`, `verified`, `rejected`), `by`, `at`, `revision`. | see §3 |
| `visibility` | string | when restricted | `public`, `internal`, `restricted`. Advisory. | `visibility: internal` |
| `license` | string | when differing from the bundle default | SPDX identifier or expression, or a URL. | `license: CC-BY-SA-4.0` |
| `source` | string | on export | URL of the page in the exporting wiki. | `source: https://wiki.example.org/wiki/Edit_Conflicts` |
| `canonical` | string | optional | Preferred public URL if different from `source`. | |
| `forked_from` | map | on forks | `site`, `page`, `revision`. | `forked_from: {site: https://a.example, page: Edit Conflicts, revision: r0410}` |
| `description` | string | encouraged | One or two sentences for previews and search. `summary` and `desc` are accepted as synonyms on import. | |
| `related` | string[] | optional | Curated related pages kept outside the body. | `related: [Revision History, Soft Security]` |
| `format` | string | when not Markdown | Media type of the body with parameters. | `format: "text/markdown; charset=UTF-8; variant=GFM"` |
| `properties` | map | when structured data exists | Free-form structured data; page references as `[[Title]]` strings; dates as RFC 3339. | see §3 |
| `schema` | string | optional | URL or bundle path of a JSON Schema describing `properties`. | `schema: structured/schemas/decision-record.schema.json` |
| `about` | string | on discussion pages | The subject page of a `kind: discussion` page. | `about: Edit Conflicts` |
| `ext` | map (engine → map) | when needed | Engine-specific data namespaced by engine name. | see §3 |

Any other top-level key is permitted and should be preserved on import and re-export.

## 2. Value conventions

- **Timestamps** are RFC 3339 with an explicit offset or `Z`. A bare date (`2026-06-01`) is acceptable when the time is unknown. Exporters quote timestamps so YAML parsers do not coerce them.
- **Language tags** are BCP 47 (`en`, `ja`, `pt-BR`, `zh-Hant`).
- **Identifiers** are strings. UUIDs are lower-case hexadecimal with hyphens. Engine identifiers carry a scheme prefix: `mw:20481`, `notion:0f3b...`, `confluence:98304`.
- **Licenses** are SPDX identifiers (`CC-BY-SA-4.0`, `CC-BY-4.0`, `CC0-1.0`, `GFDL-1.3-or-later`) or expressions (`CC-BY-SA-4.0 OR GFDL-1.3-or-later`); a URL is acceptable for licenses without identifiers.
- **Page references inside values** are written as `[[Title]]` strings so that they remain recognizable as links: `properties: {supersedes: "[[ADR-001 Use Markdown]]"}`.
- **Strings** that could be misread by YAML (`yes`, `no`, `on`, `off`, `null`, numbers with leading zeros, version-like `1.10`, anything containing `: ` or starting with `#`, `*`, `&`, `!`, `%`, `@`, `` ` ``) are quoted on export.
- **Lists** are written in flow style (`[a, b]`) or block style; both are valid YAML.

## 3. Shapes

### Person

```yaml
contributors:
  - Aiko Tanaka                        # a bare string is allowed
  - name: Ben
    id: ben                            # matches users.yaml in a bundle
    url: https://wiki.example.org/User:Ben
    role: author                       # author | maintainer | translator | reviewer | bot
  - name: anonymous
    kind: anonymous                    # person | bot | group | anonymous
```

### Review

```yaml
review:
  state: verified
  by: Docs team
  at: "2026-06-01T09:00:00Z"
  revision: r0412
```

### Properties with a schema

```yaml
schema: structured/schemas/decision-record.schema.json
properties:
  adr_number: 2
  decision_status: accepted
  deciders: ["[[User:Aiko]]", "[[User:Ben]]"]
  decided_on: "2026-05-20"
  supersedes: "[[ADR-001 Use Markdown]]"
```

### Engine-specific data

```yaml
ext:
  mediawiki:
    page_id: 20481
    display_title: Edit conflicts
    wikitext_sha256: 9f86d0...
  obsidian:
    cssclasses: [wide]
  notion:
    database_id: 7a1c...
```

## 4. Mapping to Dublin Core and schema.org

| Portable key | DCMI Terms | schema.org | Notes |
|---|---|---|---|
| `title` | `dcterms:title` | `name`, `headline` | |
| `aliases` | `dcterms:alternative` | `alternateName` | |
| `id` | `dcterms:identifier` | `identifier` | |
| `description` | `dcterms:abstract` | `description`, `abstract` | |
| `tags` | `dcterms:subject` | `keywords` | |
| `lang` | `dcterms:language` | `inLanguage` | |
| `created` | `dcterms:created` | `dateCreated` | |
| `updated` | `dcterms:modified` | `dateModified` | |
| `contributors` | `dcterms:creator`, `dcterms:contributor` | `author`, `contributor` | first contributor as creator is a convention, not a rule |
| `maintainers` | | `maintainer` | |
| `license` | `dcterms:license` | `license` | expand SPDX identifiers to URLs in HTML |
| `source` | `dcterms:source` | `isBasedOn` | |
| `canonical` | `dcterms:identifier` (URI) | `url`, `mainEntityOfPage` | |
| `translations` | `dcterms:hasVersion` | `workTranslation`, `translationOfWork` | |
| `related` | `dcterms:relation` | `relatedLink` | |
| `status`, `review` | | `creativeWorkStatus` | |
| `kind` | `dcterms:type` | `@type` | `Article` for pages, `Collection` for categories |
| `forked_from` | `dcterms:source` | `isBasedOn` | with revision in `version` |

## 5. Mapping from engines

| Engine | Native | Portable | Conversion notes |
|---|---|---|---|
| **Obsidian** | `tags`, `aliases`, `cssclasses`, custom keys; `publish`, `permalink`, `description` for Publish | `tags`, `aliases`; `cssclasses` → `ext.obsidian.cssclasses`; `description` → `description`; `permalink` → `ext.site.permalink`; custom → `properties` | Obsidian requires list values for `tags` and `aliases` since 1.9; singular keys `tag`, `alias` are legacy |
| **Dendron** | `id`, `title`, `desc`, `created`, `updated` (epoch ms), `stub`, `nav_order`, `tags` | `id`, `title`, `description`, `created`, `updated` (converted to RFC 3339), `status: draft` for stubs, `tags` | Hierarchy is the dotted file name → `pages/` path with `/` |
| **Logseq** | `title::`, `alias::`, `tags::`, `public::`, custom `key:: value` | `title`, `aliases`, `tags`, `visibility: public` when `public:: true`, custom → `properties` | Page properties live in the first block; block properties stay with blocks |
| **Hugo** | `title`, `date`, `lastmod`, `tags`, `categories`, `draft`, `aliases`, `slug`, `description` | `title`, `created`, `updated`, `tags` (categories flattened), `status: draft`, `aliases`, `description` | `slug` → file name; `canonical` from site base URL |
| **Jekyll** | `title`, `date`, `tags`, `categories`, `permalink`, `published`, `description` | `title`, `created`, `tags`, `ext.site.permalink`, `status: draft` when unpublished, `description` | |
| **Quartz** | Obsidian keys plus `publish`, `permalink`, `description`, `date` | as Obsidian; `date` → `created` | |
| **MediaWiki** | page title, `page_id`, categories, `DISPLAYTITLE`, revision table, page props, redirects | `title`, `id: "mw:<page_id>"`, `tags` from categories, `ext.mediawiki.display_title`, `contributors` from revisions, `redirect` from `#REDIRECT` | Namespace prefix kept in `title`; listed in manifest `namespaces` |
| **DokuWiki** | page ID, first heading (when `useheading`), changelog, plugin metadata | `title` (heading or ID), `created`/`updated` from changelog, `tags` from tag plugin | `:` → `/` |
| **MoinMoin** | `#format`, `#language`, `#redirect`, Category links | `format`, `lang`, `redirect`, `tags` | |
| **PmWiki** | `(:title:)`, `(:description:)`, `(:keywords:)`, group | `title`, `description`, `tags` | group → path |
| **TWiki / Foswiki** | topic name, `%META:TOPICINFO`, DataForm fields | `title`, `created`/`updated`/`contributors` from TOPICINFO, DataForm → `properties` with a generated schema | web → path |
| **XWiki** | title, tags, XObjects, parent | `title`, `tags`, XObjects → `properties` with class schemas | |
| **TiddlyWiki** | `title`, `tags`, `created`, `modified`, `modifier`, `type`, `list`, custom fields | `title`, `tags`, `created`, `updated`, `contributors` from `modifier`, `format` from `type`, custom → `properties` | Dates are compact `YYYYMMDDHHMMSSmmm` strings → RFC 3339 |
| **Federated Wiki** | `title`, `story`, `journal` | `title`; journal → history records; `forked_from` from fork actions | items → body blocks with `^id` |
| **Confluence** | title, labels, content status, version info, space, page properties macro | `title`, `tags`, `status`/`review`, `contributors`, `ext.confluence.space`, properties macro → `properties` | |
| **Notion** | title property, database properties, created/edited times and users, icon, cover | `title`, `properties` (schema from the database), `created`, `updated`, `contributors`, `ext.notion.icon` | database rows → pages plus a table index |
| **Scrapbox / Cosense** | `title`, `id`, `created`, `updated`, line `userId`s | `title`, `id: "cosense:<id>"`, `created`, `updated`, `contributors` | |
| **GROWI** | path, `_id`, tags, creator, last update user, frontmatter | `title` (last path segment), `id`, `tags`, `contributors`, frontmatter keys merged | |
| **esa.io** | `name` with category path, `wip`, `tags`, `message`, revision number | `title` (last segment), path from category, `status: wip`, `tags` | |
| **Open Knowledge Format** | `type`, `title`, `description`, `resource`, `tags`, `status`, `generated`, `verified`, `sources` | `kind` and `ext.okf.type`, `title`, `description`, `canonical`, `tags`, `status`, `updated` and `contributors`, `review`, `ext.okf.*` | See [Appendix G](G-Open_Knowledge_Format_Alignment.md) |
| **Org-mode** | `#+TITLE`, `#+FILETAGS`, `#+LANGUAGE`, `:PROPERTIES:` drawer | `title`, `tags`, `lang`, `properties` | |

## 6. Examples

### Minimal

```yaml
---
title: Edit Conflicts
---
```

### A typical exported page

```yaml
---
id: 018f6c3e-9d2b-7c4a-8e1f-2b3c4d5e6f70
title: Edit Conflicts
aliases: [Edit conflict, Editing collisions]
tags: [history, collaboration]
lang: en
created: "2024-03-02T10:15:00+09:00"
updated: "2026-09-30T18:42:11Z"
contributors:
  - {name: Aiko Tanaka, id: aiko}
  - {name: Ben, id: ben}
  - {name: anonymous, kind: anonymous}
status: stable
license: CC-BY-SA-4.0
description: What happens when two people save the same page at once, and how engines reconcile it.
source: https://wiki.example.org/wiki/Edit_Conflicts
---
```

### A redirect page

```yaml
---
title: Editing Collisions
kind: redirect
redirect: Edit Conflicts
updated: "2025-01-10T12:00:00Z"
---
```

### A category page

```yaml
---
title: Collaboration
kind: category
description: Pages about how people work together on a wiki.
---

Pages tagged *collaboration* describe the social machinery of a wiki.
```

### A template page

```yaml
---
title: Decision Record
kind: template
description: Starter content for architecture decision records.
---
```

### A translated page

```yaml
---
id: 018f6c3e-9d2b-7c4a-8e1f-2b3c4d5e6f71
title: 編集の競合
lang: ja
translations:
  en: Edit Conflicts
properties:
  translation_of_revision: r0412
  translation_status: current
---
```

### A discussion page (MediaWiki-style talk page)

```yaml
---
title: "Talk:Edit Conflicts"
kind: discussion
about: Edit Conflicts
---
```

## 7. YAML pitfalls

| Pitfall | Example | Remedy |
|---|---|---|
| Timestamp coercion | `updated: 2026-09-30T18:42:11Z` becomes a date object in YAML 1.1 parsers | Quote timestamps on export |
| Boolean coercion | `status: no`, `tags: [yes]` | Quote |
| Leading zeros and numbers | `id: 0123`, `title: 1.10` | Quote |
| Colon in a value | `title: Note: on merging` | Quote |
| Reserved first characters | `description: #1 priority`, `title: *Star*` | Quote |
| Multi-line strings | summaries with line breaks | Use `>` or `\|` block scalars |
| Non-ASCII titles | `title: 編集の競合` | No quoting needed; ensure UTF-8 without BOM |
| Tabs | YAML forbids tabs for indentation | Use spaces |
| Duplicate keys | two `tags:` lines | Merge on export; importers take the last and report |

## 8. Validation

`schemas/page-frontmatter.schema.json` validates the YAML once parsed to JSON (frontmatter is extracted between the `---` lines). Any JSON Schema validator supporting draft 2020-12 works. Exporters are encouraged to validate; importers should report rather than reject ([XFER-13](../10-Interchange_and_Portability.md)).

---

Previous: [B · Syntax Crosswalk](B-Syntax_Crosswalk.md) · Next: [D · Portable Wiki Bundle Example](D-Portable_Wiki_Bundle_Example.md)
