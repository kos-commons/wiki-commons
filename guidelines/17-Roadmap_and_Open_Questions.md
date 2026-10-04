# 17 · Roadmap and Open Questions

> **Part IV — Adoption** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [16 · Conformance Profiles and Self-Assessment](16-Conformance_Profiles_and_Self_Assessment.md) · Appendices: [A · Wiki Engine Landscape](appendices/A-Wiki_Engine_Landscape.md)

**In one sentence:** This draft is a beginning; here is what would make it trustworthy, what the authors do not know yet, and where the field is moving.

---

## 1. From draft to something people rely on

Version 0.1 is a complete first statement of the guidelines. Before anyone should depend on it, several things need to exist that a document alone cannot provide.

### 1.1 Near-term work

1. **A conformance corpus.** Sample pages exercising every construct of the Portable Wiki Markdown profile, with expected degraded renderings and expected link resolutions; sample bundles of each fidelity level; adversarial cases (ambiguous titles, non-Latin anchors, nested envelopes, label-order traps). Engines and converters test against the corpus; the corpus grows from their failures. This is the single most valuable next artifact.
2. **Reference tooling.** A bundle validator built on the JSON Schemas in `schemas/`; a linter for the Markdown profile; an import-report generator; conversion filters for common toolchains (a remark plugin set and Pandoc filters that read and write the profile, including label-order flipping and separator mapping).
3. **Engine profiles.** Appendix A should grow by contribution from engine maintainers, who know their engines better than any survey. A template is in [CONTRIBUTING](../CONTRIBUTING.md).
4. **Alignment with neighbouring formats.** Outline's Open Knowledge Format (2026), BookStack's Portable ZIP, MediaWiki's XML dump schema, Obsidian's conventions, TiddlyWiki's JSON, Federated Wiki's page JSON, and Scrapbox / Cosense's JSON export all overlap with the bundle. The goal is not to replace any of them but to agree on the shared parts (frontmatter keys, link forms, history records) so that converters are small. Conversations with those maintainers are the next step.
5. **A directive registry.** The common directive vocabulary of [EXT-10](12-Extensibility_Macros_and_Dynamic_Content.md) as a maintained file with names, attributes, meanings, degradations, and known native equivalents.
6. **An interwiki registry.** A machine-readable list of common prefixes and URL templates that engines can ship as defaults ([NAV-13](04-Discovery_Navigation_and_Topology.md#nav-13--interwiki-links)), descended from the community InterMap lists of the early 2000s.
7. **Self-assessment registry.** A place where engines and tools publish their `wiki-commons.yaml` files ([Chapter 16](16-Conformance_Profiles_and_Self_Assessment.md)), so that users can compare claims.
8. **Translation of the suite.** A Japanese translation first, given the history of wiki engines in Japan and the contributors to this draft; other languages as volunteers appear. The suite should itself be a multilingual wiki eventually.

### 1.2 Toward 1.0

A 1.0 release would be justified when, at minimum: three independently developed engines of different generations can exchange a bundle at fidelity level 3 with the round trip of [XFER-15](10-Interchange_and_Portability.md) passing; the corpus exists and is used; identifiers have been stable for two minor releases; and the open questions below have each been either resolved or explicitly deferred with a documented rationale.

## 2. Open questions

Each question is stated with the drafting group's current leaning, so that disagreement has something to push against.

**Q1 · Is the block bridge sufficient?**
Nested lists plus `^id` carry outliner structure and block identity. They do not carry block-level *history* (a block moved between pages, a block's own revision list) or block-level permissions. *Leaning:* sufficient for 1.0; block-level history as an optional `history/blocks/` extension later.

**Q2 · Should there be a portable template language?**
Parameterized transclusion is the most-used dynamic feature in classic wikis and the least portable. *Leaning:* no portable template language. Export the expansion with `name` and `params` in an envelope ([EXT-6](12-Extensibility_Macros_and_Dynamic_Content.md)); let importers with compatible template systems reconstruct calls. Revisit if two or more engines converge on a shared template syntax.

**Q3 · A minimal portable query language?**
Dataview, Bases, Logseq's Datalog, Semantic MediaWiki's `#ask`, SiYuan's SQL, Silverbullet's SLIQ, and Notion's views all query page properties. A tiny shared subset (filter by tag, property equals value, sort, limit) would cover many real uses. *Leaning:* observe for one more cycle; snapshots carry results today; a subset could become `::: query lang="portable"` if convergence appears.

**Q4 · History semantics for real-time engines.**
What should a "revision" mean when editing is continuous? Checkpoint policies differ (time window, idle pause, explicit publish). CRDT update logs are library-specific and not a portable history. *Leaning:* require linearized checkpoints for export ([HIST-10](06-Temporal_Design_and_Revision_History.md#hist-10--real-time-co-editing-with-durable-history)); document each engine's policy in its profile; do not standardize CRDT logs.

**Q5 · Identity across wikis.**
Attribution that travels needs identifiers for people that work across sites without a central directory. Candidates: profile URLs, WebFinger addresses, OpenID Connect subjects, decentralized identifiers. Pseudonymization needs a shared method so that the same person is the same pseudonym across exports from one wiki. *Leaning:* profile URL as the portable identifier; pseudonymization as a salted hash declared in the manifest; revisit identity standards as they settle.

**Q6 · Federation protocol.**
Webmention for cross-wiki backlinks, ActivityPub for change notifications, and Federated Wiki's JSON for forking each solve part of the problem. *Leaning:* describe all three as exploratory ([Chapter 11 §4](11-APIs_and_Discovery.md#4-toward-federation-exploratory)); define a minimal "wiki activity" vocabulary only if implementers ask for it.

**Q7 · Provenance of machine assistance.**
A revision drafted by a language model and accepted by a person needs a vocabulary ([AUTH-14](05-Authoring_and_Participation.md#auth-14--machine-assistance-human-authorship)): kind of assistance, tool, degree. Content-credential standards for media may or may not be the right model for text. *Leaning:* a small optional `assistance` object in history records; watch adjacent standards.

**Q8 · Scale.**
A bundle of millions of pages is a different artifact from a bundle of a hundred. MediaWiki's dump infrastructure (streamed XML, split files, incremental dumps) is the precedent. *Leaning:* the directory layout already shards naturally; define a sharded-archive convention and an incremental ("since revision") export in 0.2.

**Q9 · Label order.**
Should the profile accept both `[[Target|Label]]` and `[[Label|Target]]` with a detection heuristic, as some renderers do, or insist on declaration? *Leaning:* declaration in the manifest is normative; heuristics are permitted on import and should be documented ([MKUP-6](08-Markup_and_Syntax.md)); the corpus should include traps.

**Q10 · Title normalization.**
Engines compare titles differently (first-letter case folding, full lower-casing, separator collapsing). A single documented comparison algorithm for *cross-engine* resolution would help importers. *Leaning:* specify a comparison function in 0.2 (NFC, optional first-character folding, collapse of space/underscore/hyphen runs) with test cases, while leaving native behaviour alone.

**Q11 · Should a Markdown variant be registered?**
The IANA Markdown variants registry is first-come-first-served. Registering a variant for the portable profile would let `text/markdown; variant=...` say exactly what a response contains. *Leaning:* not until the profile is stable (1.0); use `CommonMark` or `GFM` plus the manifest until then.

**Q12 · Well-known discovery.**
A `/.well-known/wiki` location for the site description document would simplify discovery but requires registration. *Leaning:* rely on link relations now; request registration when the document's schema is stable.

**Q13 · Governance of this suite.**
Who decides? *Leaning:* an open process in the repository (proposals as pull requests, discussion in the open, consensus-seeking with a small editorial group that publishes releases), a code of conduct, and an explicit invitation to engine maintainers and wiki communities; formalize only when the volume of proposals demands it. Alliances with existing communities (the open-collaboration research community, wiki software projects, the independent web community) are preferable to a new body.

**Q14 · What does "wiki" exclude?**
Collaborative editors, documentation generators, note tools, and knowledge graphs all touch these guidelines. *Leaning:* the suite applies to anything that has pages, links, and history, in proportion to how much it has of each; the profiles let a tool claim only what fits.

## 3. Where the field is moving

Observations from the landscape survey that will shape future versions:

- **Convergence on a Markdown dialect** led by file-based note tools, now read by static publishers, code-editor extensions, and some wikis. The profile in Chapter 08 rides this wave rather than fighting it.
- **Convergence on Yjs-style CRDTs** for real-time editing across otherwise unrelated engines, which makes [HIST-10](06-Temporal_Design_and_Revision_History.md#hist-10--real-time-co-editing-with-durable-history) a widely shared concern.
- **Two portability postures** side by side: files as the database, and CRDT state with a Markdown convenience copy. Both can produce bundles; only the first *is* a bundle. The guidelines should keep serving both.
- **Open formats from vendors**: JSON Canvas, Obsidian's `.base`, Outline's Open Knowledge Format, Anytype's block protocol, BookStack's portable archive. Each is a potential ally for interchange.
- **Agent interfaces** (Model Context Protocol servers, agent command-line tools, machine-readable site indexes) are becoming a standard way to reach a wiki's content. They raise the stakes for attribution and provenance ([AUTH-14](05-Authoring_and_Participation.md#auth-14--machine-assistance-human-authorship)) and reward engines with clear page, history, and search operations.
- **Regulatory pressure** on accessibility and data portability continues to rise, which gives operators reasons to ask for the profiles in Chapter 16.
- **The classic engines are alive.** New releases in 2026 from MediaWiki, DokuWiki, PmWiki, Foswiki, ikiwiki, Gitit, JSPWiki, TiddlyWiki, Federated Wiki, and Zim mean that any guideline ignoring them would be ignoring a large part of the world's wikis.

## 4. How to help

- Try to export your engine's content as a bundle by hand and report what was hard.
- Add or correct an engine profile in [Appendix A](appendices/A-Wiki_Engine_Landscape.md).
- Propose a pattern you see in the wild that Part II lacks, with evidence.
- Argue with a leaning above; the questions are open because the answers are not.
- Translate.

See [CONTRIBUTING](../CONTRIBUTING.md) for the process.

---

Previous: [16 · Conformance Profiles and Self-Assessment](16-Conformance_Profiles_and_Self_Assessment.md) · Appendices: [A · Wiki Engine Landscape](appendices/A-Wiki_Engine_Landscape.md)
