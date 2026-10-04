# Appendix E · Glossary

> **Appendices** · **Status:** Working Draft 0.4 (October 2026)
> Previous: [D · Portable Wiki Bundle Example](D-Portable_Wiki_Bundle_Example.md) · Next: [F · References](F-References.md)

Terms are defined as used in this suite. Engine-specific synonyms are listed so that readers coming from any tradition can find their own vocabulary. Cross-references point to the chapter where a term is developed.

---

**ActivityPub.** W3C protocol for decentralized social networking; exploratory basis for wiki change notifications across sites. → [Chapter 11 §4](../11-APIs_and_Discovery.md#4-toward-federation-exploratory)

**Alias.** An alternative title that resolves to a page; carried in `aliases:`. Engines: Obsidian `aliases`, Logseq `alias::`, MediaWiki redirects. → [NAV-8](../04-Discovery_Navigation_and_Topology.md#nav-8--redirects-and-aliases)

**Anchor.** An address inside a page: a heading anchor or a block identifier. → [NAV-10](../04-Discovery_Navigation_and_Topology.md#nav-10--section-anchors-and-block-addresses)

**Assume good faith (AGF).** The community norm, articulated on MeatballWiki and Wikipedia, of treating contributors as well-intentioned absent clear evidence otherwise. → [COLL-7](../07-Collaboration_Awareness_and_Governance.md#coll-7--assume-good-faith-by-default)

**ATAG.** Authoring Tool Accessibility Guidelines (W3C). Part A: the tool is accessible; Part B: it helps authors produce accessible content. Wiki editors are authoring tools. → [Chapter 13](../13-Accessibility_Internationalization_and_Web_Standards.md)

**Atom.** IETF syndication format (RFC 4287); the recommended feed format for recent changes. → [API-6](../11-APIs_and_Discovery.md)

**Attachment.** A file stored with the wiki and referenced from pages. Engines: media, upload, asset, file. → [AUTH-7](../05-Authoring_and_Participation.md#auth-7--effortless-media), [XFER-4](../10-Interchange_and_Portability.md)

**Attribution.** The record of who made which change; also the acknowledgement that open licenses require. → [HIST-4](../06-Temporal_Design_and_Revision_History.md#hist-4--attribution-per-revision), [LIC-4](../15-Licensing_and_Attribution.md)

**Backlink.** A page that links to the current page; the set of such pages. Engines: What links here, references, linked references, incoming links. → [NAV-4](../04-Discovery_Navigation_and_Topology.md#nav-4--backlinks-what-links-here)

**Bases.** Obsidian's YAML file format for database-like views over frontmatter. → [Appendix A §4.1](A-Wiki_Engine_Landscape.md#41-obsidian)

**BCP 47.** The IETF best current practice for language tags (`en`, `ja`, `pt-BR`). → [META-10](../09-Metadata_and_Frontmatter.md)

**Block.** A sub-page unit with its own identity: a paragraph, list item, line, tiddler item, or Notion block. → [Chapter 01 §6](../01-Core_Concepts_and_Landscape.md#6-the-document-and-block-paradigms), [MKUP-9](../08-Markup_and_Syntax.md)

**Block identifier.** A stable token naming a block, written `^id` at the end of the block in the portable profile. Engines: Obsidian `^id`, Logseq `id::`, Roam block UID, SiYuan block ID. → [MKUP-9](../08-Markup_and_Syntax.md)

**Block reference / block embed.** A link to, or transclusion of, a block: `[[Page#^id]]`, `![[Page#^id]]`; `((uuid))` in outliners. → [NAV-10](../04-Discovery_Navigation_and_Topology.md#nav-10--section-anchors-and-block-addresses), [NAV-16](../04-Discovery_Navigation_and_Topology.md#nav-16--transclusion-with-provenance)

**BracketName.** The Japanese wiki term (YukiWiki, PukiWiki) for a free link in double brackets. → [NAV-2](../04-Discovery_Navigation_and_Topology.md#nav-2--free-links)

**Bundle.** See *Portable Wiki Bundle*.

**Callout.** A highlighted block (note, tip, warning); `> [!NOTE]` in the portable profile. Engines: admonition, alert, panel, info box. → [MKUP-15](../08-Markup_and_Syntax.md)

**CamelCase / WikiWord.** The original link mechanism: a capitalized compound word becomes a link automatically. → [NAV-2](../04-Discovery_Navigation_and_Topology.md#nav-2--free-links)

**Category.** A tag that is also a page listing its members; MediaWiki's term. → [NAV-7](../04-Discovery_Navigation_and_Topology.md#nav-7--tags-and-categories)

**CommonMark.** The unambiguous specification of Markdown; Layer 0 of the portable profile. → [Chapter 08](../08-Markup_and_Syntax.md)

**Conformance profile.** A named list of recommendation identifiers that an engine or tool may claim; a vocabulary, not a certification. → [Chapter 16](../16-Conformance_Profiles_and_Self_Assessment.md)

**CRDT.** Conflict-free replicated data type; the family of data structures (Yjs, Automerge, Loro) behind most modern real-time co-editing. → [HIST-10](../06-Temporal_Design_and_Revision_History.md#hist-10--real-time-co-editing-with-durable-history)

**Dangling link.** A link to a page that does not exist yet. Engines: red link, missing link, unresolved link, question-mark link, wanted page. → [NAV-3](../04-Discovery_Navigation_and_Topology.md#nav-3--dangling-link-as-invitation)

**Dead-end page.** A page with no outgoing links. → [NAV-15](../04-Discovery_Navigation_and_Topology.md#nav-15--health-views-orphans-wanted-dead-ends)

**Diff.** The difference between two revisions. → [HIST-2](../06-Temporal_Design_and_Revision_History.md#hist-2--diff-as-a-first-class-view)

**Digital garden.** A personal, continuously growing, imperfect-by-design collection of linked notes; source of the seedling/budding/evergreen maturity vocabulary. → [AUTH-4](../05-Authoring_and_Participation.md#auth-4--welcome-the-incomplete)

**Directive.** A generic extension syntax in Markdown: `::: name attrs` containers and `:name[text]{attrs}` inline; from a long-running CommonMark community proposal. → [MKUP-16](../08-Markup_and_Syntax.md)

**Discussion.** Conversation about a page kept beside it. Engines: talk page, comments, inline comments, annotations. → [COLL-3](../07-Collaboration_Awareness_and_Governance.md#coll-3--talk-beside-content)

**Document mode / thread mode.** MeatballWiki's distinction between a page written as a consolidated document and one written as a sequence of signed remarks. → [COLL-4](../07-Collaboration_Awareness_and_Governance.md#coll-4--document-mode-and-thread-mode)

**Dublin Core (DCMI Terms).** A metadata vocabulary (`dcterms:title`, `dcterms:modified`); one of the two vocabularies the portable metadata maps onto. → [META-12](../09-Metadata_and_Frontmatter.md)

**Edit summary.** A short description of a change saved with a revision. Engines: comment, commit message, version comment, change note. → [AUTH-10](../05-Authoring_and_Participation.md#auth-10--edit-summary-as-micro-narrative)

**Engine.** The software that runs a wiki. Used here for classic wikis, knowledge bases, note tools, and static generators alike.

**Envelope.** See *Snapshot envelope*.

**Federated Wiki.** Ward Cunningham's second wiki design (2011), in which each site is owned by one author and collaboration happens by forking pages between sites. → [Appendix A §2.16](A-Wiki_Engine_Landscape.md#216-federated-wiki)

**Fidelity level.** A declaration in a bundle manifest of how much was carried: 0 text, 1 structure, 2 metadata, 3 history, 4 conversation, 5 structured data. → [XFER-2](../10-Interchange_and_Portability.md)

**File over app.** The principle (Ango, 2023) that durable artifacts should be files in open formats, so that the application is replaceable. → [PR-16](../02-Guiding_Principles.md)

**Fork.** Copying a page with recorded provenance to develop it independently; Federated Wiki's collaboration primitive. → [COLL-13](../07-Collaboration_Awareness_and_Governance.md#coll-13--fork-instead-of-fight)

**Free link.** A link written as the target's title in brackets, `[[Title]]`; introduced by UseModWiki in 2001 and independently as BracketName in YukiWiki. → [NAV-2](../04-Discovery_Navigation_and_Topology.md#nav-2--free-links)

**Frontmatter.** A YAML block at the top of a Markdown file holding metadata; the portable container for Portable Page Metadata. → [Chapter 09](../09-Metadata_and_Frontmatter.md)

**GFM.** GitHub Flavored Markdown; its specification adds tables, task lists, strikethrough, and autolinks to CommonMark. GitHub's renderer adds alerts, footnotes, math, and Mermaid beyond the specification. → [Chapter 08](../08-Markup_and_Syntax.md)

**Graceful degradation.** The property that a construct still conveys its meaning in a renderer that does not understand it. → [Chapter 08 §4](../08-Markup_and_Syntax.md#4-the-degradation-ladder)

**Hierarchy.** Optional grouping of pages by prefix or path. Engines: namespace, subpage, folder, space, group, web, collection, book. → [NAV-6](../04-Discovery_Navigation_and_Topology.md#nav-6--flat-names-optional-hierarchy)

**History.** The sequence of revisions of a page. Engines: page history, versions, attic, journal, backups. → [Chapter 06](../06-Temporal_Design_and_Revision_History.md)

**IME.** Input method editor, used to type Chinese, Japanese, Korean, and other scripts; web editors should not break its composition. → [I18N-7](../13-Accessibility_Internationalization_and_Web_Standards.md)

**Import report.** The importer's account of what it imported, degraded, or dropped. → [XFER-13](../10-Interchange_and_Portability.md)

**Interwiki link / InterMap.** A prefixed link into another wiki (`[[wikipedia:Topic]]`) resolved through a prefix-to-URL map; the map concept originated on MeatballWiki. → [NAV-13](../04-Discovery_Navigation_and_Topology.md#nav-13--interwiki-links)

**IRI.** Internationalized Resource Identifier (RFC 3987); allows non-ASCII characters in web addresses. → [I18N-2](../13-Accessibility_Internationalization_and_Web_Standards.md)

**JSON Canvas.** Obsidian's open file format for infinite canvases (2024, MIT). → [Appendix A §4.1](A-Wiki_Engine_Landscape.md#41-obsidian)

**JSON Lines.** One JSON object per line; used for history and discussion records in bundles. → [XFER-7](../10-Interchange_and_Portability.md)

**Journal.** Federated Wiki's per-page list of actions (create, add, edit, move, remove, fork); history embedded in the page. → [Appendix A §2.16](A-Wiki_Engine_Landscape.md#216-federated-wiki)

**Kind.** The portable metadata field saying what sort of page this is (`page`, `category`, `template`, `help`, `system`, `discussion`, `user`, `redirect`). → [META-7](../09-Metadata_and_Frontmatter.md)

**Lineup.** Federated Wiki's horizontal arrangement of visited pages. → [NAV-11](../04-Discovery_Navigation_and_Topology.md#nav-11--spatial-orientation)

**Local-first software.** Software that keeps the primary copy of data on the user's device and synchronizes, following seven ideals set out by Ink & Switch (2019). → [WEB-6](../13-Accessibility_Internationalization_and_Web_Standards.md)

**Macro.** A construct in page source that the engine replaces with generated content. Engines: plugin, directive, parser function, template, widget, processor. → [Chapter 12](../12-Extensibility_Macros_and_Dynamic_Content.md)

**Manifest.** `wiki-bundle.yaml`, the file describing a bundle's origin, conventions, contents, and fidelity. → [XFER-1](../10-Interchange_and_Portability.md)

**Markdown variant.** The `variant` parameter of the `text/markdown` media type (RFC 7763), drawn from an IANA registry (CommonMark, GFM, pandoc, ...). → [MKUP-1](../08-Markup_and_Syntax.md)

**Maturity marker.** A visible label of how finished a page is (draft, WIP, stub; seedling, budding, evergreen). → [AUTH-4](../05-Authoring_and_Participation.md#auth-4--welcome-the-incomplete)

**Minor edit.** A revision flagged as small enough to hide from change feeds. Engines: trivial change, quiet save. → [HIST-8](../06-Temporal_Design_and_Revision_History.md#hist-8--minor-edits-and-noise-control)

**Namespace.** A prefix grouping pages (MediaWiki `Talk:`, DokuWiki `ns:`); in the portable profile, MediaWiki-style prefixes are kept in titles and listed in the manifest, while hierarchy uses `/`. → [MKUP-7](../08-Markup_and_Syntax.md)

**Neighbourhood.** Federated Wiki's set of sites known to the current session, used to resolve links and build recent changes. → [NAV-13](../04-Discovery_Navigation_and_Topology.md#nav-13--interwiki-links)

**NFC.** Unicode Normalization Form C; recommended for titles and link targets so that visually identical strings compare equal. → [MKUP-19](../08-Markup_and_Syntax.md)

**Obsidian Flavored Markdown (OFM).** Obsidian's dialect: CommonMark + GFM + LaTeX + wikilinks, embeds, block identifiers, callouts, comments, highlights. Widely read by other tools. → [Chapter 08](../08-Markup_and_Syntax.md)

**Open Definition.** The Open Knowledge Foundation's criteria for open licenses and content; CC0, CC BY, and CC BY-SA conform, NC and ND variants do not. → [Chapter 15](../15-Licensing_and_Attribution.md)

**Open Knowledge Format (OKF).** Google Cloud's 2026 specification for directories of Markdown concept documents with YAML frontmatter, `index.md` listings, and `log.md` histories; Outline exports it. A sibling of the Portable Wiki Bundle. → [Appendix G](G-Open_Knowledge_Format_Alignment.md)

**OpenAPI.** The specification language for describing HTTP APIs; recommended for REST APIs. → [API-1](../11-APIs_and_Discovery.md)

**OpenSearch description.** A small XML document describing a search endpoint so browsers and aggregators can use it. → [API-7](../11-APIs_and_Discovery.md)

**Operational transformation (OT).** The older family of real-time co-editing algorithms (Etherpad, Google Docs, HackMD lineage). → [HIST-10](../06-Temporal_Design_and_Revision_History.md#hist-10--real-time-co-editing-with-durable-history)

**Orphan.** A page with no inbound links. Engines: lonely page. → [NAV-15](../04-Discovery_Navigation_and_Topology.md#nav-15--health-views-orphans-wanted-dead-ends)

**Outliner.** An engine whose pages are trees of blocks, each a list item (Logseq, Roam, Tana; historically ThinkTank and OPML). → [Chapter 01 §6](../01-Core_Concepts_and_Landscape.md#6-the-document-and-block-paradigms)

**Page.** The unit of address and history. Engines: article, topic, note, document, item, tiddler, post, memo.

**Pandoc.** The universal document converter; reads and writes several wiki markups and serves as a bridge between them. → [MKUP-18](../08-Markup_and_Syntax.md)

**Parsoid.** MediaWiki's bidirectional converter between wikitext and a specified HTML form; an example of a rendering serving as an interchange surface. → [MKUP-18](../08-Markup_and_Syntax.md)

**Pattern.** A named, reusable solution to a recurring design problem, with its context and tensions; the unit of Part II. → [Chapter 03](../03-Pattern_Language_Overview.md)

**Pattern language.** A structured collection of related patterns (Alexander, 1977); the first wiki was built to write one. → [Chapter 03](../03-Pattern_Language_Overview.md)

**Permalink.** A stable URL to a specific revision. → [HIST-5](../06-Temporal_Design_and_Revision_History.md#hist-5--permalinks-to-revisions)

**Portable Page Metadata.** The frontmatter vocabulary of Chapter 09 and Appendix C.

**Portable Wiki Bundle.** The directory or archive layout of Chapter 10: `wiki-bundle.yaml`, `pages/`, `attachments/`, optional `history/`, `discussions/`, `users.yaml`, `structured/`.

**Portable Wiki Markdown.** The layered Markdown profile of Chapter 08: CommonMark, shared extensions, wiki extensions, declared engine extensions.

**Properties.** Structured key–value data on a page or block. Engines: fields, attributes, infobox parameters, DataForm fields, XObjects, database columns. → [META-8](../09-Metadata_and_Frontmatter.md)

**Provenance.** Where content came from: author, revision, source page, template, snapshot origin. → [TRUST-1](../14-Security_Privacy_and_Trust.md)

**Recent changes.** The wiki-wide chronological list of revisions; the first wiki's first social feature. Engines: activity feed, updates, timeline. → [COLL-1](../07-Collaboration_Awareness_and_Governance.md#coll-1--recent-changes)

**Red link.** MediaWiki's rendering of a dangling link; now the generic term. → [NAV-3](../04-Discovery_Navigation_and_Topology.md#nav-3--dangling-link-as-invitation)

**Redirect.** A page that sends readers to another page. → [NAV-8](../04-Discovery_Navigation_and_Topology.md#nav-8--redirects-and-aliases)

**Revert.** Restoring an earlier revision, creating a new revision in the process. Engines: undo, rollback, restore. → [HIST-3](../06-Temporal_Design_and_Revision_History.md#hist-3--revert-with-dignity)

**Revision.** One saved state of a page with time, author, and summary. Engines: version, edit, commit, snapshot. → [HIST-1](../06-Temporal_Design_and_Revision_History.md#hist-1--non-destructive-history)

**schema.org.** A vocabulary for structured data on the web (`Article`, `dateModified`, `license`); one of the two vocabularies the portable metadata maps onto. → [META-12](../09-Metadata_and_Frontmatter.md)

**Section editing.** Editing one part of a page rather than the whole. → [AUTH-5](../05-Authoring_and_Participation.md#auth-5--section-and-block-editing)

**Site description document.** A small JSON document describing a wiki's name, engine, formats, APIs, feeds, and interwiki map, discoverable from any page. → [API-1](../11-APIs_and_Discovery.md)

**Slug.** A URL-safe form of a title. The portable profile keeps the true title in metadata whatever the slug.

**Snapshot envelope.** HTML-comment markers (`<!-- wiki:snapshot ... --> ... <!-- /wiki:snapshot -->`) wrapping the static output of a macro, template, query, or embed on export, recording its origin. → [EXT-4](../12-Extensibility_Macros_and_Dynamic_Content.md)

**Soft security.** Protecting a wiki by visibility and reversibility rather than by locks; a MeatballWiki term. → [COLL-6](../07-Collaboration_Awareness_and_Governance.md#coll-6--soft-security)

**SPDX identifier.** A short standard name for a license (`CC-BY-SA-4.0`). → [LIC-1](../15-Licensing_and_Attribution.md)

**Stigmergy.** Coordination through traces left in a shared environment; the mechanism by which Recent Changes lets a community organize itself. → [PR-12](../02-Guiding_Principles.md)

**Story.** Federated Wiki's array of items that make up a page's content.

**Stub.** A page that exists but is deliberately short, inviting expansion. → [AUTH-4](../05-Authoring_and_Participation.md#auth-4--welcome-the-incomplete)

**Suppression.** Hiding the content, summary, or author of a revision while keeping the revision's place in history; MediaWiki's RevisionDelete and oversight. → [HIST-12](../06-Temporal_Design_and_Revision_History.md#hist-12--suppression-without-erasure)

**Tag.** A free-form label on a page. Engines: label, hashtag, keyword, category. → [NAV-7](../04-Discovery_Navigation_and_Topology.md#nav-7--tags-and-categories)

**Talk page.** MediaWiki's discussion page paired with each page. → [COLL-3](../07-Collaboration_Awareness_and_Governance.md#coll-3--talk-beside-content)

**Template.** A page designed to be transcluded with parameters, or offered as starter content. → [AUTH-6](../05-Authoring_and_Participation.md#auth-6--starters-and-templates), [EXT-6](../12-Extensibility_Macros_and_Dynamic_Content.md)

**Tiddler.** TiddlyWiki's unit of content: a small titled, tagged chunk of text with fields. → [Appendix A §2.15](A-Wiki_Engine_Landscape.md#215-tiddlywiki)

**Title.** The human-readable name of a page, used in links and URLs. → [NAV-1](../04-Discovery_Navigation_and_Topology.md#nav-1--page-as-the-unit-of-address)

**Transclusion.** Showing the content of one page, or part of it, inside another, live. Engines: include, embed, excerpt, synced block. → [NAV-16](../04-Discovery_Navigation_and_Topology.md#nav-16--transclusion-with-provenance)

**Two-hop link.** Scrapbox / Cosense's relation: pages sharing a link or tag with the current page, and pages one hop beyond each link target. → [NAV-12](../04-Discovery_Navigation_and_Topology.md#nav-12--related-pages-and-the-two-hop-neighborhood)

**UUID.** Universally unique identifier (RFC 9562); versions 4 (random) and 7 (time-ordered) are recommended for page and block identity. → [META-2](../09-Metadata_and_Frontmatter.md)

**Vault / graph / space / project / notebook.** Engine-specific names for a whole wiki or workspace (Obsidian, Logseq, Silverbullet and Confluence, Scrapbox / Cosense, SiYuan respectively).

**Visibility.** The advisory portable field (`public`, `internal`, `restricted`) that tells importers how carefully to treat a page. → [COLL-10](../07-Collaboration_Awareness_and_Governance.md#coll-10--open-by-default-narrow-with-care)

**Wanted page.** A dangling link target, ranked by how many pages want it. → [NAV-15](../04-Discovery_Navigation_and_Topology.md#nav-15--health-views-orphans-wanted-dead-ends)

**Watchlist.** A user's personal list of pages whose changes they follow. Engines: subscriptions, follows, watches. → [COLL-2](../07-Collaboration_Awareness_and_Governance.md#coll-2--watch-and-subscribe)

**WCAG.** Web Content Accessibility Guidelines (W3C); version 2.2 Level AA is the target. → [A11Y-1](../13-Accessibility_Internationalization_and_Web_Standards.md)

**Web Annotation.** W3C data model for annotations with selectors that anchor to text; the reference design for portable inline comments. → [COLL-5](../07-Collaboration_Awareness_and_Governance.md#coll-5--inline-comments-and-annotations)

**Webmention.** W3C protocol by which one site notifies another of a link; exploratory basis for cross-wiki backlinks. → [Chapter 11 §4](../11-APIs_and_Discovery.md#4-toward-federation-exploratory)

**WikiCreole.** The 2006–2007 attempt at a common wiki markup; frozen at version 1.0. → [Chapter 01 §9](../01-Core_Concepts_and_Landscape.md#9-lessons-from-earlier-standardization-attempts)

**Wikilink.** A free link; the term used by Markdown tooling.

**WikiRPCInterface.** An early-2000s shared XML-RPC API defined by JSPWiki and implemented by MoinMoin and DokuWiki. → [Chapter 11 §5](../11-APIs_and_Discovery.md#5-observed-in)

**Wikitext.** MediaWiki's markup language.

**WIP.** Work in progress; a first-class page state in esa.io and GROWI, and a recommended `status` value. → [AUTH-4](../05-Authoring_and_Participation.md#auth-4--welcome-the-incomplete)

**Yjs.** A widely used CRDT library for real-time collaboration (also *yrs*, its Rust port). → [HIST-10](../06-Temporal_Design_and_Revision_History.md#hist-10--real-time-co-editing-with-durable-history)

**Zettelkasten.** Niklas Luhmann's card-index method of small, uniquely numbered, cross-referenced notes; an ancestor of modern networked note tools. → [Appendix F](F-References.md)

---

Previous: [D · Portable Wiki Bundle Example](D-Portable_Wiki_Bundle_Example.md) · Next: [F · References](F-References.md)
