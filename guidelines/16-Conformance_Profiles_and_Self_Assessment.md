# 16 · Conformance Profiles and Self-Assessment

> **Part IV — Adoption** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [15 · Licensing and Attribution](15-Licensing_and_Attribution.md) · Next: [17 · Roadmap and Open Questions](17-Roadmap_and_Open_Questions.md)

**In one sentence:** Profiles are named bundles of recommendations that let an engine, a converter, or an operator say precisely what they do in a few words; they are a vocabulary for honest self-description, not a certification.

---

## 1. What a profile is, and is not

Nothing in this suite is mandatory, so "conformance" cannot mean passing a gate. It means something more useful: a shared shorthand. When an engine says it follows the *Portable Content* profile, a migration tool author knows what to expect without reading a feature list, and a community choosing software knows what questions are already answered.

A profile is a list of pattern and recommendation identifiers from Parts II and III. An engine, tool, or deployment **may** claim a profile when it satisfies the listed items, or satisfies most of them and documents the exceptions. Claims are self-made, public, and revisable. There is no certifying body, no logo program, and no fee; a community-maintained registry of self-assessments is proposed as future work ([17 · Roadmap](17-Roadmap_and_Open_Questions.md)).

Profiles are versioned with the suite. A claim **should** name the version: `portable-content@0.1`.

## 2. The profiles

### 2.1 Core Reading (`core-reading`)

The minimum that makes a public wiki a good citizen of the web. Suitable for any engine, including static and single-file ones.

| Item | Summary |
|---|---|
| [MKUP-12](08-Markup_and_Syntax.md) | Semantic HTML with heading identifiers and recognizable internal links |
| [META-12](09-Metadata_and_Frontmatter.md) | Page metadata exposed through schema.org and link relations |
| [API-2](11-APIs_and_Discovery.md) | A raw source URL for every page, advertised as `rel="alternate"` |
| [A11Y-3](13-Accessibility_Internationalization_and_Web_Standards.md) | Semantic structure, landmarks, language attributes |
| [WEB-1](13-Accessibility_Internationalization_and_Web_Standards.md) | Content readable without scripts |
| [WEB-5](13-Accessibility_Internationalization_and_Web_Standards.md) | Stable, readable URLs over HTTPS |
| [LIC-1](15-Licensing_and_Attribution.md) | Content license declared on every page and in the HTML head |

### 2.2 Portable Content (`portable-content`)

The engine can write and read the Portable Wiki Bundle at fidelity level 2 (metadata), so that its content can move to or from any other engine claiming the same profile.

| Area | Items |
|---|---|
| Markup | [MKUP-1](08-Markup_and_Syntax.md), MKUP-2, MKUP-3, MKUP-4, MKUP-5, MKUP-6, MKUP-7, MKUP-8, MKUP-10, MKUP-11, MKUP-13, MKUP-14, MKUP-17, MKUP-19 |
| Metadata | [META-1](09-Metadata_and_Frontmatter.md), META-2, META-3, META-4, META-5, META-7, META-9, META-10, META-11, META-13 |
| Interchange | [XFER-1](10-Interchange_and_Portability.md), XFER-2, XFER-3, XFER-4, XFER-5, XFER-6, XFER-12, XFER-13, XFER-15 |
| Patterns | [NAV-2](04-Discovery_Navigation_and_Topology.md#nav-2--free-links), [NAV-3](04-Discovery_Navigation_and_Topology.md#nav-3--dangling-link-as-invitation), [NAV-8](04-Discovery_Navigation_and_Topology.md#nav-8--redirects-and-aliases) |

An engine that only *writes* bundles (a static generator, a read-only archive) **may** claim `portable-content/export`; one that only *reads* them, `portable-content/import`.

### 2.3 Living History (`living-history`)

History is whole, legible, attributable, and exportable (bundle fidelity level 3).

| Area | Items |
|---|---|
| Patterns | [HIST-1](06-Temporal_Design_and_Revision_History.md#hist-1--non-destructive-history), HIST-2, HIST-3, HIST-4, HIST-5, HIST-6, HIST-7, HIST-8, HIST-11 |
| Interchange | [XFER-7](10-Interchange_and_Portability.md), XFER-8 |
| API | [API-4](11-APIs_and_Discovery.md) |
| Encouraged | HIST-9, HIST-10, HIST-12 |

### 2.4 Open Collaboration (`open-collaboration`)

The social machinery of a community wiki, with discussions that travel (bundle fidelity level 4).

| Area | Items |
|---|---|
| Patterns | [COLL-1](07-Collaboration_Awareness_and_Governance.md#coll-1--recent-changes), COLL-2, COLL-3, COLL-6, COLL-7, COLL-8, COLL-10, COLL-12; [AUTH-1](05-Authoring_and_Participation.md#auth-1--edit-is-one-step-away), AUTH-4, AUTH-9, AUTH-10 |
| Interchange | [XFER-10](10-Interchange_and_Portability.md) |
| API | [API-6](11-APIs_and_Discovery.md) |
| Encouraged | COLL-4, COLL-5, COLL-9, COLL-14 |

### 2.5 Connected Wiki (`connected-wiki`)

The wiki is legible to tools and to other wikis.

| Area | Items |
|---|---|
| API | [API-1](11-APIs_and_Discovery.md), API-2, API-3, API-4, API-5, API-6, API-7, API-9, API-13, API-14, and the link relations of [Chapter 11 §3](11-APIs_and_Discovery.md#3-link-relations-in-the-page-head) |
| Patterns | [NAV-4](04-Discovery_Navigation_and_Topology.md#nav-4--backlinks-what-links-here), [NAV-13](04-Discovery_Navigation_and_Topology.md#nav-13--interwiki-links), [NAV-15](04-Discovery_Navigation_and_Topology.md#nav-15--health-views-orphans-wanted-dead-ends) |
| Encouraged | API-10, API-11, API-12, API-15 |

### 2.6 Accessible Authoring (`accessible-authoring`)

Reading and writing are accessible, and the editor helps authors produce accessible content.

| Area | Items |
|---|---|
| Accessibility | [A11Y-1](13-Accessibility_Internationalization_and_Web_Standards.md) through A11Y-11 |
| Patterns | [AUTH-12](05-Authoring_and_Participation.md#auth-12--accessible-authoring), [AUTH-13](05-Authoring_and_Participation.md#auth-13--gentle-guidance), [HIST-2](06-Temporal_Design_and_Revision_History.md#hist-2--diff-as-a-first-class-view) (accessible diffs) |
| Internationalization | [I18N-1](13-Accessibility_Internationalization_and_Web_Standards.md), I18N-3, I18N-7 |

### 2.7 Many Languages (`many-languages`)

The wiki works for every writing system and can hold multilingual knowledge explicitly.

| Area | Items |
|---|---|
| Internationalization | [I18N-1](13-Accessibility_Internationalization_and_Web_Standards.md) through I18N-9 |
| Metadata | [META-10](09-Metadata_and_Frontmatter.md) (`lang`, `translations`) |

### 2.8 Graceful Extension (`graceful-extension`)

Macros, templates, queries, and embeds are declared, degrade visibly, and travel as snapshots.

| Area | Items |
|---|---|
| Extensibility | [EXT-1](12-Extensibility_Macros_and_Dynamic_Content.md), EXT-2, EXT-3, EXT-4, EXT-6, EXT-7, EXT-8, EXT-9, EXT-13 |
| Markup and interchange | [MKUP-16](08-Markup_and_Syntax.md), [XFER-12](10-Interchange_and_Portability.md) |
| Encouraged | EXT-5, EXT-10, EXT-11, EXT-12 |

### 2.9 Block Bridge (`block-bridge`)

For block, outliner, and line-based engines, and for document engines that want to receive their content without loss of addressability.

| Area | Items |
|---|---|
| Markup | [MKUP-9](08-Markup_and_Syntax.md), MKUP-10, and the conventions of [Chapter 08 §5](08-Markup_and_Syntax.md#5-bridging-the-document-and-block-paradigms) |
| Patterns | [NAV-9](04-Discovery_Navigation_and_Topology.md#nav-9--stable-identity-beneath-the-title), [NAV-10](04-Discovery_Navigation_and_Topology.md#nav-10--section-anchors-and-block-addresses), [NAV-16](04-Discovery_Navigation_and_Topology.md#nav-16--transclusion-with-provenance) |
| Interchange and extension | [XFER-3](10-Interchange_and_Portability.md) (block index), [EXT-5](12-Extensibility_Macros_and_Dynamic_Content.md) |

### 2.10 Trustworthy Operation (`trustworthy-operation`)

The engine protects its users, their privacy, and the integrity of the record.

| Area | Items |
|---|---|
| Security | [SEC-1](14-Security_Privacy_and_Trust.md) through SEC-10 |
| Privacy | PRIV-1 through PRIV-7 |
| Trust | TRUST-1, TRUST-3, TRUST-4 |
| Encouraged | PRIV-8, TRUST-2, [HIST-12](06-Temporal_Design_and_Revision_History.md#hist-12--suppression-without-erasure) |

### 2.11 Tool profiles

Converters and migration tools are not wikis but are central to the suite's purpose.

- **Bundle Exporter** (`bundle-exporter`): [XFER-1](10-Interchange_and_Portability.md) through XFER-12 as applicable to the source engine, with a truthful `fidelity` declaration.
- **Bundle Importer** (`bundle-importer`): [XFER-13](10-Interchange_and_Portability.md), XFER-14; [META-11](09-Metadata_and_Frontmatter.md) (preserve unknown keys); [LIC-4](15-Licensing_and_Attribution.md), LIC-5 (attribution and license checks); [SEC-7](14-Security_Privacy_and_Trust.md) (untrusted input).

## 3. How to declare

**Where.**
- In the site description document and bundle manifest: `conformance: [portable-content@0.1, living-history@0.1]` ([API-1](11-APIs_and_Discovery.md), [XFER-1](10-Interchange_and_Portability.md)).
- In the engine's documentation or repository: a `wiki-commons.yaml` self-assessment (below) and a sentence in the README such as "Follows the Wiki Commons guidelines 0.1: portable-content, living-history (partial)".
- Operators of a deployment **may** declare profiles that depend on configuration (for example `trustworthy-operation`) separately from the engine's own claims.

**How.** The self-assessment file lists each item of each claimed profile with a status and a note. Statuses: `yes`, `partial`, `planned`, `no`, `n/a`. A `no` or `partial` **should** carry a reason or a link to an issue. The file is advisory and human-readable first; its schema is `schemas/self-assessment.schema.json`.

```yaml
format: wiki-commons-self-assessment
version: "0.1"
subject:
  name: ExampleWiki
  version: "4.2.0"
  url: https://example.org/examplewiki
  kind: engine            # engine | tool | deployment
assessed_at: "2026-10-04"
profiles:
  portable-content:
    claim: yes
    items:
      MKUP-1: {status: yes, note: "Markdown served as text/markdown; charset=UTF-8; variant=GFM; profile declared in manifest"}
      MKUP-6: {status: yes, note: "target-first natively; label-first accepted on import when unambiguous"}
      MKUP-7: {status: partial, note: "native separator is ':'; mapped to '/' on export; import mapping planned", issue: "https://example.org/issues/812"}
      META-2: {status: yes}
      XFER-7: {status: n/a, note: "history is covered by the living-history claim"}
  living-history:
    claim: partial
    items:
      HIST-12: {status: no, note: "no revision suppression; full deletion only"}
      XFER-7: {status: yes, note: "full content per revision; patches not used"}
  connected-wiki:
    claim: planned
```

## 4. Guidance for claimants

- **Be literal.** A profile claim is a promise to tool authors. Claim `partial` rather than stretching.
- **Date it.** Claims rot. Re-assess with each major release and keep the file in version control so its history is visible.
- **Show your evidence.** Link to documentation, test output, or the published sample pages of [MKUP-20](08-Markup_and_Syntax.md).
- **Invite correction.** Communities and users will notice discrepancies; a visible place to report them is part of the claim.

## 5. Guidance for readers of claims

A self-assessment is a starting point for evaluation, not a substitute for it. Readers **should** test the things they depend on, especially export fidelity ([XFER-15](10-Interchange_and_Portability.md)), and **should** report discrepancies to the claimant and, where useful, to this project so that the profiles themselves can improve.

---

Previous: [15 · Licensing and Attribution](15-Licensing_and_Attribution.md) · Next: [17 · Roadmap and Open Questions](17-Roadmap_and_Open_Questions.md)
