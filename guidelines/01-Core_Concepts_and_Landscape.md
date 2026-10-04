# 01 · Core Concepts and Landscape

> **Part I — Foundations** · **Status:** Working Draft 0.4 (October 2026)
> Previous: [00 · Overview and Vision](00-Overview_and_Vision.md) · Next: [02 · Guiding Principles](02-Guiding_Principles.md)

**In one sentence:** This chapter names the concepts the rest of the suite relies on, maps three overlapping generations of wiki engines, shows what nearly all of them share and where they split, and draws lessons from twenty years of attempts to standardize them.

A fuller engine-by-engine survey is in [Appendix A](appendices/A-Wiki_Engine_Landscape.md); a syntax comparison is in [Appendix B](appendices/B-Syntax_Crosswalk.md); definitions are collected in [Appendix E](appendices/E-Glossary.md).

---

## 1. What a wiki is

Ward Cunningham, who built the first wiki in 1995, later described it as "the simplest online database that could possibly work". The first book on the subject put the social half plainly: a wiki "invites all users—not just experts—to edit any page or to create new pages within the wiki website", and is "*not* a carefully crafted site created by experts and professional writers and designed for casual visitors", but one that "seeks to involve the typical visitor/user in an ongoing process of creation and collaboration" (Leuf and Cunningham, 2001).

Three decades of engines have varied almost everything about how that is done. What they have not varied is a small conceptual core:

- There are **pages**, each with a **title** that is also its address.
- Pages **link** to one another by title, including to pages that do not exist yet.
- Every page has a **history**, so change is cheap and reversible.
- The whole is **observable**: anyone can see what changed.

Everything else in this suite is an elaboration of those four sentences.

## 2. Core concepts

The vocabulary below is used throughout. Terms are defined conceptually, not as a data model; engines realize them in very different structures.

| Concept | Meaning | Where it is developed |
|---|---|---|
| **Page** | The unit of address and of history. In block-based engines a page is a container of blocks; in line-based engines, of lines; in single-file wikis, a "tiddler"; in Federated Wiki, a "story" with a "journal". | [NAV-1](04-Discovery_Navigation_and_Topology.md#nav-1--page-as-the-unit-of-address) |
| **Title** | The human-readable name of a page, used in links and URLs. | [NAV-1](04-Discovery_Navigation_and_Topology.md#nav-1--page-as-the-unit-of-address), [MKUP-5](08-Markup_and_Syntax.md) |
| **Identifier** | A stable, opaque name for a page or block that survives renames. | [NAV-9](04-Discovery_Navigation_and_Topology.md#nav-9--stable-identity-beneath-the-title), [META-2](09-Metadata_and_Frontmatter.md) |
| **Free link** | A link written as the target's title, conventionally `[[Title]]`, resolved by the engine. | [NAV-2](04-Discovery_Navigation_and_Topology.md#nav-2--free-links), [MKUP-4](08-Markup_and_Syntax.md) |
| **Dangling link** | A free link whose target does not exist yet. Also "red link", "missing link", "wanted page". | [NAV-3](04-Discovery_Navigation_and_Topology.md#nav-3--dangling-link-as-invitation) |
| **Backlink** | The inverse of a link: the set of pages that link to a given page. | [NAV-4](04-Discovery_Navigation_and_Topology.md#nav-4--backlinks-what-links-here) |
| **Anchor** | An address within a page: a heading or a block identifier. | [NAV-10](04-Discovery_Navigation_and_Topology.md#nav-10--section-anchors-and-block-addresses) |
| **Namespace / hierarchy** | Optional grouping of pages by prefix or path; also "space", "folder", "group", "web", "book". | [NAV-6](04-Discovery_Navigation_and_Topology.md#nav-6--flat-names-optional-hierarchy) |
| **Tag / category** | A many-to-many label on pages, often itself a page. | [NAV-7](04-Discovery_Navigation_and_Topology.md#nav-7--tags-and-categories) |
| **Redirect / alias** | A title that resolves to another page. | [NAV-8](04-Discovery_Navigation_and_Topology.md#nav-8--redirects-and-aliases) |
| **Interwiki link** | A prefixed link into another wiki, resolved through a map. | [NAV-13](04-Discovery_Navigation_and_Topology.md#nav-13--interwiki-links) |
| **Transclusion** | Showing the content of one page (or part of it) inside another, live. | [NAV-16](04-Discovery_Navigation_and_Topology.md#nav-16--transclusion-with-provenance) |
| **Template** | A page designed to be transcluded with parameters, or used as starter content. | [AUTH-6](05-Authoring_and_Participation.md#auth-6--starters-and-templates), [EXT-6](12-Extensibility_Macros_and_Dynamic_Content.md) |
| **Macro / directive** | A construct in page source that the engine replaces with generated content. | [Chapter 12](12-Extensibility_Macros_and_Dynamic_Content.md) |
| **Revision** | One saved state of a page, with time, author, and summary. | [HIST-1](06-Temporal_Design_and_Revision_History.md#hist-1--non-destructive-history) |
| **Diff** | The difference between two revisions. | [HIST-2](06-Temporal_Design_and_Revision_History.md#hist-2--diff-as-a-first-class-view) |
| **Attribution** | The record of who made which change. | [HIST-4](06-Temporal_Design_and_Revision_History.md#hist-4--attribution-per-revision) |
| **Discussion** | Conversation about a page kept beside, not inside, it. | [COLL-3](07-Collaboration_Awareness_and_Governance.md#coll-3--talk-beside-content) |
| **Recent changes** | The wiki-wide chronological list of revisions. | [COLL-1](07-Collaboration_Awareness_and_Governance.md#coll-1--recent-changes) |
| **Attachment** | A file (image, document) stored with the wiki and referenced from pages. | [AUTH-7](05-Authoring_and_Participation.md#auth-7--effortless-media), [XFER-4](10-Interchange_and_Portability.md) |
| **Block** | A sub-page unit with its own identity (paragraph, list item, line, tiddler item). | [MKUP-9](08-Markup_and_Syntax.md), [§6](#6-the-document-and-block-paradigms) |
| **Structured data** | Typed properties attached to pages: infobox fields, forms, database columns, classes. | [META-8](09-Metadata_and_Frontmatter.md), [XFER-11](10-Interchange_and_Portability.md) |
| **Bundle** | A portable export: pages, attachments, and optional history and discussions with a manifest. | [Chapter 10](10-Interchange_and_Portability.md) |

## 3. Three generations, overlapping

Wiki engines are often sorted into "traditional wikis" and "modern knowledge bases". The reality is a continuum with three broad generations, and the generations overlap: several of the oldest engines have adopted the newest ideas, and several of the newest have rediscovered the oldest.

### 3.1 Classic wikis (1995 to roughly 2005)

The WikiWikiWeb (1995, Perl) was cloned within weeks. The classic generation includes UseModWiki (1999, which named "free links" in 2001 and ran Wikipedia in its first year), MoinMoin (2000), TWiki (1998), PmWiki (2002), MediaWiki (2002), DokuWiki (2004), JSPWiki, Trac's wiki (2004), and in Japan YukiWiki and its PHP descendant PukiWiki (2001), whose bracket links answered a language that CamelCase could not serve. TiddlyWiki (2004) belongs here by age but is unlike anything else: a wiki inside a single HTML file.

Shared traits: pages are text in an engine-specific markup; rendering happens on the server; links are CamelCase or `[[brackets]]`; missing pages are marked with a question mark or a red link; every page has a revision history with diffs; RecentChanges is the social hub; storage is flat files or a relational database in PHP, Perl, or Python. Macros arrive early and diverge immediately.

Most of these engines are still maintained in 2026. MediaWiki ships two release lines a year and now serves an OpenAPI description of its REST API; DokuWiki added JSON-RPC with a generated OpenAPI document in 2024; PmWiki, ikiwiki, Foswiki, Gitit, JSPWiki, and Zim all released in 2026. Age is not obsolescence.

### 3.2 Transitional wikis and knowledge bases (roughly 2005 to 2018)

The second generation added structure, services, and polish. XWiki (2004) and Foswiki pursued the "structured wiki" or "wiki application" idea: pages carry typed objects and forms, and macros query them. Confluence (2004) brought the wiki into the enterprise and, in 2011, abandoned its wiki markup for a visual editor, a widely cited portability regression. Tiki became an all-in-one groupware. Git-backed wikis appeared: ikiwiki (2006) compiling to static HTML, Gitit (2008) on Pandoc, Gollum (2010) powering the GitHub wiki, and the wikis of GitLab, Gitea, Azure DevOps, and Bitbucket, each a git repository of Markdown files.

Markdown spread from these into the self-hosted "wiki as an application" generation: Wiki.js (2016), BookStack (2015), Outline (2017), Growi (2017, from Crowi), Otter Wiki, and in Japan esa.io (2015), Kibela (2017), and Qiita Team (2013), where ideas such as the first-class "work in progress" post took shape. Scrapbox (2016, renamed Cosense in 2024) rejected hierarchy entirely in favour of links and two-hop relations, and edited line by line in real time. Notion (2016) made the block, not the page, the unit, and attached databases to pages. Federated Wiki (2011), Cunningham's own second act, made forking between sites the collaboration primitive and embedded each page's history inside the page.

Shared traits: Markdown or a visual editor (often both); REST or GraphQL APIs; single sign-on; hierarchy as spaces, collections, or paths; tags; comments; the first real-time co-editing (Etherpad in 2008, Confluence in 2016); SaaS business models alongside open source.

### 3.3 Block-based, outliner, and local-first tools (roughly 2019 onward)

Roam Research (2019) popularized "bidirectional links" and block references for a new audience; Obsidian (2020) and Logseq (2020) brought the same ideas to local Markdown files; Foam and Dendron did it inside a code editor; Silverbullet did it in a self-hosted browser app with a scripting language. AFFiNE, AppFlowy, Anytype, and SiYuan built block-based, local-first tools on CRDT synchronization. Docmost (2024) and Outline's later versions are open-source answers to Confluence and Notion with real-time editing on Yjs. Quartz turns an Obsidian vault into a static site. Tana and Capacities make typed objects the unit.

Shared traits: `[[wikilinks]]` inside Markdown or a block model, usually target-first with a `|` label; backlinks with context; graph views; properties in YAML frontmatter (`tags`, `aliases`); block identifiers (`^id`); embeds (`![[...]]`); callouts (`> [!note]`); plugins; CRDT-based collaboration; and, increasingly, agent-oriented interfaces. Two opposite stances on portability coexist: "file over app", where the Markdown files *are* the database (Obsidian, Silverbullet, Foam), and local-first CRDT state with Markdown as a convenience export (Anytype, AFFiNE, Logseq's database version).

The convergence that matters for this suite is that a de facto "Obsidian dialect" of wiki Markdown is now read by many tools that otherwise share nothing. Chapter 08 builds on it.

## 4. What they share

Across all three generations, a surprisingly stable set of capabilities recurs. Appendix A gives the per-engine matrix; the summary:

| Capability | Prevalence | Notes |
|---|---|---|
| Free links by title | Near-universal | Syntax differs; see §5. Notion and a few visual-first tools link by object reference instead. |
| Visible marker for missing pages | Classic: universal; modern: common | Question mark, red link, dimmed link, or implicit creation. |
| Backlinks | Common, rising | A footer or panel in most; a central feature in outliners. |
| Recent changes / activity | Near-universal | The oldest social feature; sometimes the home page itself. |
| Revision history with diff and revert | Classic and transitional: universal; modern: variable | Single-file and static wikis outsource history to files or git; some commercial tools tie retention to plans. |
| Edit summaries | Classic: common; modern: rare | Replaced by continuous history in real-time tools; by commit messages in git-backed ones. |
| Discussion beside content | Common | Talk pages, comments, inline comments; absent by design in Scrapbox / Cosense and Federated Wiki. |
| Tags or categories | Near-universal | Often pages themselves. |
| Optional hierarchy | Common | Strict only in a few (BookStack); absent by design in several (TiddlyWiki, Scrapbox / Cosense). |
| Transclusion | Common | Templates, includes, embeds, synced blocks. |
| Macros or directives | Near-universal | A dozen syntaxes; see Chapter 12. |
| Attachments | Near-universal | Licensing and metadata handling vary widely. |
| Search and feeds | Classic: universal; modern: search yes, feeds rare | Atom/RSS feeds are a classic-generation strength. |
| API | Common | REST, GraphQL, JSON-RPC, XML-RPC, plain JSON files; several with OpenAPI descriptions. |
| Export | Universal in some form | Fidelity varies enormously; see Chapter 10. |
| Real-time co-editing | Modern: common; classic: rare | Yjs has become the shared engine; XWiki is the classic exception. |
| Block identifiers | Modern: common; classic: rare | The main technical divide; see §6. |

## 5. Where they split

The fault lines are few and well defined, which is good news for an interoperability effort: each has a bridging convention in Part III.

1. **Markup.** Wikitext, DokuWiki syntax, MoinMoin syntax, PmWiki, TML, XWiki Syntax, Tiki, TiddlyWiki WikiText, PukiWiki, Org-mode, AsciiDoc, Textile, Scrapbox notation, several Markdown dialects, and several JSON block models. Bridge: a portable Markdown profile as an export and import target ([Chapter 08](08-Markup_and_Syntax.md)).
2. **Link label order.** `[[Target|Label]]` (MediaWiki, DokuWiki, MoinMoin, PmWiki, Trac, Redmine, Obsidian, and most Markdown tools) versus `[[Label|Target]]` (TiddlyWiki, ikiwiki, Gollum, GitLab, JSPWiki, Dendron) and other delimiters (`>`, `>>`, `][`, `->`). Bridge: declare the order; converters flip it ([MKUP-6](08-Markup_and_Syntax.md)).
3. **Hierarchy separator.** `:` (DokuWiki, Zim), `/` (MoinMoin, ikiwiki, Growi, Logseq, MediaWiki subpages), `.` (Dendron, PmWiki, XWiki, Foswiki), structural containers (BookStack, Confluence, Notion), or none. Bridge: `/` in interchange with the native separator declared ([MKUP-7](08-Markup_and_Syntax.md)).
4. **Macro syntax.** At least a dozen shapes, with `{{...}}` alone meaning template, image, transclusion, or macro depending on the engine. Bridge: snapshot envelopes and a small shared directive vocabulary ([Chapter 12](12-Extensibility_Macros_and_Dynamic_Content.md)).
5. **Content model.** Linear document, outliner, block tree, line list, tiddler set, story-and-journal. Bridge: nested lists, `^id` block identifiers, and property conventions ([Chapter 08 §5](08-Markup_and_Syntax.md#5-bridging-the-document-and-block-paradigms)).
6. **History model.** Full revisions, time-windowed snapshots, journals of actions, git commits, continuous CRDT state, or nothing. Bridge: a linearized history record ([XFER-7](10-Interchange_and_Portability.md)).
7. **Identity.** Title as identity (file-based tools, DokuWiki, TiddlyWiki) versus identifier as identity (Confluence, Notion, Logseq blocks). Bridge: `title` plus optional `id` ([META-2](09-Metadata_and_Frontmatter.md)).
8. **Collaboration.** Turn-taking with merge on save versus simultaneous editing. Bridge: durable checkpoints ([HIST-10](06-Temporal_Design_and_Revision_History.md#hist-10--real-time-co-editing-with-durable-history)).
9. **Portability posture.** File-first engines are nearly bundles already; database-first engines export convenience copies of varying fidelity; a few export only same-version archives. Bridge: declared fidelity and import reports ([Chapter 10](10-Interchange_and_Portability.md)).
10. **Openness.** GPL, AGPL, MIT, Apache, LGPL, BSD; source-available licenses that convert to open source after a delay; proprietary software that is free to use; proprietary SaaS. The content's portability matters most where the software's openness is least.

## 6. The document and block paradigms

The source report identified the document-versus-block divide as the hardest conceptual problem for any wiki standard. It is real, and it is smaller than it looks.

A *document* engine treats a page as one text that is parsed on render. A *block* engine treats a page as a tree of units, each with an identifier, which can be referenced, embedded, moved, and edited independently. Outliners (Logseq, Roam, Tana) are block engines whose blocks are list items; line-based engines (Scrapbox / Cosense) are block engines whose blocks are lines; Federated Wiki's story items and TiddlyWiki's tiddlers are blocks under other names.

Three observations make the bridge practical:

- **Blocks already serialize to Markdown.** Logseq stores pages as nested Markdown lists; Obsidian keeps block identifiers as text; Notion, Roam, SiYuan, and Anytype all export Markdown, losing identifiers to differing degrees.
- **Documents already have blocks.** Paragraphs, list items, and table rows are the natural split points, and heading anchors are a kind of block address every document engine has.
- **Identifiers are cheap to carry and cheap to ignore.** A trailing `^id` token is invisible enough that a document engine can leave it alone and a block engine can use it.

Chapter 08 §5 turns these into conventions. What does *not* travel well is behaviour that depends on the block tree at render time (live embeds of blocks, queries over block properties); those are extensions and are snapshotted ([Chapter 12](12-Extensibility_Macros_and_Dynamic_Content.md)).

## 7. Macros, plugins, and the limits of standardization

Wikis get their power from extension, and extension is bound to a host language and data model: Lua modules in MediaWiki, Velocity and Groovy in XWiki, Space Lua in Silverbullet, Datalog queries in Logseq, SQL-like queries in SiYuan, Dataview and Bases in Obsidian, database views in Notion, hundreds of macros in Confluence. The source report rightly concluded that standardizing their *execution* is impossible and unwise. This suite therefore standardizes only three things about extensions: that they are *declared*, that they *degrade* to readable content, and that their output *travels* with a record of what produced it ([Chapter 12](12-Extensibility_Macros_and_Dynamic_Content.md)).

## 8. Incentives, lock-in, and the counter-trend

Open-source engines gain users when content can move; proprietary platforms, especially hosted ones, gain revenue when it cannot. The report's observation stands: commercial incentives for portability are weak. Two things soften it. Regulation increasingly treats data portability as a right. And the market has begun to reward openness: Obsidian built a large following on "file over app"; Google Cloud published the Open Knowledge Format in 2026 and Outline shipped an export for it within months; BookStack documents a portable archive; GitBook and others serve every page as Markdown for machine consumption; Anytype publishes its block protocol. Guidelines cannot create incentives, but they can lower the cost of acting on the ones that exist, and they can give users a vocabulary for asking.

## 9. Lessons from earlier standardization attempts

| Attempt | Layer | Outcome | Lesson |
|---|---|---|---|
| **WikiRPCInterface** (early 2000s; JSPWiki, MoinMoin, DokuWiki) | API | Implemented by a few engines, then outgrown; DokuWiki still exposes its methods. | A shared API spreads when it is small and when it maps onto what engines already do. |
| **WikiCreole 1.0** (2006 to 2007) | Markup | Adopted by a handful of engines; frozen since 2007. | Asking engines to change their native markup does not work, even with a careful design. |
| **Wiki Interchange Format** (2006, research) | Interchange | Academic proposal; no adoption. | An interchange format needs a bundle, tooling, and a reason to export, not just a model. |
| **MediaWiki Markup spec** (2006 to 2010) | Grammar | Abandoned; wikitext remains defined by its parser. Parsoid later provided a specified HTML form instead. | When a grammar is intractable, a specified *rendering* can serve as the interchange surface. |
| **Markdown → CommonMark** (2004; 2014) | Markup | Became the de facto common tongue. | A format wins when it is already what people paste, read, and write, and when its ambiguities are finally specified. |
| **OPML** (2000) | Outline interchange | Still the way outliners exchange outlines. | A tiny format for one well-understood structure can last decades. |
| **Obsidian dialect and JSON Canvas** (2020 to 2024) | Markup and canvas | Adopted by many independent tools. | A vendor can lead an open convention when the files are plain and the specification is published. |
| **Implicit UX patterns** (1995 onward) | Experience | Red links, Recent Changes, talk pages, diffs: understood by millions, specified by nobody. | The most durable standard the wiki world has is the one nobody wrote down. Part II writes it down. |

The pattern is consistent. Efforts that asked engines to *become* something failed; efforts that described a shared *target* that engines could read and write, or that named what they already did, succeeded. This suite is designed on the second model.

## 10. Scope boundaries, restated

Four areas are left to each engine, for reasons the report gave and this chapter has illustrated:

- **Storage.** Flat files, a single HTML file, git, relational and document databases, CRDT stores, and JSON files are all in active use and all work. Only the exchange form is discussed.
- **Layout and styling.** The lineup of Federated Wiki, the story river of TiddlyWiki, the sidebar tree of Confluence, and the recency grid of Scrapbox / Cosense are all good designs. Patterns describe capabilities, not positions.
- **Access control.** From anonymous public editing to directory-integrated enterprise permissions, models differ legitimately. Only visibility signals and their effect on portability are addressed.
- **Code execution.** Scripting inside content is powerful and engine-bound; only declaration and degradation are addressed.

---

Previous: [00 · Overview and Vision](00-Overview_and_Vision.md) · Next: [02 · Guiding Principles](02-Guiding_Principles.md)
