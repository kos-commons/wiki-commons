# 02 · Guiding Principles

> **Part I — Foundations** · **Status:** Working Draft 0.4 (October 2026)
> Previous: [01 · Core Concepts and Landscape](01-Core_Concepts_and_Landscape.md) · Next: [03 · Pattern Language Overview](03-Pattern_Language_Overview.md)

**In one sentence:** Before any pattern or format, a wiki is a stance toward people: that they can be trusted to improve a shared thing, that unfinished work deserves a home, and that knowledge should be free to move.

---

## 1. Why principles come first

Every wiki engine embodies answers to a few human questions. Who is allowed to change this? What happens if I get it wrong? Is it acceptable to leave something half-finished? Will I be able to find my way back? Does what I write here belong to me, to the group, or to the vendor?

Patterns and formats are the visible answers. Principles are the reasoning behind them. Stating the principles openly lets an engine make different design choices from another engine while still being recognizably "a wiki", and it gives communities a vocabulary for what they value.

The principles below are organized around the cognitive and social forces that make wikis work: psychological safety, tolerance of imperfection, shared mental models, serendipity, self-organization, and an ethic of portability. Each principle is given a short identifier (`PR-n`) so later chapters can point back to it.

A table at the end relates these principles to Ward Cunningham's original design principles for the first wiki, which remain remarkably current.

## 2. Psychological safety: removing the fear of ruin

Fear is the enemy of contribution. People hesitate to edit when they believe they could break something, lose something, or offend someone irreversibly. Wikis thrive when the cost of a mistake is low and visible, so that daring becomes rational.

### PR-1 · Nothing is ever truly lost

Every change should be recoverable. Revertability is not an administrative feature; it is the foundation that makes "be bold" reasonable advice. When contributors know that any edit can be undone in one step, they edit more, and communities can afford to be welcoming rather than defensive.

*Design implications:* non-destructive revision history ([HIST-1](06-Temporal_Design_and_Revision_History.md#hist-1--non-destructive-history)), one-step revert ([HIST-3](06-Temporal_Design_and_Revision_History.md#hist-3--revert-with-dignity)), soft deletion ([HIST-7](06-Temporal_Design_and_Revision_History.md#hist-7--soft-deletion)), draft recovery ([AUTH-8](05-Authoring_and_Participation.md#auth-8--never-lose-a-draft)).

### PR-2 · The page is a shared artifact, not a possession

A wiki page has contributors, not an owner. Design should avoid signalling individual ownership (author-locked pages, "my documents" framing as the primary model) and instead emphasize the collective artifact and its history. Attribution remains important, but it is attribution *to a change*, not a claim *on a page*.

*Design implications:* attribution per revision ([HIST-4](06-Temporal_Design_and_Revision_History.md#hist-4--attribution-per-revision)), shared artifact framing ([COLL-11](07-Collaboration_Awareness_and_Governance.md#coll-11--shared-artifact-not-possession)), open-by-default access ([COLL-10](07-Collaboration_Awareness_and_Governance.md#coll-10--open-by-default-narrow-with-care)).

### PR-3 · Mistakes are cheap, visible, and forgivable

Because everything is observable and reversible, a wiki can rely on *soft security*: the community sees and corrects rather than the system forbids. Engines should make correction easy and friendly, and should avoid interfaces that treat every edit as a potential attack. Research on Wikipedia has repeatedly shown that aggressive, impersonal reversion of newcomers' edits drives them away (Halfaker, Kittur and Riedl, 2011; Halfaker et al., 2013); the tone of the undo matters as much as its existence.

*Design implications:* soft security ([COLL-6](07-Collaboration_Awareness_and_Governance.md#coll-6--soft-security)), assume good faith ([COLL-7](07-Collaboration_Awareness_and_Governance.md#coll-7--assume-good-faith-by-default)), gentle conflict resolution ([HIST-9](06-Temporal_Design_and_Revision_History.md#hist-9--gentle-conflict-resolution)), sandbox ([AUTH-9](05-Authoring_and_Participation.md#auth-9--sandbox)).

## 3. Embracing imperfection: the incentive to contribute

A wiki is never finished. Its value comes from being improvable, and improvement requires that something imperfect exists to be improved. Engines that push for completion before publication suppress exactly the contributions they most need.

### PR-4 · Unfinished is a valid state

Stubs, drafts, "work in progress" markers, seedling notes, and open questions are legitimate content. Engines are encouraged to give them a visible, respectable status rather than hiding them or shaming them. Several modern tools have made this explicit: a first-class "WIP" flag on posts, or epistemic maturity labels such as *seedling*, *budding*, and *evergreen*. The same idea underlies Wikipedia's stubs and "under construction" notices.

*Design implications:* welcome the incomplete ([AUTH-4](05-Authoring_and_Participation.md#auth-4--welcome-the-incomplete)), a `status` or `maturity` field in portable metadata ([09](09-Metadata_and_Frontmatter.md)), gentle guidance instead of blocking validation ([AUTH-13](05-Authoring_and_Participation.md#auth-13--gentle-guidance)).

### PR-5 · Absence is an invitation

A link to a page that does not yet exist is one of the wiki's great inventions. It expresses an intention, reserves a name, and creates a visible gap that someone will feel compelled to fill. This "vacuum effect" turns the structure of the wiki into a to-do list that writes itself; on Wikipedia, most new articles are created shortly after a link to them appears somewhere else (Spinellis and Louridas, 2008). Engines should keep dangling links visible and actionable rather than suppressing them or auto-creating empty pages silently.

*Design implications:* dangling link as invitation ([NAV-3](04-Discovery_Navigation_and_Topology.md#nav-3--dangling-link-as-invitation)), health views such as wanted pages ([NAV-15](04-Discovery_Navigation_and_Topology.md#nav-15--health-views-orphans-wanted-dead-ends)), search or create ([NAV-5](04-Discovery_Navigation_and_Topology.md#nav-5--search-or-create)).

### PR-6 · Progress over perfection

Small, frequent, imperfect edits are healthier than rare, large, polished ones: they are easier to review, easier to revert, and easier to build upon. Engines can encourage this with low-friction editing, section-level edits, short edit summaries, and a history view that makes small steps legible.

*Design implications:* edit is one step away ([AUTH-1](05-Authoring_and_Participation.md#auth-1--edit-is-one-step-away)), section and block editing ([AUTH-5](05-Authoring_and_Participation.md#auth-5--section-and-block-editing)), edit summary as micro-narrative ([AUTH-10](05-Authoring_and_Participation.md#auth-10--edit-summary-as-micro-narrative)), minor edits ([HIST-8](06-Temporal_Design_and_Revision_History.md#hist-8--minor-edits-and-noise-control)).

## 4. Shared mental models: intuitive "wiki-ness"

People carry expectations from one wiki to the next. A design that honours those expectations feels instantly usable; one that violates them for no reason feels foreign even when it is objectively fine.

### PR-7 · One model: pages, links, history

The simplest wiki model has three parts: there are **pages** (or blocks within pages), pages **link** to one another by name, and every page has a **history**. Everything else (categories, templates, queries, discussions) can be explained in terms of these three. Engines are encouraged to keep this model learnable in a minute and to make additional concepts optional and explainable in its terms.

*Design implications:* page as the unit of address ([NAV-1](04-Discovery_Navigation_and_Topology.md#nav-1--page-as-the-unit-of-address)), free links ([NAV-2](04-Discovery_Navigation_and_Topology.md#nav-2--free-links)), non-destructive history ([HIST-1](06-Temporal_Design_and_Revision_History.md#hist-1--non-destructive-history)).

### PR-8 · Conceal complexity, expose capability

The internal machinery of a wiki (parsers, caches, storage, conflict resolution) should stay invisible. What should be visible is *capability*: that one can edit, see what changed, undo, find what links here. Cunningham's principle of the *mundane* applies: a small number of conventions should give access to the most useful behaviours.

*Design implications:* read-to-edit transition ([AUTH-1](05-Authoring_and_Participation.md#auth-1--edit-is-one-step-away)), two views of one document ([AUTH-2](05-Authoring_and_Participation.md#auth-2--two-views-of-one-document)), the capability-oriented framing of Part III.

### PR-9 · Predictability across engines

When a convention is already widely shared, following it is a kindness to users: `[[double brackets]]` for links, a visible marker for pages that do not exist yet, a history view with diffs, a Recent Changes list. Where an engine chooses to differ, it is encouraged to do so deliberately and to explain the difference in its documentation and its exports.

*Design implications:* the whole of Part II; the syntax crosswalk in [Appendix B](appendices/B-Syntax_Crosswalk.md).

## 5. Architectural serendipity: fostering unintended discovery

Hierarchies are good for storage and poor for discovery. The wiki's defining structural insight is that *links are the architecture*: meaning emerges from a mesh of associations that no one designed as a whole.

### PR-10 · Links are the architecture

A wiki does not need a complete taxonomy before it can be useful. Pages can be placed by linking alone; hierarchy, where offered, should be optional scaffolding rather than a prerequisite. Engines are encouraged to treat the link graph as a first-class structure: computed backlinks, related pages, and link health are features of the graph, not add-ons.

*Design implications:* flat names with optional hierarchy ([NAV-6](04-Discovery_Navigation_and_Topology.md#nav-6--flat-names-optional-hierarchy)), backlinks ([NAV-4](04-Discovery_Navigation_and_Topology.md#nav-4--backlinks-what-links-here)), graph as a lens ([NAV-14](04-Discovery_Navigation_and_Topology.md#nav-14--graph-as-a-lens-not-a-map)).

### PR-11 · Design for the cognitive jump

Readers learn by jumping: from the page they came for to the page they did not know they needed. Contextual links in running text, backlink panels, "related pages" computed from shared links, and the two-hop neighbourhood popularized by line-based wikis all create opportunities for such jumps. Engines should protect these affordances even as they add search and recommendations.

*Design implications:* related pages and the two-hop neighbourhood ([NAV-12](04-Discovery_Navigation_and_Topology.md#nav-12--related-pages-and-the-two-hop-neighborhood)), interwiki links ([NAV-13](04-Discovery_Navigation_and_Topology.md#nav-13--interwiki-links)), transclusion with provenance ([NAV-16](04-Discovery_Navigation_and_Topology.md#nav-16--transclusion-with-provenance)).

### PR-12 · Make the whole observable

A wiki is a shared workspace, and the work should be visible: who changed what, where activity is happening, which pages are wanted. Observability is how a community coordinates without a manager, a phenomenon the literature calls *stigmergy* (Elliott, 2006): people act on the traces others leave. Recent Changes was the first social feature of the first wiki, and it remains the heartbeat of every healthy one.

*Design implications:* recent changes ([COLL-1](07-Collaboration_Awareness_and_Governance.md#coll-1--recent-changes)), visible activity ([COLL-8](07-Collaboration_Awareness_and_Governance.md#coll-8--visible-activity-and-contribution-history)), page lifecycle at a glance ([HIST-11](06-Temporal_Design_and_Revision_History.md#hist-11--page-lifecycle-at-a-glance)).

## 6. Self-organizing communities: organic governance

Rules imposed from outside rarely fit. Wikis have shown that communities can govern themselves when the software gives them visibility, reversibility, and a place to talk.

### PR-13 · Soft security over hard locks

Prefer mechanisms that make bad changes easy to see and undo over mechanisms that make good changes hard to make. Locks, approvals, and permissions have their place, especially in regulated settings, but they should be added deliberately where needed rather than applied everywhere by default.

*Design implications:* soft security ([COLL-6](07-Collaboration_Awareness_and_Governance.md#coll-6--soft-security)), review as an overlay rather than a gate ([COLL-14](07-Collaboration_Awareness_and_Governance.md#coll-14--review-as-an-overlay-not-a-gate)).

### PR-14 · Assume good faith, and make trust visible

Most edits are well-intentioned. Interfaces should default to treating contributors as colleagues: explaining rather than warning, inviting rather than gatekeeping. At the same time, trust is built by visibility, so attribution, contribution history, and discussion should be easy to find.

*Design implications:* assume good faith by default ([COLL-7](07-Collaboration_Awareness_and_Governance.md#coll-7--assume-good-faith-by-default)), talk beside content ([COLL-3](07-Collaboration_Awareness_and_Governance.md#coll-3--talk-beside-content)).

### PR-15 · The wiki documents itself

A wiki's conventions, style guides, templates, and governance decisions should live *in the wiki*, as pages anyone can read and improve. The software can encourage this by making conventions discoverable (templates offered at creation time, help pages linked from the editor) rather than burying them in configuration.

*Design implications:* the wiki documents itself ([COLL-12](07-Collaboration_Awareness_and_Governance.md#coll-12--the-wiki-documents-itself)), starters and templates ([AUTH-6](05-Authoring_and_Participation.md#auth-6--starters-and-templates)).

## 7. Portability as an ethic

The final group of principles concerns the relationship between the wiki and the software that hosts it. They are what makes the rest of this suite necessary.

### PR-16 · Knowledge outlives software

Formats, tools, and companies come and go; the knowledge a community accumulates should not go with them. "File over app" (Ango, 2023), the maxim popularized by local-first note tools, and the seven ideals of local-first software (Kleppmann et al., 2019) express the same idea from the user's side: if the files are durable and legible, the app is replaceable. Engines are encouraged to treat their export as a product, not a chore, and to make the plainest possible representation of content available at all times.

*Design implications:* Chapters [08](08-Markup_and_Syntax.md), [09](09-Metadata_and_Frontmatter.md), and [10](10-Interchange_and_Portability.md); raw source access per page ([API-2](11-APIs_and_Discovery.md)).

### PR-17 · Declare what you drop

Conversions between engines are lossy. That is acceptable; what is not acceptable is silent loss. Exporters and importers should report what they could not carry over, mark degraded content in place, and preserve the original where it is cheap to do so.

*Design implications:* graceful degradation and snapshot envelopes ([12](12-Extensibility_Macros_and_Dynamic_Content.md)), fidelity levels and import reports ([10](10-Interchange_and_Portability.md)).

### PR-18 · Attribution travels with content

Authorship is part of the knowledge. When content moves between engines, the record of who contributed what should move with it, in a form that respects both the license under which it was contributed and the privacy of the contributors.

*Design implications:* history export ([10](10-Interchange_and_Portability.md)), licensing and attribution ([15](15-Licensing_and_Attribution.md)), privacy of contributor data ([14](14-Security_Privacy_and_Trust.md)).

## 8. Relationship to Cunningham's original design principles

Ward Cunningham later wrote down, "from memory", the design principles he had sought to satisfy with the first wiki in 1995; the list is still on the original site. The table quotes them and shows where this suite carries each forward (see [Appendix F](appendices/F-References.md) for the source).

| Original principle (quoted) | Essence | Carried forward in |
|---|---|---|
| **Simple** | "Easier to use than abuse. A wiki that reinvents HTML markup has lost the path!" | PR-8, Chapter 08 |
| **Open** | "Should a page be found to be incomplete or poorly organized, any reader can edit it as they see fit." | PR-2, PR-13, AUTH-1 |
| **Incremental** | "Pages can cite other pages, including pages that have not been written yet." | PR-5, NAV-3 |
| **Organic** | "The structure and text content of the site are open to editing and evolution." | PR-4, PR-10, NAV-6 |
| **Mundane** | "A small number of (irregular) text conventions will provide access to the most useful page markup." | PR-8, Chapter 08 |
| **Universal** | "The mechanisms of editing and organizing are the same as those of writing, so that any writer is automatically an editor and organizer." | PR-7, AUTH-2 |
| **Overt** | "The formatted (and printed) output will suggest the input required to reproduce it." | AUTH-2, AUTH-11 |
| **Unified** | "Page names will be drawn from a flat space so that no additional context is required to interpret them." | NAV-6, NAV-9 |
| **Precise** | "Pages will be titled with sufficient precision to avoid most name clashes, typically by forming noun phrases." | NAV-2, NAV-8 |
| **Tolerant** | "Interpretable (even if undesirable) behavior is preferred to error messages." | PR-4, AUTH-13, MKUP degradation rules |
| **Observable** | "Activity within the site can be watched and reviewed by any other visitor to the site." | PR-12, COLL-1, COLL-8 |
| **Convergent** | "Duplication can be discouraged or removed by finding and citing similar or related content." | NAV-12, NAV-15, NAV-8 |
| **Trust**, **Fun**, **Sharing**, **Interaction** | Added on the same page by other wiki authors, "not of primary concern" to Cunningham: "Trust the people, trust the process, enable trust-building"; "Everybody can contribute; nobody has to." | PR-3, PR-14, COLL-7 |

A later editor of that page remarks that *Unified* and *Precise* are the least convincing points for non-English wikis and for engines with namespaces; the pattern language takes that criticism seriously ([NAV-6](04-Discovery_Navigation_and_Topology.md#nav-6--flat-names-optional-hierarchy)). That so much of a 1995 list maps onto a 2026 guideline is not nostalgia. It is evidence that the wiki is a stable idea whose implementations keep changing, which is exactly why guidelines for its shared ground are worth writing.

---

Previous: [01 · Core Concepts and Landscape](01-Core_Concepts_and_Landscape.md) · Next: [03 · Pattern Language Overview](03-Pattern_Language_Overview.md)
