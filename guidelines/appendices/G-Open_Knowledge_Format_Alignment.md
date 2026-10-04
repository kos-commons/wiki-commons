# Appendix G · Open Knowledge Format Alignment

> **Appendices** · **Status:** Working Draft 0.2 (October 2026)
> Previous: [F · References](F-References.md) · Index: [README](../../README.md)

**In one sentence:** The Open Knowledge Format (OKF) and the Portable Wiki Bundle are both "a directory of Markdown files with YAML frontmatter", built for different purposes; this appendix maps one onto the other field by field, records the choices made to keep them close, and describes the converter that implements the mapping.

---

## 1. What OKF is

The **Open Knowledge Format** is a specification published by Google Cloud in June 2026 (version 0.1) and revised to version 0.2 the same year. Its canonical home is the `GoogleCloudPlatform/open-knowledge-format` repository ([Appendix F](F-References.md)). It describes a *knowledge bundle*: a directory tree of Markdown *concept* documents, each with YAML frontmatter, cross-linked with ordinary Markdown links, optionally with `index.md` listings for progressive disclosure and `log.md` files recording changes. It was designed so that software agents and people can read the same corpus, and so that an agent-maintained corpus stays trustworthy: version 0.2 added frontmatter families for provenance (`sources`), trust (`generated`, `verified`), lifecycle (`status`, `stale_after`), and attested computations.

Outline added an OKF export in September 2026 (version 1.10.1), writing one concept per document with `type: Document`, `title`, `description`, `resource` (the document's URL), `status`, and `generated`, plus a root `index.md` carrying `okf_version`. Other knowledge tools are likely to follow, which makes OKF a natural neighbour of the Portable Wiki Bundle ([Chapter 10](../10-Interchange_and_Portability.md)).

An earlier draft of this suite attributed the format to Outline; that was wrong, and this appendix corrects it.

## 2. Shared ground

The two formats agree on more than they differ:

- **Plain files.** Both are directories of UTF-8 Markdown with YAML frontmatter, distributable as a git repository or an archive, readable with `cat`.
- **Permissive consumers.** OKF requires consumers to preserve unknown frontmatter keys and to tolerate broken links and unknown types; the bundle asks the same of importers ([META-11](../09-Metadata_and_Frontmatter.md), [NAV-3](../04-Discovery_Navigation_and_Topology.md#nav-3--dangling-link-as-invitation)).
- **Declared loss and provenance.** OKF's `generated`, `verified`, and `sources` and the bundle's `contributors`, `review`, `source`, and history records answer the same questions: who wrote this, who checked it, where did it come from.
- **Links as the structure.** OKF treats links between concepts as untyped graph edges and tolerates dangling ones; so does the wiki tradition.
- **A root listing.** OKF's `index.md` and the bundle's manifest both let a consumer learn what is in the directory before opening files.

## 3. Where they differ

| Aspect | Open Knowledge Format 0.2 | Portable Wiki Bundle 0.1 |
|---|---|---|
| Purpose | Knowledge *about* assets and systems, for agents and people | Knowledge *written* in wikis, moved between engines |
| Unit | Concept, with a required open-vocabulary `type` | Page, with an optional small-vocabulary `kind` |
| Links | Standard Markdown links, bundle-absolute `/path.md` recommended | Free links `[[Title]]`, resolved by title and alias |
| Sub-page addressing | None | Heading anchors and `^id` block identifiers |
| History | Prose `log.md` entries grouped by date | Structured `history/*.jsonl` records with content, authors, events |
| Discussions, attachments, structured data | Not specified | `discussions/`, `attachments/` with sidecars, `structured/` |
| Trust | `generated`, `verified` with an actor convention, trust tiers | `contributors`, `review`, per-revision attribution |
| Freshness | `stale_after` | `updated`, `review`, maturity markers |
| Dynamic content | Attested computations (sanctioned computations with executors and attesters) | Snapshot envelopes around macro output |
| Listings | `index.md` per directory | Derived; not stored |
| Reserved names | `index.md`, `log.md` | `wiki-bundle.yaml`, `sha256sums.txt` |

None of these is a conflict. A wiki page can be an OKF concept of type `Wiki Page`; an OKF concept can be a wiki page whose frontmatter carries the OKF families under `ext.okf`.

## 4. Field mapping

### 4.1 Bundle to OKF (export)

| Portable Page Metadata | OKF frontmatter | Notes |
|---|---|---|
| `kind` | `type` | `page` → `Wiki Page` (configurable), `category` → `Category`, `template` → `Template`, `help` → `Help Page`, `system` → `System Page`, `discussion` → `Discussion`, `user` → `User Page`, `redirect` → `Redirect` |
| `title` | `title` | |
| `description` | `description` | Collapsed to one line |
| `canonical`, else `source` | `resource` | The page's URL in the source wiki |
| `tags` | `tags` | |
| `status` | `status` | `draft`, `wip` → `draft`; `stable` → `stable`; `deprecated`, `archived`, `deleted` → `deprecated`. When the mapping loses information the original value is kept as `wiki_status`. |
| `updated` + most recent author | `generated: {by, at}` | The actor is `human:<id>` for people, `process:<id>` for bots, `team:<id>` for groups ([OKF §7](F-References.md)); the author comes from the latest history record when history is present, else from `contributors` |
| `review` (state `reviewed` or `verified`) | `verified: [{by, at}]` | `review` is also kept as-is so that an import restores it exactly |
| `source` | `sources: [{id: origin, resource, title}]` | The original page is the concept's provenance |
| everything else (`id`, `aliases`, `lang`, `translations`, `created`, `contributors`, `license`, `visibility`, `properties`, `ext`, ...) | kept as additional keys | OKF §4.1 permits producer-defined keys and requires consumers to preserve them |

### 4.2 OKF to bundle (import)

| OKF frontmatter | Portable Page Metadata | Notes |
|---|---|---|
| `type` | `kind` and `ext.okf.type` | Known type names map back to kinds; every type is preserved under `ext.okf` |
| `title` | `title` | Falls back to the file name |
| `description` | `description` | |
| `resource` | `canonical` when it is a URL, else `ext.okf.resource` | |
| `tags` | `tags` | |
| `status` | `status` | `wiki_status`, when present, wins |
| `generated.at` | `updated` | A v0.1 `timestamp` is accepted as a fallback |
| `generated.by` | `contributors: [{name, id, kind}]` | `human:` → person, `process:` → bot, `team:` → group, `producer/version` → bot |
| `verified` | `review: {state: verified, by, at}` from the latest event, plus `ext.okf.verified` | A bare mapping is treated as a one-element list, as OKF requires |
| `sources`, `usage_window`, `stale_after`, `runtime`, `parameters`, `computation`, `executor`, `attester` | `ext.okf.*` | Preserved for round-trips; attested computations are not executed |
| portable keys written by a Wiki Commons exporter | restored directly | `contributors`, `created`, `updated`, `review`, `canonical`, `status` from `wiki_status` |
| other keys | preserved | |

### 4.3 Structure and content

| Bundle | OKF | Notes |
|---|---|---|
| `pages/<path>.md` | `<path>.md` at the root | A page whose file name is reserved (`index.md`, `log.md`) becomes `<name>-page.md` |
| `[[Title]]`, `[[Title\|Label]]`, `[[Title#Heading]]` | `[Label](/path.md)`, `[Label](/path.md#anchor)` | Bundle-absolute links, as OKF recommends; unlabelled links take the target page's title |
| `[[Title#^id]]`, `![[Title#^id]]` | `[Title](/path.md)` | Block addressing has no OKF equivalent; degraded to a page link and noted |
| `![[Title]]` | `[Title](/path.md)` | Transclusion degraded to a link |
| `^id` tokens | removed | |
| `[[prefix:Title]]` | `[Title](https://...)` | Expanded through the manifest's interwiki map |
| Dangling links | plain text | OKF tolerates broken links, but the exporter has no path to write; the title remains readable |
| `attachments/` with sidecars | `attachments/` | Files copied; sidecars travel as non-Markdown files; references become `/attachments/...` |
| `history/*.jsonl` | `log.md` | One entry per revision under its date, newest first; suppressed revisions appear as suppression entries |
| `wiki-bundle.yaml` | `wiki-bundle.yaml` | Kept beside the concepts (not a reserved name, not a `.md` file) so that an import can recover the conventions |
| (derived) | `index.md` per directory | Root index carries `okf_version: "0.2"`, lists concepts with descriptions and subdirectories with counts |
| `discussions/`, `structured/`, `users.yaml`, `blocks.json`, `links.json` | not exported | Noted in the export report; OKF has no place for them yet |

On import, OKF `index.md` files are skipped (they are listings an exporter regenerates) and `log.md` files become pages of `kind: system` titled "Update Log", so that no prose is lost; standard Markdown links to concepts become free links by title, with heading anchors mapped back to heading text where the target page has a matching heading; links that point outside the bundle are left as written.

## 5. Choices made for alignment

Three small changes were made to this suite in version 0.2 so that the two formats stay close without either bending:

1. **`description` replaces `summary`** as the Portable Page Metadata key for a one-line description ([META-6](../09-Metadata_and_Frontmatter.md)). OKF, Dublin Core, schema.org, Hugo, Jekyll, Obsidian Publish, and Dendron (`desc`) all use that word; `summary` was an invention. Importers accept `summary` as a synonym.
2. **The actor convention is adopted for export.** Contributor kinds (`person`, `bot`, `group`) map onto OKF's `human:`, `process:`, and `team:` prefixes, which also gives exporters a consistent way to represent anonymous and temporary-account editors (`human:~2026-30581-12`).
3. **Lossy mappings carry the original.** Where OKF's vocabulary is coarser (`status`), the original value travels as an extra key, and where OKF has no field (`review`, `translations`, `aliases`), the portable key travels untouched. OKF's own §4.1 makes this legitimate.

Nothing was removed from the bundle to fit OKF, and nothing OKF-specific became required in the bundle.

## 6. What OKF could take from the wiki tradition, and what wikis could take from OKF

*Exploratory.* These are observations for the two communities, not requirements.

- OKF has no way to address a part of a concept. Heading anchors already work through ordinary fragment links; a `^id` convention for blocks ([MKUP-9](../08-Markup_and_Syntax.md)) would cost OKF nothing and would let agents cite paragraphs.
- OKF's `log.md` is prose; a structured history alongside it, even one record per entry, would let consumers reconstruct what changed. The bundle's history record ([XFER-7](../10-Interchange_and_Portability.md)) is a candidate shape.
- OKF has no alias or redirect convention; agents that rename concepts break inbound links. `aliases` ([META-4](../09-Metadata_and_Frontmatter.md)) is a one-line addition.
- Wikis, in turn, could adopt OKF's `stale_after` as a portable freshness signal alongside review states ([HIST-11](../06-Temporal_Design_and_Revision_History.md#hist-11--page-lifecycle-at-a-glance)), and its `sources` list as a structured home for the "References" sections that wiki pages write by hand.
- OKF's actor convention is a ready-made answer to [Q5](../17-Roadmap_and_Open_Questions.md) (identity across wikis) for the limited purpose of saying who or what produced a revision, and to [AUTH-14](../05-Authoring_and_Participation.md#auth-14--machine-assistance-human-authorship) (machine assistance), since `producer/version` actors are distinguishable from `human:` ones.

## 7. Tooling

The reference tooling implements both directions:

```sh
python3 tools/wikicommons.py okf export examples/portable-wiki-bundle out/okf
python3 tools/wikicommons.py okf import out/okf out/bundle --name "Example Project Wiki"
```

The export writes concepts, per-directory `index.md` files, a `log.md` from history, the attachments, and the original manifest; the import produces a bundle that validates and preserves the OKF families under `ext.okf`. `tests/test_bundle_roundtrip.py` round-trips the example bundle and checks that titles, links, status, review state, contributors, and attachment references survive.

---

Previous: [F · References](F-References.md) · Index: [README](../../README.md)
