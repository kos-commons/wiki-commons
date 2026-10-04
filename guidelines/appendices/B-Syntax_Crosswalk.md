# Appendix B · Syntax Crosswalk

> **Appendices** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [A · Wiki Engine Landscape](A-Wiki_Engine_Landscape.md) · Next: [C · Portable Page Metadata Reference](C-Portable_Page_Metadata_Reference.md)

**In one sentence:** The same twenty ideas, written twenty ways: a construct-by-construct comparison of wiki markups with the Portable Wiki Markdown form of each, for converter authors and for anyone who wants to see how small the real differences are.

Conventions: `Target` is the page linked to, `Label` the shown text, `ns` a namespace or folder. Pipes inside cells are escaped as `\|` for the table syntax; read them as plain `|`. Entries describe the native syntax as documented by each project; where a feature exists only through a plugin, the cell says so. Blank cells mean "no native equivalent". The last row of each table gives the **Portable Wiki Markdown** form from [Chapter 08](../08-Markup_and_Syntax.md).

---

## 1. Internal link and labelled link

| Engine | Internal link | Labelled link | Order |
|---|---|---|---|
| MediaWiki | `[[Target]]` | `[[Target\|Label]]` | T\|L |
| DokuWiki | `[[target]]` | `[[target\|Label]]` | T\|L |
| MoinMoin | `[[Target]]` or `WikiWord` | `[[Target\|Label]]` | T\|L |
| PmWiki | `[[Target]]` | `[[Target\|Label]]` and `[[Label -> Target]]` | both |
| TWiki / Foswiki | `[[Target]]` or `WikiWord` | `[[Target][Label]]` | T][L |
| XWiki 2.1 | `[[Target]]` | `[[Label>>Target]]` | L>>T |
| Tiki | `((Target))` or `WikiWord` | `((Target\|Label))` | T\|L |
| JSPWiki | `[Target]` | `[Label\|Target]` | L\|T |
| Trac | `[[Target]]`, `wiki:Target`, `WikiWord` | `[[wiki:Target\|Label]]`, `[wiki:Target Label]` | T\|L |
| ikiwiki | `[[Target]]` | `[[Label\|Target]]` | L\|T |
| Gollum / GitLab wiki | `[[Target]]` | `[[Label\|Target]]` (GitHub's docs say `[[Target\|Label]]`) | contested |
| Gitit | `[Target]()` | `[Label](Target)` | Markdown |
| PukiWiki | `[[Target]]` or `WikiName` | `[[Label>Target]]` | L>T |
| TiddlyWiki | `[[Target]]` or `CamelCase` | `[[Label\|Target]]` | L\|T |
| Federated Wiki | `[[Target]]` | | |
| Zim | `[[target]]` | `[[target\|Label]]` | T\|L |
| Redmine | `[[Target]]` | `[[Target\|Label]]` | T\|L |
| Wikidot | `[[[target]]]` | `[[[target \| Label]]]` | T\|L |
| WikiCreole 1.0 | `[[Target]]` | `[[Target\|Label]]` | T\|L |
| Confluence wiki markup (legacy) | `[Target]` | `[Label\|Target]` | L\|T |
| Obsidian / Quartz / Foam / Silverbullet | `[[Target]]` | `[[Target\|Label]]` | T\|L |
| Logseq | `[[Target]]` | `[Label]([[Target]])` | L then T |
| Dendron | `[[target]]` | `[[Label\|target]]` | L\|T |
| GROWI | `[[/Target]]` | `[[Label>/Target]]` | L>T |
| Scrapbox / Cosense | `[Target]` | | |
| Org-mode | `[[file:target.org]]`, `[[*Heading]]`, `[[id:uuid]]` | `[[file:target.org][Label]]` | T][L |
| AsciiDoc | `xref:target.adoc[]` | `xref:target.adoc[Label]` | T[L] |
| CommonMark / GFM | `[Label](target.md)` | same | Markdown |
| **Portable Wiki Markdown** | `[[Target]]` | `[[Target\|Label]]` (declare `label-first` if native order differs) | T\|L |

## 2. Section, anchor, and block links

| Engine | Heading / anchor link | Block or line reference |
|---|---|---|
| MediaWiki | `[[Target#Section heading]]` | |
| DokuWiki | `[[target#section]]` | |
| MoinMoin | `[[Target#anchor]]`, `<<Anchor(name)>>` | |
| PmWiki | `[[Target#name]]`, `[[#name]]` defines | |
| TWiki / Foswiki | `[[Target#AnchorName]]`, `#AnchorName` defines | |
| XWiki 2.1 | `[[Target\|\|anchor="HHeading"]]` | |
| Trac | `[[Target#anchor]]` | |
| ikiwiki | `[[Target#anchor]]` | |
| Redmine | `[[Target#anchor]]` | |
| Wikidot | `[[[target#anchor \| Label]]]` | |
| Obsidian | `[[Target#Heading]]`, `[[Target#H1#H2]]` | `[[Target#^block-id]]`; define with trailing `^block-id` |
| Foam / Quartz | `[[Target#Heading]]` | `[[Target#^block-id]]` |
| Dendron | `[[target#heading]]` | `[[target#^block-id]]` |
| Silverbullet | `[[target#Heading]]` | `[[target@pos]]` (character position) |
| Logseq | | `((uuid))`; define with `id:: uuid` property |
| Roam | | `((block-uid))` |
| SiYuan | | `((id "anchor text"))` |
| Notion | | URL fragment with block id |
| Scrapbox / Cosense | | line permalink in URL |
| Federated Wiki | | item `id` in page JSON |
| Org-mode | `[[*Heading]]`, `[[#custom-id]]` | `[[id:uuid]]` |
| **Portable Wiki Markdown** | `[[Target#Heading text]]` (heading text, not slug) | `[[Target#^id]]`; define with trailing ` ^id` |

## 3. Hierarchy and namespaces in links

| Engine | Form | Separator | Notes |
|---|---|---|---|
| MediaWiki | `[[Help:Contents]]`, `[[Parent/Child]]` | `:` namespace, `/` subpage | Namespaces are fixed prefixes, not folders |
| DokuWiki | `[[ns:sub:page]]` | `:` | Maps to directories; `.:` and `..:` relative |
| MoinMoin | `[[Parent/Sub]]`, `[[/Sub]]`, `[[../Sibling]]` | `/` | |
| PmWiki | `[[Group/Page]]`, `[[Group.Page]]` | `/` or `.` | Two levels |
| TWiki / Foswiki | `Web.Topic`, `Web/Subweb.Topic` | `.` | |
| XWiki | `[[Space.Page]]`, `[[.Child]]`, `wiki:Space.Page` | `.` | Nested pages |
| Trac | `Parent/Child` | `/` | |
| ikiwiki | `[[parent/child]]` | `/` | SubPage linking rules |
| Gollum / forges | `[[/Folder/Page]]` | `/` | Relative to linking page by default |
| PukiWiki | `[[Parent/Child]]` | `/` | |
| GROWI | `[[/parent/child]]` | `/` | Path is identity |
| Zim | `[[:top:page]]`, `[[+sub]]` | `:` | `+` for child |
| Dendron | `[[project.area.topic]]` | `.` | File name is hierarchy |
| Logseq | `[[parent/child]]` | `/` | Namespace pages |
| Obsidian | `[[Folder/Note]]` | `/` | Bare title resolves vault-wide |
| Redmine | `[[project:Page]]` | `:` | Cross-project |
| Confluence wiki markup | `[SPACE:Page]` | `:` | Space key |
| Scrapbox / Cosense | `[/project/page]` | `/` (project only) | No hierarchy within a project |
| TiddlyWiki, Federated Wiki | | none | Flat by design |
| **Portable Wiki Markdown** | `[[ns/sub/Target]]` | `/` | Native separator declared in manifest; MediaWiki-style prefixes listed in `namespaces` |

## 4. Interwiki links

| Engine | Form | Map |
|---|---|---|
| MediaWiki | `[[wikipedia:Target]]`, `[[w:Target]]`; interlanguage `[[fr:Target]]` | interwiki table |
| DokuWiki | `[[wp>Target]]` | `conf/interwiki.conf` |
| MoinMoin | `MeatBall:Target`, `[[MeatBall:Target\|Label]]` | intermap |
| PmWiki | `[[Wikipedia:Target]]` | InterMap page |
| TWiki / Foswiki | `Wikipedia:Target` (plugin) | InterWikis topic |
| XWiki | `[[interwiki:wikipedia:Target]]` | configuration |
| Tiki | `ExternalWiki:Target` | external wikis |
| JSPWiki | `[Wikipedia:Target]` | InterWiki refs |
| Trac | `MeatBall:Target`, InterTrac `Trac:ticket:1` | InterMapTxt |
| ikiwiki | `[[!wikipedia Target]]` (shortcut directive) | shortcuts page |
| PukiWiki | `[[InterWikiName:Target]]` | InterWikiName page |
| Redmine | `[[project:Target]]` | projects |
| Federated Wiki | `[[Target]]` resolved across the neighbourhood | sitemaps |
| **Portable Wiki Markdown** | `[[prefix:Target]]` | manifest `interwiki` map (prefix → URL template) |

## 5. External links with label

| Engine | Form |
|---|---|
| MediaWiki | `[https://example.org Label]` |
| DokuWiki, MoinMoin, Zim, Creole | `[[https://example.org\|Label]]` |
| PmWiki | `[[https://example.org \| Label]]` |
| TWiki / Foswiki | `[[https://example.org][Label]]` |
| XWiki | `[[Label>>https://example.org]]` |
| JSPWiki | `[Label\|https://example.org]` |
| Trac | `[https://example.org Label]` |
| PukiWiki | `[[Label>https://example.org]]` |
| TiddlyWiki | `[[Label\|https://example.org]]`, `[ext[Label\|https://example.org]]` |
| Scrapbox / Cosense | `[https://example.org Label]` or `[Label https://example.org]` |
| Confluence wiki markup | `[Label\|https://example.org]` |
| Org-mode | `[[https://example.org][Label]]` |
| AsciiDoc | `link:https://example.org[Label]` or `https://example.org[Label]` |
| **Portable Wiki Markdown** (CommonMark) | `[Label](https://example.org)` |

## 6. Images and attachments

| Engine | Image | Notes |
|---|---|---|
| MediaWiki | `[[File:img.png\|thumb\|alt=Alt text\|Caption]]` | Media namespace; license required on Wikimedia projects |
| DokuWiki | `{{ns:img.png?200\|Caption}}` | Alignment by spaces inside braces |
| MoinMoin | `{{attachment:img.png}}` | |
| PmWiki | `Attach:img.png`, `http://.../img.png` | |
| TWiki / Foswiki | `%ATTACHURL%/img.png` | |
| XWiki | `[[image:attach:img.png]]` | |
| Tiki | `{img src="img.png"}` | |
| Trac | `[[Image(img.png)]]` | |
| ikiwiki | `[[!img img.png]]` | |
| PukiWiki | `#ref(img.png)`, `&ref(img.png);` | |
| TiddlyWiki | `[img[img.png]]`, `[img width=100 [img.png]]` | |
| Zim | `{{./img.png}}` | |
| Confluence wiki markup | `!img.png!` | |
| Obsidian | `![[img.png\|200]]`, also `![alt](img.png)` | |
| Logseq | `![alt](../assets/img.png)` | |
| Scrapbox / Cosense | bare image URL on a line; `[https://.../img.png]` | |
| Org-mode | `[[file:img.png]]` | |
| AsciiDoc | `image::img.png[Alt text]` | |
| **Portable Wiki Markdown** | `![Alt text](../attachments/img.png)` | Relative to the page file; metadata in sidecar |

## 7. Transclusion and includes

| Engine | Page include | Parameterized |
|---|---|---|
| MediaWiki | `{{:Target}}` | `{{Template\|param=value}}`; labelled sections by extension |
| DokuWiki | `{{page>ns:target}}` (include plugin) | |
| MoinMoin | `<<Include(Target)>>` | |
| PmWiki | `(:include Target:)` | `(:include Target#from#to:)` |
| TWiki / Foswiki | `%INCLUDE{"Web.Target"}%` | `%INCLUDE{"Web.Target" param="value"}%` |
| XWiki | `{{include reference="Space.Target"/}}`, `{{display .../}}` | |
| Tiki | `{include page="Target"}` | |
| JSPWiki | `[{InsertPage page='Target'}]` | |
| Trac | `[[Include(Target)]]` (plugin) | |
| ikiwiki | `[[!inline pages="target" raw=yes]]` | `[[!template id=name param=value]]` |
| PukiWiki | `#include(Target)` | |
| TiddlyWiki | `{{Target}}`, `{{Target!!field}}` | `{{Target\|\|Template}}`, `<<macro param>>` |
| Redmine | `{{include(Target)}}` | |
| Otter Wiki | `{{include\|src=/Target\|section=...}}` | |
| Confluence | Include Page / Excerpt Include macros (`ac:structured-macro`) | |
| Obsidian / Foam / Dendron / Quartz | `![[Target]]`, `![[Target#Heading]]`, `![[Target#^id]]` | |
| Logseq | `{{embed [[Target]]}}`, `{{embed ((uuid))}}` | `{{template name}}` |
| Roam | `{{embed: ((uid))}}` | |
| Notion | synced blocks | |
| Org-mode | `#+INCLUDE: "target.org"` | |
| AsciiDoc | `include::target.adoc[]` | attributes |
| **Portable Wiki Markdown** | `![[Target]]`, `![[Target#Heading text]]`, `![[Target#^id]]` | Snapshot envelope with `name` and `params` ([EXT-6](../12-Extensibility_Macros_and_Dynamic_Content.md)) |

## 8. Headings

| Engine | Level 1 | Level 2 | Notes |
|---|---|---|---|
| MediaWiki | `= H1 =` (reserved for the title) | `== H2 ==` | Body starts at `==` |
| DokuWiki | `====== H1 ======` | `===== H2 =====` | Fewer `=` means deeper |
| MoinMoin, Trac, XWiki, Creole | `= H1 =` | `== H2 ==` | |
| PmWiki | `! H1` | `!! H2` | |
| TWiki / Foswiki | `---+ H1` | `---++ H2` | |
| Tiki | `! H1` | `!! H2` | |
| JSPWiki | `!!! H1` | `!! H2` | Reversed count |
| PukiWiki | `* H` | `** H` | Renders as h2, h3 |
| TiddlyWiki | `! H1` | `!! H2` | |
| Confluence wiki markup | `h1. H1` | `h2. H2` | |
| Scrapbox / Cosense | `[*** text]` | `[** text]` | Size emphasis, not structure |
| Org-mode | `* H1` | `** H2` | |
| AsciiDoc | `= H1` | `== H2` | |
| Markdown family | `# H1` | `## H2` | |
| **Portable Wiki Markdown** | title in frontmatter; optional `# Title` | `## H2` | Body starts at `##` |

## 9. Emphasis

| Engine | Bold | Italic | Other |
|---|---|---|---|
| MediaWiki, MoinMoin, PmWiki, Trac | `'''bold'''` | `''italic''` | |
| PukiWiki | `''bold''` | `'''italic'''` | Note the reversal relative to MediaWiki |
| DokuWiki, Creole, XWiki, Zim, TiddlyWiki | `**bold**` | `//italic//` | DokuWiki `__underline__`, `''monospace''` |
| TWiki / Foswiki, Confluence wiki markup, AsciiDoc | `*bold*` | `_italic_` | |
| Tiki | `__bold__` | `''italic''` | |
| JSPWiki | `__bold__` | `''italic''` | |
| Scrapbox / Cosense | `[* bold]`, `[[bold]]` | `[/ italic]` | `[- strike]` |
| Org-mode | `*bold*` | `/italic/` | `_underline_`, `+strike+`, `~code~` |
| Markdown family | `**bold**` | `*italic*` | GFM `~~strike~~`; Obsidian `==highlight==` |
| **Portable Wiki Markdown** | `**bold**` | `*italic*` | `~~strike~~`; highlight has no portable form (use `<mark>` sparingly) |

## 10. Lists

| Engine | Bulleted | Numbered | Notes |
|---|---|---|---|
| MediaWiki, PmWiki, Creole, XWiki | `* item` | `# item` | Nesting by repeating markers |
| DokuWiki | `  * item` | `  - item` | Two-space indent required |
| MoinMoin, Trac | ` * item` | ` 1. item` | Leading space required |
| TWiki / Foswiki | `   * item` | `   1 item` | Three spaces |
| PukiWiki | `- item` | `+ item` | `--` nests |
| TiddlyWiki | `* item` | `# item` | |
| Confluence wiki markup | `* item` | `# item` | |
| Scrapbox / Cosense | indentation only | | Every indented line is a list item |
| Logseq | `- item` (every block) | numbered via property | Outliner |
| Org-mode | `- item` | `1. item` | |
| AsciiDoc | `* item` | `. item` | |
| Markdown family | `- item` | `1. item` | GFM task lists `- [ ] item` |
| **Portable Wiki Markdown** | `- item` | `1. item` | Nested lists carry outliner structure |

## 11. Code and preformatted text

| Engine | Block | Inline |
|---|---|---|
| MediaWiki | `<syntaxhighlight lang="x">...</syntaxhighlight>`, `<pre>`, leading space | `<code>...</code>` |
| DokuWiki | `<code php>...</code>`, `<file>`, two-space indent | `''mono''` |
| MoinMoin, Trac | `{{{#!python ... }}}`, `{{{ ... }}}` | `` `code` `` |
| PmWiki | `[@ code @]` | `@@code@@` |
| TWiki / Foswiki | `<verbatim>...</verbatim>` | `=code=` |
| XWiki | `{{code language="java"}}...{{/code}}` | `##code##` |
| Tiki | `{CODE()}...{CODE}` | `-+code+-` |
| PukiWiki | leading space (preformatted) | |
| TiddlyWiki | ```` ```lang ```` fenced | `` `code` `` |
| Confluence wiki markup | `{code:java}...{code}` | `{{code}}` |
| Scrapbox / Cosense | `code:filename.ext` then indented lines | `` `code` `` |
| Org-mode | `#+BEGIN_SRC lang ... #+END_SRC` | `~code~`, `=verbatim=` |
| AsciiDoc | `[source,lang]` + `----` block | `` `code` `` |
| Markdown family | ```` ```lang ```` fenced; four-space indent | `` `code` `` |
| **Portable Wiki Markdown** | ```` ```lang ```` fenced (info string carries language or diagram type) | `` `code` `` |

## 12. Tables

| Engine | Form |
|---|---|
| MediaWiki | `{\| class="wikitable"` ... `! header` ... `\| cell` ... `\|}` |
| DokuWiki | `^ header ^ header ^` / `\| cell \| cell \|` |
| MoinMoin, Trac | `\|\| cell \|\| cell \|\|` |
| PmWiki | `\|\| cell \|\| cell \|\|` (simple) or `(:table:)` directives |
| TWiki / Foswiki, TiddlyWiki | `\| cell \| cell \|` (TiddlyWiki `\|!header\|`) |
| XWiki, Creole | `\|=header\|=header` / `\|cell\|cell` |
| PukiWiki | `\|cell\|cell\|` with `\|h` suffix for header rows |
| Confluence wiki markup | `\|\|header\|\|header\|\|` / `\|cell\|cell\|` |
| Scrapbox / Cosense | `table:name` then tab-separated lines |
| Org-mode | `\| cell \| cell \|` with `\|---\|` |
| AsciiDoc | `\|===` block with `\|cell` |
| GFM | `\| a \| b \|` / `\|---\|---\|` / `\| c \| d \|` |
| **Portable Wiki Markdown** | GFM table; cells with spans or block content fall back to a small HTML subset declared in the manifest |

## 13. Footnotes and references

| Engine | Form |
|---|---|
| MediaWiki | `<ref>text</ref>` ... `<references />` |
| DokuWiki, PukiWiki | `((footnote text))` |
| MoinMoin | `<<FootNote(text)>>` |
| XWiki | `{{footnote}}text{{/footnote}}` |
| JSPWiki | `[1]` ... `[#1]` |
| Org-mode | `[fn:1]` ... `[fn:1] text` |
| AsciiDoc | `footnote:[text]` |
| GFM (GitHub), Obsidian, PHP Markdown Extra | `[^1]` ... `[^1]: text` |
| **Portable Wiki Markdown** | `[^1]` ... `[^1]: text` |

## 14. Hidden comments

| Engine | Form |
|---|---|
| MediaWiki, TiddlyWiki, Markdown family | `<!-- comment -->` |
| MoinMoin | `## comment` (line) |
| PmWiki | `(:comment text:)` |
| XWiki | `{{comment}}...{{/comment}}` |
| Trac | `{{{#!comment ... }}}` |
| PukiWiki | `// comment` (line) |
| Obsidian, Quartz | `%% comment %%` |
| Org-mode | `# comment`, `#+BEGIN_COMMENT ... #+END_COMMENT` |
| AsciiDoc | `// comment`, `//// block ////` |
| **Portable Wiki Markdown** | `<!-- comment -->` (`<!-- wiki:... -->` reserved for envelopes) |

## 15. Tags and categories

| Engine | Form | Tags are pages? |
|---|---|---|
| MediaWiki | `[[Category:Name]]` on the page | yes (category pages) |
| MoinMoin, first wiki | link to `CategoryName` page | yes |
| DokuWiki | `{{tag>name other}}` (plugin) | tag pages via plugin |
| PmWiki | `[[!Name]]` | yes (Category group) |
| TWiki / Foswiki | DataForm fields, tag plugins | no |
| XWiki | tag objects | no |
| ikiwiki | `[[!tag name]]` | yes (tag pages) |
| TiddlyWiki | `tags` field | yes |
| Confluence | labels | no |
| BookStack | name–value tags | no |
| Obsidian | `#tag` inline or `tags:` property | no (tag pane) |
| Logseq, Scrapbox / Cosense | `#tag` | yes |
| Org-mode | `:tag:` on headlines, `#+FILETAGS:` | no |
| **Portable Wiki Markdown** | `tags:` in frontmatter (inline `#tag` optional) | tag pages exported with `kind: category` |

## 16. Redirects and aliases

| Engine | Form |
|---|---|
| MediaWiki | `#REDIRECT [[Target]]` as the page body |
| MoinMoin | `#redirect Target` processing instruction |
| PmWiki | `(:redirect Target:)` |
| ikiwiki | `[[!meta redir=Target]]` |
| DokuWiki, Trac, Foswiki | plugins |
| Obsidian | `aliases:` property |
| Logseq | `alias::` property |
| Scrapbox / Cosense, Obsidian, Logseq | rename rewrites links instead |
| Confluence, Notion | identifier-based links; no redirect needed |
| **Portable Wiki Markdown** | `redirect:` and `kind: redirect` in frontmatter; `aliases:` on the target |

## 17. Table of contents and common macros

| Engine | TOC | General macro shape |
|---|---|---|
| MediaWiki | `__TOC__`, `__NOTOC__` | `{{Name\|param}}`, `{{#function:...}}`, `<tag>` |
| DokuWiki | `~~NOTOC~~` (TOC automatic) | `~~CONTROL~~`, `<plugin>`, `{{plugin>arg}}` |
| MoinMoin | `<<TableOfContents>>` | `<<Macro(args)>>` |
| PmWiki | `(:toc:)` | `(:directive args:)` |
| TWiki / Foswiki | `%TOC%` | `%MACRO{param="value"}%` |
| XWiki | `{{toc/}}` | `{{macro param="x"}}...{{/macro}}` |
| Tiki | `{maketoc}` | `{PLUGIN(params)}body{PLUGIN}` |
| JSPWiki | `[{TableOfContents}]` | `[{INSERT plugin WHERE param=value}]` |
| Trac | `[[TOC]]` | `[[Macro(args)]]`, `{{{#!processor}}}` |
| ikiwiki | `[[!toc]]` | `[[!directive param="value"]]` |
| Gollum | `[[_TOC_]]` | `<<Macro()>>` |
| PukiWiki | `#contents` | `#plugin(args)`, `&plugin(args){text};` |
| TiddlyWiki | `<<toc>>` | `<<macro param>>`, `<$widget>` |
| Redmine | `{{toc}}` | `{{macro(args)}}` |
| Confluence | Table of Contents macro | `ac:structured-macro` (storage); `{macro:param}` (legacy) |
| Otter Wiki | | `{{Macro\|param=value}}` |
| Logseq | | `{{macro arg}}`, `{{query ...}}`, `{{embed ...}}` |
| Silverbullet | | `${lua}`, ```` ```space-lua ```` |
| Org-mode | `#+TOC: headlines 2` | `#+BEGIN_name ... #+END_name`, `#+KEYWORD:` |
| AsciiDoc | `:toc:` attribute | `name::target[attrs]` block macro, `name:target[attrs]` inline |
| **Portable Wiki Markdown** | `::: toc` | `::: name key=value` container, `:name[text]{key=value}` inline; snapshot envelopes on export |

## 18. Callouts and admonitions

| Engine | Form |
|---|---|
| MediaWiki | templates (`{{Note\|...}}`), community-defined |
| DokuWiki | plugins (`<note>`, `<WRAP>`) |
| Confluence | `{info}`, `{note}`, `{tip}`, `{warning}` (legacy); panel macros |
| Logseq | `#+BEGIN_NOTE ... #+END_NOTE`, `#+BEGIN_TIP`, `#+BEGIN_WARNING`, `#+BEGIN_CAUTION`, `#+BEGIN_IMPORTANT` |
| Otter Wiki, Docmost, BookStack | "fancy blocks" / callout blocks (editor-specific) |
| MyST, Docusaurus, markdown-it-container | `:::note` ... `:::` |
| AsciiDoc | `NOTE: text`, `[WARNING]` + `====` block |
| GitHub (2023), Obsidian, Zettlr, Quartz | `> [!NOTE]` + block quote body (Obsidian adds many types and folding `+`/`-`) |
| **Portable Wiki Markdown** | `> [!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]`, `[!CAUTION]`; other types allowed |

## 19. Mathematics and diagrams

| Engine | Math | Diagrams |
|---|---|---|
| MediaWiki | `<math>...</math>` | extensions (Graph, Mermaid) |
| DokuWiki | plugins (`<latex>`, `$$`) | plugins |
| XWiki | `{{formula}}` macro | PlantUML macro |
| Confluence | LaTeX macros | draw.io, PlantUML, Mermaid apps |
| Scrapbox / Cosense | `[$ TeX]` | |
| TiddlyWiki | KaTeX plugin `$$` | |
| Logseq | `$...$`, `$$...$$` | Mermaid, PlantUML, Excalidraw |
| Obsidian | `$...$`, `$$...$$` | ```` ```mermaid ````; Canvas; Excalidraw plugin |
| GitHub, GROWI, Wiki.js, Docmost, HedgeDoc | `$...$`, `$$...$$` | ```` ```mermaid ```` and others |
| Org-mode | `$...$`, `\(...\)` | `#+BEGIN_SRC dot/plantuml` |
| AsciiDoc | `stem:[...]` | Asciidoctor Diagram |
| **Portable Wiki Markdown** | `$...$`, `$$...$$` (optional, declared) | fenced code with `mermaid`, `plantuml`, `graphviz` info strings |

## 20. Metadata and properties

| Engine | Mechanism |
|---|---|
| MediaWiki | categories; `{{DISPLAYTITLE:}}`; infobox templates; page props; Semantic MediaWiki `[[property::value]]` |
| DokuWiki | first heading as title; plugins (`struct`, `tag`) |
| MoinMoin | `#format`, `#language`, `#acl` processing instructions |
| PmWiki | `(:title Text:)`, `(:description ...:)`, page text variables `Name: value` |
| TWiki / Foswiki | DataForms (`%META:FIELD{...}%`) |
| XWiki | XObjects (typed classes) |
| TiddlyWiki | tiddler fields (`.tid` header lines) |
| Federated Wiki | page JSON (`title`, `story`, `journal`) |
| Confluence | labels, content properties, page status |
| Notion | database properties |
| Obsidian, Dendron, Hugo, Jekyll, Quartz | YAML frontmatter |
| Logseq | `key:: value` properties (page: first block) |
| Org-mode | `#+TITLE:`, `:PROPERTIES:` drawers |
| AsciiDoc | document attributes `:name: value` |
| Scrapbox / Cosense | none (JSON export carries dates and ids) |
| **Portable Wiki Markdown** | YAML frontmatter with the Portable Page Metadata vocabulary ([Appendix C](C-Portable_Page_Metadata_Reference.md)) |

## 21. Reading the crosswalk

Three observations follow from the tables.

1. **The ideas are identical; only the spelling differs.** Every engine has a way to link by title, label a link, embed an image, include a page, call a macro, and comment out text. A converter's work is spelling, order, and separator mapping, which is mechanical once declared.
2. **Four traps account for most conversion errors.** Label order (`T|L` versus `L|T`); hierarchy separator (`:` versus `/` versus `.`); the overloaded `{{...}}`; and emphasis markers that mean different things (`''text''` is italic in MediaWiki and bold in PukiWiki). Converters should test exactly these.
3. **Markdown has absorbed the common denominator.** Headings, emphasis, lists, code, tables, footnotes, and comments all have a single Markdown spelling that most new tools share; the wiki-specific additions of Chapter 08 are small by comparison.

---

Previous: [A · Wiki Engine Landscape](A-Wiki_Engine_Landscape.md) · Next: [C · Portable Page Metadata Reference](C-Portable_Page_Metadata_Reference.md)
