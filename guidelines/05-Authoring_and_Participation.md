# 05 · Authoring and Participation

> **Part II — The Pattern Language** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [04 · Discovery, Navigation and Topology](04-Discovery_Navigation_and_Topology.md) · Next: [06 · Temporal Design and Revision History](06-Temporal_Design_and_Revision_History.md)

**In one sentence:** These fourteen patterns lower the barrier between reading and writing: they make editing one step away, let people choose how they write, welcome half-finished work, protect drafts, and keep the author human even when machines help.

The pattern format is explained in [03 · Pattern Language Overview](03-Pattern_Language_Overview.md#2-pattern-format).

---

## AUTH-1 · Edit Is One Step Away

**Also known as:** seamless read-to-edit, always editable, the Edit tab.
**Maturity:** Established.

**Context.** A reader notices something missing or wrong and feels the impulse to fix it.

**Tension.** The impulse decays fast; every extra step between noticing and editing loses contributors. But an always-editable surface risks accidental changes, confuses readers who only want to read, and can hide the boundary between "looking" and "changing".

**Guidance.**
- From any page, a reader with permission **should** be able to begin editing in a single action, visible on the page itself.
- A keyboard shortcut for "edit this page" is **encouraged**.
- Engines that make pages always editable **should** make the mode legible (where am I typing, has it been saved, what counts as a revision) and **should** protect against accidental edits in reading contexts (touch scrolling, screen readers).
- When a reader lacks permission to edit, the engine **should** still show *why* and **should** let them view the source, so the page remains overt and the path to contribution remains visible ([COLL-10](07-Collaboration_Awareness_and_Governance.md#coll-10--open-by-default-narrow-with-care)).

**Observed in.** The classic Edit tab or button (MediaWiki, DokuWiki, PukiWiki, TiddlyWiki per tiddler, Confluence) with per-section edit links. Notion, Scrapbox / Cosense, Outline (optionally), and Logseq make the page itself the editor with no separate mode. Obsidian toggles between reading view and live preview. MediaWiki shows a "View source" tab in place of "Edit" when a page is protected.

**Interchange.** Not applicable.

**Related.** AUTH-2, AUTH-5; PR-6, PR-8; Cunningham's *Open*.

---

## AUTH-2 · Two Views of One Document

**Also known as:** markup and WYSIWYG, source and visual, live preview, "overt" output.
**Maturity:** Established.

**Context.** Some contributors think in text and want markup; others want to see the page as it will look. The same page must serve both.

**Tension.** Markup is portable, diffable, and precise; visual editing is approachable and faster for many. Supporting both means the two views must round-trip without loss, which is hard. Engines that abandoned markup for WYSIWYG often lost portability; engines that refused WYSIWYG lost contributors.

**Guidance.**
- Engines **should** store (or be able to produce on demand) a plain-text representation of every page, and that representation **should** be the one that is exported ([Chapter 08](08-Markup_and_Syntax.md)).
- Where both a source view and a visual view exist, switching between them **should** preserve content; where a construct cannot round-trip, the engine **should** say so before switching rather than silently flatten it.
- A live preview that renders markup in place is **encouraged** as a middle path.
- The rendered output **should** suggest the input that produced it (Cunningham's *Overt*): visible structure, copyable source, and consistent conventions.
- Binding a page permanently to one editor type is **discouraged**; if unavoidable, the engine **should** offer a conversion path.

**Observed in.** MediaWiki pairs a source editor with VisualEditor, switching through a round-trip HTML representation. BookStack lets each page use WYSIWYG or Markdown; Wiki.js binds a page to the editor it was created with but documents exactly what its conversion between editors loses, which is the right way to be lossy. XWiki switches between WYSIWYG and several syntaxes. Obsidian's live preview and Typora-style editors render Markdown in place. Notion, Outline, Docmost, and AFFiNE are visual-first with Markdown shortcuts and Markdown export. Confluence removed wiki markup editing in 2011, a widely cited portability regression.

**Interchange.** The plain-text representation is what travels. Visual-first engines **should** treat Markdown export as a product and declare its flavour ([MKUP-1](08-Markup_and_Syntax.md)).

**Related.** AUTH-3, AUTH-11; PR-8, PR-16.

---

## AUTH-3 · Preview and Live Feedback

**Also known as:** show preview, show changes, split view.
**Maturity:** Established.

**Context.** A contributor wants to know what their edit will look like, and what it changes, before committing it.

**Tension.** Previewing adds a step; skipping it produces broken pages and unintended changes. Live preview removes the step but needs the same renderer as the final page or it misleads.

**Guidance.**
- Markup editors **should** offer a preview rendered by the same pipeline as the final page.
- A "show changes" diff against the current revision before saving is **encouraged**; it catches accidental deletions and is the single most effective guard against edit regret ([HIST-2](06-Temporal_Design_and_Revision_History.md#hist-2--diff-as-a-first-class-view)).
- Live or side-by-side preview is **encouraged** where it does not harm performance or accessibility.
- Preview **should** make dangling links, unknown macros, and degraded constructs visible, so that problems surface before publishing.

**Observed in.** MediaWiki's *Show preview* and *Show changes*; DokuWiki and PukiWiki previews; split-pane live preview in Growi, Wiki.js, HackMD-derived editors, and Silverbullet; in-place rendering in Obsidian; visual-first editors where preview is implicit.

**Interchange.** Not applicable.

**Related.** AUTH-2, AUTH-13, HIST-2.

---

## AUTH-4 · Welcome the Incomplete

**Also known as:** stubs, WIP, drafts, seedlings, maturity markers, under construction.
**Maturity:** Established.

**Context.** Someone knows a little about a topic, or has a half-formed idea, or has run out of time.

**Tension.** Publishing unfinished work exposes the author and may mislead readers; withholding it loses the contribution entirely and denies others the chance to continue it. "Not ready" is the most common reason knowledge never enters a wiki.

**Guidance.**
- Engines **should** make it easy to save and share unfinished pages without stigma.
- A visible, respectful status (draft, work in progress, stub, maturity level) is **recommended**, exposed as metadata (`status:` or `maturity:`, [META-6](09-Metadata_and_Frontmatter.md)) and shown to readers.
- A private draft (visible to the author) and a public work-in-progress (visible to all, marked as unfinished) are different needs; engines are **encouraged** to support both.
- Engines **should not** require completeness checks, mandatory fields, or approvals before a page can exist; such requirements belong to optional review overlays ([COLL-14](07-Collaboration_Awareness_and_Governance.md#coll-14--review-as-an-overlay-not-a-gate)).
- Readers **should** be able to find unfinished pages that want help (a "stubs" or "WIP" view).

**Observed in.** Wikipedia's stubs and maintenance templates. esa.io's first-class **WIP** flag, where a post is created as WIP and "shipped" when ready, under the motto of *nurturing* information through three stages, share, develop, organize ("nothing is perfect from the beginning"). GROWI's WIP pages go further: a new page left untouched becomes WIP automatically, is excluded from search, and expires after a short period unless published. Confluence's unpublished drafts and content-state labels; Outline's drafts and publish step; Wiki.js unpublished pages; BookStack private drafts. Digital-garden conventions label notes *seedling*, *budding*, or *evergreen*. Dendron auto-creates stub notes. Logseq and Scrapbox / Cosense create pages on first reference, so almost every page starts incomplete by design.

**Interchange.** `status` in frontmatter; drafts **should** be included in exports when the exporting user has access, flagged so that importers do not publish them unintentionally ([XFER-5](10-Interchange_and_Portability.md)).

**Related.** AUTH-10, AUTH-13, NAV-3, COLL-14; PR-4.

---

## AUTH-5 · Section and Block Editing

**Also known as:** edit section, in-place block editing, per-item editing.
**Maturity:** Established.

**Context.** A contributor wants to fix one paragraph of a long page.

**Tension.** Editing the whole page is heavier for the author and raises the chance of conflicts with others editing elsewhere on the page. Editing a fragment needs stable fragment boundaries and a merge model.

**Guidance.**
- Engines **should** allow editing a part of a page (a section, block, or line) without loading the whole page into the editor.
- Edits to non-overlapping parts of the same page **should** merge automatically ([HIST-9](06-Temporal_Design_and_Revision_History.md#hist-9--gentle-conflict-resolution)).
- Partial edits **should** still produce page-level revisions with attribution, so that history stays whole.
- Block-level editing in block engines and section-level editing in document engines are two realizations of the same pattern; exports from either **should** be a coherent page ([Chapter 10](10-Interchange_and_Portability.md)).

**Observed in.** MediaWiki and DokuWiki section edit links. Notion, Logseq, Roam, Scrapbox / Cosense, and Federated Wiki edit blocks or lines in place; Federated Wiki keeps per-item history in the page journal. TiddlyWiki sidesteps the issue by keeping tiddlers small.

**Interchange.** Not applicable beyond block identifiers ([NAV-10](04-Discovery_Navigation_and_Topology.md#nav-10--section-anchors-and-block-addresses)).

**Related.** AUTH-1, HIST-9; PR-6.

---

## AUTH-6 · Starters and Templates

**Also known as:** page templates, blueprints, preload, scaffolds, namespace templates.
**Maturity:** Established.

**Context.** A new page of a familiar kind (meeting notes, a decision record, a how-to) is about to be created.

**Tension.** Blank pages are intimidating and produce inconsistent structure; rigid forms produce bureaucracy and empty fields. Templates that are also macros (expanding dynamically) do not travel between engines.

**Guidance.**
- Engines **should** let communities define starter content offered at page creation, and **should** keep it optional.
- Templates **should** be pages themselves, editable and versioned like any other ([COLL-12](07-Collaboration_Awareness_and_Governance.md#coll-12--the-wiki-documents-itself)).
- Structure that templates introduce (headings, properties) **should** be expressible in the portable profile, so that pages created from templates remain readable after export; structured fields are **encouraged** to map to frontmatter properties ([META-8](09-Metadata_and_Frontmatter.md)).
- Templates that are expanded dynamically on every view are an extension ([Chapter 12](12-Extensibility_Macros_and_Dynamic_Content.md)) and **should** be snapshotted on export.

**Observed in.** MediaWiki preload parameters and infobox templates; DokuWiki namespace templates; Confluence templates and blueprints; Notion page and database templates; Obsidian templates; Outline, BookStack, Growi, and esa.io page templates.

**Interchange.** Templates export as pages; template-driven structure exports as content and frontmatter.

**Related.** AUTH-4, COLL-12, NAV-16.

---

## AUTH-7 · Effortless Media

**Also known as:** drag-and-drop upload, paste image, attachments, media manager.
**Maturity:** Established.

**Context.** A contributor has a screenshot, a diagram, or a document that belongs on the page.

**Tension.** Media is heavy, licensed differently from text, hard to make accessible, and hard to move between engines. Making upload effortless invites unlicensed or inaccessible media; making it hard loses content.

**Guidance.**
- Pasting or dropping an image into the editor **should** attach it and insert a reference in one gesture.
- The engine **should** prompt for alternative text at the moment of insertion, without blocking ([AUTH-12](#auth-12--accessible-authoring), [A11Y-6](13-Accessibility_Internationalization_and_Web_Standards.md)).
- Attachments **should** be referenced relatively (so that bundles are self-contained) and **should** carry their own metadata: original filename, media type, license, source, alt text ([XFER-4](10-Interchange_and_Portability.md)).
- Engines are **encouraged** to deduplicate by content hash and to keep originals alongside any derived sizes.
- Hotlinking external images by default is **discouraged** on privacy and durability grounds; engines **may** offer to fetch and store a copy.

**Observed in.** Paste-to-upload is now universal in modern editors (Obsidian, Notion, Confluence, Growi, Wiki.js, Outline, HedgeDoc). MediaWiki's upload wizard and `[[File:...]]` syntax, with Wikimedia Commons requiring a license for every file, is the most rigorous model. DokuWiki's media manager and `{{...}}` syntax; PukiWiki's `&ref()` and attachment lists.

**Interchange.** `attachments/` in the bundle with a sidecar metadata file ([Appendix D](appendices/D-Portable_Wiki_Bundle_Example.md)).

**Related.** AUTH-12; Chapters 10 and 15.

---

## AUTH-8 · Never Lose a Draft

**Also known as:** autosave, draft recovery, edit recovery.
**Maturity:** Emerging.

**Context.** A browser crashes, a session times out, a laptop battery dies, a tab is closed by mistake.

**Tension.** Autosaving to the server turns every keystroke into a potential revision and raises privacy and noise questions; autosaving locally is invisible to collaborators and lost when the device is. Unsaved work, meanwhile, is the most demoralizing loss a contributor can suffer.

**Guidance.**
- Engines **should** preserve in-progress edits across crashes and session expiry, whether in the browser, on the device, or on the server.
- A session timeout **should never** discard an edit: the engine **should** let the user re-authenticate and continue.
- Autosaved drafts **should** be clearly distinct from published revisions ([HIST-8](06-Temporal_Design_and_Revision_History.md#hist-8--minor-edits-and-noise-control)) and **should** be discoverable ("you have an unsaved draft of this page").
- Local-first tools that write to disk immediately already satisfy the pattern; they **should** also guard against sync conflicts destroying work ([HIST-9](06-Temporal_Design_and_Revision_History.md#hist-9--gentle-conflict-resolution)).

**Observed in.** Continuous saving in Notion, Outline, Confluence drafts, Scrapbox / Cosense; file-level immediate writes in Obsidian and Logseq; DokuWiki's server-side drafts; MediaWiki's edit-recovery feature storing drafts in the browser; Growi's autosave.

**Interchange.** Drafts **may** be exported with `status: draft`.

**Related.** AUTH-4, HIST-8, HIST-9; PR-1.

---

## AUTH-9 · Sandbox

**Also known as:** playground, scratch page, try it here.
**Maturity:** Established.

**Context.** A newcomer wants to try editing without fear of breaking anything real.

**Tension.** Every page can be reverted, but newcomers do not yet believe that. A sandbox gives explicit permission to experiment, at the cost of occasional clutter.

**Guidance.**
- Public and community wikis **should** provide an explicitly consequence-free place to practise, linked from help and from the editor.
- Sandboxes **may** be reset periodically; the reset **should** be announced on the page itself.
- Personal sandboxes (a scratch area per user) are **encouraged** where user spaces exist.
- Desktop and local-first tools **may** satisfy the pattern with a disposable sample vault or demo project.

**Observed in.** Wikipedia's *Sandbox* and per-user sandboxes; DokuWiki's `playground` namespace; Confluence personal spaces; Obsidian's sandbox vault in its help menu; TiddlyWiki, where the empty file itself is the sandbox.

**Interchange.** Not applicable; sandboxes **may** be excluded from exports.

**Related.** AUTH-13, COLL-7; PR-3.

---

## AUTH-10 · Edit Summary as Micro-Narrative

**Also known as:** change comment, commit message, version comment, "what did you change?".
**Maturity:** Established.

**Context.** Someone looking at history, a watchlist, or Recent Changes wants to understand a change without opening the diff.

**Tension.** Summaries are invaluable for review and for understanding the story of a page, but requiring them adds friction and produces "asdf". Continuous-save engines have no natural moment to ask.

**Guidance.**
- Engines with explicit saves **should** offer an optional, short summary field and **should** show it in history, Recent Changes, feeds, and notifications.
- Requiring a summary is **discouraged**; prefilling one from context (the section edited, "reverted to revision N", "uploaded image") is **encouraged**.
- Continuous-save engines are **encouraged** to offer summaries at natural checkpoints (publish, "save a version", end of a session) ([HIST-10](06-Temporal_Design_and_Revision_History.md#hist-10--real-time-co-editing-with-durable-history)).
- Summaries **should** be exported with revisions ([XFER-7](10-Interchange_and_Portability.md)).

**Observed in.** MediaWiki's summary field with automatic section prefixes and auto-summaries; DokuWiki's edit summary; MoinMoin's comment field; git-backed wikis (Gollum, ikiwiki, Otter Wiki) where the commit message is the summary; Confluence's optional version comment. PukiWiki, Notion, Scrapbox / Cosense, and most real-time tools have no summaries, relying on diffs and timestamps instead.

**Interchange.** `summary` per revision in the history export.

**Related.** HIST-2, HIST-8, COLL-1; PR-6.

---

## AUTH-11 · Paste In, Copy Out

**Also known as:** clipboard portability, rich paste, copy as Markdown.
**Maturity:** Emerging.

**Context.** Knowledge arrives from emails, documents, chat, and other wikis, and leaves the same way, through the clipboard, far more often than through formal export.

**Tension.** Rich-text pasting is convenient and usually produces a mess of inline styles; plain-text pasting loses structure. Copying from a rendered page should give back something the reader could paste into another wiki.

**Guidance.**
- Pasting rich text **should** convert into the engine's native structure (headings, lists, links, tables, code) rather than into raw HTML or styled spans, discarding presentational noise.
- Pasting a URL to a page in the same wiki is **encouraged** to become a free link.
- Copying a selection from a rendered page **should** yield portable markup (Markdown in the portable profile is **recommended**) in addition to rich text, so that content moves between wikis through the clipboard without a converter.
- *Exploratory:* engines **may** place a `text/markdown` flavour on the clipboard alongside `text/html` and `text/plain`.

**Observed in.** Notion, Confluence, Outline, and Obsidian convert pasted HTML into blocks or Markdown. Obsidian and Logseq copy plain Markdown. VisualEditor in MediaWiki handles pasted rich text into wikitext. Scrapbox / Cosense converts pasted indented text into its line structure.

**Interchange.** The clipboard is the most-used interchange channel; it benefits directly from the portable profile ([Chapter 08](08-Markup_and_Syntax.md)).

**Related.** AUTH-2; Cunningham's *Overt*; PR-16.

---

## AUTH-12 · Accessible Authoring

**Also known as:** ATAG-aware editing, inclusive editor.
**Maturity:** Emerging.

**Context.** Contributors use screen readers, keyboards only, voice input, magnification, or have cognitive and motor differences. A wiki is an authoring tool as much as a reading tool.

**Tension.** Visual editors are often inaccessible; markup editors are accessible but demand syntax knowledge. Accessibility of the *output* depends on choices authors make (alt text, headings, table headers) that the tool can encourage but should not force.

**Guidance.**
- The editing interface **should** itself be accessible: keyboard operable, screen-reader compatible, with no time limits that discard work (W3C ATAG 2.0 Part A).
- The editor **should** help authors produce accessible content (ATAG 2.0 Part B): prompt for alt text, encourage heading hierarchy, support table headers, warn about link text like "click here", without blocking saves ([AUTH-13](#auth-13--gentle-guidance)).
- Markup editors **should** offer syntax help and highlighting; visual editors **should** expose structure (current heading level, list depth) to assistive technologies.
- Diff and history views used during authoring **should** be accessible ([HIST-2](06-Temporal_Design_and_Revision_History.md#hist-2--diff-as-a-first-class-view)).

**Observed in.** MediaWiki's accessibility work on VisualEditor and its alt-text prompts; Confluence and Notion with partial screen-reader support; CodeMirror-based editors in many engines offering accessible text editing. Few engines document ATAG conformance, which is an opportunity.

**Interchange.** Alt text and heading structure travel in content; see [A11Y](13-Accessibility_Internationalization_and_Web_Standards.md).

**Related.** AUTH-7, AUTH-13; Chapter 13.

---

## AUTH-13 · Gentle Guidance

**Also known as:** lint without blocking, inline help, suggestions not errors.
**Maturity:** Emerging.

**Context.** A contributor writes something imperfect: a broken table, a heading skipped, a citation missing, a link to nowhere.

**Tension.** Pointing out problems improves quality; refusing to save until they are fixed drives people away and contradicts the wiki's tolerance for imperfection. Silent acceptance lets problems accumulate invisibly.

**Guidance.**
- Engines **should** accept any input that can be interpreted (Cunningham's *Tolerant*) and **should** render it as well as possible rather than refusing.
- Quality hints **should** be offered as suggestions, in the editor or in maintenance views, never as save blockers.
- Syntax help **should** be one step away from the editor; a cheat sheet or toolbar is **encouraged** for markup editors.
- Automated checks (lint reports, "edit checks" that nudge for references or alt text) are **encouraged** when their tone is helpful and their findings are reviewable.

**Observed in.** MediaWiki's *Linter* extension reports markup problems in a special page instead of blocking saves; its *Edit check* nudges new editors to add references. DokuWiki ships a toolbar and a syntax page. Obsidian and Foam highlight syntax and unresolved links. Most engines accept arbitrary Markdown without validation, which is the pattern's baseline.

**Interchange.** Not applicable.

**Related.** AUTH-3, AUTH-4, AUTH-12; PR-4.

---

## AUTH-14 · Machine Assistance, Human Authorship

**Also known as:** AI-assisted editing, suggested edits, automated contributions.
**Maturity:** Exploratory.

**Context.** Language models and other automation can draft, summarize, translate, and tidy wiki content. Communities want the help without losing trust in the record.

**Tension.** Assistance lowers barriers and can improve accessibility and consistency; silent machine edits erode attribution, provenance, and the sense that a wiki is a human conversation. Licensing and factual reliability of generated text are unsettled.

**Guidance (exploratory).**
- Machine-generated or machine-suggested changes **should** be visible as such in revision metadata, and **should** be attributed to the human who accepted them.
- Assistance **should** be offered as a proposal (a draft, a suggested diff) that a person reviews, rather than applied silently.
- Fully automated edits (bots) **should** be flagged, filterable in Recent Changes, and reversible in bulk ([HIST-8](06-Temporal_Design_and_Revision_History.md#hist-8--minor-edits-and-noise-control)).
- Engines **may** record assistance in portable metadata (for example an `assistance:` field per revision) so that the information survives export; a shared vocabulary for this is an open question ([17 · Roadmap](17-Roadmap_and_Open_Questions.md)).
- Communities **should** be able to set their own norms, and engines **should** make those norms enforceable by visibility rather than by hidden policy.

**Observed in.** Wikipedia's long-standing bot policy, bot flags, and machine-learning revert tools with human review; assistant features in Notion, Confluence, and Outline that draft or summarize on request; community debates in several projects about labelling generated text. In 2025 and 2026 several engines (Docmost, SiYuan, Nuclino, GitBook, DocBase, Outline, Scrapbox / Cosense) added agent-oriented interfaces such as Model Context Protocol servers or agent command-line tools, which makes the attribution questions above practical rather than hypothetical.

**Interchange.** Revision metadata field, exploratory.

**Related.** HIST-4, HIST-8, COLL-7; PR-14, PR-18.

---

Previous: [04 · Discovery, Navigation and Topology](04-Discovery_Navigation_and_Topology.md) · Next: [06 · Temporal Design and Revision History](06-Temporal_Design_and_Revision_History.md)
