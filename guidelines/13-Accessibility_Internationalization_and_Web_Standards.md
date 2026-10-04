# 13 · Accessibility, Internationalization and Web Standards

> **Part III — Interoperability Guidelines** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [12 · Extensibility, Macros and Dynamic Content](12-Extensibility_Macros_and_Dynamic_Content.md) · Next: [14 · Security, Privacy and Trust](14-Security_Privacy_and_Trust.md)

**In one sentence:** A wiki is both a publication and an authoring tool, read and written by people of every ability and every language; these guidelines point to the web's existing accessibility and internationalization standards and add the handful of wiki-specific concerns (red links, diffs, free links in scripts without capital letters, input methods) that those standards do not spell out.

Recommendations carry the prefixes `A11Y-` (accessibility), `I18N-` (internationalization and localization), and `WEB-` (web platform).

---

## 1. Standards this chapter leans on

- **WCAG 2.2** (W3C Recommendation), Level AA, for everything a reader or contributor sees.
- **ATAG 2.0** (Authoring Tool Accessibility Guidelines, W3C Recommendation), because a wiki editor is an authoring tool: Part A asks that the tool itself be accessible, Part B that it help authors produce accessible content.
- **WAI-ARIA** for rich widgets (editors, menus, live regions) where native HTML elements do not suffice.
- **The HTML Living Standard**, **CSS**, and **MathML Core** for output.
- **Unicode** (including normalization forms), **BCP 47** language tags, **RFC 3987** IRIs, and **CLDR** locale data for plural rules, collation, and formatting.
- **EN 301 549** and the regulatory frameworks that reference WCAG, which increasingly apply to software used by the public and by employees.

The accessibility of the *content* contributors write depends on the tool: that is the wiki-specific insight of ATAG, and it runs through this chapter.

## 2. Accessibility

### A11Y-1 · Target WCAG 2.2 AA for reading and editing, and say so

Engines **should** aim for WCAG 2.2 Level AA across reading views, editing views, history, search, and administration, and **should** publish an accessibility statement describing conformance, known gaps, and how to report problems. Themes and plugins **should not** lower the baseline ([EXT-11](12-Extensibility_Macros_and_Dynamic_Content.md)).

### A11Y-2 · Treat the editor as an authoring tool (ATAG 2.0)

- *Part A:* the editor **should** be fully operable by keyboard and compatible with screen readers; it **should not** impose time limits that discard work ([AUTH-8](05-Authoring_and_Participation.md#auth-8--never-lose-a-draft)); its toolbars and dialogs **should** expose names, roles, and states.
- *Part B:* the editor **should** help authors produce accessible content: prompt for alternative text at image insertion, encourage heading hierarchy, offer table header controls, flag empty link text or "click here", and provide accessible templates. These are suggestions, not blockers ([AUTH-13](05-Authoring_and_Participation.md#auth-13--gentle-guidance)).

### A11Y-3 · Semantic structure in output

Rendered pages **should** use landmarks (`<main>`, `<nav>`, `<aside>`, `<header>`, `<footer>`), a correct heading hierarchy that begins with the page title, lists for lists, tables for tabular data with header cells, `<time>` for dates, and the `lang` attribute on the document and on fragments in other languages. A "skip to content" link is **encouraged**.

### A11Y-4 · No information by colour or vision alone

- Dangling links **should** be distinguishable without colour (an icon, a distinct underline style, or a visible marker) and **should** carry an accessible description such as "page does not exist yet" ([NAV-3](04-Discovery_Navigation_and_Topology.md#nav-3--dangling-link-as-invitation)).
- Graph views **should** have textual equivalents ([NAV-14](04-Discovery_Navigation_and_Topology.md#nav-14--graph-as-a-lens-not-a-map)).
- Drag-and-drop (reordering blocks, uploading) **should** have keyboard and button alternatives.
- Status conveyed by icon or colour (draft, protected, reviewed) **should** also be conveyed by text.

### A11Y-5 · Accessible diffs

Diff views **should** mark insertions and deletions with `<ins>` and `<del>` (or ARIA equivalents), **should** provide a textual summary ("3 lines added, 1 removed"), **should** allow navigation from change to change by keyboard, and **should not** rely on red and green alone ([HIST-2](06-Temporal_Design_and_Revision_History.md#hist-2--diff-as-a-first-class-view)).

### A11Y-6 · Alternative text travels with media

Images **should** have alternative text; the editor **should** prompt for it; decorative images **should** be markable as such; captions **should** be supported. Alternative text **should** be stored in the content (`![alt](...)`) and in attachment metadata ([XFER-4](10-Interchange_and_Portability.md)) so that it survives export ([AUTH-7](05-Authoring_and_Participation.md#auth-7--effortless-media)).

### A11Y-7 · Keyboard everywhere

Every action **should** be reachable by keyboard with visible focus. Shortcuts **should** be documented, discoverable, and remappable, and **should** avoid conflicts with assistive technologies and browser defaults. Editors **should not** trap focus.

### A11Y-8 · Motion, timing, and media

Engines **should** honour `prefers-reduced-motion`, **should not** auto-play media, and **should** avoid timeouts that discard work.

### A11Y-9 · Collaboration features

Presence indicators, remote cursors, mentions, and comment threads **should** be perceivable by assistive technologies without flooding them: live regions **should** be polite and summarizing ("two others are editing") rather than announcing every keystroke.

### A11Y-10 · Mathematics, code, and tables

Mathematics **should** be rendered as MathML (now supported natively across browsers) or with an accessible alternative, never as an image without alternative text. Code **should** be text, not an image, with the language declared. Tables **should** have header cells and, where complex, captions and scope attributes.

### A11Y-11 · Test, and keep testing

Automated checks catch a fraction of problems; engines **should** also test with keyboards and screen readers, **should** include accessibility in release checklists, and **should** make it easy for users to report barriers.

## 3. Internationalization and localization

Wikis were born in English and grew up everywhere. Several of the field's most important conventions (free links instead of CamelCase, for example) exist because of languages other than English. The following concerns are wiki-specific or wiki-critical.

### I18N-1 · Unicode throughout, with explicit rules

Titles, tags, link targets, usernames, and content **should** accept any Unicode text. Titles and link targets **should** be normalized to NFC for comparison and storage ([MKUP-19](08-Markup_and_Syntax.md)). Case rules **should** be documented and **should** be chosen with non-Latin scripts in mind: forcing titles to lower case (as some engines do for file names) or capitalizing the first letter (as others do) are both legitimate, but engines **should** apply such rules only to scripts that have case, **should** preserve the author's title for display, and **should** compare using a documented case-folding.

### I18N-2 · Readable URLs in every script

Page URLs **should** present the title in its own script (`/wiki/編集の競合`, `/wiki/Конфликт_редактирования`), encoded as the IRI and URL specifications require, rather than transliterating or replacing it with an identifier. Where a slug is used, the true title **should** remain in metadata. Percent-encoding **should** be applied consistently to the UTF-8 bytes, and engines **should** decode liberally on input.

### I18N-3 · Language tags on everything

Pages **should** carry a BCP 47 `lang` ([META-10](09-Metadata_and_Frontmatter.md)), rendered as the HTML `lang` attribute; fragments in another language **should** be markable with their own `lang` (a Markdown span with an attribute, or a small HTML `<span lang>`), because screen readers, hyphenation, and fonts depend on it.

### I18N-4 · Text processing for all writing systems

- *Search* **should** handle languages without word delimiters (Chinese, Japanese, Thai) through n-gram or morphological tokenization, **should** fold diacritics and width variants (full-width and half-width forms) where the language expects it, and **should** be tested on non-Latin content.
- *Sorting* of titles, categories, and lists **should** use locale-aware collation, not code-point order.
- *Dates and numbers* **should** be stored in interchange form (RFC 3339, plain numerals) and displayed in the user's locale, with the time zone shown or selectable ([I18N-9](#i18n-9--time-zones)).
- *Bidirectional text* **should** render correctly: `dir="auto"` on user-supplied titles and fields, logical CSS properties in themes, and mirrored layouts for right-to-left interfaces.
- *Line breaking and typography* **should** follow the language (no forced word spacing in CJK, correct quotation marks and punctuation where the engine autoformats).

### I18N-5 · Localizable interface

Engines **should** externalize every interface string, **should** support plural and gender rules through CLDR-based libraries, **should** allow right-to-left layouts, and **should** make community translation possible (translation files in a standard format, or a translation platform). The interface language **should** be selectable per user and **should** default from the browser.

### I18N-6 · Multilingual content, explicitly linked

Communities organize multilingual knowledge in several ways: separate wikis per language joined by interlanguage links; one wiki with per-language subpages; one wiki with a translation extension managing units; per-page `translations` metadata. Any of these is fine. Whatever the model, the relationship between language versions **should** be explicit in metadata (`translations`, [Chapter 09](09-Metadata_and_Frontmatter.md)) and in HTML (`<link rel="alternate" hreflang="ja" href="...">`), **should** be exported, and **should** be visible to readers. Translation status ("this translation is outdated relative to revision N") is **encouraged** where translation is systematic.

### I18N-7 · Respect input methods

Editors **should** work correctly with input method editors (IMEs) used for Chinese, Japanese, Korean, and other languages: they **should not** intercept keystrokes during composition, autocompletion and slash-command popups **should not** consume the Enter or Escape keys that commit or cancel a composition, and shortcuts **should** be tested with an IME active. This is one of the most common accessibility failures of web editors for a large part of the world and is rarely checked.

### I18N-8 · Markup that works in every language

Free links ([NAV-2](04-Discovery_Navigation_and_Topology.md#nav-2--free-links)) exist because CamelCase cannot express links in scripts without capital letters or word spaces; engines **should** treat explicit link syntax as primary and CamelCase, if supported, as an option. Heading anchors, tags, and block identifiers **should** accept non-ASCII text ([MKUP-8](08-Markup_and_Syntax.md), [MKUP-14](08-Markup_and_Syntax.md)). Markdown emphasis delimiters have known difficulties with CJK punctuation; engines **should** test and document their behaviour.

### I18N-9 · Time zones

Timestamps **should** be stored in UTC or with an explicit offset, displayed in the user's zone, and labelled. Exports **should** never contain naive local times.

## 4. The web platform

### WEB-1 · Progressive enhancement: reading works without scripts

A page's content **should** be readable with JavaScript disabled or failed, so that archives, text browsers, assistive tools, and low-end devices all work. Editing and collaboration **may** require scripts. Single-page applications that render nothing without scripts are **discouraged** for reading surfaces; server rendering or static output is **encouraged**.

### WEB-2 · Standards-conformant, responsive, printable, themeable

Output **should** be valid HTML and CSS, **should** adapt to narrow and wide viewports, **should** have a print stylesheet (people still print wikis), and **should** support light and dark colour schemes through `prefers-color-scheme` with sufficient contrast in both.

### WEB-3 · Discoverable metadata

Pages **should** expose their metadata through schema.org and link relations ([META-12](09-Metadata_and_Frontmatter.md), [Chapter 11 §3](11-APIs_and_Discovery.md#3-link-relations-in-the-page-head)) and **may** add Open Graph data for link previews.

### WEB-4 · Performance as inclusion

Fast pages are accessible pages. Engines **should** keep reading views light, **should** size and lazy-load images, **should** avoid shipping editor code to readers, and **should** measure on low-end devices and slow networks.

### WEB-5 · Stable, meaningful URLs over HTTPS

URLs **should** be stable across engine upgrades, readable ([I18N-2](#i18n-2--readable-urls-in-every-script)), free of session tokens, served over HTTPS with `rel="canonical"`, and preserved through redirects when a wiki moves.

### WEB-6 · Offline and local-first (exploratory)

Engines **may** support offline reading and editing through service workers or local files with later synchronization, following the principles of local-first software. Where they do, they **should** keep the durable-history guarantees of [HIST-10](06-Temporal_Design_and_Revision_History.md#hist-10--real-time-co-editing-with-durable-history).

## 5. Observed in

MediaWiki has long-standing accessibility and internationalization programmes: interface translation through a community platform for hundreds of languages, right-to-left support, language-aware search, and accessibility work on its editors; its red links rely on colour by default and communities add styles for contrast. DokuWiki and PukiWiki ship with UTF-8 page names and many interface languages; PukiWiki's bracket links are a direct response to Japanese text. Scrapbox / Cosense and Growi grew up in Japanese and handle IME input and CJK search as a matter of course. Modern block editors have improved screen-reader support unevenly; several still break IME composition in autocompletion popups. Few engines publish accessibility statements or document ATAG conformance, which is an opportunity rather than a criticism.

---

Previous: [12 · Extensibility, Macros and Dynamic Content](12-Extensibility_Macros_and_Dynamic_Content.md) · Next: [14 · Security, Privacy and Trust](14-Security_Privacy_and_Trust.md)
