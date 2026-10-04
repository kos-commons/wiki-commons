# Wiki Commons

**Open guidelines for wiki engines: a pattern language for the wiki experience and a set of portable conventions so that knowledge outlives the software it was written in.**

> Status: **Working Draft 0.1** (October 2026). Everything here is open for discussion; identifiers may still change before 1.0. See [CHANGELOG](CHANGELOG.md) and [CONTRIBUTING](CONTRIBUTING.md).
>
> Read online: **<https://kos-commons.github.io/wiki-commons/>** (built from this repository on every push to `main`).

## Why

Wikis are thirty years old and there is still no shared standard for them. Markup never converged (WikiCreole tried and was frozen in 2007; Markdown won by default but cannot express `[[free links]]`, transclusion, or macros). Data never flowed (there is no common way to ask a wiki for a page, its history, or its metadata, and migrations still mean bespoke scripts). The patterns that millions of people understand, red links, Read / Edit / History / Discussion, Recent Changes, diffs, "assume good faith", are documented nowhere as a design vocabulary. Meanwhile pages are becoming blocks, editing is becoming simultaneous, knowledge bases are becoming local files that sync, and commercial platforms hold more collective knowledge than ever.

Wiki Commons is a response. It does not propose "the wiki protocol". It names what the wiki family already shares, recommends a small set of portable conventions where sharing is cheap and valuable, and describes the user-experience patterns that make a wiki feel trustworthy and alive. It uses the language of guidance (*should*, *recommended*, *encouraged*), never of mandates, and it draws on every generation of engine: classic flat-file and database wikis, single-file and git-backed wikis, enterprise knowledge bases, block-based and outliner tools, local-first note systems, and real-time collaborative documents, from MediaWiki and DokuWiki to TiddlyWiki, Federated Wiki, PukiWiki, Scrapbox / Cosense, Confluence, Notion, Obsidian, Logseq, and the rest.

## What is here

```
guidelines/
  Part I   — Foundations
    00-Overview_and_Vision.md                      what this is, guidance language, scope, how to read
    01-Core_Concepts_and_Landscape.md              concepts, three generations of engines, shared ground, fault lines, lessons
    02-Guiding_Principles.md                       psychological safety, imperfection, mental models, serendipity, governance, portability
  Part II  — The Pattern Language (56 patterns)
    03-Pattern_Language_Overview.md                pattern format, full index, three reading paths
    04-Discovery_Navigation_and_Topology.md        NAV-1 … NAV-16: links, dangling links, backlinks, hierarchy, tags, interwiki, transclusion
    05-Authoring_and_Participation.md              AUTH-1 … AUTH-14: edit in one step, two views, welcome the incomplete, drafts, accessible authoring
    06-Temporal_Design_and_Revision_History.md     HIST-1 … HIST-12: non-destructive history, diffs, revert, attribution, real-time, suppression
    07-Collaboration_Awareness_and_Governance.md   COLL-1 … COLL-14: recent changes, talk, soft security, good faith, forking, review overlays
  Part III — Interoperability Guidelines
    08-Markup_and_Syntax.md                        the Portable Wiki Markdown profile (MKUP-1 … MKUP-20) and its degradation ladder
    09-Metadata_and_Frontmatter.md                 the Portable Page Metadata vocabulary (META-1 … META-14)
    10-Interchange_and_Portability.md              the Portable Wiki Bundle (XFER-1 … XFER-15): pages, attachments, history, discussions
    11-APIs_and_Discovery.md                       capabilities and link relations, not a protocol (API-1 … API-15)
    12-Extensibility_Macros_and_Dynamic_Content.md declare, degrade, snapshot (EXT-1 … EXT-13)
    13-Accessibility_Internationalization_and_Web_Standards.md   A11Y, I18N, WEB
    14-Security_Privacy_and_Trust.md               SEC, PRIV, TRUST
    15-Licensing_and_Attribution.md                LIC-1 … LIC-10
  Part IV  — Adoption
    16-Conformance_Profiles_and_Self_Assessment.md ten profiles and a self-assessment format; no certification
    17-Roadmap_and_Open_Questions.md               what would make this trustworthy, and what we do not know yet
  appendices/
    A-Wiki_Engine_Landscape.md                     fifty-odd engines across three generations, with a feature matrix
    B-Syntax_Crosswalk.md                          twenty constructs, twenty ways to write them
    C-Portable_Page_Metadata_Reference.md          field-by-field reference and engine mappings
    D-Portable_Wiki_Bundle_Example.md              walkthrough of the example bundle
    E-Glossary.md
    F-References.md                                standards (versions checked October 2026), history, research
schemas/                                           JSON Schemas for frontmatter, manifest, history, discussions, attachments, site description, self-assessment
examples/portable-wiki-bundle/                     a small, complete bundle exercising every optional part
tools/                                             bundle validator, link checkers, and the site assembly script
book/                                              mdBook configuration and table of contents for the published site
.github/workflows/pages.yml                        CI: checks, site build, and GitHub Pages deployment
```

## Where to start

- **You build an engine and want it to interoperate:** [00](guidelines/00-Overview_and_Vision.md), [01](guidelines/01-Core_Concepts_and_Landscape.md), then Part III in order, then [16](guidelines/16-Conformance_Profiles_and_Self_Assessment.md).
- **You design the experience of a wiki:** [00](guidelines/00-Overview_and_Vision.md), [02](guidelines/02-Guiding_Principles.md), [03](guidelines/03-Pattern_Language_Overview.md), then Part II, then [13](guidelines/13-Accessibility_Internationalization_and_Web_Standards.md).
- **You write a migration or conversion tool:** [08](guidelines/08-Markup_and_Syntax.md), [09](guidelines/09-Metadata_and_Frontmatter.md), [10](guidelines/10-Interchange_and_Portability.md), [Appendix B](guidelines/appendices/B-Syntax_Crosswalk.md), [Appendix C](guidelines/appendices/C-Portable_Page_Metadata_Reference.md), and the [example bundle](examples/portable-wiki-bundle/).
- **You lead a community:** [00](guidelines/00-Overview_and_Vision.md), [02](guidelines/02-Guiding_Principles.md), [07](guidelines/07-Collaboration_Awareness_and_Governance.md), [15](guidelines/15-Licensing_and_Attribution.md).
- **You want to understand the field:** [01](guidelines/01-Core_Concepts_and_Landscape.md) and [Appendix A](guidelines/appendices/A-Wiki_Engine_Landscape.md).

## Three things any engine can do this month

1. **Give every page a raw source URL** in Markdown (or your native format), advertised with `<link rel="alternate" type="text/markdown">`. ([API-2](guidelines/11-APIs_and_Discovery.md))
2. **Put the basics in frontmatter** when you export: `title`, `id`, `aliases`, `tags`, `created`, `updated`, `contributors`, `status`, `license`. ([Chapter 09](guidelines/09-Metadata_and_Frontmatter.md))
3. **Write a manifest** for your export and say truthfully what it drops. ([Chapter 10](guidelines/10-Interchange_and_Portability.md))

## Validating a bundle

```sh
python3 tools/validate_bundle.py examples/portable-wiki-bundle
```

## Building the site locally

The site is an [mdBook](https://rust-lang.github.io/mdBook/). The source tree is assembled from the repository by a script, then built:

```sh
python3 tools/build_book.py
mdbook build book            # output in book/book/
mdbook serve book --open     # local preview
```

See [book/README.md](book/README.md) for details.

## Contributing

Evidence from real engines, especially less-known ones, is the most valued contribution. Patterns, recommendations, engine profiles, corrections, translations, and tooling are all welcome; see [CONTRIBUTING](CONTRIBUTING.md) for the process and templates.

## License

The contents of this repository (text, schemas, examples, tools) are licensed under the Apache License 2.0; see [LICENSE](LICENSE).

## A note on the name

"Wiki Commons" refers to the shared ground between wiki engines. This is an independent community effort, not affiliated with the Wikimedia Foundation or with Wikimedia Commons, the media repository.
