# 15 · Licensing and Attribution

> **Part III — Interoperability Guidelines** · **Status:** Working Draft 0.4 (October 2026)
> Previous: [14 · Security, Privacy and Trust](14-Security_Privacy_and_Trust.md) · Next: [16 · Conformance Profiles and Self-Assessment](16-Conformance_Profiles_and_Self_Assessment.md)

**In one sentence:** Knowledge can only outlive its software if it is legally allowed to move; these guidelines ask every wiki to declare its content license visibly and machine-readably, to carry licenses and attribution through every export, and to prefer, for shared knowledge, licenses that meet the Open Definition.

Recommendations carry the prefix `LIC-`. The numbered recommendations are the guidance of this chapter ([00 §4](00-Overview_and_Vision.md#4-guidance-language)); the surrounding sections explain, give evidence, and add no obligations. Nothing in this chapter is legal advice; it describes practices that make licensing legible and portable.

---

## 1. Why licensing belongs in an interoperability guideline

A perfectly exported bundle of pages that nobody may legally reuse is not portable. Conversely, content under a clear open license can move between engines, be forked, archived, translated, and republished without asking anyone. The source report's call to "prioritize data portability" therefore has a legal half: the terms must travel with the text, and the attribution those terms require must travel too.

Three distinctions keep the topic manageable:

- **Software license versus content license.** The engine's license (GPL, AGPL, MIT, Apache, a source-available license, or proprietary) governs the code. The content license (typically a Creative Commons license for public wikis, or an organization's internal policy for private ones) governs what people wrote. They are independent, and confusing them is common.
- **Default versus override.** A wiki has a default content license; individual pages, and especially attachments, may carry their own.
- **Open versus merely published.** The Open Definition recognizes as open only licenses that permit free use, modification, and redistribution, including commercially. Among Creative Commons licenses, CC0, CC BY, and CC BY-SA qualify; the NonCommercial and NoDerivatives variants do not.

## 2. Recommendations

### LIC-1 · Declare a default content license, everywhere it matters

Every wiki **should** have an explicit default license for contributions. It **should** be visible on every page (a footer line is the convention), declared in the HTML head (`<link rel="license" href="...">`) and in page metadata ([META-12](09-Metadata_and_Frontmatter.md)), stated in the site description document ([API-1](11-APIs_and_Discovery.md)), and recorded in every bundle manifest ([XFER-1](10-Interchange_and_Portability.md)). SPDX identifiers (`CC-BY-SA-4.0`, `CC-BY-4.0`, `CC0-1.0`) **should** be used wherever a license is named in metadata. Private and internal wikis **should** still declare their terms ("internal use; all rights reserved by the organization" is a declaration) so that an export is never of unknown status.

### LIC-2 · Show the terms at the moment of contribution

The editor **should** state, briefly and near the save action, the license under which the contribution will be released, with a link to the full text. Communities **should** be able to edit that notice as a page ([COLL-12](07-Collaboration_Awareness_and_Governance.md#coll-12--the-wiki-documents-itself)). Requiring a click-through on every edit is **discouraged**; a persistent notice suffices and is the long-standing practice of large public wikis.

### LIC-3 · Per-page and per-file licenses with SPDX identifiers

Pages **may** override the default through `license:` in frontmatter ([META-9](09-Metadata_and_Frontmatter.md)); attachments **should** carry their own `license` and `attribution` in their metadata ([XFER-4](10-Interchange_and_Portability.md)), because images and documents are the most frequently differently-licensed content in any wiki. Quotations and other third-party material **should** be attributed in the text. Engines **should** display per-file licenses with the file.

### LIC-4 · Attribution that satisfies the license and respects people

Attribution-requiring licenses are satisfied by a reasonable means appropriate to the medium. For wikis the established practice is a visible list of contributors or a link to the page's history. Therefore:
- The history export and `contributors` metadata ([XFER-7](10-Interchange_and_Portability.md), [META-3](09-Metadata_and_Frontmatter.md)) are the attribution. Exporters **should** include them whenever the license requires attribution and privacy rules permit.
- Importers **should** preserve and display attribution: a per-page "contributors" view, an "imported from" notice linking to the source page and its history, or both. Dropping contributor data from BY-licensed content on import is **discouraged** and may violate the license.
- Where contributors are pseudonymized ([PRIV-3](14-Security_Privacy_and_Trust.md)), the stable pseudonym plus a link to the source wiki is acceptable attribution; the manifest **should** say that pseudonymization was applied.
- A "cite this page" affordance that produces a citation with the permalink, revision, and contributor summary is **encouraged** ([HIST-5](06-Temporal_Design_and_Revision_History.md#hist-5--permalinks-to-revisions)).

### LIC-5 · Check compatibility on import

Importers **should** compare the bundle's declared license (and any page overrides) with the destination wiki's license and **should** warn when they are incompatible or when the bundle's license is unknown. A simplified guide, which operators **should** verify for their situation:

| Imported content | Into a CC0 wiki | Into a CC BY wiki | Into a CC BY-SA wiki | Into an all-rights-reserved wiki |
|---|---|---|---|---|
| CC0 | fine | fine | fine | fine |
| CC BY 4.0 | needs attribution; not fully CC0 | fine | fine (BY-SA accepts BY content) | fine with attribution |
| CC BY-SA 4.0 | no | no | fine | no (must remain BY-SA) |
| CC BY-NC / BY-ND | no | no | no | only under the original terms |
| GFDL (legacy) | no | no | compatible only where the relicensing path applies | no |
| Unknown / none | no | no | no | ask the source |

Engines **should** record the per-page `license` of imported content rather than silently relabelling it.

### LIC-6 · Relicensing is history too

A wiki that changes its default license **should** record when, and **should** make the terms of each revision discoverable, because older revisions were contributed under older terms. A `license` field **may** be added to history records when a change occurred. The best-known precedent is Wikipedia's migration from the GNU Free Documentation License to CC BY-SA 3.0 in 2009, achieved through a license-compatibility clause and a community vote, followed by the move to CC BY-SA 4.0 in June 2023, under which new edits are 4.0 while older revisions remain under 3.0.

### LIC-7 · Keep software and content licenses legible and separate

Engines **should** display their own license in the interface and documentation and **should not** let it be confused with the content license. Projects **should** be clear about terms that affect operators, such as network-use clauses in some copyleft licenses or restrictions in source-available licenses. Where an engine's software license is not an open-source license, the portability of the content matters even more, and such engines are especially **encouraged** to implement [Chapter 10](10-Interchange_and_Portability.md) in full.

### LIC-8 · For shared knowledge, prefer open licenses

Wikis whose purpose is a shared body of knowledge (public reference wikis, community documentation, open educational resources) are **encouraged** to choose a license that meets the Open Definition: CC BY-SA 4.0 is the choice of the largest public wikis and keeps derivatives open; CC BY 4.0 maximizes reuse with attribution; CC0 waives rights entirely for data and reference material. NonCommercial and NoDerivatives licenses are legitimate choices for some projects but **should** be chosen knowing that they prevent the content from joining the open commons and from being imported into most open wikis. Internal and private wikis have different needs and are not asked to be open, only to be explicit.

### LIC-9 · Machine reuse is governed by the license

Whatever the wiki's stance on indexing, archiving, and text and data mining, the license already states what may be done with the content and under what conditions; attribution and share-alike obligations apply to derivative uses by machines as by people. Engines **may** additionally expose machine-readable reservation signals ([PRIV-8](14-Security_Privacy_and_Trust.md)); those are *exploratory* and do not replace the license declaration.

### LIC-10 · Names and marks

The content license does not cover the names, logos, and marks of the wiki, the engine, or the organization. Projects **should** state their trademark policy separately and **should** make clear that forking the content ([COLL-13](07-Collaboration_Awareness_and_Governance.md#coll-13--fork-instead-of-fight)) does not convey the name.

## 3. Attribution in practice

Different engine generations attribute differently; the bundle lets them meet.

- **Revision-attributed engines** (MediaWiki, DokuWiki, Confluence, BookStack, git-backed wikis) export `history/` and `users.yaml`; attribution is complete.
- **Line- or block-attributed engines** (Scrapbox / Cosense, Federated Wiki, Etherpad-style editors) roll per-segment authorship up into `contributors` and, where feasible, into coalesced revisions.
- **Engines without history** (single-file and static wikis) export `contributors` from whatever they know, often a single `modifier` field; importers **should** display it as "last known contributor" rather than as a complete record.
- **Pseudonymized exports** carry stable opaque identifiers; the source URL and history link carry the rest.

A reasonable importer-side attribution notice:

> This page was imported from *Example Project Wiki* ([source page](https://wiki.example.org/wiki/Edit_Conflicts), [history](https://wiki.example.org/wiki/Edit_Conflicts?action=history)) on 2026-10-04. Original contributors: Aiko Tanaka, Ben, and two anonymous editors. Licensed under CC BY-SA 4.0.

## 4. Observed in

Wikipedia and its sister projects license text under CC BY-SA 4.0 (with media licensed individually, and a strict requirement that every uploaded file carry a license) and treat a link to the page history as attribution. Many documentation wikis use CC BY or CC BY-SA; some community wikis use GFDL for historical reasons; hosted wiki farms often set a default license for all hosted wikis. DokuWiki ships a configurable license selector that places the license notice in the footer and in the HTML head, a small feature worth copying. Most enterprise and personal knowledge tools have no license concept at all, because their content is assumed private, which is exactly why an exported bundle from them needs a manifest that says so.

---

Previous: [14 · Security, Privacy and Trust](14-Security_Privacy_and_Trust.md) · Next: [16 · Conformance Profiles and Self-Assessment](16-Conformance_Profiles_and_Self_Assessment.md)
