# 07 · Collaboration, Awareness and Governance

> **Part II — The Pattern Language** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [06 · Temporal Design and Revision History](06-Temporal_Design_and_Revision_History.md) · Next: [08 · Markup and Syntax](08-Markup_and_Syntax.md)

**In one sentence:** These fourteen patterns are the social machinery of a wiki: how a community sees itself at work, talks beside the content, trusts by default, protects softly, and governs through visibility rather than locks.

The pattern format is explained in [03 · Pattern Language Overview](03-Pattern_Language_Overview.md#2-pattern-format). Access-control *models* are out of scope ([00 §7.2](00-Overview_and_Vision.md#72-explicitly-out-of-scope)); this chapter addresses only how access decisions are made visible and how they interact with portability.

---

## COLL-1 · Recent Changes

**Also known as:** activity feed, what's new, the heartbeat.
**Maturity:** Established.

**Context.** A community needs to know what is happening across the whole wiki.

**Tension.** A firehose of every change overwhelms; a curated digest hides. Private or scoped wikis need the feed limited to what the viewer may see. Real-time engines produce changes faster than a list can be read.

**Guidance.**
- Every wiki **should** offer a chronological view of changes across all pages, showing page, time, author, summary, and a link to the diff.
- The view **should** be filterable: by namespace or space, by minor and automated edits ([HIST-8](06-Temporal_Design_and_Revision_History.md#hist-8--minor-edits-and-noise-control)), by author, by type of event (edit, create, rename, delete, upload).
- Recent changes **should** be available as a standard feed (Atom is **recommended**) for the whole wiki and **encouraged** per namespace and per page ([API-6](11-APIs_and_Discovery.md)).
- Grouping consecutive changes to one page and live updating are **encouraged**.
- In scoped wikis the view **should** respect the viewer's access, and the engine **should** say when results are filtered.

**Observed in.** RecentChanges was the first wiki's first social feature. MediaWiki's *Recent changes* with rich filters, grouped view, live updates, and Atom/RSS feeds is the fullest realization. DokuWiki, MoinMoin, and PukiWiki (which maintains RecentChanges as an actual page) ship it by default. TiddlyWiki has a *Recent* sidebar tab. Scrapbox / Cosense makes the project home page a recency-ordered grid, so Recent Changes *is* the home page. Confluence, Notion, Outline, BookStack, and Growi offer activity feeds or "recently updated" views. Federated Wiki shows recent changes across a neighbourhood of sites.

**Interchange.** Derived from history; a bundle's `history/` reconstructs it.

**Related.** COLL-2, COLL-8, HIST-8; PR-12; Cunningham's *Observable*.

---

## COLL-2 · Watch and Subscribe

**Also known as:** watchlist, follow, subscribe, notifications for a page.
**Maturity:** Established.

**Context.** A contributor cares about particular pages and wants to know when they change, without reading everything.

**Tension.** Subscriptions are the main way stewardship scales, but every subscription is a future interruption; digests reduce noise and delay awareness.

**Guidance.**
- Users **should** be able to watch individual pages and, where hierarchy exists, namespaces or spaces.
- Watching **should** feed a personal view (a watchlist) and **may** feed notifications, with per-user choice of immediacy and digest.
- A per-page feed (Atom) is **encouraged** so that watching works even without an account or from outside the wiki.
- Watching a page **should** include its discussion ([COLL-3](#coll-3--talk-beside-content)).
- Auto-watching pages one edits is **encouraged** as a default that can be turned off.

**Observed in.** MediaWiki's watchlist and email notifications; DokuWiki's page and namespace subscriptions with digests; MoinMoin subscriptions; Confluence page and space watching; Notion's page following; Outline's document and collection subscriptions; BookStack's watch feature; Growi's subscriptions.

**Interchange.** Not exported; personal preferences.

**Related.** COLL-1, COLL-9.

---

## COLL-3 · Talk Beside Content

**Also known as:** talk page, discussion, comments, meta-page.
**Maturity:** Established.

**Context.** People disagree about a page, have questions about it, or want to coordinate work on it.

**Tension.** Discussion is essential and it pollutes the artifact if mixed into it. Putting discussion in a separate place keeps the page clean but can hide it; putting it in comments under the page is visible but shallow; forbidding it pushes conversation into chat where it is lost.

**Guidance.**
- Every page **should** have an associated place for discussion that is linked from the page and separate from its content.
- The discussion **should** be as durable and attributable as the page: versioned, authored, exportable with the page ([XFER-10](10-Interchange_and_Portability.md)).
- Discussion **should** be able to reference specific parts of the page ([COLL-5](#coll-5--inline-comments-and-annotations)) and specific revisions ([HIST-5](06-Temporal_Design_and_Revision_History.md#hist-5--permalinks-to-revisions)).
- Resolved discussions **should** be markable as such and **should** remain readable.
- Engines **may** also support light in-content notes for editors (hidden comments) and **should** export them in a form that stays hidden in other renderers ([MKUP-11](08-Markup_and_Syntax.md)).

**Observed in.** MediaWiki pairs every page with a talk page in a parallel namespace, with modern reply and topic tools. DokuWiki and PukiWiki add discussions through plugins, PukiWiki's `#comment` tradition placing a comment form inside the page itself. Confluence, Notion, Outline, BookStack, Wiki.js, Growi, and Docmost offer page comments, several with inline anchoring. Scrapbox / Cosense has no comments: discussion happens in the text, which is then refactored. Federated Wiki has no comments either: one forks the page and writes a response on one's own site.

**Interchange.** `discussions/<page-id>.jsonl` or Markdown threads in the bundle.

**Related.** COLL-4, COLL-5, COLL-2; PR-14.

---

## COLL-4 · Document Mode and Thread Mode

**Also known as:** consolidated vs. conversational, refactoring, summarize and resolve.
**Maturity:** Established.

**Context.** A page starts as a conversation (a sequence of signed remarks) and should become a document (a consolidated statement), or the reverse.

**Tension.** Thread mode is fast and faithful to who said what; document mode is useful to readers but erases the conversation. Neither should be the only mode, and a page in the wrong mode frustrates everyone.

**Guidance.**
- Engines **should** make the mode of a page recognizable: discussion-shaped content (signed, timestamped, chronological) **should** be distinguishable from document-shaped content.
- Tools for moving between modes are **encouraged**: signing and timestamping in discussion contexts; a "summarize and resolve" or "refactor into page" action that turns a thread's conclusion into content while preserving the thread.
- Communities **should** be able to document their conventions for when each mode applies ([COLL-12](#coll-12--the-wiki-documents-itself)).

**Observed in.** The *DocumentMode* and *ThreadMode* distinction was articulated on MeatballWiki ("pages that work as documents, rather than discussions") and practised on the first wiki, where refactoring threads into documents became a named communal activity. MediaWiki talk pages use `~~~~` signatures and section threads. Scrapbox / Cosense pages often begin as threaded notes and are rewritten into prose by the same contributors.

**Interchange.** Threads export as discussions; documents as pages.

**Related.** COLL-3, AUTH-4.

---

## COLL-5 · Inline Comments and Annotations

**Also known as:** anchored comments, highlights, marginalia.
**Maturity:** Emerging.

**Context.** A comment is about *this sentence*, not about the page.

**Tension.** Anchoring a comment to a text range is precise and fragile: the text changes, and the anchor floats or breaks. Inline comments visible in the page distract readers; hidden ones are missed.

**Guidance.**
- Engines offering inline comments **should** anchor them robustly (quoted text plus position, with re-anchoring heuristics) rather than by offset alone; the W3C Web Annotation model's selectors are **recommended** as a reference design.
- Readers **should** be able to hide annotations; authors **should** be able to resolve them.
- Inline comments **should** export as annotations tied to the page (and ideally to a revision), degrading to a list of quoted comments when the importer cannot anchor them ([XFER-10](10-Interchange_and_Portability.md)).

**Observed in.** Confluence inline comments; Notion and Docmost block-level comments; Outline inline comments; external annotation layers such as Hypothesis implementing the W3C model over any page. MediaWiki keeps comments at the section level on talk pages.

**Interchange.** Web Annotation JSON-LD in `discussions/`, or a simplified equivalent ([Appendix D](appendices/D-Portable_Wiki_Bundle_Example.md)).

**Related.** COLL-3, NAV-10.

---

## COLL-6 · Soft Security

**Also known as:** security through visibility, revert over restrict.
**Maturity:** Established.

**Context.** A wiki is open to many people, some of whom will damage it by accident or intent.

**Tension.** Preventing bad edits in advance (locks, approvals, permissions) also prevents good ones and consumes the energy of the people who maintain them. Allowing everything and cleaning up afterwards scales with the community but requires excellent visibility and reversibility.

**Guidance.**
- Engines **should** make soft security possible by excelling at [COLL-1](#coll-1--recent-changes), [COLL-2](#coll-2--watch-and-subscribe), [HIST-2](06-Temporal_Design_and_Revision_History.md#hist-2--diff-as-a-first-class-view), and [HIST-3](06-Temporal_Design_and_Revision_History.md#hist-3--revert-with-dignity); these are the community's tools.
- Protective friction (captchas, rate limits, protection levels, blocks) **should** be applied progressively and in response to observed problems, not everywhere by default.
- Protective actions **should** be visible and logged: a protected page **should** say that it is protected and why; a block **should** be explained to the blocked person.
- Temporary protections (with expiry) are **encouraged** over permanent ones.
- Automated defences (spam filters, edit filters, machine-learning scoring) are engine-specific; they **should** keep a human in the loop and **should** be reviewable.

**Observed in.** MeatballWiki named *SoftSecurity* as the wiki's defining stance. Wikipedia's layered protection levels, patrolling, abuse filters, and rollback rights are the large-scale case study. Smaller engines typically rely on registration requirements, captchas, and rate limiting.

**Interchange.** Protection status **may** be exported as metadata (`protection:`), advisory only.

**Related.** COLL-7, COLL-10, HIST-3; PR-3, PR-13.

---

## COLL-7 · Assume Good Faith by Default

**Also known as:** AGF, welcome the newcomer, explain before you warn.
**Maturity:** Established.

**Context.** A new contributor makes a first edit that is imperfect.

**Tension.** Most imperfect edits are well-meant, but tools built for fighting vandalism treat all of them alike. Studies of large wikis found that impersonal reverts and templated warnings sharply reduced newcomer retention, and that mentoring spaces and friendlier tools helped.

**Guidance.**
- Defaults **should** treat contributors as colleagues: explain markup and conventions, thank, and invite discussion before restricting.
- Automated messages (reverts, warnings) **should** be worded for a person acting in good faith, and **should** link to help and to the discussion page.
- Newcomer-specific restrictions (waiting periods, edit limits) **should** be minimal, explained, and lifted automatically.
- Positive feedback mechanisms (a "thanks" action, welcoming messages) are **encouraged**; they are cheap and measurably effective.
- Engines **should** make it easy for communities to create mentoring spaces (help desks, "teahouse" pages) and to route newcomers to them.

**Observed in.** Wikipedia's *Assume good faith* guideline, its *Thanks* notification, the *Teahouse* help space, and tooling research that reshaped anti-vandalism interfaces. Most engines leave tone to community configuration, which is why the pattern names it explicitly.

**Interchange.** Not applicable.

**Related.** COLL-6, HIST-3, AUTH-9, AUTH-13; PR-3, PR-14.

---

## COLL-8 · Visible Activity and Contribution History

**Also known as:** user contributions, logs, profile activity, who did what.
**Maturity:** Established.

**Context.** Someone wants to understand a contributor's work, or an administrator's actions, or the history of a decision.

**Tension.** Visibility builds trust and enables self-governance; it also exposes individuals. Logs of administrative actions keep power accountable but can be used to harass.

**Guidance.**
- Each contributor **should** have a view of their contributions across the wiki; each page has its history ([HIST-1](06-Temporal_Design_and_Revision_History.md#hist-1--non-destructive-history)).
- Administrative actions (protect, block, delete, rename, suppress) **should** be logged where the community can see them, subject to privacy constraints ([Chapter 14](14-Security_Privacy_and_Trust.md)).
- Users **should** be able to export their own contributions ([PRIV-5](14-Security_Privacy_and_Trust.md)).
- Visibility **should** be proportionate: public wikis publish more; private wikis show activity to members.

**Observed in.** MediaWiki's per-user contributions pages and public logs; profile activity in Confluence and Growi; page-level history nearly everywhere; little cross-wiki contribution visibility in most modern tools.

**Interchange.** `users.json` plus `history/` allow per-author reconstruction.

**Related.** COLL-1, HIST-4; PR-12, PR-14.

---

## COLL-9 · Notifications with Restraint

**Also known as:** mentions, alerts, digests, thanks.
**Maturity:** Emerging.

**Context.** Something happened that a person would want to know about.

**Tension.** Notifications keep collaboration alive and destroy attention when overused. Email, in-app, mobile push, and chat integrations multiply every event.

**Guidance.**
- Engines **should** notify on events that involve the person (mentions, replies, changes to watched pages, reverts of their edits) and **should** batch everything else.
- Users **should** control channels and frequency; digests **should** be available.
- Positive notifications (thanks, acknowledgement) are **encouraged**.
- Notification text **should not** leak content the recipient could not otherwise see, and **should** respect that email is not private ([Chapter 14](14-Security_Privacy_and_Trust.md)).
- Feeds ([COLL-1](#coll-1--recent-changes), [COLL-2](#coll-2--watch-and-subscribe)) are a notification channel that needs no account and no vendor; engines **should** keep them available.

**Observed in.** MediaWiki's notification system with mentions, thanks, and digests; DokuWiki's digest subscriptions; Confluence, Notion, Outline, and Slack-integrated tools with per-user settings; the widely shared experience of notification fatigue in enterprise tools.

**Interchange.** Not applicable.

**Related.** COLL-2, COLL-7, HIST-3.

---

## COLL-10 · Open by Default, Narrow with Care

**Also known as:** visible restrictions, least surprise, "view source".
**Maturity:** Established.

**Context.** Not everyone may read or edit everything; some wikis are private, some pages are protected.

**Tension.** Access control models are legitimately diverse and out of scope here. What is in scope is that invisible restrictions confuse people and break portability: content that was private in one engine can become public in another if the export carries no signal.

**Guidance.**
- The default posture of a wiki **should** be as open as its purpose allows; restrictions **should** be applied at the coarsest level that works (space, namespace) and narrowed deliberately.
- A restriction **should** be visible to those it affects: a protected page says it is protected; a reader without edit rights still sees "view source" rather than nothing ([AUTH-1](05-Authoring_and_Participation.md#auth-1--edit-is-one-step-away)).
- Exports **should** carry a minimal visibility signal per page or per space (`visibility: public | internal | restricted`) so that importers do not publish private content by accident ([XFER-5](10-Interchange_and_Portability.md)). Full permission models **should not** be expected to transfer.
- Search, feeds, backlinks, and recent changes **should** respect the viewer's access, and **should** say when results are filtered.

**Observed in.** MediaWiki's "View source" tab and lock indicators; Confluence restriction indicators; Notion's sharing status; space- and collection-level permissions in Outline, BookStack, and Wiki.js; DokuWiki's namespace-based ACL. None of these models transfers between engines, which is the reason for the minimal visibility signal.

**Interchange.** `visibility` in frontmatter and manifest; advisory, never a substitute for access control.

**Related.** COLL-6, AUTH-1; PR-13.

---

## COLL-11 · Shared Artifact, Not Possession

**Also known as:** no page owner, stewardship not ownership, communal editing.
**Maturity:** Established.

**Context.** A page was started by one person; others want to improve it.

**Tension.** Ownership gives accountability and protects a personal voice; it also freezes pages and discourages the small improvements that make wikis work. Enterprises want an accountable owner for stale content; communities want a commons.

**Guidance.**
- Shared pages **should not** be locked to their creator by default; anyone with access to the space **should** be able to edit.
- Where accountability is needed, engines are **encouraged** to model *stewardship* (a maintainer listed in metadata who is notified and asked to review) rather than *control* (a lock).
- Personal voice **should** have its own place: user pages, personal spaces, blog-like posts, or drafts, clearly distinguished from shared pages.
- Attribution **should** remain per revision ([HIST-4](06-Temporal_Design_and_Revision_History.md#hist-4--attribution-per-revision)) and pages **should** show plural contributors.

**Observed in.** MediaWiki pages have no owner (user pages are owned by convention only). Kibela has distinguished personal blog-style posts from shared wiki articles; esa.io posts are team-editable. Confluence added an optional *page owner* for accountability; Notion and Outline show creators but allow shared editing. Federated Wiki inverts the model: every page is owned by its site, and others fork rather than edit ([COLL-13](#coll-13--fork-instead-of-fight)).

**Interchange.** `maintainers:` as optional metadata; no ownership lock is exported.

**Related.** HIST-4, COLL-10, COLL-13; PR-2.

---

## COLL-12 · The Wiki Documents Itself

**Also known as:** help pages as pages, conventions in the wiki, system pages, self-hosting documentation.
**Maturity:** Established.

**Context.** A community develops conventions: how to name pages, which templates to use, how to behave.

**Tension.** Conventions buried in configuration files or external documents are invisible to contributors; conventions written as wiki pages are visible, improvable, and sometimes outdated.

**Guidance.**
- Help and syntax documentation **should** ship as editable pages in the wiki and **should** be linked from the editor.
- Communities **should** be able to write style guides, templates, and policies as pages, and engines **should** surface them at the moment of need (page creation, first edit).
- Where configuration is content-like (sidebar, navigation, interface messages, templates), engines are **encouraged** to make it editable as pages with history, so that changes to the wiki's own shape are as reversible as changes to its content.
- Engines are **encouraged** to publish their own documentation as a wiki built with the engine.

**Observed in.** DokuWiki and PukiWiki ship syntax and help pages; MediaWiki's `Help:`, `Project:`, and `MediaWiki:` namespaces make help, policy, and interface text into pages, with the sidebar itself a page. DokuWiki's sidebar and Growi's sidebar are pages. TiddlyWiki's documentation is a TiddlyWiki; Obsidian's help is a published vault; Scrapbox / Cosense's help is a project; Federated Wiki documents itself in Federated Wiki.

**Interchange.** Help, template, and configuration pages export as ordinary pages; engines **should** flag them (`kind: template | help | system`) so that importers can treat them appropriately ([META-7](09-Metadata_and_Frontmatter.md)).

**Related.** AUTH-6, COLL-4; PR-15.

---

## COLL-13 · Fork Instead of Fight

**Also known as:** federation, chorus of voices, divergent versions, plural truth.
**Maturity:** Exploratory.

**Context.** Two people or two communities disagree irreconcilably about a page, or want to build on each other's work across wiki boundaries.

**Tension.** The classic wiki forces convergence on one page, which produces either consensus or edit wars. Forking allows divergence and preserves everyone's version, at the cost of fragmentation and the loss of a single answer.

**Guidance (exploratory).**
- Engines **may** allow a page to be copied with recorded provenance (source wiki, page, revision) and developed independently, within a wiki or across wikis.
- Fork lineage **should** be visible on both ends when it exists, and merging changes back **should** be possible by the ordinary editing tools.
- Cross-wiki forking depends on portable pages ([Chapter 10](10-Interchange_and_Portability.md)), machine-readable site discovery ([Chapter 11](11-APIs_and_Discovery.md)), and attribution that travels ([LIC-4](15-Licensing_and_Attribution.md)); engines interested in federation are **encouraged** to adopt those first.
- Communities **should** decide whether they want convergence, plurality, or both for different kinds of pages.

**Observed in.** Federated Wiki's design: every site is owned by one author, pages are forked between sites with the journal recording provenance ("where it has traveled"), and the "neighbourhood" of sites makes plural versions browsable, an approach often described as a chorus of voices in contrast to a single consensus article. Git-backed wikis fork as repositories. Local-first tools make copying a vault trivial but record no provenance. Wikipedia's language editions are, in effect, long-running forks of the same topics with interlanguage links.

**Interchange.** `forked_from:` with site, page, and revision; interwiki map in the manifest.

**Related.** NAV-13, NAV-16, COLL-11; PR-2, PR-16.

---

## COLL-14 · Review as an Overlay, Not a Gate

**Also known as:** flagged revisions, pending changes, content states, verified pages, approval workflow.
**Maturity:** Emerging.

**Context.** Some wikis need to show readers a reviewed version while editing continues, for quality, compliance, or liability reasons.

**Tension.** Approval gates ensure quality and kill contribution; open editing invites contribution and worries compliance officers. The two can coexist if review is layered *over* editing rather than placed *in front of* it.

**Guidance.**
- Where review is needed, engines are **encouraged** to let editing continue freely while marking which revision is reviewed, and optionally showing readers the reviewed revision by default with the latest one a click away.
- Review status **should** be visible, dated, and attributed, and **should** be recorded in history ([HIST-1](06-Temporal_Design_and_Revision_History.md#hist-1--non-destructive-history)).
- Review requirements **should** be scoped (a namespace, a kind of page) rather than global.
- Status **should** export as metadata (`review: {state, by, at, revision}`) so that an importer can at least display it ([META-6](09-Metadata_and_Frontmatter.md)).

**Observed in.** MediaWiki's *Flagged Revisions* and Wikipedia's *pending changes* show a stable version while edits await review. Confluence's content states (draft, in progress, verified). XWiki's publication workflow application. Approval features in several enterprise tools are gates rather than overlays, which this pattern gently argues against.

**Interchange.** `review` object in frontmatter.

**Related.** AUTH-4, COLL-6, COLL-10; PR-13.

---

Previous: [06 · Temporal Design and Revision History](06-Temporal_Design_and_Revision_History.md) · Next: [08 · Markup and Syntax](08-Markup_and_Syntax.md)
