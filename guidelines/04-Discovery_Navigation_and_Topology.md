# 04 · Discovery, Navigation and Topology

> **Part II — The Pattern Language** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [03 · Pattern Language Overview](03-Pattern_Language_Overview.md) · Next: [05 · Authoring and Participation](05-Authoring_and_Participation.md)

**In one sentence:** These sixteen patterns describe how a wiki is *shaped*: how pages are named and addressed, how links weave them into a mesh, how gaps become invitations, and how readers keep their bearings while jumping between ideas.

The pattern format is explained in [03 · Pattern Language Overview](03-Pattern_Language_Overview.md#2-pattern-format). Guidance uses the vocabulary of [00 · Overview and Vision §4](00-Overview_and_Vision.md#4-guidance-language).

---

## NAV-1 · Page as the Unit of Address

**Also known as:** everything is a page; one name, one place.
**Maturity:** Established.

**Context.** Readers, writers, and other systems all need a way to point at a piece of knowledge.

**Tension.** Human-readable addresses (titles) are memorable and self-describing but change when a page is renamed. Opaque identifiers are stable but meaningless to people. Block-based tools want to address something smaller than a page; hierarchical tools want the address to encode the location.

**Guidance.**
- Every page **should** be addressable by a human-readable title, and the title **should** be visible in the page's URL in a readable, properly encoded form (see [I18N](13-Accessibility_Internationalization_and_Web_Standards.md) for non-Latin titles).
- Engines are **encouraged** to also give each page a stable identifier that survives renames ([NAV-9](#nav-9--stable-identity-beneath-the-title)).
- Where content is finer-grained than a page (sections, blocks, lines), those parts **should** be addressable *within* the page's address rather than instead of it ([NAV-10](#nav-10--section-anchors-and-block-addresses)).
- Addresses **should** remain valid over time: a renamed, moved, or merged page **should** keep answering at its old address through a redirect or an identifier-based lookup ([NAV-8](#nav-8--redirects-and-aliases)).

**Observed in.** Classic engines address pages by title (`/wiki/Title`, `?id=ns:page`, `?Group/Page`), and most keep working after renames by leaving a redirect. Enterprise and block-based tools address pages by numeric or UUID identifiers with a slug appended for readability; renaming never breaks the link but the URL is unreadable without the slug. Single-file wikis address tiddlers by title within one document, using URL fragments for permalinks. Federated Wiki addresses a page by *site plus slug*, so the same slug can exist, legitimately different, on many sites.

**Interchange.** In a Portable Wiki Bundle ([10](10-Interchange_and_Portability.md)) a page's path within `pages/` carries its namespace and slug; `title` and `id` travel in frontmatter so that importers can rebuild both kinds of address.

**Related.** NAV-2, NAV-8, NAV-9, NAV-10; PR-7.

---

## NAV-2 · Free Links

**Also known as:** wikilinks, bracket links, `[[double brackets]]`, BracketName.
**Maturity:** Established.

**Context.** A writer wants to connect the sentence they are writing to another page without leaving the flow of writing.

**Tension.** Links should be effortless to type and should read naturally in the source text. Early wikis used CamelCase "WikiWords" so that a link needed no syntax at all, but that produced accidental links, awkward titles, and nothing at all for languages without word spacing or capital letters, such as Japanese. Explicit bracket syntax solved this at the cost of two keystrokes.

**Guidance.**
- Writers **should** be able to link to a page by its title alone, without knowing its URL, identifier, or location in any hierarchy.
- The `[[Title]]` form is **recommended** as the shared syntax for free links in Markdown-based engines and for interchange. It is the most widely recognized wiki convention across every engine generation ([Appendix B](appendices/B-Syntax_Crosswalk.md)).
- A labelled form **should** be available. The order *target first, label second* (`[[Title|shown text]]`) is **recommended** for new engines and for interchange, because it is the majority convention; engines that use the reverse order are **encouraged** to document it and to declare it in their exports ([MKUP-6](08-Markup_and_Syntax.md)).
- Link resolution **should** be tolerant: case differences in the first character, spaces versus underscores or hyphens, and Unicode normalization differences **should** resolve to the same page where the engine's naming rules allow. Engines **should** document their normalization rules.
- Engines **may** also support CamelCase WikiWords, URL-style Markdown links, or single-bracket links, but **should** be able to express each of them as a free link on export.
- Autocompletion of existing titles while typing a link is **encouraged**; it reduces duplicates and typos without constraining the writer.

**Observed in.** UseModWiki introduced and named `[[free links]]` in 2001, and Wikipedia, which ran on UseModWiki until January 2002, carried the form into MediaWiki; YukiWiki arrived at the same bracket convention independently for Japanese text at about the same time. `[[Title]]` is now native to MediaWiki, DokuWiki, MoinMoin, PmWiki, PukiWiki, Trac, Redmine, Zim, ikiwiki, Gollum-based wikis, TiddlyWiki, Obsidian, Logseq, Foam, Dendron, Silverbullet, and many others, with differing label order and separators (see Appendix B); a few engines use single brackets (JSPWiki, Scrapbox / Cosense) or double parentheses (Tiki), and Gitit reuses Markdown link syntax with an empty URL. CamelCase remains supported alongside brackets in several classic engines. Scrapbox / Cosense uses single brackets, `[Title]`, and treats hashtags as links. Block editors such as Notion and Outline offer `[[` or `@` as a trigger that inserts a page mention object rather than text markup. Japanese wikis adopted bracket links early precisely because CamelCase could not serve Japanese text.

**Interchange.** Free links are the single most important thing to preserve in any export. Chapter 08 defines the portable form and its resolution rules; Appendix B maps native forms to it.

**Related.** NAV-3, NAV-6, NAV-8, NAV-13; PR-7, PR-10.

---

## NAV-3 · Dangling Link as Invitation

**Also known as:** red link, question-mark link, missing link, unresolved link, wanted page.
**Maturity:** Established.

**Context.** A writer links to a page that does not exist yet, either deliberately (to reserve a topic) or because the page has not been written.

**Tension.** A dangling link is simultaneously an error (nothing is there) and a feature (someone should write it). Hiding it loses the invitation; rendering it as a normal link disappoints the reader; refusing to save it blocks the writer. The invitation works: on Wikipedia, most new articles are created shortly after a link to them appears (Spinellis and Louridas, 2008).

**Guidance.**
- Links to pages that do not exist **should** be saved, rendered, and visibly distinguished from links to existing pages. The distinction **should not** rely on colour alone ([A11Y](13-Accessibility_Internationalization_and_Web_Standards.md)).
- Following a dangling link **should** lead directly to creating the page, with the title prefilled.
- Dangling link targets **should** be aggregated into a "wanted pages" view ranked by how many pages want them ([NAV-15](#nav-15--health-views-orphans-wanted-dead-ends)).
- Engines that create a page the moment it is referenced are **encouraged** to keep empty pages visibly distinguishable from pages with content, so the invitation is not lost.
- Engines that cannot represent a link to a nonexistent page (because links are object references) are **encouraged** to offer an equivalent affordance, such as a "create page from mention" action and a list of unresolved mentions.

**Observed in.** The original WikiWikiWeb appended a question mark to an unwritten WikiWord; UseModWiki, PukiWiki, TWiki and Foswiki, PmWiki, and Trac kept that convention. MediaWiki introduced the red link, now the best-known rendering. DokuWiki, MoinMoin, and TiddlyWiki each style missing links distinctly (red, dashed, italic). Obsidian dims unresolved links and creates the note on click. Logseq creates a page on reference. Scrapbox / Cosense shows links to empty pages in a distinct colour, lists them under the page, and still counts them when computing related pages, so an unwritten page already connects the pages that mention it. Federated Wiki searches the neighbourhood of federated sites for a missing page before offering to create it. Notion links can only point at existing pages, so the pattern is absent there; Confluence historically listed "undefined pages" per space.

**Interchange.** A dangling link exports as an ordinary free link. Importers **should not** strip or rewrite links whose target is missing from the bundle; they **should** keep them dangling.

**Related.** NAV-2, NAV-5, NAV-15; PR-5.

---

## NAV-4 · Backlinks (What Links Here)

**Also known as:** incoming links, references, linked references, bidirectional links.
**Maturity:** Established.

**Context.** A reader on a page wants to know where else this topic is discussed; a writer wants to know what depends on the page before changing or renaming it.

**Tension.** Backlinks are derived data: cheap to compute, expensive to keep consistent, and potentially noisy on hub pages. Showing them in the page body competes with the content; hiding them behind a menu loses the serendipity.

**Guidance.**
- Every page **should** offer a list of pages that link to it, reachable from the page itself.
- Backlinks **should** be computed by the engine from the content, not maintained by hand, and **should** update when pages change.
- Showing the linking context (the sentence or block containing the link) is **encouraged**; it is what turns a backlink list into a reading aid.
- "Unlinked mentions" (pages that contain the title as plain text without linking) **may** be offered as a secondary list with a one-step "link it" action.
- Backlinks **should** be available through the API ([API-5](11-APIs_and_Discovery.md)).

**Observed in.** The first wiki implemented backlinks as a full-text search triggered by clicking the page title; MoinMoin kept that gesture. MediaWiki offers *What links here* as a special page. DokuWiki has a backlinks action; PukiWiki and TiddlyWiki list referring pages in the page footer or an info tab. Obsidian, Logseq, and Roam made backlinks with context a central panel and popularized the phrase "bidirectional links" in 2019 to 2020. Scrapbox / Cosense renders linked pages as a grid under the page. Notion added a backlinks list at the top of pages in 2020. Confluence exposes incoming links in its page information view.

**Interchange.** Backlinks are not exported as content; they are re-derived on import. A bundle **may** include a precomputed link graph for convenience ([XFER-9](10-Interchange_and_Portability.md)), but it is advisory.

**Related.** NAV-2, NAV-12, NAV-14; PR-10, PR-11.

---

## NAV-5 · Search or Create

**Also known as:** go-or-create, quick switcher, "create this page".
**Maturity:** Established.

**Context.** Someone has a topic in mind and does not know whether a page for it exists.

**Tension.** Creating a page that already exists under a slightly different name produces duplicates; searching first and creating second is two separate tasks in many interfaces. Making creation too easy can fragment knowledge; making it too hard loses it.

**Guidance.**
- The search affordance **should** offer to create a page when no exact match exists, carrying the typed text over as the title.
- Visiting the address of a nonexistent page **should** present a creation affordance rather than a bare error.
- Before creating, the engine **should** show similar existing titles (fuzzy and alias matches) so that the writer can choose to extend rather than duplicate ([PR-9](02-Guiding_Principles.md); Cunningham's *Convergent*).
- A keyboard-driven "jump to or create" command is **encouraged** in editors and desktop tools.

**Observed in.** MediaWiki's search page offers "Create the page ... on this wiki" and nonexistent titles show a creation prompt. DokuWiki's "This topic does not exist yet" message carries a create action. Obsidian's quick switcher, Logseq's search, and Scrapbox / Cosense's title entry all create on Enter when nothing matches. Enterprise tools generally separate search from a "Create" button but prefill templates.

**Interchange.** Not applicable to data; the pattern depends on NAV-2 and NAV-8 (aliases) to work well after import.

**Related.** NAV-2, NAV-3, NAV-8, NAV-15; PR-5.

---

## NAV-6 · Flat Names, Optional Hierarchy

**Also known as:** namespaces, subpages, folders, spaces, paths, groups.
**Maturity:** Established.

**Context.** A wiki grows past the point where a flat list of titles is comfortable; some pages belong together; some teams want their own area.

**Tension.** Hierarchy aids orientation, bulk operations, and access scoping, but it forces a decision ("where does this go?") before anything can be written, and it tends to encode one organization's view at one point in time. The original wiki deliberately used a flat space so that a name needed no context to be understood.

**Guidance.**
- A page **should** be creatable and linkable by title without first placing it in a hierarchy. Hierarchy, where offered, **should** be scaffolding rather than a prerequisite.
- When a hierarchy exists, links **should** be resolvable both by full path and, where unambiguous, by bare title; the engine **should** document its disambiguation rule (for example, "same namespace first, then shortest path").
- For interchange, `/` is **recommended** as the path separator. Engines using `:` or `.` natively **should** map them to `/` on export and back on import ([MKUP-7](08-Markup_and_Syntax.md)).
- Moving a page within the hierarchy **should not** break inbound links ([NAV-8](#nav-8--redirects-and-aliases), [HIST-6](06-Temporal_Design_and_Revision_History.md#hist-6--rename-preserves-history)).
- Hierarchies and graphs are complementary. Engines are **encouraged** to offer tags, links, and backlinks alongside any tree, so that a page can belong to several contexts at once.

**Observed in.** MediaWiki combines fixed namespaces (`Talk:`, `User:`, `Category:`) with optional `/` subpages. DokuWiki namespaces (`ns:page`) and PmWiki groups (`Group/Page`) map directly to directories. PukiWiki and Growi use `/`-separated hierarchical names as a first-class feature. Dendron makes dotted hierarchy (`project.area.topic`) the core model and auto-creates stub parents. Logseq offers `/` namespaces as pages. BookStack imposes a strict shelf, book, chapter, page structure; Confluence and Notion use spaces with nested page trees; XWiki nests pages arbitrarily. Obsidian uses folders but resolves links by bare filename across the whole vault. Scrapbox / Cosense and TiddlyWiki deliberately have no hierarchy at all, relying on links and tags.

**Interchange.** The directory structure of `pages/` in a bundle carries hierarchy; engines without hierarchy **may** flatten on import, keeping the original path in metadata so that nothing is lost.

**Related.** NAV-1, NAV-7, NAV-11; PR-10; Cunningham's *Unified*.

---

## NAV-7 · Tags and Categories

**Also known as:** labels, categories, hashtags, keywords.
**Maturity:** Established.

**Context.** Pages belong to several topics at once; a tree cannot express this.

**Tension.** Free-form tags are easy to add and quickly become inconsistent (`api`, `API`, `apis`). Curated category trees are consistent and quickly become bureaucratic. Some engines make tags into pages; others make them metadata.

**Guidance.**
- Pages **should** be taggable with any number of free-form labels, and each label **should** be addressable as a page or view listing its members.
- Tags **should** be exportable as a list of strings in page metadata (`tags:`), regardless of how the engine stores them ([META-5](09-Metadata_and_Frontmatter.md)).
- Hierarchical categories **may** be offered; for interchange they **should** be expressible as tags, with a documented convention for the hierarchy (for example, `parent/child`).
- Engines are **encouraged** to help convergence with autocompletion, merge and rename tools, and "similar tag" hints, rather than enforcing a controlled vocabulary.
- Making tags into pages (so that a tag can carry a description, links, and its own history) is **encouraged**; it is the oldest wiki approach and still one of the best.

**Observed in.** The first wiki and MoinMoin used "Category" pages linked from members, so a backlink list *was* the category. MediaWiki's `[[Category:X]]` creates category pages with member lists and category hierarchies. TiddlyWiki's tags are tiddlers and drive most of its structure. Obsidian supports inline `#tags` and a `tags:` property; Logseq and Scrapbox / Cosense treat `#tag` as a link to a page. Confluence labels, BookStack name–value tags, Wiki.js tags, and Notion multi-select properties are metadata rather than pages.

**Interchange.** `tags:` in frontmatter. Category hierarchies that cannot be expressed as tags **should** be preserved in the bundle as pages (the category pages themselves) so that structure survives.

**Related.** NAV-4, NAV-6; Chapter 09.

---

## NAV-8 · Redirects and Aliases

**Also known as:** synonyms, moved pages, "redirected from".
**Maturity:** Established.

**Context.** Titles evolve. A page is renamed, two pages are merged, or a topic is known by several names.

**Tension.** Links by title break when titles change. Links by identifier do not break but are unreadable. Rewriting every link on rename is thorough but invisible to authors and impossible across wiki boundaries.

**Guidance.**
- Renaming or merging a page **should** keep the old title working, by a redirect, an alias, identifier-based resolution, or link rewriting. Engines **should** document which approach they use.
- Redirects **should** be visible to the reader ("redirected from ...") and editable, so that a redirect can be turned back into a page.
- Aliases **should** be first-class metadata (`aliases:`) so that free links to any alias resolve ([META-4](09-Metadata_and_Frontmatter.md)).
- Engines **should** detect redirect chains and loops and **should** offer a report of broken and double redirects ([NAV-15](#nav-15--health-views-orphans-wanted-dead-ends)).
- Engines that rewrite links on rename are **encouraged** to record the rename in history and to still accept the old title as an alias, so that external links and other wikis keep working.

**Observed in.** MediaWiki's `#REDIRECT [[Target]]` pages with the "redirected from" notice and *Double redirects* report are the reference implementation. MoinMoin and PmWiki have redirect directives; DokuWiki uses a plugin. Obsidian resolves links through an `aliases` property; Logseq merges pages through `alias::`. Scrapbox / Cosense, Obsidian, and Logseq rewrite links across the project on rename. Confluence and Notion link by identifier, so renames are harmless within the tool.

**Interchange.** A redirect exports as a page whose frontmatter carries `redirect:` and no body; aliases export as `aliases:`. Importers lacking redirects **may** merge aliases into the target page's metadata.

**Related.** NAV-2, NAV-9, HIST-6.

---

## NAV-9 · Stable Identity Beneath the Title

**Also known as:** page ID, UUID, permanent identifier.
**Maturity:** Emerging.

**Context.** Pages are renamed, merged, split, moved between wikis, and referenced from outside systems.

**Tension.** Titles are the natural human address but are mutable. Identifiers are immutable but meaningless. File-based tools equate identity with path, which is simple but fragile.

**Guidance.**
- Engines are **encouraged** to assign each page an identifier that never changes and to expose it in exports (`id:` in frontmatter) and APIs.
- UUIDs (version 4 or the time-ordered version 7) are **recommended** for interchange because they can be minted without coordination; engine-local numeric IDs **may** be exported alongside.
- Identifiers **should not** be the only address; titles and paths remain primary for people.
- Block-based engines **should** apply the same idea to blocks ([NAV-10](#nav-10--section-anchors-and-block-addresses)).
- Importers **should** preserve incoming identifiers where their model allows, and otherwise keep them as metadata, so that a round-trip can re-associate pages.

**Observed in.** MediaWiki pages have stable numeric IDs reachable through `curid`; Wikidata assigns Q-identifiers to concepts. Confluence and Notion URLs are identifier-based with a title slug. Logseq blocks carry UUIDs; Dendron notes carry an `id` in frontmatter. Growi stores a database identifier beside the path. Obsidian, DokuWiki, and TiddlyWiki identify by path or title, relying on link rewriting or plugins when titles change.

**Interchange.** `id` in page frontmatter ([Appendix C](appendices/C-Portable_Page_Metadata_Reference.md)); block identifiers as `^id` suffixes ([MKUP-9](08-Markup_and_Syntax.md)).

**Related.** NAV-1, NAV-8, NAV-10, HIST-6.

---

## NAV-10 · Section Anchors and Block Addresses

**Also known as:** fragment links, heading anchors, block references, line permalinks.
**Maturity:** Emerging.

**Context.** A reader wants to point at *this paragraph*, not the whole page; a writer wants to quote or embed a specific block.

**Tension.** Heading-based anchors are readable but change when headings are edited. Block identifiers are stable but must be generated and stored. Addressing below the page level pulls document-based engines toward the block paradigm.

**Guidance.**
- Headings **should** receive predictable anchors derived from their text, with duplicates disambiguated deterministically, and `[[Page#Heading]]` **should** link to them.
- Engines with a block or line model **should** expose stable block identifiers and accept `[[Page#^id]]` as the portable link form ([MKUP-9](08-Markup_and_Syntax.md)).
- Document-based engines **may** support block identifiers as an optional `^id` suffix on a paragraph or list item, which is invisible enough to ignore and stable enough to link.
- Rendered HTML **should** carry `id` attributes on headings and identified blocks, so that ordinary URL fragments work ([MKUP-12](08-Markup_and_Syntax.md)).

**Observed in.** MediaWiki and DokuWiki link to headings with `#Section`. Obsidian introduced `^block-id` suffixes and `[[Page#^id]]` references; Logseq and Roam use `((uuid))` references to blocks that carry an `id::` property. Notion exposes block links as URL fragments. Scrapbox / Cosense gives every line a permalink; Federated Wiki gives every story item an identifier.

**Interchange.** Heading anchors need no extra data. Block identifiers travel as `^id`; importers without block support **should** keep the suffix as text or metadata rather than dropping it, so that references remain resolvable later.

**Related.** NAV-9, NAV-16; Chapter 08.

---

## NAV-11 · Spatial Orientation

**Also known as:** where am I, breadcrumbs, trail, lineup, story river.
**Maturity:** Established.

**Context.** Readers follow links several hops deep and need to know where they are, how they got there, and how to get back.

**Tension.** Hierarchical breadcrumbs only work when there is a hierarchy. History trails show the path but not the place. Showing too much context crowds the content.

**Guidance.**
- Every page **should** show its own title prominently and, where a hierarchy exists, its place in it.
- Engines are **encouraged** to offer a *trail* of recently visited pages distinct from the browser history, because wiki reading is non-linear.
- Internal, external, dangling, and interwiki links **should** be distinguishable, so that a reader knows whether following a link leaves the wiki.
- Core affordances (search, edit, history, discussion) **should** be findable from the same place on every page. Their position is a design choice; their presence is the pattern.
- Readers **should** be able to tell which wiki or site they are on, which matters in farms, federations, and embedded contexts.

**Observed in.** DokuWiki offers both a visited trail and a hierarchical breadcrumb. MediaWiki shows subpage breadcrumbs and a fixed tab bar. Enterprise tools rely on a persistent page tree and breadcrumbs. TiddlyWiki's "story river" stacks opened tiddlers vertically; Federated Wiki's "lineup" lays visited pages out horizontally so the reading path itself becomes the navigation. Scrapbox / Cosense orients by showing related pages beneath the current one.

**Interchange.** Not applicable; orientation is rebuilt by the importing engine from hierarchy and links.

**Related.** NAV-6, NAV-13, NAV-14.

---

## NAV-12 · Related Pages and the Two-Hop Neighborhood

**Also known as:** 2-hop links, see also, more like this, co-citation.
**Maturity:** Emerging.

**Context.** The most valuable page for a reader is often one they did not know to search for.

**Tension.** Hand-maintained "See also" lists go stale. Recommendation algorithms can be opaque and can favour popularity over relevance. Showing too many related pages becomes noise.

**Guidance.**
- Engines are **encouraged** to compute related pages from the link graph (shared links, co-citation, shared tags) and to show them near the page.
- The two-hop neighbourhood is a particularly cheap and effective relation: pages that link to the same pages this page links to. Engines **may** show it directly, as line-based wikis do.
- Related pages **should** be explainable ("related because both link to X"), so that readers can trust and learn from the suggestion.
- Hand-written "See also" sections remain valuable and **should** be preserved as ordinary links.

**Observed in.** Scrapbox / Cosense built its navigation around two-hop links displayed under every page: pages that share a link or hashtag with the current page are related, and so are the pages one hop beyond each link target, even when that target does not exist yet. PukiWiki lists related pages in the footer. MediaWiki offers "Related articles" through an extension using search similarity. Obsidian and Logseq surface unlinked mentions and local graphs. Most enterprise tools offer search-based recommendations rather than graph-based ones.

**Interchange.** Derived data; not exported. Depends on link preservation.

**Related.** NAV-4, NAV-14; PR-11.

---

## NAV-13 · Interwiki Links

**Also known as:** intermap, prefixed links, sister sites, cross-wiki links.
**Maturity:** Established.

**Context.** A wiki wants to link to pages in other wikis as easily as to its own.

**Tension.** Full URLs are portable but long and brittle. Prefix shortcuts (`[[wikipedia:Topic]]`) are concise but depend on a map that each wiki maintains separately; there is no shared registry.

**Guidance.**
- Engines **should** support prefixed links to configured external wikis and **should** publish their interwiki map in a machine-readable form ([API-9](11-APIs_and_Discovery.md)).
- The prefix form **should** be preserved in the source on export, and the bundle manifest **should** carry the map, so that an importer can either keep the shortcuts or expand them to full URLs ([XFER-6](10-Interchange_and_Portability.md)).
- Interlanguage links (the same topic in another language edition) are a special case worth treating explicitly ([I18N-6](13-Accessibility_Internationalization_and_Web_Standards.md)).
- *Exploratory:* a community-maintained registry of common prefixes would benefit every engine; see [17 · Roadmap](17-Roadmap_and_Open_Questions.md).

**Observed in.** MediaWiki's interwiki table and interlanguage links, DokuWiki's `interwiki.conf` with `[[wp>Topic]]`, MoinMoin's and PmWiki's InterMap, Trac's InterWiki, and PukiWiki's InterWikiName page all implement the idea from the same early Meatball proposal. Federated Wiki resolves bare links across a neighbourhood of sites through their published sitemaps, which is interwiki without prefixes. Most modern note tools use plain URLs.

**Interchange.** Manifest `interwiki:` map plus preserved prefixes in source.

**Related.** NAV-2, COLL-13; Chapter 11.

---

## NAV-14 · Graph as a Lens, Not a Map

**Also known as:** graph view, local graph, link visualization.
**Maturity:** Emerging.

**Context.** The wiki's link structure is interesting in itself; people want to see it.

**Tension.** Global graphs of thousands of nodes are beautiful and nearly useless for navigation. Local graphs (a page and its neighbours) are useful but duplicate the backlink list. Graphs are inaccessible to many users unless an alternative is offered.

**Guidance.**
- Graph views are **optional**. Where offered, local, filterable views centred on the current page are **encouraged** over global overviews.
- A graph view **should** have a textual equivalent (the backlink and outgoing link lists) so that no information is available only visually ([A11Y-4](13-Accessibility_Internationalization_and_Web_Standards.md)).
- Graph data **may** be exposed through the API as a plain edge list, which also serves link-health tooling ([NAV-15](#nav-15--health-views-orphans-wanted-dead-ends)).

**Observed in.** Obsidian, Logseq, and Roam made graph views a signature feature; TiddlyWiki has graph plugins; Semantic MediaWiki offers visualizations of structured relations. Scrapbox / Cosense deliberately omits a graph view in favour of in-context related pages.

**Interchange.** Edge lists **may** be included in a bundle as advisory data.

**Related.** NAV-4, NAV-12.

---

## NAV-15 · Health Views: Orphans, Wanted, Dead Ends

**Also known as:** maintenance reports, special pages, wanted pages, lonely pages, broken redirects.
**Maturity:** Established.

**Context.** A wiki accumulates structural gaps: pages nobody links to, titles many pages want, pages that lead nowhere, redirects to nothing.

**Tension.** Gaps are normal and even healthy (they are where the next contributions happen), but invisible gaps cannot be filled. Reports that nobody looks at are wasted; reports that shame contributors are harmful.

**Guidance.**
- Engines **should** provide, at minimum, lists of **wanted pages** (dangling link targets, ranked by inbound links), **orphaned pages** (no inbound links), **dead-end pages** (no outgoing links), and **broken or double redirects**.
- These views **should** be framed as opportunities ("pages waiting to be written") rather than errors.
- Each entry **should** link to the action that resolves it (create, link, fix redirect).
- The same data **should** be available through the API so that communities can build dashboards and bots ([API-5](11-APIs_and_Discovery.md)).

**Observed in.** MediaWiki's special pages (*Wanted pages*, *Lonely pages*, *Dead-end pages*, *Double redirects*, *Broken redirects*, *Uncategorized pages*) are the canonical set. TiddlyWiki ships "Missing" and "Orphans" tabs. DokuWiki and Obsidian rely on plugins; Obsidian's graph marks unresolved links. Few enterprise tools offer structural health views at all.

**Interchange.** Derived; rebuilt on import.

**Related.** NAV-3, NAV-4, NAV-8; PR-5, PR-12.

---

## NAV-16 · Transclusion with Provenance

**Also known as:** embedding, include, excerpt, synced block, template expansion.
**Maturity:** Established.

**Context.** The same content belongs on several pages: a definition, a warning, a table, a shared section.

**Tension.** Copying creates drift; transcluding creates hidden dependencies. Readers of a page containing transcluded content may not know where it comes from or how to edit it. Parameterized transclusion (templates) is powerful and almost entirely engine-specific.

**Guidance.**
- Engines offering transclusion **should** make provenance visible: where the content comes from, and a way to edit it at its source.
- The portable syntax `![[Page]]`, `![[Page#Heading]]`, and `![[Page#^id]]` is **recommended** for simple transclusion in Markdown-based engines ([MKUP-10](08-Markup_and_Syntax.md)).
- Engines **should** detect and stop transclusion cycles gracefully.
- On export, transcluded content **should** either remain a reference (when the source is in the same bundle) or be snapshotted in place with a marker recording its origin ([EXT-4](12-Extensibility_Macros_and_Dynamic_Content.md)). Parameterized templates **should** be snapshotted, since their logic does not travel.
- Engines **may** go further and show, on the source page, where it is transcluded (a special kind of backlink).

**Observed in.** MediaWiki templates (`{{Name|param=...}}`) and page transclusion (`{{:Page}}`), with labelled section transclusion by extension, are the most elaborate system. TiddlyWiki's `{{Tiddler}}` transclusion is core to its design. Obsidian `![[...]]` embeds, Logseq `{{embed}}` blocks, Roam block embeds, Notion synced blocks, Confluence *Include Page* and *Excerpt* macros, and DokuWiki's include plugin all realize the idea. Federated Wiki does not transclude: it *forks* a page with a journal entry recording the source, which is provenance by copying.

**Interchange.** Keep as `![[...]]` when the target travels; otherwise snapshot with a provenance envelope. Never export a bare hole.

**Related.** NAV-10, COLL-13; Chapter 12.

---

Previous: [03 · Pattern Language Overview](03-Pattern_Language_Overview.md) · Next: [05 · Authoring and Participation](05-Authoring_and_Participation.md)
