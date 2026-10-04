# 09 · Metadata and Frontmatter

> **Part III — Interoperability Guidelines** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [08 · Markup and Syntax](08-Markup_and_Syntax.md) · Next: [10 · Interchange and Portability](10-Interchange_and_Portability.md)

**In one sentence:** A small, shared vocabulary of page metadata, carried in YAML frontmatter and mapped to Dublin Core and schema.org, lets titles, aliases, tags, dates, authorship, status, and license survive the move between engines that otherwise agree on nothing.

Recommendations in this chapter carry the prefix `META-`. The machine-readable form is `schemas/page-frontmatter.schema.json`; the field-by-field reference is [Appendix C](appendices/C-Portable_Page_Metadata_Reference.md).

---

## 1. Why metadata needs a shared vocabulary

The source report identified the "core knowledge" that must survive migration as text, links, hierarchy, and author attribution. Text and links are the business of [Chapter 08](08-Markup_and_Syntax.md). Almost everything else about a page is metadata: what it is called and also called, when it was made and changed, who contributed, what state it is in, how it may be reused, where it came from. Every engine records some of this and no two record it the same way: database columns in one, special fields in another, properties, labels, page props, tiddler fields, journal entries.

Frontmatter, a YAML block at the top of a Markdown file, has become the de facto container for such data across static site generators (Jekyll, Hugo), note tools (Obsidian, Dendron, Foam, Quartz), and several wikis. The container has converged; the keys have not. This chapter proposes a vocabulary, **Portable Page Metadata**, for the keys that matter most, and asks engines to use it on export and import while keeping any keys of their own.

## 2. The container

### META-1 · YAML frontmatter is the portable container

A page in the portable profile **should** begin with a YAML block delimited by `---` lines, before any content. Exporters **should** write YAML; importers **may** also accept TOML (`+++`) and JSON frontmatter, which some tools emit. The YAML used **should** be the plain subset: scalars, sequences, and mappings, without anchors, custom tags, or multi-document streams. Strings that could be misread by a YAML parser (dates, versions, `yes`/`no`, strings containing `:` or `#`) **should** be quoted on export.

A minimal page:

```yaml
---
title: Edit Conflicts
---
```

A full page:

```yaml
---
id: 018f6c3e-9d2b-7c4a-8e1f-2b3c4d5e6f70
title: Edit Conflicts
aliases: [Edit conflict, Editing collisions]
tags: [history, collaboration]
kind: page
lang: en
created: "2024-03-02T10:15:00+09:00"
updated: "2026-09-30T18:42:11Z"
contributors:
  - name: Aiko Tanaka
    id: aiko
  - name: anonymous
status: stable
review:
  state: verified
  by: maintainers
  at: "2026-06-01"
  revision: r0412
license: CC-BY-SA-4.0
description: What happens when two people save the same page at once, and how engines reconcile it.
canonical: https://wiki.example.org/wiki/Edit_Conflicts
visibility: public
properties:
  topic_area: collaboration
  difficulty: introductory
ext:
  mediawiki:
    page_id: 20481
    display_title: Edit conflicts
---
```

## 3. The vocabulary

The keys below are the shared vocabulary. All are optional except that a page **should** have a `title`. Unknown keys are allowed and **should** be preserved ([META-11](#meta-11--preserve-what-you-do-not-understand)).

### Identity

#### META-2 · `title` and `id`

- `title` (string): the human-readable title. **Should** be present. It is the primary address ([NAV-1](04-Discovery_Navigation_and_Topology.md#nav-1--page-as-the-unit-of-address)).
- `id` (string): a stable identifier that survives renames ([NAV-9](04-Discovery_Navigation_and_Topology.md#nav-9--stable-identity-beneath-the-title)). A UUID (RFC 9562, version 4 or the time-ordered version 7) is **recommended**; engine-native identifiers **may** be used when they are globally unique within the exporting wiki and **should** then be prefixed with a scheme (`mw:20481`). Importers **should** preserve the incoming `id`.

#### META-4 · `aliases`

`aliases` (list of strings): other titles that **should** resolve to this page ([NAV-8](04-Discovery_Navigation_and_Topology.md#nav-8--redirects-and-aliases)). Exporters **should** include former titles after renames. Engines that implement redirects as separate pages **may** export both the redirect pages (with `redirect:`) and the target's `aliases`; importers with aliases but without redirects **should** fold the redirects into `aliases`.

**`redirect`** (string): present on a page that exists only to redirect; the value is the target title or path. Such a page **should** have no body beyond an optional note.

### Classification

#### META-5 · `tags`

`tags` (list of strings): free-form labels ([NAV-7](04-Discovery_Navigation_and_Topology.md#nav-7--tags-and-categories)). Hierarchical categories **should** be flattened as `parent/child` strings. Exporters **should** merge inline hashtags into this list ([MKUP-14](08-Markup_and_Syntax.md)). Tag strings **should** be NFC-normalized; case is preserved and comparison is engine-defined.

#### META-7 · `kind`

`kind` (string): what sort of page this is. Values: `page` (default), `category` (a tag or category page), `template`, `help`, `system` (interface or configuration content), `discussion`, `user`, `redirect`. Importers **should** use `kind` to decide how to treat special pages ([COLL-12](07-Collaboration_Awareness_and_Governance.md#coll-12--the-wiki-documents-itself)) and **should** import unknown kinds as ordinary pages.

**`lang`** (string, **META-10**): the page's primary language as a BCP 47 tag (`en`, `ja`, `pt-BR`). **Should** be present when the wiki is multilingual. `translations` (map of BCP 47 tag → page path or title) **may** link language versions of the same topic ([I18N-6](13-Accessibility_Internationalization_and_Web_Standards.md)).

### Time and people

#### META-3 · `created` and `updated`

Both are RFC 3339 timestamps with an explicit offset or `Z`. `created` is the first revision's time; `updated` the latest revision's. A date without time (`2026-06-01`) **may** be used when the time is unknown. Importers **should** preserve these rather than resetting them to import time ([HIST-11](06-Temporal_Design_and_Revision_History.md#hist-11--page-lifecycle-at-a-glance)).

**`contributors`** (list): people who edited the page, each either a string (display name) or a mapping with `name`, optional `id` (stable within the bundle, matching `users.json`), optional `url`, and optional `role` (`author`, `maintainer`, `translator`, `bot`). The order **should** be by first contribution. Per-revision attribution lives in the history export ([XFER-7](10-Interchange_and_Portability.md)); `contributors` is the summary that survives when history is not exported. Privacy considerations apply ([PRIV-3](14-Security_Privacy_and_Trust.md), [LIC-4](15-Licensing_and_Attribution.md)).

**`maintainers`** (list, same shape): people or groups responsible for keeping the page current, as stewardship rather than ownership ([COLL-11](07-Collaboration_Awareness_and_Governance.md#coll-11--shared-artifact-not-possession)).

### State

#### META-6 · `status` and `review`

- `status` (string): the page's lifecycle state. Recommended values: `draft` (not meant for readers yet), `wip` (public, visibly unfinished), `stable`, `deprecated` (kept for reference), `archived`, `deleted` (exported tombstone). Engines **may** use other values and **should** document them. Maturity vocabularies such as `seedling`, `budding`, `evergreen` **may** be used as `status` values or placed in `properties.maturity`; importers **should** treat unknown values as `stable` for display and preserve the string ([AUTH-4](05-Authoring_and_Participation.md#auth-4--welcome-the-incomplete)).
- `review` (mapping): `state` (`none`, `pending`, `reviewed`, `verified`, `rejected`), `by` (name or id), `at` (RFC 3339), `revision` (the reviewed revision identifier) ([COLL-14](07-Collaboration_Awareness_and_Governance.md#coll-14--review-as-an-overlay-not-a-gate)).
- `visibility` (string, **META-13**): `public`, `internal` (members of the wiki), or `restricted` (narrower than the wiki). Advisory; it tells an importer how careful to be ([COLL-10](07-Collaboration_Awareness_and_Governance.md#coll-10--open-by-default-narrow-with-care)).

### Rights and provenance

#### META-9 · `license`

`license` (string): an SPDX license identifier or expression (`CC-BY-SA-4.0`, `CC0-1.0`, `CC-BY-4.0`) or, for licenses without an identifier, a URL. A page-level `license` overrides the bundle's default license in the manifest. Attachments carry their own ([XFER-4](10-Interchange_and_Portability.md)). See [Chapter 15](15-Licensing_and_Attribution.md).

**`source`** (string): URL of the page in the exporting wiki, for provenance. **`canonical`** (string): the preferred public URL, if different. **`forked_from`** (mapping with `site`, `page`, `revision`): when the page was copied from elsewhere ([COLL-13](07-Collaboration_Awareness_and_Governance.md#coll-13--fork-instead-of-fight)).

### Description and relations

**`description`** (string): one or two sentences describing the page, suitable for search results, link previews, and `<meta name="description">`. The key is shared with Dublin Core, schema.org, the Open Knowledge Format, Hugo, Jekyll, and Obsidian Publish; importers **should** accept `summary` and `desc` as synonyms.

**`related`** (list of titles or paths): hand-curated related pages, when the engine keeps them outside the body.

### Structured data

#### META-8 · `properties`

`properties` (mapping): free-form structured data attached to the page: infobox fields, form data, template parameters, database columns, outliner page properties. Values **may** be scalars, lists, or nested mappings. References to other pages **should** be written as `[[Title]]` strings so that they remain recognizable as links. Dates **should** be RFC 3339 strings. An optional `schema` key (URL or path to a JSON Schema in the bundle) **may** describe the expected shape for pages of a given type. Engines with typed structured data (XWiki classes, Semantic MediaWiki properties, Notion databases, Foswiki DataForms, Tiki trackers) **should** export their field values here and their schemas as bundle-level files ([XFER-11](10-Interchange_and_Portability.md)).

### Engine-specific data

#### META-11 · Preserve what you do not understand

Importers **should** preserve unknown top-level keys and **should** carry them through a later export. Engine-specific data **should** be placed under `ext` keyed by engine name (`ext.mediawiki`, `ext.obsidian`, `ext.notion`), so that two engines' keys never collide and so that a round trip through a third engine loses nothing. Secrets, access tokens, and internal permission structures **should not** be placed in frontmatter ([META-14](#meta-14--treat-metadata-with-the-care-given-to-content)).

## 4. Mapping to established vocabularies

### META-12 · Emit established vocabularies in HTML

When rendering a page to HTML, engines **should** expose the portable metadata through schema.org (as JSON-LD or microdata) and **may** add Dublin Core `<meta>` elements, so that search engines, citation tools, and archives understand the page without knowing the engine. The mapping:

| Portable key | Dublin Core (DCMI Terms) | schema.org (`Article` / `WebPage`) |
|---|---|---|
| `title` | `dcterms:title` | `name`, `headline` |
| `aliases` | `dcterms:alternative` | `alternateName` |
| `id` | `dcterms:identifier` | `identifier` |
| `description` | `dcterms:abstract`, `dcterms:description` | `description`, `abstract` |
| `tags` | `dcterms:subject` | `keywords` |
| `lang` | `dcterms:language` | `inLanguage` |
| `created` | `dcterms:created` | `dateCreated` |
| `updated` | `dcterms:modified` | `dateModified` |
| `contributors` | `dcterms:creator`, `dcterms:contributor` | `author`, `contributor` |
| `maintainers` | `dcterms:publisher` (loosely) | `maintainer` |
| `license` | `dcterms:license`, `dcterms:rights` | `license` |
| `source` | `dcterms:source` | `isBasedOn` |
| `canonical` | `dcterms:identifier` (URI) | `url`, `mainEntityOfPage` |
| `translations` | `dcterms:hasVersion` | `workTranslation`, `translationOfWork` |
| `related` | `dcterms:relation` | `relatedLink` |
| `status`, `review` | — | `creativeWorkStatus` |
| `kind` | `dcterms:type` | `@type` (`Article`, `WebPage`, `Collection`) |

A page rendered to HTML would then carry, for example:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Edit Conflicts",
  "dateCreated": "2024-03-02T10:15:00+09:00",
  "dateModified": "2026-09-30T18:42:11Z",
  "inLanguage": "en",
  "keywords": ["history", "collaboration"],
  "license": "https://creativecommons.org/licenses/by-sa/4.0/",
  "contributor": [{"@type": "Person", "name": "Aiko Tanaka"}],
  "url": "https://wiki.example.org/wiki/Edit_Conflicts"
}
</script>
```

Link relations in the HTML `<head>` (`rel="license"`, `rel="alternate" type="text/markdown"`, `rel="version-history"`, `rel="edit"`) are covered in [Chapter 11](11-APIs_and_Discovery.md).

## 5. Mapping from engines

Appendix C gives a full crosswalk. The main correspondences:

| Engine | Native mechanism | Portable mapping |
|---|---|---|
| **Obsidian** | Properties (YAML): `tags`, `aliases`, `cssclasses`, custom | Same keys for `tags` and `aliases`; `cssclasses` and custom keys under `ext.obsidian` or `properties` |
| **Dendron** | `id`, `title`, `desc`, `created`, `updated` (epoch milliseconds) | `id`, `title`, `description`; timestamps converted to RFC 3339 |
| **Logseq** | Page properties `title::`, `alias::`, `tags::`, custom `key:: value` | `title`, `aliases`, `tags`; custom into `properties` |
| **Hugo / Jekyll** | `title`, `date`, `lastmod`, `tags`, `categories`, `draft`, `aliases`, `slug`, `description` | `title`, `created`, `updated`, `tags` (categories flattened), `status: draft`, `aliases`, `description` |
| **MediaWiki** | Page title, categories, `DISPLAYTITLE`, page props, revision table | `title`, `tags` from categories, `ext.mediawiki.display_title`, `contributors` from history |
| **DokuWiki** | Page ID, first heading as title (optional), plugin metadata | `title`, `tags` from plugin, `created`/`updated` from changelog |
| **Confluence** | Title, labels, content status, version, space | `title`, `tags`, `status`, `review`, `ext.confluence.space` |
| **Notion** | Properties per database schema; created/edited times and users | `title`, `created`, `updated`, `contributors`; schema-driven fields into `properties` with a `schema` |
| **TiddlyWiki** | Fields: `title`, `tags`, `created`, `modified`, `type`, `list`, custom | `title`, `tags`, `created`, `updated`, `format` from `type`; custom fields into `properties` |
| **Federated Wiki** | `title`, `story`, `journal` | `title`; journal into history export; `forked_from` from fork actions |
| **Scrapbox / Cosense** | `title`, `created`, `updated`, `id`, line authors | `title`, `created`, `updated`, `id` (prefixed), `contributors` |
| **Growi** | Path, `_id`, tags, creator, last update user | `title` from last path segment, `id`, `tags`, `contributors` |

## 6. Block-level metadata

Pages are not the only things with metadata. Outliners attach properties to blocks; wikis attach captions and licenses to images; some engines attach comments to paragraphs.

- Page-level properties **should** go to frontmatter.
- Block-level properties **should** stay with the block in a form that degrades to text: a `key:: value` line following the block, or an HTML-comment envelope ([EXT-5](12-Extensibility_Macros_and_Dynamic_Content.md)).
- Attachment metadata **should** live in the attachment sidecar ([XFER-4](10-Interchange_and_Portability.md)).

## 7. Metadata is content

### META-14 · Treat metadata with the care given to content

Frontmatter is versioned, diffed, attributed, and exported like the body. Engines **should** show metadata changes in history ([HIST-2](06-Temporal_Design_and_Revision_History.md#hist-2--diff-as-a-first-class-view)), **should** make it editable through the same affordances as the body, and **should not** place anything in it that would be inappropriate in the body: secrets, raw IP addresses, internal access control structures. Contributor identities **should** follow the privacy guidance of [Chapter 14](14-Security_Privacy_and_Trust.md).

## 8. Validation

`schemas/page-frontmatter.schema.json` is a JSON Schema for the vocabulary. It is deliberately permissive: it checks types and formats for known keys and allows any additional keys. Exporters are **encouraged** to validate against it; importers **should not** reject pages that fail validation but **should** report problems in the import report ([XFER-13](10-Interchange_and_Portability.md)).

---

Previous: [08 · Markup and Syntax](08-Markup_and_Syntax.md) · Next: [10 · Interchange and Portability](10-Interchange_and_Portability.md)
