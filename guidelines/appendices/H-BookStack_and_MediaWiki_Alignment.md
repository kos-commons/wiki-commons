# Appendix H · BookStack Portable ZIP and MediaWiki XML Dump Alignment

> **Appendices** · **Status:** Working Draft 0.3 (October 2026)
> Previous: [G · Open Knowledge Format Alignment](G-Open_Knowledge_Format_Alignment.md) · Index: [README](../../README.md)

**In one sentence:** Two widely used export formats, BookStack's Portable ZIP and MediaWiki's XML dump, are mapped onto the Portable Wiki Bundle field by field, with the losses named in both directions and a converter that implements each mapping.

Like everything in this suite, the mappings are optional directions: an engine or an operator *may* use them; nothing here is a requirement on BookStack, MediaWiki, or anyone else.

---

## 1. Why these two

Between them, the two formats represent the two ends of the field. MediaWiki's XML dump is the oldest and most complete wiki export in existence: every revision of every page with its author, timestamp, and comment, in a schema (`export-0.11`) that has been stable for years and that many tools already read. BookStack's Portable ZIP is one of the newest and most deliberately designed: a documented, forward-compatible archive of a book, chapter, or page with its images and attachments, written for "readers, apps, import for other platforms", and explicitly *not* a backup format. One carries history and no files; the other carries files and no history. The bundle has places for both.

## 2. BookStack Portable ZIP

### 2.1 The format

A ZIP archive with `data.json` and a `files/` directory. `data.json` holds `instance` (source identifier and version), `exported_at`, and exactly one of `book`, `chapter`, or `page`. Books contain chapters and direct pages; chapters contain pages; all three carry `tags` (name and optional value). Pages carry `markdown` or `html` (Markdown is CommonMark plus tables and task lists), `images` (gallery or draw.io, in png, jpg, gif, or webp), and `attachments` (a file or a link). Cross-references inside content are written `[[bsexport:page:40]]`, `[[bsexport:image:22]]`, `[[bsexport:attachment:55]]`, `[[bsexport:chapter:2]]`, `[[bsexport:book:8]]`. There is no revision history, no page metadata beyond name, tags, and priority, and the format is documented in BookStack's repository ([Appendix F](F-References.md)).

### 2.2 Mapping to the bundle (import)

| Portable ZIP | Portable Wiki Bundle | Notes |
|---|---|---|
| `book` | `pages/<Book>.md` with `kind: category` and `description`, plus a directory `pages/<Book>/` | The book page carries the book's tags and description |
| `chapter` | `pages/<Book>/<Chapter>.md` with `kind: category`, plus `pages/<Book>/<Chapter>/` | `priority` under `ext.bookstack` |
| `page` | `pages/<Book>/[<Chapter>/]<Page>.md` | `id` becomes `bookstack:page:<id>`; `priority` under `ext.bookstack` |
| `markdown` | the body, converted to the portable profile | Already CommonMark; nothing to change but references |
| `html` (no `markdown`) | the body, converted to Markdown with Pandoc when installed; otherwise kept as HTML with `format: text/html` | Declared in the manifest's `fidelity.degraded` either way |
| `tags` with empty value | `tags: [name]` | |
| `tags` with a value | `tags: [name]` and `properties: {name: value}` | BookStack's name–value tags are closer to properties ([META-8](../09-Metadata_and_Frontmatter.md)) |
| `[[bsexport:page:N]]` in a link destination | `[[Title]]` or `[[Title\|label]]` | Resolved by id to the page's title |
| `[[bsexport:chapter:N]]`, `[[bsexport:book:N]]` | `[[Book/Chapter]]`, `[[Book]]` | Links to the category pages |
| `[[bsexport:image:N]]`, `[[bsexport:attachment:N]]` | relative paths into `attachments/` | Files copied with sidecars; the display name is kept as `original_filename` and, for images, as `alt` |
| attachment `link` | the URL | |
| `instance.version`, `exported_at` | `source.engine_version`, `source.exported_at` in the manifest | |

Fidelity level 2. Dropped: revision history (the format carries none). Degraded: books and chapters, represented as category pages with subdirectories; HTML pages when Pandoc is not available.

### 2.3 Mapping from the bundle (export)

A bundle becomes **one book**. If the bundle's root holds exactly one category page and a directory of the same name (the shape an import produces), that directory is the book; otherwise the bundle's name is the book and its root is the book's content. First-level directories become chapters, and a category page describing a directory supplies the chapter's description and tags rather than becoming a page. Deeper directories are flattened into their chapter with the path kept in the page name. Free links become `[label]([[bsexport:page:N]])`; images in png, jpg, gif, or webp become `images` entries and other files become `attachments`, both referenced as `[[bsexport:...]]`; `tags` become name-only tags and `properties` with scalar values become name–value tags. Redirect pages are not exported (BookStack has no redirects) and are listed in the export report; block identifiers and embeds degrade as for any static target ([Chapter 08 §4](../08-Markup_and_Syntax.md#4-the-degradation-ladder)).

## 3. MediaWiki XML dump

### 3.1 The format

The dump written by `Special:Export` and `dumpBackup.php` follows the `export-0.11` XML schema: a `siteinfo` block (site name, base URL, generator, namespaces) followed by `page` elements, each with `title`, `ns`, `id`, an optional `redirect`, and one or more `revision` elements carrying `id`, `parentid`, `timestamp`, `contributor` (username and id, or `ip`), `minor`, `comment`, `model`, `format`, `text`, and `sha1`. Suppressed fields carry a `deleted` attribute. Uploaded files are not in the dump; `File:` description pages are.

### 3.2 Mapping to the bundle (import)

| XML dump | Portable Wiki Bundle | Notes |
|---|---|---|
| `page/title` | `title`; path `pages/<Title>.md`, with `/` subpages as directories | MediaWiki-style namespace prefixes stay in the title and move into a directory: `Talk:Edit conflicts` → `pages/Talk/Edit conflicts.md` ([MKUP-7](../08-Markup_and_Syntax.md)) |
| `page/ns` | `kind`: talk namespaces → `discussion` (with `about`), `Category` → `category`, `Template` → `template`, `Help` and `Project` → `help`, `MediaWiki` → `system`, `User` → `user` | Namespace names from `siteinfo` go to the manifest's `namespaces` list |
| `page/id` | `id: mw:<id>` and `ext.mediawiki.page_id` | |
| `redirect`, `#REDIRECT [[Target]]` | `kind: redirect`, `redirect: Target`; the target page gains the redirect's title in `aliases` | [NAV-8](../04-Discovery_Navigation_and_Topology.md#nav-8--redirects-and-aliases) |
| `[[Category:X]]` | `tags: [X]` | Removed from the body |
| `[[Target\|label]]`, `[[Target]]` | unchanged | Already the portable form |
| `{{Template\|...}}`, `{{#if:...}}` | a snapshot envelope with `engine="mediawiki"` and the call in `src`, and a visible note as the body | Templates cannot be expanded without the wiki ([EXT-6](../12-Extensibility_Macros_and_Dynamic_Content.md)); on export to MediaWiki the call is restored from `src` |
| wikitext (headings, emphasis, lists, external links, references, images, `<nowiki>`) | Markdown | With Pandoc installed, through its `mediawiki` reader; otherwise through a built-in converter that handles these constructs and keeps tables as wikitext source in envelopes. The manifest records which converter ran |
| each `revision` | a history record: `rev: r<id>`, `parent: r<parentid>`, `at`, `author`, `summary`, `minor`, `content`, `sha256` | Content is the revision converted to the portable form; `sha256` is of that content ([XFER-7](../10-Interchange_and_Portability.md)) |
| `contributor/username` | `author: {id, name}` and an entry in `users.yaml` | |
| `contributor/ip` | `author: {anonymous: true, label: "~ip-<hash>"}` | IP addresses are replaced by a stable pseudonym per address ([PRIV-3](../14-Security_Privacy_and_Trust.md)); `--keep-ips` keeps them |
| `deleted` attributes on `text`, `comment`, `contributor` | `suppressed: [content, summary, author]` with `reason: revision-deleted-in-source` | [HIST-12](../06-Temporal_Design_and_Revision_History.md#hist-12--suppression-without-erasure) |
| `siteinfo/sitename`, `base`, `generator` | manifest `source.name`, `source.url`, `source.engine_version`; `native_format: text/x-wiki` | |

Fidelity level 3 (2 with `--no-history`). Dropped: uploaded media (not in dumps), IP addresses (pseudonymized). Degraded: templates and parser functions (not expanded), wikitext tables when Pandoc is absent, and any construct Pandoc's reader does not know.

### 3.3 Mapping from the bundle (export)

The exporter writes an `export-0.11` document that `Special:Import` accepts: `siteinfo` from the manifest with the canonical namespace table; one `page` per bundle page with the title rebuilt from the path (a first-level directory listed in the manifest's `namespaces` becomes a `Namespace:` prefix), a `redirect` element for redirect pages, and one `revision` per history record carrying content (or a single revision from the current page when there is no history). Markdown becomes wikitext through Pandoc's `mediawiki` writer when installed, reading the portable profile with its wikilink extension so that `[[Target|Label]]` survives; snapshot envelopes whose `engine` is `mediawiki` are replaced by their original `src`, so templates imported from MediaWiki go back as templates; `tags` become `[[Category:...]]` lines; anonymous authors become `ip` contributors with their label; `sha1` is computed as MediaWiki does (base-36 SHA-1 of the text). Without Pandoc the Markdown is written as-is into `text`, which MediaWiki will not render as wikitext; the export report says so.

## 4. Lessons for the guidelines

- **History and files are complementary blind spots.** Each format omits what the other keeps. The bundle's separation of `history/` from `attachments/` means neither omission is a failure of the layout, only of the source.
- **Pseudonymizing addresses is a conversion decision, not a format feature.** Both MediaWiki (through temporary accounts) and this converter arrived at the same answer: a stable pseudonym per address, with the raw address available only on explicit request.
- **Unexpanded templates are survivable.** Keeping the call in an envelope and restoring it on the way back is lossless for a MediaWiki-to-MediaWiki round trip through the bundle, and honest for everyone else.
- **Optional dependencies should be visible.** Whether Pandoc ran is recorded in the manifest and the reports, because the quality of the result depends on it.

## 5. Tooling

```sh
python3 tools/wikicommons.py bookstack import Handbook.zip out/bundle
python3 tools/wikicommons.py bookstack export out/bundle out/handbook.zip
python3 tools/wikicommons.py mediawiki import dump.xml out/bundle            # --no-history, --keep-ips
python3 tools/wikicommons.py mediawiki export out/bundle out/dump.xml --base https://wiki.example.org/wiki
```

Each command writes `import-report.md` or `export-report.md` beside its result ([XFER-13](../10-Interchange_and_Portability.md)) unless `--no-report` is given. Set `WIKI_COMMONS_PANDOC` to a Pandoc binary that is not on the `PATH`. `tests/test_formats.py` round-trips a synthetic Portable ZIP and a synthetic dump, with and without Pandoc.

---

Previous: [G · Open Knowledge Format Alignment](G-Open_Knowledge_Format_Alignment.md) · Index: [README](../../README.md)
