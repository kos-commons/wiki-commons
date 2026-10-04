# 03 · Pattern Language Overview

> **Part II — The Pattern Language** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [02 · Guiding Principles](02-Guiding_Principles.md) · Next: [04 · Discovery, Navigation and Topology](04-Discovery_Navigation_and_Topology.md)

**In one sentence:** Part II describes the wiki experience as a pattern language: fifty-odd named, reusable solutions with their context, tensions, and real-world examples, organized so that designers, developers, and communities can talk about "wiki-ness" precisely without prescribing layouts.

---

## 1. Why a pattern language

There is a pleasing circularity in describing wikis with patterns. The first wiki, Ward Cunningham's WikiWikiWeb, was created in 1995 to host the Portland Pattern Repository, a collection of software design patterns inspired by Christopher Alexander's *A Pattern Language* (1977). The wiki was invented as a tool for writing pattern languages collaboratively; thirty years later, the wiki itself is a pattern language waiting to be written down.

A pattern, in Alexander's sense, is a recurring solution to a recurring problem in a context, stated so that it can be reused "a million times over, without ever doing it the same way twice". That last clause is the point. A pattern language is the opposite of a UI specification: it says *what a solution achieves and why*, and leaves the *how* to each designer. This is exactly the register the source report asked for ("a wiki SHOULD provide a non-destructive revision history", not "a wiki MUST use a relational database").

Patterns also travel well between engine generations. "Dangling Link as Invitation" is realized as a red link in one engine, a trailing question mark in another, a dimmed link in a third, and an implicit page creation in a fourth. The pattern is the same; the rendering is free.

## 2. Pattern format

Every pattern in Chapters 04 to 07 uses the same structure.

| Field | Content |
|---|---|
| **Code and name** | A stable identifier (`NAV-3`) and a Title Case name (`Dangling Link as Invitation`). |
| **Also known as** | Other names in use across engines and communities. |
| **Maturity** | *Established* (found in most engines of several generations), *Emerging* (common in modern tools, spreading), or *Exploratory* (promising, rarely implemented). |
| **Context** | When the pattern applies. |
| **Tension** | The forces the pattern balances: the problem, stated as competing needs. |
| **Guidance** | What an engine should, is encouraged to, or may do. Capability language, never layout. |
| **Observed in** | How existing engines realize the pattern, across generations. Descriptive, not exhaustive, not an endorsement. |
| **Interchange** | How the pattern's data survives export and import, and how it degrades. Links to Part III where relevant. |
| **Related** | Neighbouring patterns and principles. |

Codes are permanent once released. Names may be lightly edited for clarity, but the code is what should be cited.

## 3. The patterns

### Chapter 04 · Discovery, Navigation and Topology (`NAV`)

| Code | Pattern | Maturity |
|---|---|---|
| NAV-1 | Page as the Unit of Address | Established |
| NAV-2 | Free Links | Established |
| NAV-3 | Dangling Link as Invitation | Established |
| NAV-4 | Backlinks (What Links Here) | Established |
| NAV-5 | Search or Create | Established |
| NAV-6 | Flat Names, Optional Hierarchy | Established |
| NAV-7 | Tags and Categories | Established |
| NAV-8 | Redirects and Aliases | Established |
| NAV-9 | Stable Identity Beneath the Title | Emerging |
| NAV-10 | Section Anchors and Block Addresses | Emerging |
| NAV-11 | Spatial Orientation | Established |
| NAV-12 | Related Pages and the Two-Hop Neighborhood | Emerging |
| NAV-13 | Interwiki Links | Established |
| NAV-14 | Graph as a Lens, Not a Map | Emerging |
| NAV-15 | Health Views: Orphans, Wanted, Dead Ends | Established |
| NAV-16 | Transclusion with Provenance | Established |

### Chapter 05 · Authoring and Participation (`AUTH`)

| Code | Pattern | Maturity |
|---|---|---|
| AUTH-1 | Edit Is One Step Away | Established |
| AUTH-2 | Two Views of One Document | Established |
| AUTH-3 | Preview and Live Feedback | Established |
| AUTH-4 | Welcome the Incomplete | Established |
| AUTH-5 | Section and Block Editing | Established |
| AUTH-6 | Starters and Templates | Established |
| AUTH-7 | Effortless Media | Established |
| AUTH-8 | Never Lose a Draft | Emerging |
| AUTH-9 | Sandbox | Established |
| AUTH-10 | Edit Summary as Micro-Narrative | Established |
| AUTH-11 | Paste In, Copy Out | Emerging |
| AUTH-12 | Accessible Authoring | Emerging |
| AUTH-13 | Gentle Guidance | Emerging |
| AUTH-14 | Machine Assistance, Human Authorship | Exploratory |

### Chapter 06 · Temporal Design and Revision History (`HIST`)

| Code | Pattern | Maturity |
|---|---|---|
| HIST-1 | Non-Destructive History | Established |
| HIST-2 | Diff as a First-Class View | Established |
| HIST-3 | Revert with Dignity | Established |
| HIST-4 | Attribution per Revision | Established |
| HIST-5 | Permalinks to Revisions | Established |
| HIST-6 | Rename Preserves History | Established |
| HIST-7 | Soft Deletion | Established |
| HIST-8 | Minor Edits and Noise Control | Established |
| HIST-9 | Gentle Conflict Resolution | Established |
| HIST-10 | Real-Time Co-Editing with Durable History | Emerging |
| HIST-11 | Page Lifecycle at a Glance | Established |
| HIST-12 | Suppression Without Erasure | Emerging |

### Chapter 07 · Collaboration, Awareness and Governance (`COLL`)

| Code | Pattern | Maturity |
|---|---|---|
| COLL-1 | Recent Changes | Established |
| COLL-2 | Watch and Subscribe | Established |
| COLL-3 | Talk Beside Content | Established |
| COLL-4 | Document Mode and Thread Mode | Established |
| COLL-5 | Inline Comments and Annotations | Emerging |
| COLL-6 | Soft Security | Established |
| COLL-7 | Assume Good Faith by Default | Established |
| COLL-8 | Visible Activity and Contribution History | Established |
| COLL-9 | Notifications with Restraint | Emerging |
| COLL-10 | Open by Default, Narrow with Care | Established |
| COLL-11 | Shared Artifact, Not Possession | Established |
| COLL-12 | The Wiki Documents Itself | Established |
| COLL-13 | Fork Instead of Fight | Exploratory |
| COLL-14 | Review as an Overlay, Not a Gate | Emerging |

## 4. Three ways to read the language

The same patterns can be approached from different directions. The source report proposed three organizing perspectives; all three are offered here as indexes. Pick the one that matches your question.

### 4.1 By user journey (experience-driven)

Follow a person from first contact to long-term stewardship.

1. **Core values of the wiki experience** → [02 · Guiding Principles](02-Guiding_Principles.md)
2. **Discovery and navigation (finding knowledge)** → NAV-2, NAV-3, NAV-4, NAV-5, NAV-6, NAV-7, NAV-11, NAV-12, NAV-13, NAV-14
3. **Reading and contextualization (understanding knowledge)** → NAV-8, NAV-10, NAV-16, HIST-11, COLL-3, COLL-4, AUTH-4 (maturity markers)
4. **Participation and editing (lowering the barrier)** → AUTH-1 through AUTH-13, HIST-9
5. **Connection and expansion (weaving knowledge)** → NAV-3, NAV-6, NAV-7, NAV-13, NAV-16, COLL-13
6. **Temporal evolution (fostering and tracking change)** → HIST-1 through HIST-12, COLL-1, COLL-2

### 4.2 By structural component (pattern-catalogue view)

For designers and developers choosing how to build a specific part of an engine.

1. **Knowledge architecture and topology** (graph vs. tree, visible connections) → NAV-1, NAV-6, NAV-7, NAV-9, NAV-12, NAV-14, NAV-16
2. **Authoring and content expression** (markup vs. WYSIWYG, media, structured data) → AUTH-2, AUTH-3, AUTH-5, AUTH-6, AUTH-7, AUTH-11, AUTH-12; Chapters 08 and 09
3. **Temporal design and revision control** (immutable histories, conflicts) → HIST-1 through HIST-12
4. **Awareness and open governance** (open editing vs. control, activity tracking) → COLL-1, COLL-2, COLL-6, COLL-7, COLL-8, COLL-9, COLL-10, COLL-14
5. **Context preservation and metadata** (talk pages, attribution) → COLL-3, COLL-4, COLL-5, HIST-4, HIST-11, NAV-8, NAV-9; Chapter 09

### 4.3 By cognitive and psychological effect (mindset view)

For those asking what the patterns do to the people who use them.

1. **Designing psychological safety** (removing fear of ruin) → HIST-1, HIST-3, HIST-5, HIST-7, HIST-9, AUTH-8, AUTH-9, COLL-6, COLL-7, COLL-11
2. **Embracing imperfection** (incentivizing contribution) → AUTH-4, AUTH-10, AUTH-13, NAV-3, NAV-15
3. **Shared mental models** (intuitive wiki-ness) → NAV-1, NAV-2, AUTH-1, AUTH-2, HIST-2, COLL-1, COLL-3
4. **Architectural serendipity** (unintended discovery) → NAV-4, NAV-12, NAV-13, NAV-14, NAV-16
5. **Self-organizing communities** (organic governance) → COLL-1, COLL-2, COLL-6, COLL-7, COLL-8, COLL-12, COLL-13, COLL-14

## 5. How to use the pattern language

- **In design reviews.** Walk through the relevant chapter and ask, for each pattern, "do we realize this, and if not, is that deliberate?" Deliberate omissions are fine; accidental ones are where the value lies.
- **In migration planning.** The *Interchange* field of each pattern tells you which data must travel for the pattern to survive a move between engines. Together they form a checklist for exporters and importers (see [10 · Interchange and Portability](10-Interchange_and_Portability.md)).
- **In documentation and onboarding.** Pattern names give communities a shared vocabulary ("our wiki has backlinks but no dangling-link invitations, so wanted pages need a different mechanism").
- **In research and teaching.** The *Observed in* fields collect comparative evidence across engine generations; corrections and additions are welcome through [CONTRIBUTING](../CONTRIBUTING.md).

## 6. Relationship to Part III

Part II says *what* a wiki offers people. Part III says *how that offer travels* between engines: the markup that carries links, the metadata that carries status and attribution, the bundle that carries history, the API that exposes it all. A pattern without a portable representation is fragile; a format without a pattern behind it is pointless. The two parts are written to be read together.

---

Previous: [02 · Guiding Principles](02-Guiding_Principles.md) · Next: [04 · Discovery, Navigation and Topology](04-Discovery_Navigation_and_Topology.md)
