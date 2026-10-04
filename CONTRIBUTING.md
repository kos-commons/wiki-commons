# Contributing to Wiki Commons

Thank you for helping. These guidelines are only as good as the evidence behind them, and the people who know the evidence best are the ones who build, run, and use wiki engines.

## What to contribute

- **Corrections.** A fact about an engine that is wrong or out of date; a recommendation that would not work in practice; a pattern whose "Observed in" misses a good example. Small corrections are the most common and most useful contribution.
- **Engine profiles** for [Appendix A](guidelines/appendices/A-Wiki_Engine_Landscape.md), especially for engines not yet covered or covered thinly. Maintainers' own profiles of their engines are especially welcome.
- **Patterns** for Part II that you see in the wild and that the language lacks, with evidence from at least two engines or a strong argument from one.
- **Recommendations** for Part III, with the interoperability problem they solve and the engines that already do something like it.
- **Syntax crosswalk rows** for [Appendix B](guidelines/appendices/B-Syntax_Crosswalk.md).
- **Tooling:** converters, validators, and test cases for the conformance corpus ([corpus/README.md](corpus/README.md), [17 · Roadmap](guidelines/17-Roadmap_and_Open_Questions.md)). A corpus case that reproduces a disagreement between two real engines is especially valuable.
- **Answers to the open questions** in Chapter 17, or better questions.

The suite is written and maintained in English; translations are not planned.

## How

1. **Open an issue** describing the change and the evidence. For a correction, a link to the primary source (project documentation, release notes, source code) is enough.
2. **Discuss** if needed. Most changes do not need discussion; proposals that add or change identifiers do.
3. **Open a pull request.** Keep it focused. Editorial changes and substantive changes are easier to review separately.
4. An editor merges when the change is consistent with the editorial principles below and nobody has raised an unresolved objection. The editorial group is small and open to anyone who has contributed.

Identifiers (`NAV-3`, `MKUP-6`, `XFER-7`) are stable once released in a numbered version: never reuse one for a different meaning; mark retired items as deprecated and keep them.

## Editorial principles

- **Guidance, not mandates.** Use *should*, *recommended*, *encouraged*, *may*, *discouraged*, *exploratory* as defined in [00 §4](guidelines/00-Overview_and_Vision.md#4-guidance-language). Never introduce a *must* except when quoting another standard or stating a logical necessity.
- **Evidence first.** Claims about engines come from primary sources. If you cannot verify something, mark it *(unverified)* rather than leaving it out or stating it flatly.
- **Engine-plural.** No engine is "the wiki". Draw on classic, transitional, and modern engines, and on engines outside the English-speaking world.
- **Capabilities, not layouts.** Patterns describe what a user can do, never where a control sits or how it looks.
- **Small core.** Prefer adding an optional layer to enlarging the required core.
- **Lean on existing standards.** Cite them by name and version; do not paraphrase them into new requirements.
- **Declared loss is fine; silent loss is not.** Any proposal touching interchange must say how its construct degrades.
- **Plain language.** Short sentences. Define terms in the [glossary](guidelines/appendices/E-Glossary.md). Expand acronyms on first use.

## Templates

### Pattern proposal

```markdown
## XXX-n · Pattern Name

**Also known as:** ...
**Maturity:** Established | Emerging | Exploratory

**Context.** When does this apply?

**Tension.** What competing needs does it balance?

**Guidance.**
- ... **should** ...
- ... is **encouraged** ...

**Observed in.** Engine A (how), Engine B (how), Engine C (how). Include at least one classic and one modern engine where possible.

**Interchange.** How does the pattern's data survive export and import? How does it degrade?

**Related.** Other patterns and principles.

**Evidence.** Links to documentation or source for each "Observed in" claim.
```

### Recommendation proposal (Part III)

```markdown
**PREFIX-n · Short imperative title.**
One paragraph: what engines **should** / are **encouraged** to do, and why it helps interoperability or users.

Degradation: what happens in an engine that does not implement it.
Observed in: engines that already do something like it.
Evidence: links.
```

### Engine profile (Appendix A)

```markdown
### Engine name

- **Origin/status:** maintainer, first release, status as of <date>, latest version/date (with source). **License:** SPDX. **Stack:** language; storage model.
- **Model:** document / outliner / block / line / tiddler / other. **Markup:** native syntax; Markdown support; WYSIWYG. **Links:** plain form; labelled form and order (T|L or L|T); hierarchy separator; anchors; interwiki; how missing pages are shown.
- **Embeds/macros:** transclusion and macro syntax with one literal example.
- **Metadata:** categories, tags, frontmatter, properties, forms.
- **History:** revision model, diff, revert, summaries, minor flag, attribution. **Collaboration:** discussion mechanism, recent changes, watching, real-time editing (and library).
- **API:** type, machine-readable description, auth. **Export:** formats; Pandoc support.
- **Distinctive:** what this engine contributed or does unusually well.
- **Sources:** URLs verified.
```

## Conduct

This project follows the wiki's own oldest norm: assume good faith. Be welcoming, explain rather than warn, argue about evidence rather than people, and remember that the goal is knowledge that outlives any of our software. Harassment, discrimination, and personal attacks are not acceptable; the editors will remove them and may exclude people who persist.

## License of contributions

By contributing you agree that your contribution is licensed under the Apache License 2.0, like the rest of the repository ([LICENSE](LICENSE)).
