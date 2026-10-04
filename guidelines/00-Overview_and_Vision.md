# 00 · Overview and Vision

> **Part I — Foundations** · **Status:** Working Draft 0.1 (October 2026)
> Index: [README](../README.md) · Next: [01 · Core Concepts and Landscape](01-Core_Concepts_and_Landscape.md)

**In one sentence:** Wiki Commons is a set of open, voluntary guidelines that help wiki engines of every generation keep the knowledge entrusted to them portable, legible, and alive, without asking any of them to become the same product.

---

## 1. Why these guidelines exist

Wikis are three decades old. In that time they have grown from a single Perl script with CamelCase links into an entire family of software: encyclopedic engines serving billions of page views, flat-file wikis that fit on a USB stick, single-file wikis that live inside one HTML document, git-backed static wikis, enterprise knowledge bases, block-based note tools, outliners, local-first personal knowledge graphs, and real-time collaborative documents that have quietly become "the wiki" for many teams.

Despite that success, no shared standard emerged. Containers have OCI, the web has the W3C and the IETF, but wikis rely on fragmented de facto conventions and historical habits:

- **Markup never converged.** WikiCreole (2006) tried to become the universal wiki markup and did not reach the largest engines. Wikitext remains powerful but is difficult to parse outside its home. Markdown became the practical common tongue, yet it has no native way to express the things that make a wiki a wiki: `[[free links]]`, transclusion, macros, backlinks.
- **Data never flowed.** There is no shared way to ask a wiki for a page, its history, or its metadata. Moving a knowledge base from one engine to another still means bespoke scripts, lossy exports, and lost attribution.
- **Patterns stayed implicit.** Red links, the Read / Edit / History / Discussion tabs, Recent Changes, diffs, and "assume good faith" are understood by millions of people, but they are documented nowhere as a shared design vocabulary.

Meanwhile the ground has shifted. Pages are becoming collections of blocks. Editing is becoming simultaneous. Knowledge bases are becoming local-first files that sync, rather than servers that serve. Commercial platforms hold more collective knowledge than ever, with correspondingly weaker incentives to let it leave.

These guidelines are a response to that situation. They do not try to win the markup war or to specify "the wiki protocol". They try to name what the wiki family already shares, to recommend a small set of portable conventions where sharing is cheap and valuable, and to describe the user experience patterns that make a wiki feel trustworthy and alive.

## 2. Vision: knowledge that outlives its software

The guiding aspiration can be stated simply:

> **The knowledge people put into a wiki should outlive the software it was written in.**

Everything else follows from three commitments.

### 2.1 Portability over feature parity

No two wikis need the same features. What they share should be the ability to hand over the core of what users created: text, structure, links, metadata, authorship, and history, in a form another engine can read. A wiki does not need to be able to *run* another wiki's macros; it needs to be able to *read* what they produced.

### 2.2 Shared patterns over shared code

Interoperability between wikis is as much about shared mental models as shared bytes. A person who has learned one wiki should feel at home in another: links that invite creation, history that can be undone, discussion that sits beside content. These guidelines describe such patterns as a **pattern language**, in the sense of Christopher Alexander and the early wiki community: named, reusable solutions with their context and trade-offs, not prescriptions of layout.

### 2.3 Graceful degradation over all-or-nothing

Rich features are welcome. What matters is that each one has a defined "downhill" path: a dynamic table becomes a static table, a transcluded block becomes an inline copy with a note, an unknown macro becomes visible plain text rather than silence. Degradation should be *declared* so that importers and users know what they are looking at.

## 3. What this is, and what it is not

**This is:**

- A **guideline suite**: recommendations and rationale for people building wiki engines, plugins, migration tools, and the communities around them.
- A **pattern language**: a catalogue of named user-experience patterns, with context, tensions, and examples drawn from real engines.
- A set of **interchange conventions**: a Markdown profile, a metadata vocabulary, a bundle layout, and API capabilities that engines are encouraged to support alongside their native formats.
- A **map of the landscape**: a survey of classic, transitional, and modern engines showing what they have in common and where they differ.

**This is not:**

- A protocol or a wire format that engines must implement.
- A certification scheme. Conformance profiles exist for self-assessment and clear communication only.
- A UI kit or style guide. No sidebar position, button placement, or color is mandated anywhere in this suite.
- A replacement for existing standards. Where the web already has a good answer (CommonMark, WCAG, OpenAPI, Atom, OAuth, Dublin Core, schema.org), these guidelines point to it instead of inventing another.

## 4. Guidance language

These documents deliberately avoid the imperative vocabulary of IETF-style specifications. The words below are used consistently:

| Term | Meaning in this suite |
|---|---|
| **should** / **recommended** | The default choice. Following it brings clear interoperability or user-experience benefits. Deviations are legitimate when a reason exists and, ideally, is documented. |
| **encouraged** | A good idea whose value depends on context. Worth doing when it fits the engine's goals. |
| **may** / **optional** | Explicitly permitted. Mentioned so that engines choosing it do so in a compatible way. |
| **discouraged** / **should not** | Known to cause portability or usability problems. Not forbidden, but worth a second thought and a documented reason. |
| **exploratory** | A forward-looking idea that is not yet widely practised. Included to orient, not to recommend. |

The word **must** appears only when quoting another standard, or when describing a logical necessity (for example, "a revision must have a parent to be diffed against"). It never introduces a requirement of this suite.

Sections titled **Observed in** describe how existing engines behave. They are evidence, not endorsements, and they are not exhaustive.

## 5. Who this is for

- **Engine developers** of every kind: database-backed encyclopedic wikis, flat-file wikis, git-backed and static wikis, single-file wikis, enterprise knowledge bases, block-based and outliner tools, local-first note systems, and real-time collaborative documents.
- **Plugin, theme, and editor authors**, who shape how content is written and how it degrades.
- **Migration and conversion tool authors**, for whom the interchange chapters are written most directly.
- **Operators and administrators** choosing, configuring, or migrating a wiki.
- **Designers and researchers** who want a shared vocabulary for wiki experience.
- **Communities of contributors**, whose norms are as much a part of a wiki as its software.

## 6. Principles behind the guidelines themselves

1. **Evidence first.** Recommendations are grounded in what real engines do. Where the field has converged, the guidelines name the convergence; where it has not, they say so and explain the trade-offs.
2. **Engine-plural.** MediaWiki shaped the public imagination of what a wiki is, but it is one voice among many. Flat-file, single-file, block-based, outliner, static, and federated engines each solved problems the others did not. The guidelines draw on all of them.
3. **Small core, optional layers.** The portable core is intentionally minimal: text, links, metadata, authorship. Everything else is layered and optional.
4. **Lossy is fine when declared.** Round-trips are rarely perfect. A conversion that reports what it dropped is more trustworthy than one that pretends to be lossless.
5. **Humans before machines.** Portability serves people: the contributor who wants to leave, the reader who wants to understand, the newcomer who wants to dare an edit.
6. **Lean on the web.** Reuse existing standards for timestamps, language tags, identifiers, feeds, link relations, accessibility, and licensing.
7. **Forward-looking.** Blocks, local-first storage, CRDT-based co-editing, federation, and machine-assisted authoring are treated as part of the family's future, not as exceptions to be ignored.

## 7. Scope and non-goals

### 7.1 In scope

- Exchange formats for pages, links, metadata, attachments, discussions, and history.
- Semantics of links: free links, aliases, namespaces, anchors, block references, redirects, interwiki links, and how they degrade.
- A vocabulary for page metadata and its mapping to established vocabularies.
- The behaviour, not the storage, of revision history: immutability, attribution, diff, revert.
- User-experience patterns, expressed as capabilities ("a reader can see what changed") rather than layouts.
- Capabilities an engine's API is encouraged to expose, and how to describe them with existing standards.
- Accessibility, internationalization, licensing, privacy, and security as they relate to the above.

### 7.2 Explicitly out of scope

These are left to each engine, for the reasons given in the source report and expanded in [01 · Core Concepts and Landscape](01-Core_Concepts_and_Landscape.md):

1. **Backend architecture and storage.** Relational database, flat files, git, a single HTML file, a CRDT document: all are legitimate. Only the *exchange* representation is discussed.
2. **Specific UI layouts and styling.** Guidelines speak of what a user can do, never where a control sits or how it looks.
3. **Access control models.** Permissions vary from fully open public wikis to directory-integrated enterprise deployments. The guidelines touch only on how access decisions should be *visible* and how they interact with portability.
4. **Execution of dynamic code.** Macros, templates, embedded scripts, and query languages are engine-specific extensions. The guidelines address only how they are *declared* and how their output *degrades*.

## 8. How the suite is organized

The suite is a collection of Markdown files that can be read in order or consulted independently. Chapters are numbered; patterns and recommendations carry stable identifiers so that they can be cited.

```
guidelines/
  Part I   — Foundations
    00-Overview_and_Vision.md                      (this document)
    01-Core_Concepts_and_Landscape.md
    02-Guiding_Principles.md
  Part II  — The Pattern Language
    03-Pattern_Language_Overview.md
    04-Discovery_Navigation_and_Topology.md
    05-Authoring_and_Participation.md
    06-Temporal_Design_and_Revision_History.md
    07-Collaboration_Awareness_and_Governance.md
  Part III — Interoperability Guidelines
    08-Markup_and_Syntax.md
    09-Metadata_and_Frontmatter.md
    10-Interchange_and_Portability.md
    11-APIs_and_Discovery.md
    12-Extensibility_Macros_and_Dynamic_Content.md
    13-Accessibility_Internationalization_and_Web_Standards.md
    14-Security_Privacy_and_Trust.md
    15-Licensing_and_Attribution.md
  Part IV  — Adoption
    16-Conformance_Profiles_and_Self_Assessment.md
    17-Roadmap_and_Open_Questions.md
  appendices/
    A-Wiki_Engine_Landscape.md
    B-Syntax_Crosswalk.md
    C-Portable_Page_Metadata_Reference.md
    D-Portable_Wiki_Bundle_Example.md
    E-Glossary.md
    F-References.md
schemas/          machine-readable JSON Schemas for metadata and manifests
examples/         a small, complete Portable Wiki Bundle
tools/            bundle validator, link checkers, and the site assembly script
book/             mdBook configuration for the published site
```

### 8.1 Identifiers

- **Patterns** are named in Title Case and carry a code: `NAV-3 · Dangling Link as Invitation`, `HIST-1 · Non-Destructive History`.
- **Recommendations** in Part III carry a code per chapter: `MKUP-4`, `META-2`, `XFER-7`, `API-3`, `EXT-2`, `A11Y-1`, `I18N-3`, `SEC-5`, `PRIV-2`, `LIC-1`.
- **Conformance profiles** in Chapter 16 are lists of these codes. Nothing else is needed to "conform": a profile is a vocabulary for saying what an engine does.

Once published in a numbered release, an identifier is never reused for a different meaning. Retired items are marked as deprecated and kept for reference.

### 8.2 Reading paths

Different readers can take different paths through the same material:

- **"I build an engine and want it to interoperate."** Read 00, 01, then Part III in order, then 16.
- **"I design the experience of a wiki."** Read 00, 02, 03, then Part II, then 13.
- **"I write a migration or conversion tool."** Read 08, 09, 10, Appendix B, Appendix C, and the example bundle.
- **"I lead a community and want to understand what good looks like."** Read 00, 02, 07, and 15.
- **"I want to understand the field."** Read 01 and Appendix A.

Chapter 03 also offers three alternative indexes into the pattern language: by user journey, by structural component, and by cognitive effect.

## 9. Relationship to existing standards

The suite stands on existing open standards and names them explicitly rather than paraphrasing them:

- **Markup:** CommonMark and GitHub Flavored Markdown as the baseline for interchange; the `text/markdown` media type (RFC 7763) with its `variant` parameter.
- **Metadata and identifiers:** YAML, JSON Schema, Dublin Core, schema.org, RFC 3339 timestamps, BCP 47 language tags, RFC 9562 UUIDs, Unicode normalization, SPDX license identifiers.
- **Web and APIs:** HTTP semantics, Web Linking (RFC 8288) and the IANA link relations registry, OpenAPI, Atom, OpenSearch, Sitemaps, OAuth 2.0 and OpenID Connect, Webmention and ActivityPub for the exploratory federation ideas.
- **Accessibility and inclusion:** WCAG 2.2, ATAG 2.0, WAI-ARIA.
- **Licensing:** Creative Commons 4.0 licenses and the Open Definition.

Appendix F lists the versions consulted while drafting.

## 10. Evolution of this suite

- **Status.** Everything here is a *Working Draft*. Wording, identifiers, and structure may change until a 1.0 release.
- **Versioning.** Releases follow a semantic scheme: a major version only when published identifiers change meaning, a minor version when patterns or recommendations are added, a patch version for editorial corrections.
- **Process.** Proposals for new patterns, recommendations, or engine profiles are welcomed through the process described in [CONTRIBUTING](../CONTRIBUTING.md). Evidence from real engines, especially less-known ones, is the most valued kind of contribution.
- **Neutrality.** The suite does not favour a license, a language, a storage model, or a business model, beyond the conviction that users' knowledge belongs to users.

## 11. A note on the name

"Wiki Commons" refers to the shared ground between wiki engines: the conventions, patterns, and formats they hold in common. It is an independent community effort and is not affiliated with the Wikimedia Foundation or with Wikimedia Commons, the media repository.

---

Next: [01 · Core Concepts and Landscape](01-Core_Concepts_and_Landscape.md)
