# 06 · Temporal Design and Revision History

> **Part II — The Pattern Language** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [05 · Authoring and Participation](05-Authoring_and_Participation.md) · Next: [07 · Collaboration, Awareness and Governance](07-Collaboration_Awareness_and_Governance.md)

**In one sentence:** A wiki page is not a document but a *history*: these twelve patterns keep that history whole, legible, attributable, and forgiving, from the classic revision list to real-time co-editing and the rare case where something must be hidden without being erased.

The pattern format is explained in [03 · Pattern Language Overview](03-Pattern_Language_Overview.md#2-pattern-format). The portable representation of history is defined in [10 · Interchange and Portability](10-Interchange_and_Portability.md).

---

## HIST-1 · Non-Destructive History

**Also known as:** revision history, page history, immutable revisions, the attic, the journal.
**Maturity:** Established.

**Context.** Every edit replaces what was there before.

**Tension.** Keeping everything forever costs storage and raises privacy questions; keeping nothing makes every edit an irreversible risk. Some commercial tools tie history retention to pricing tiers; some single-file and local tools have no history at all without external help.

**Guidance.**
- Every saved change **should** produce a retrievable revision; saving **should never** overwrite the only copy of the previous state.
- History **should** be available to readers, not only to editors or administrators; it is part of the content's credibility.
- Retention **should** be unlimited by default. Where an engine or plan limits retention, the limit **should** be stated plainly and users **should** be able to export history before it expires ([PR-16](02-Guiding_Principles.md)).
- Revisions **should** record at least: a revision identifier, the parent revision, a timestamp, the author ([HIST-4](#hist-4--attribution-per-revision)), an optional summary, and the full content or enough to reconstruct it.
- History **should** be exportable in a portable form ([XFER-7](10-Interchange_and_Portability.md)) and reachable through the API ([API-4](11-APIs_and_Discovery.md)).
- Engines without built-in history (single-file, static, or file-based designs) are **encouraged** to integrate with a versioning layer (git, snapshots, sync history) and to document how users obtain history.

**Observed in.** MediaWiki stores the full text of every revision and exposes it to everyone. DokuWiki keeps old revisions in an "attic" with a per-page changelog; PukiWiki keeps time-windowed backups; MoinMoin and Confluence keep numbered versions. Git-backed wikis (Gollum, ikiwiki, Gitit, Otter Wiki, Wiki.js with git sync) inherit git history. Federated Wiki embeds a *journal* of actions inside each page's JSON, so the history travels with the page. Notion and Obsidian Sync offer version history whose retention depends on the plan; Obsidian's local file-recovery plugin keeps time-limited snapshots. TiddlyWiki has no history in its single-file form and relies on external versioning. BookStack keeps a configurable number of revisions.

**Interchange.** `history/<page-id>.jsonl` in a bundle; one record per revision ([Appendix D](appendices/D-Portable_Wiki_Bundle_Example.md)).

**Related.** HIST-2, HIST-3, HIST-5, HIST-12; PR-1, PR-7.

---

## HIST-2 · Diff as a First-Class View

**Also known as:** compare revisions, show changes, visual diff.
**Maturity:** Established.

**Context.** A reader or reviewer wants to know what changed between two points in time.

**Tension.** Line-based diffs are precise but hard to read for prose; word-level and rendered diffs are readable but can hide structural changes. Colour-only diffs exclude many users. Diffs across renames, moves, and metadata changes are often missing.

**Guidance.**
- The engine **should** show a diff between any two revisions of a page, with the latest-versus-previous diff one step away from the history and from Recent Changes.
- Word-level or character-level highlighting within changed lines is **recommended** for prose; a side-by-side layout and an inline layout are both **encouraged**.
- Diffs **should** be accessible without colour: use markers, labels, and ARIA roles so that insertions and deletions are distinguishable by assistive technologies ([A11Y-5](13-Accessibility_Internationalization_and_Web_Standards.md)).
- Diffs **should** cover metadata and structural events (rename, tag change, attachment change) as well as text.
- A visual diff of rendered output is **encouraged** in visual-first engines, alongside a source diff where source exists.
- Every diff **should** have a stable URL ([HIST-5](#hist-5--permalinks-to-revisions)).

**Observed in.** MediaWiki's two-column diff, inline diff, and VisualEditor's rendered diff; DokuWiki's side-by-side and inline diffs; PukiWiki's coloured line diff; Confluence's version comparison; Outline's and BookStack's revision comparisons; git diffs in git-backed wikis; Obsidian Sync's version diff. Notion offers restore points but no diff view.

**Interchange.** Diffs are derived from revisions and need not be exported; exporters **may** include patches instead of full text for large histories ([XFER-7](10-Interchange_and_Portability.md)).

**Related.** HIST-1, HIST-3, AUTH-3, COLL-1.

---

## HIST-3 · Revert with Dignity

**Also known as:** undo, rollback, restore version, revert.
**Maturity:** Established.

**Context.** A change was mistaken, harmful, or simply disagreed with.

**Tension.** Reverting must be effortless or soft security fails; but a revert is also a social act that can humiliate a newcomer, and research on large wikis shows that curt reverts drive contributors away. Reverting one change among several is harder than reverting everything since a point in time.

**Guidance.**
- Restoring any earlier revision **should** take one action and **should** create a new revision rather than deleting later ones.
- Undoing a single intermediate change (leaving later changes intact) is **encouraged**; it is more precise and less confrontational than rolling back.
- The engine **should** let the reverter explain, and **should** prefill a neutral summary ("Restored revision N") rather than an accusatory one.
- Notifying the person whose change was reverted is **encouraged**, with wording that invites discussion ([COLL-7](07-Collaboration_Awareness_and_Governance.md#coll-7--assume-good-faith-by-default), [COLL-9](07-Collaboration_Awareness_and_Governance.md#coll-9--notifications-with-restraint)).
- Bulk reverts (of a bot run, of a compromised account) **may** be offered to trusted roles and **should** be logged.

**Observed in.** MediaWiki distinguishes *undo* (editable, with summary) from *rollback* (one click, for trusted users) and offers *restore this version*; Wikipedia's etiquette around reverts (discuss, do not edit-war) grew from this tooling. DokuWiki restores by opening and saving an old revision. Confluence and Notion offer *restore this version*. Git-backed wikis revert through commits.

**Interchange.** A revert is an ordinary revision; exporters **may** mark it (`reverts: <revision-id>`).

**Related.** HIST-1, HIST-2, COLL-6, COLL-7; PR-1, PR-3.

---

## HIST-4 · Attribution per Revision

**Also known as:** authorship, blame, edited by, contributor record.
**Maturity:** Established.

**Context.** Readers want to know who said this; contributors deserve credit; licenses often require it.

**Tension.** Attribution supports trust and license compliance but exposes contributors, including their IP addresses in engines that allow anonymous editing. Real-time editing blurs authorship below the revision level.

**Guidance.**
- Every revision **should** record who made it: an account, a pseudonym, or an explicit anonymous marker.
- Attribution **should** be visible from the page (at least "last edited by", with the full list one step away), not only in the history.
- Engines that record IP addresses for anonymous edits **should** protect them, for example by showing a temporary pseudonym publicly and restricting the raw address ([PRIV-3](14-Security_Privacy_and_Trust.md)).
- Real-time and line-based engines are **encouraged** to keep finer-grained attribution (per line, per segment, per session) and to roll it up into revision-level attribution for history and export.
- Attribution **should** be exported with history in a form that satisfies the content license and respects contributor privacy ([XFER-8](10-Interchange_and_Portability.md), [LIC-4](15-Licensing_and_Attribution.md)).

**Observed in.** MediaWiki records a user or IP per revision and, since the mid-2020s, has been replacing public IPs with temporary accounts. DokuWiki records user or IP; git-backed wikis record the commit author. Confluence and Notion record version authors and show "last edited by". Scrapbox / Cosense records the author of every *line* and shows contributor icons. Federated Wiki's journal records the site and author of each action. Etherpad-style editors colour text by author.

**Interchange.** `author` per revision in `history/`, with an optional `users.json` directory mapping identifiers to display names and profile URIs.

**Related.** HIST-1, HIST-10, COLL-8; PR-2, PR-18.

---

## HIST-5 · Permalinks to Revisions

**Also known as:** permanent link, oldid, cite this version.
**Maturity:** Established.

**Context.** Someone wants to cite exactly what a page said at a moment, or to share a diff.

**Tension.** Current-page URLs are what people copy, but what they point at changes. Revision URLs are stable but can be mistaken for the current page.

**Guidance.**
- Every revision **should** have a stable URL, and the history view **should** make it easy to copy.
- A page rendered at an old revision **should** say so clearly and link to the current version.
- Diff URLs **should** be stable too ([HIST-2](#hist-2--diff-as-a-first-class-view)).
- A "cite this version" or "copy permanent link" affordance is **encouraged**.
- Revision identifiers **should** appear in the API and in exports so that citations survive migration ([API-4](11-APIs_and_Discovery.md)).

**Observed in.** MediaWiki's `oldid` URLs and *Permanent link* tool; DokuWiki's `rev` parameter; Confluence version URLs; commit URLs in git-backed wikis. Many modern tools expose version history only inside the interface, with no shareable URL.

**Interchange.** Revision identifiers in `history/`.

**Related.** HIST-1, HIST-2.

---

## HIST-6 · Rename Preserves History

**Also known as:** move page, rename with redirect, relink.
**Maturity:** Established.

**Context.** A page's title no longer fits.

**Tension.** Renaming is routine, yet in many engines it either breaks inbound links or severs the page from its past. Rewriting links everywhere is thorough but opaque and does not reach other wikis.

**Guidance.**
- Renaming or moving a page **should** carry its entire history with it and **should** be recorded as an event in that history.
- Inbound links **should** keep working ([NAV-8](04-Discovery_Navigation_and_Topology.md#nav-8--redirects-and-aliases)): by redirect, alias, stable identifier, or link rewriting, with the old title retained as an alias in any case.
- Associated resources (discussion, attachments, subpages) **should** move with the page or the engine **should** ask.
- Renames **should** be reversible like any other change.

**Observed in.** MediaWiki's *Move* carries history and talk pages, leaves a redirect, and logs the move. Confluence and Notion rename freely because links are identifier-based. Obsidian, Logseq, and Scrapbox / Cosense rewrite links across the vault or project. DokuWiki needs a plugin to move pages with link rewriting; TiddlyWiki needs a relink plugin. Git-backed wikis preserve history across renames through the version control system.

**Interchange.** Rename events in `history/` (`type: rename`, `from`, `to`); old titles in `aliases:`.

**Related.** NAV-8, NAV-9, HIST-1.

---

## HIST-7 · Soft Deletion

**Also known as:** trash, recycle bin, archive, undelete.
**Maturity:** Established.

**Context.** A page should go away: it is obsolete, duplicated, or should never have existed.

**Tension.** Deletion is sometimes right, but a deleted page takes its history with it, and the people who linked to it lose context. Permanent deletion is irreversible; indefinite retention of deleted pages has privacy implications.

**Guidance.**
- Deletion **should** be reversible for a meaningful period, with the deleted page and its history recoverable by an appropriate role.
- Deletion **should** be logged and visible; links to a deleted page **should** become dangling links rather than silent dead ends ([NAV-3](04-Discovery_Navigation_and_Topology.md#nav-3--dangling-link-as-invitation)).
- Engines **should** distinguish *deletion* (the page is gone from view) from *suppression* (specific content is hidden for legal or privacy reasons, [HIST-12](#hist-12--suppression-without-erasure)).
- Permanent purge **may** exist for administrators and **should** be clearly separate from ordinary deletion.

**Observed in.** MediaWiki archives deleted pages for administrators to restore and keeps a deletion log. Confluence, Notion, Outline, and BookStack provide trash with restore. DokuWiki treats deletion as saving an empty page, leaving old revisions in the attic. Obsidian moves files to a trash folder.

**Interchange.** Deleted pages **may** be exported with `status: deleted` when the exporter has access, or omitted; the manifest **should** say which.

**Related.** HIST-1, HIST-12, NAV-3; PR-1.

---

## HIST-8 · Minor Edits and Noise Control

**Also known as:** minor edit flag, trivial change, coalesced revisions, bot flag.
**Maturity:** Established.

**Context.** History and change feeds fill with typo fixes, autosaves, and bot runs, burying the changes that matter.

**Tension.** Every change deserves a record, but not every change deserves attention. Continuous-save engines generate a revision per keystroke unless they coalesce, and coalescing loses granularity.

**Guidance.**
- Explicit-save engines **should** let an editor mark a change as minor and **should** let viewers filter minor changes out of history, Recent Changes, watchlists, and feeds.
- Automated edits **should** be flagged distinctly and filterable.
- Continuous-save engines **should** coalesce rapid consecutive changes by the same author into one revision for history readability, while keeping fine-grained recovery available where feasible ([AUTH-8](05-Authoring_and_Participation.md#auth-8--never-lose-a-draft)).
- Coalescing rules (time window, author change, explicit checkpoint) **should** be documented.

**Observed in.** MediaWiki's minor-edit checkbox and bot flag with filters everywhere. DokuWiki's minor-change option. MoinMoin's trivial change. PukiWiki coalesces backups within a time window. Notion, Outline, and Scrapbox / Cosense coalesce continuous edits into history snapshots. Confluence offers publishing without notifying watchers.

**Interchange.** `minor: true` and `automated: true` per revision.

**Related.** AUTH-10, COLL-1, COLL-9; PR-6.

---

## HIST-9 · Gentle Conflict Resolution

**Also known as:** edit conflict, three-way merge, optimistic concurrency, soft lock.
**Maturity:** Established.

**Context.** Two people edit the same page at the same time.

**Tension.** Hard locks prevent conflicts but block collaboration and strand pages when a locker walks away. Last-writer-wins silently destroys work. Merge interfaces are confusing when they appear unexpectedly.

**Guidance.**
- Engines **should** detect conflicts by comparing against the revision an edit was based on, rather than by locking.
- Non-overlapping changes **should** merge automatically.
- When a conflict cannot be merged, the engine **should** present both versions clearly, keep both texts recoverable, and let the editor resolve them; it **should never** discard either side.
- If locks are used, they **should** be advisory and visible ("someone else is editing"), time-limited, and overridable.
- Real-time co-editing removes the classic conflict but introduces others (offline edits, sync divergence); see [HIST-10](#hist-10--real-time-co-editing-with-durable-history).

**Observed in.** MediaWiki merges non-overlapping edits and shows a two-text conflict view, later improved to a side-by-side resolver. DokuWiki uses visible, timed page locks. PukiWiki detects collisions and shows the diff. Confluence moved from merge dialogs to simultaneous editing. esa.io's API performs a three-way merge when a client supplies the revision it edited from. Obsidian Sync and Logseq sync merge or keep both copies. Git-backed wikis fall back to git merge conflicts.

**Interchange.** Not applicable.

**Related.** AUTH-5, AUTH-8, HIST-10; PR-3.

---

## HIST-10 · Real-Time Co-Editing with Durable History

**Also known as:** simultaneous editing, collaborative editing, CRDT, OT.
**Maturity:** Emerging.

**Context.** Several people write together, seeing each other's cursors.

**Tension.** Real-time editing is wonderful for drafting and eliminates edit conflicts, but it dissolves the revision: there is no moment of "save", attribution becomes per-character, and history becomes a continuous stream that is hard to diff, cite, revert, or export. It also tends to depend on one engine's synchronization protocol.

**Guidance.**
- Real-time co-editing is **encouraged** where collaboration is intense, and **optional** elsewhere.
- Engines offering it **should** still produce durable, named revisions: at explicit checkpoints ("publish", "save a version"), at natural pauses, or at regular intervals, so that [HIST-1](#hist-1--non-destructive-history) through [HIST-5](#hist-5--permalinks-to-revisions) remain meaningful.
- Attribution **should** be preserved per contributor across a session and rolled up into revisions ([HIST-4](#hist-4--attribution-per-revision)).
- Offline and reconnecting edits **should** merge without loss, and the engine **should** document its merge semantics.
- The synchronization protocol is an engine extension; exports **should** linearize the collaborative history into ordinary revisions ([XFER-7](10-Interchange_and_Portability.md)). Engines using open CRDT libraries are **encouraged** to say which.

**Observed in.** Confluence's collaborative editing, Notion's live editing, Scrapbox / Cosense's line-level real-time model, Growi's simultaneous editing, Outline, Docmost, AFFiNE, and HedgeDoc built on open CRDT libraries, Etherpad's authorship-coloured text. Among classic engines, XWiki ships a real-time WYSIWYG editor enabled by default since its 16.9 release, while still producing numbered versions. MediaWiki remains single-author per edit with merge on save, which is a deliberate trade-off that preserves crisp revisions.

**Interchange.** Linearized revisions with per-revision contributor lists.

**Related.** HIST-1, HIST-4, HIST-9; Chapter 11.

---

## HIST-11 · Page Lifecycle at a Glance

**Also known as:** last edited, byline, freshness, verified, created/updated.
**Maturity:** Established.

**Context.** A reader wonders whether what they are reading is current and who has touched it.

**Tension.** Timestamps alone do not tell a reader whether content is still true. Verification labels help but need maintenance; stale labels are worse than none.

**Guidance.**
- Each page **should** show when it was created and last changed, and by whom, near the content.
- `created` and `updated` **should** be exported as metadata ([META-3](09-Metadata_and_Frontmatter.md)) and rendered machine-readably in HTML (`<time datetime>`; schema.org `dateCreated` and `dateModified`).
- Knowledge bases where staleness matters are **encouraged** to offer freshness or verification markers ("verified on", "needs review") as metadata that readers can see and maintainers can query.
- Engines **may** compute staleness signals (long untouched, many dangling links, outdated template) and surface them in health views ([NAV-15](04-Discovery_Navigation_and_Topology.md#nav-15--health-views-orphans-wanted-dead-ends)).

**Observed in.** The footer line "This page was last edited on ... by ..." in MediaWiki and DokuWiki; bylines in Confluence, Notion, Outline, and BookStack; `created` and `modified` fields on every tiddler in TiddlyWiki; frontmatter dates in Dendron and Obsidian workflows; Confluence content states and Wikipedia's "may be outdated" templates as freshness markers.

**Interchange.** `created`, `updated`, and optional `verified` in frontmatter.

**Related.** HIST-4, AUTH-4, NAV-15; PR-12.

---

## HIST-12 · Suppression Without Erasure

**Also known as:** revision deletion, oversight, redaction, tombstone.
**Maturity:** Emerging.

**Context.** A revision contains something that must not remain visible: private personal data, defamation, copyright infringement, a leaked credential.

**Tension.** "Nothing is ever lost" ([PR-1](02-Guiding_Principles.md)) collides with legal and ethical duties to remove content. Rewriting history destroys the integrity of the record and breaks every reference to later revisions; leaving the content in place is unacceptable.

**Guidance.**
- Engines **should** be able to hide the content (and, separately, the summary or the author) of a specific revision while preserving the revision's existence, position, and identifier in the history.
- The hidden revision **should** appear as a tombstone with a reason category and the identity of the role that acted, visible to the community to the extent privacy allows.
- Suppression **should** be logged and reversible by an appropriate role.
- Exports **should** represent tombstones rather than silently skipping revisions, so that imported histories stay consistent ([XFER-7](10-Interchange_and_Portability.md)).
- Rewriting or purging history **may** be offered as a last resort and **should** be documented as such.

**Observed in.** MediaWiki's *RevisionDelete* hides text, summary, or author of a revision while keeping its row, and its stricter *suppression* role handles legal cases; both are logged. Most other engines offer only full deletion of a version or page, or history rewriting in git, which illustrates the gap this pattern names.

**Interchange.** `suppressed: [content, author, summary]` with `reason` per revision; content omitted.

**Related.** HIST-1, HIST-7; Chapter 14; PR-1, PR-18.

---

Previous: [05 · Authoring and Participation](05-Authoring_and_Participation.md) · Next: [07 · Collaboration, Awareness and Governance](07-Collaboration_Awareness_and_Governance.md)
