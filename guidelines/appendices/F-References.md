# Appendix F · References

> **Appendices** · **Status:** Working Draft 0.4 (October 2026)
> Previous: [E · Glossary](E-Glossary.md) · Index: [README](../../README.md)

Versions and dates were checked against primary sources (specification home pages, the RFC Editor, IANA registries, W3C technical reports, project release pages) in the first week of October 2026. Where a date or version could not be confirmed against a primary source it is marked *(unverified)*. Standards evolve; readers should check the canonical URL.

---

## 1. Standards and specifications

### Markup

- **CommonMark Spec**, version 0.31.2, 28 January 2024. John MacFarlane and the CommonMark project. https://spec.commonmark.org/0.31.2/ — No wikilink extension; no extension mechanism.
- **GitHub Flavored Markdown Spec**, version 0.29-gfm, 6 April 2019. GitHub. https://github.github.com/gfm/ — Tables, task lists, strikethrough, autolinks, tag filter.
- **GitHub Markdown alerts** (`> [!NOTE]` and four other types), announced 14 December 2023. https://github.blog/changelog/2023-12-14-new-markdown-extension-alerts-provide-distinctive-styling-for-significant-content/ — Footnotes (2021), math (2022), and Mermaid (2022) are GitHub renderer features outside the GFM specification.
- **Generic directives / plugins syntax** discussion, CommonMark forum (since 2014; not adopted into the specification). https://talk.commonmark.org/t/generic-directives-plugins-syntax/444 — Implementations: `remark-directive` (4.0.0, 2025), `markdown-it-container` (4.0.0, 2023).
- **Obsidian Flavored Markdown**, **Callouts**, **Properties**, **Bases** (help documentation). Obsidian. https://help.obsidian.md/obsidian-flavored-markdown , https://help.obsidian.md/callouts , https://help.obsidian.md/properties , https://help.obsidian.md/bases — Bases introduced in 1.9.0 (May 2025), generally available in 1.9.10 (August 2025).
- **JSON Canvas Spec**, version 1.0, 11 March 2024, MIT license. https://jsoncanvas.org/spec/1.0/
- **Pandoc** 3.12 (29 September 2026), John MacFarlane. https://pandoc.org/ (Lua filters: https://pandoc.org/lua-filters.html) — Wikilink extensions `wikilinks_title_after_pipe` and `wikilinks_title_before_pipe` since 3.0 (January 2023). Readers: creole, djot, dokuwiki, jira, mediawiki, muse, org, t2t, tikiwiki, twiki, vimwiki. Writers: djot, dokuwiki, jira, markua, mediawiki, muse, org, t2t, xwiki, zimwiki.
- **RFC 7763**, *The text/markdown Media Type*, March 2016, Informational. https://www.rfc-editor.org/info/rfc7763 — `charset` parameter required; optional `variant`.
- **RFC 7764**, *Guidance on Markdown: Design Philosophies, Stability Strategies, and Select Registrations*, March 2016, Informational. https://www.rfc-editor.org/info/rfc7764
- **IANA Markdown Variants registry** (first come, first served; thirteen entries including Original, MultiMarkdown, GFM, pandoc, CommonMark, Extra, myst). https://www.iana.org/assignments/markdown-variants/
- **Djot** (John MacFarlane; pre-1.0, syntax "not completely stable"). https://djot.net/
- **MyST Markdown** specification (in development). https://spec.mystmd.org/
- **AsciiDoc Language** specification project, Eclipse Foundation (incubating; no released version). https://projects.eclipse.org/projects/asciidoc.asciidoc-lang
- **reStructuredText** (Docutils 0.23, May 2026). https://docutils.sourceforge.io/rst.html
- **Org Syntax** (v2), Worg. https://orgmode.org/worg/org-syntax.html
- **WikiCreole 1.0**, final specification 4 July 2007 (frozen). http://www.wikicreole.org/wiki/Creole1.0 *(site intermittently unavailable)*. Sauer, C., Smith, C., Benz, T., "WikiCreole: a common wiki markup", *WikiSym 2007*, https://doi.org/10.1145/1296951.1296966
- **YAML 1.2.2**, 1 October 2021. https://yaml.org/spec/1.2.2/
- **TOML 1.1.0**, 18 December 2025. https://toml.io/en/v1.1.0
- **JSON Schema**, draft 2020-12. https://json-schema.org/specification — IETF JSON Schema working group drafts in progress (RFC targeted 2027).
- **MediaWiki DOM Spec (Parsoid HTML)**, version 2.8.0. https://www.mediawiki.org/wiki/Specs/HTML/2.8.0
- **MediaWiki XML export schema**, version 0.11. https://www.mediawiki.org/xml/export-0.11.xsd
- **Confluence storage format** (XHTML with `ac:`/`ri:` namespaces). https://confluence.atlassian.com/doc/confluence-storage-format-790796544.html
- **Atlassian Document Format** (JSON). https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/
- **Notion API block object**. https://developers.notion.com/reference/block
- **Portable Text** (Sanity). https://github.com/portabletext/portabletext
- **ProseMirror document model**. https://prosemirror.net/docs/guide/#doc
- **BookStack Portable ZIP file format**, BookStack project, `dev/docs/portable-zip-file-format.md` in the BookStack repository (https://codeberg.org/bookstack/bookstack; mirrored at https://github.com/BookStackApp/BookStack). See [Appendix H](H-BookStack_and_MediaWiki_Alignment.md).
- **Open Knowledge Format (OKF)**, version 0.2, Google Cloud, 2026 (0.1 published June 2026). Canonical repository: https://github.com/GoogleCloudPlatform/open-knowledge-format (specification in `SPEC.md`; an earlier frozen copy lives under `okf/` in `GoogleCloudPlatform/knowledge-catalog`). Outline's OKF export shipped in Outline 1.10.1 (September 2026). See [Appendix G](G-Open_Knowledge_Format_Alignment.md).

### Metadata and identifiers

- **DCMI Metadata Terms**, 20 January 2020. Dublin Core Metadata Initiative. https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ — Also ISO 15836-1:2017 and ISO 15836-2:2019.
- **schema.org**, version 30.1, 16 September 2026. https://schema.org/ — `CreativeWork`, `Article`, `WebPage`, `author`, `dateCreated`, `dateModified`, `license`, `inLanguage`.
- **RFC 9562**, *Universally Unique IDentifiers (UUIDs)*, May 2024, Proposed Standard (obsoletes RFC 4122; defines versions 6, 7, 8). https://www.rfc-editor.org/info/rfc9562
- **RFC 3339**, *Date and Time on the Internet: Timestamps*, July 2002 (updated by RFC 9557, April 2024). https://www.rfc-editor.org/info/rfc3339
- **BCP 47 / RFC 5646**, *Tags for Identifying Languages*, September 2009. https://www.rfc-editor.org/info/rfc5646
- **Unicode 18.0.0**, 16 September 2026; **UAX #15 Unicode Normalization Forms**, revision 58, August 2026. https://www.unicode.org/reports/tr15/
- **RFC 3987**, *Internationalized Resource Identifiers (IRIs)*, January 2005. https://www.rfc-editor.org/info/rfc3987
- **RFC 3986**, *Uniform Resource Identifier (URI): Generic Syntax*, January 2005, Internet Standard 66. https://www.rfc-editor.org/info/rfc3986
- **RFC 8288**, *Web Linking*, October 2017. https://www.rfc-editor.org/info/rfc8288
- **IANA Link Relations registry**. https://www.iana.org/assignments/link-relations/ — Relations used in this suite and their defining documents: `edit`, `service` (RFC 5023); `edit-form` (RFC 6861); `version-history`, `latest-version`, `predecessor-version`, `successor-version`, `working-copy` (RFC 5829); `alternate`, `author`, `bookmark` (HTML); `canonical` (RFC 6596); `license` (RFC 4946); `describedby` (POWDER); `search` (OpenSearch); `hub` (WebSub); `replies` (RFC 4685); `collection`, `item` (RFC 6573); `related`, `via` (RFC 4287); `service-desc`, `service-doc` (RFC 8631).
- **RFC 9457**, *Problem Details for HTTP APIs*, July 2023. https://www.rfc-editor.org/info/rfc9457
- **RFC 8594**, *The Sunset HTTP Header Field*, May 2019; **RFC 9745**, *The Deprecation HTTP Response Header Field*, March 2025. https://www.rfc-editor.org/info/rfc8594 , https://www.rfc-editor.org/info/rfc9745
- **RateLimit header fields for HTTP** (IETF HTTPAPI working group draft; not yet an RFC). https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/
- **RFC 4180**, *Common Format and MIME Type for Comma-Separated Values (CSV) Files*, October 2005. https://www.rfc-editor.org/info/rfc4180

### Licensing

- **SPDX License List**, version 3.29.0, 16 September 2026. https://spdx.org/licenses/
- **Creative Commons 4.0 licenses** (CC BY 4.0, CC BY-SA 4.0; CC0 1.0 public domain dedication). https://creativecommons.org/licenses/ — 4.0 released November 2013 *(date unverified)*.
- **Open Definition 2.1** and conformant licenses. Open Knowledge Foundation. https://opendefinition.org/od/2.1/en/ , https://opendefinition.org/licenses/
- **Wikimedia Terms of Use, Creative Commons 4.0 update**, effective 7 June 2023. https://meta.wikimedia.org/wiki/Terms_of_use/Creative_Commons_4.0 — Earlier migration from GFDL to CC BY-SA 3.0 in June 2009 *(date not re-verified)*.

### APIs, feeds, discovery, identity

- **OpenAPI Specification**, version 3.2.1, 10 September 2026 (3.2.0: 19 September 2025). OpenAPI Initiative. https://spec.openapis.org/oas/latest.html
- **JSON:API**, version 1.1, 30 September 2022. https://jsonapi.org/format/1.1/
- **GraphQL Specification**, September 2025 edition. GraphQL Foundation. https://spec.graphql.org/
- **AsyncAPI**, version 3.1.0, 31 January 2026. https://www.asyncapi.com/docs/reference/specification/latest
- **RFC 4287**, *The Atom Syndication Format*, December 2005. https://www.rfc-editor.org/info/rfc4287
- **RSS 2.0 Specification**, version 2.0.11, 30 March 2009. RSS Advisory Board. https://www.rssboard.org/rss-specification
- **JSON Feed**, version 1.1, 7 August 2020. https://www.jsonfeed.org/version/1.1/
- **WebSub**, W3C Recommendation 23 January 2018; republished 2 June 2026. https://www.w3.org/TR/websub/
- **Webmention**, W3C Recommendation 12 January 2017. https://www.w3.org/TR/webmention/
- **Micropub**, W3C Recommendation 23 May 2017. https://www.w3.org/TR/micropub/
- **ActivityPub**, W3C Recommendation 23 January 2018; **Activity Streams 2.0** and **Activity Vocabulary**, W3C Recommendations 23 May 2017. https://www.w3.org/TR/activitypub/ , https://www.w3.org/TR/activitystreams-core/ — Maintained by the W3C Social Web Working Group chartered January 2026.
- **Web Annotation Data Model**, W3C Recommendation 23 February 2017 (with Vocabulary and Protocol). https://www.w3.org/TR/annotation-model/
- **OpenSearch 1.1 Draft 6** (de facto, frozen). https://github.com/dewitt/opensearch
- **Sitemaps protocol**, version 0.9. https://www.sitemaps.org/protocol.html
- **RFC 9309**, *Robots Exclusion Protocol*, September 2022. https://www.rfc-editor.org/info/rfc9309
- **RFC 8615**, *Well-Known Uniform Resource Identifiers (URIs)*, May 2019; IANA well-known URIs registry. https://www.rfc-editor.org/info/rfc8615 , https://www.iana.org/assignments/well-known-uris/
- **RFC 7033**, *WebFinger*, September 2013. https://www.rfc-editor.org/info/rfc7033
- **RFC 9116**, *A File Format to Aid in Security Vulnerability Disclosure* (`security.txt`), April 2022. https://www.rfc-editor.org/info/rfc9116
- **RFC 6749**, *The OAuth 2.0 Authorization Framework*, October 2012; **RFC 6750**, *Bearer Token Usage*; **RFC 7636**, *PKCE*, September 2015; **RFC 9700**, *Best Current Practice for OAuth 2.0 Security*, January 2025. https://www.rfc-editor.org/info/rfc6749
- **OAuth 2.1** (IETF draft-ietf-oauth-v2-1-16, September 2026; not yet an RFC). https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/
- **OpenID Connect Core 1.0 incorporating errata set 2**, 15 December 2023. https://openid.net/specs/openid-connect-core-1_0.html
- **Web Authentication Level 3**, W3C Recommendation 25 August 2026. https://www.w3.org/TR/webauthn-3/
- **Model Context Protocol** (specification for connecting software agents to tools and data; referenced as an emerging agent interface). https://modelcontextprotocol.io/

### Accessibility, internationalization, security, privacy

- **WCAG 2.2**, W3C Recommendation 5 October 2023 (republished with errata 12 December 2024). https://www.w3.org/TR/WCAG22/ — **WCAG 3.0** remains a Working Draft (September 2026).
- **ATAG 2.0**, *Authoring Tool Accessibility Guidelines*, W3C Recommendation 24 September 2015. https://www.w3.org/TR/ATAG20/
- **WAI-ARIA 1.2**, W3C Recommendation 6 June 2023; **WAI-ARIA 1.3** Working Draft (June 2026). https://www.w3.org/TR/wai-aria-1.2/
- **EN 301 549** V4.1.1, September 2026 (web baseline moves to WCAG 2.2). ETSI/CEN/CENELEC. https://www.etsi.org/deliver/etsi_en/301500_301599/301549/
- **European Accessibility Act**, Directive (EU) 2019/882, applicable from 28 June 2025 *(date not re-verified)*.
- **MathML Core**, W3C. https://www.w3.org/TR/mathml-core/
- **Unicode CLDR** (locale data: plural rules, collation, formats). https://cldr.unicode.org/
- **Content Security Policy Level 3**, W3C Working Draft (September 2026). https://www.w3.org/TR/CSP3/
- **HTML Sanitizer API** (merged into the HTML Living Standard: `setHTML()`; partial browser support). https://html.spec.whatwg.org/multipage/dynamic-markup-insertion.html
- **Subresource Integrity** (Level 1 Recommendation 2016; Level 2 Working Draft 2026). https://www.w3.org/TR/sri-2/
- **Trusted Types**, W3C Working Draft (June 2026). https://www.w3.org/TR/trusted-types/
- **OWASP Application Security Verification Standard** 5.0.0, May 2025. https://owasp.org/www-project-application-security-verification-standard/
- **OWASP Top 10:2025**. https://owasp.org/Top10/2025/
- **GDPR**, Regulation (EU) 2016/679, Article 20 (right to data portability). **EU Data Act**, Regulation (EU) 2023/2854, applicable from 12 September 2025 *(not re-verified)*.
- **TDM Reservation Protocol (TDMRep)**, W3C Community Group Final Report, 2 February 2024. https://www.w3.org/community/reports/tdmrep/CG-FINAL-tdmrep-20240202/
- **IETF AI Preferences (aipref) working group** drafts (vocabulary and attachment; no RFC yet). https://datatracker.ietf.org/wg/aipref/about/

### Real-time collaboration and local-first

- **Yjs** 13.6.x (MIT), Kevin Jahns. https://yjs.dev/ — **yrs** (Rust port) used by AppFlowy; **y-octo** by AFFiNE.
- **Hocuspocus** 4.x (MIT), the Yjs WebSocket backend used by Outline and Docmost. https://tiptap.dev/docs/hocuspocus
- **Automerge** 3.x (MIT). https://automerge.org/
- **Loro** 1.x (MIT). https://loro.dev/
- Kleppmann, M., Wiggins, A., van Hardenberg, P., McGranaghan, M., *Local-first software: You own your data, in spite of the cloud*, Ink & Switch, April 2019. https://www.inkandswitch.com/essay/local-first/ — Also *Onward! 2019*, https://doi.org/10.1145/3359591.3359737
- **ChainPad** (used by XWiki's real-time editor) and **Easysync** (Etherpad's operational-transformation model) as the non-CRDT reference points.

## 2. Wiki history, philosophy, and community norms

- Cunningham, W., *Wiki Design Principles*, c2.com. https://wiki.c2.com/?WikiDesignPrinciples — The list quoted in [Chapter 02](../02-Guiding_Principles.md); Cunningham notes it is "a reconstruction from memory of intentions I held at the beginning".
- Cunningham, W., *Wiki History* and *Why Wiki Works*, c2.com. https://wiki.c2.com/?WikiHistory , https://wiki.c2.com/?WhyWikiWorks — "This began on March 25, 1995."; "Possibly it works because there is no mechanically enforced authority."
- Cunningham, W., *What is Wiki*, wiki.org, 27 June 2002: "the simplest online database that could possibly work" (as quoted in the Wikipedia article *Wiki*).
- Leuf, B., Cunningham, W., *The Wiki Way: Quick Collaboration on the Web*, Addison-Wesley, 2001.
- MeatballWiki (Sunir Shah and contributors): *SoftSecurity*, *AssumeGoodFaith*, *PeerReview*, *ForgiveAndForget*, *DocumentMode*, *ThreadMode*, *BarnRaising*, *GodKing*, *CommunityExpectations*, *LinkPattern*, *InterMap*, *InterWiki*, *TwinPages*, *WikiNow*, *FreeLink*, *PageDatabase*. http://meatballwiki.org/wiki/
- Wikipedia (English) policies and help pages: *Five pillars*, *Be bold*, *Assume good faith*, *Ignore all rules*, *Etiquette*, *Red link*, *Stub*, *BOLD, revert, discuss cycle*, *Orphan*, *Dead-end pages*; *Help:Talk pages*, *Help:Watchlist*, *Help:Edit summary*, *Help:Minor edit*. https://en.wikipedia.org/wiki/Wikipedia:Five_pillars and related.
- UseModWiki and free links: Adams, C., UseModWiki, 1999 onward; free links named February 2001. https://en.wikipedia.org/wiki/UseModWiki
- Cunningham, W., *Smallest Federated Wiki* (2011) and Federated Wiki documentation: *Journal*, *Neighborhood*, *About Federated Wiki*. https://github.com/WardCunningham/Smallest-Federated-Wiki , http://fed.wiki.org/view/about-federated-wiki
- Caulfield, M., *The Garden and the Stream: A Technopastoral*, 17 October 2015. https://hapgood.us/2015/10/17/the-garden-and-the-stream-a-technopastoral/
- Appleton, M., *A Brief History & Ethos of the Digital Garden*, 10 June 2020. https://maggieappleton.com/garden-history — Six patterns; seedling, budding, evergreen markers.
- Critchlow, T., *Of Digital Streams, Campfires and Gardens* (2018) and *Building a digital garden* (2019). https://tomcritchlow.com/2018/10/10/of-gardens-and-wikis/
- Hooks, J., *My blog is a digital garden, not a blog* (2019). https://joelhooks.com/digital-garden
- Matuschak, A., *Evergreen notes*. https://notes.andymatuschak.org/Evergreen_notes
- Matuschak, A., Nielsen, M., *How can we develop transformative tools for thought?*, October 2019. https://numinous.productions/ttft/
- Ango, S., *File over app*, 1 July 2023. https://stephango.com/file-over-app — Obsidian manifesto: https://obsidian.md/about
- Masui, T., *Scrapboxは情報整理ツールなのか* (2019) and *なぜScrapboxはMarkdownを採用していないのか* (2019). https://scrapbox.io/masui/ — Cosense help: *Cosenseの特長*, *関連ページリスト*, *ブラケティング*. https://scrapbox.io/help-jp/
- Helpfeel Inc., *Scrapbox renamed Helpfeel Cosense*, press release, 21 May 2024. https://prtimes.jp/main/html/rd/p/000000323.000027275.html
- esa LLC, *esa concept* ("Nothing is perfect from the beginning"; Share → Develop → Organize; WIP). https://esa.io/concept
- Nelson, T., *Literary Machines* (1980), origin of the term *transclusion*.
- Winer, D., outliners (ThinkTank, 1983) and **OPML** (2000). http://dev.opml.org/spec2.html

## 3. Research

- Spinellis, D., Louridas, P., "The collaborative organization of knowledge", *Communications of the ACM* 51(8), 2008. https://doi.org/10.1145/1378704.1378720 — Most new Wikipedia articles are created shortly after a link to them appears.
- Nov, O., "What motivates Wikipedians?", *Communications of the ACM* 50(11), 2007. https://doi.org/10.1145/1297797.1297798
- Halfaker, A., Kittur, A., Riedl, J., "Don't bite the newbies: how reverts affect the quantity and quality of Wikipedia work", *WikiSym 2011*. https://doi.org/10.1145/2038558.2038585
- Halfaker, A., Geiger, R. S., Morgan, J. T., Riedl, J., "The Rise and Decline of an Open Collaboration System", *American Behavioral Scientist* 57(5), 2013. https://doi.org/10.1177/0002764212469365
- Butler, B., Joyce, E., Pike, J., "Don't look now, but we've created a bureaucracy", *CHI 2008*. https://doi.org/10.1145/1357054.1357227
- Suh, B., Convertino, G., Chi, E. H., Pirolli, P., "The singularity is not near: slowing growth of Wikipedia", *WikiSym 2009*. https://doi.org/10.1145/1641309.1641322
- Elliott, M., "Stigmergic Collaboration: The Evolution of Group Work", *M/C Journal* 9(2), 2006. https://doi.org/10.5204/mcj.2599
- Halfaker, A., Geiger, R. S., Terveen, L., "Snuggle: Designing for efficient socialization and ideological critique", *CHI 2014*. https://doi.org/10.1145/2556288.2557313
- Morgan, J. T., Bouterse, S., Walls, H., Stierch, S., "Tea and sympathy: crafting positive new user experiences on Wikipedia", *CSCW 2013*. https://doi.org/10.1145/2441776.2441871
- Edmondson, A., "Psychological Safety and Learning Behavior in Work Teams", *Administrative Science Quarterly* 44(2), 1999. https://doi.org/10.2307/2666999
- Alexander, C., Ishikawa, S., Silverstein, M., *A Pattern Language*, Oxford University Press, 1977.
- Luhmann, N., "Kommunikation mit Zettelkästen", 1981. https://doi.org/10.1007/978-3-322-87749-9_19 ; Ahrens, S., *How to Take Smart Notes*, 2017.
- Rheingold, H., *Tools for Thought*, 1985.

## 4. Prior standardization attempts

- Sauer, C., Smith, C., Benz, T., "WikiCreole: a common wiki markup", *WikiSym 2007*. https://doi.org/10.1145/1296951.1296966 ; Junghans, M., Riehle, D., Yalcinalp, U., "An XML interchange format for Wiki Creole 1.0", *ACM SIGWEB Newsletter*, 2007. https://doi.org/10.1145/1324960.1324965
- Völkel, M., Oren, E., "Towards a Wiki Interchange Format (WIF)", *SemWiki 2006*, CEUR-WS Vol. 206. http://ceur-ws.org/Vol-206/
- Völkel, M., Krötzsch, M., Vrandečić, D., Haller, H., Studer, R., "Semantic Wikipedia", *WWW 2006*. https://doi.org/10.1145/1135777.1135863
- MediaWiki *Markup spec* project (2006–2010, inactive). https://www.mediawiki.org/wiki/Markup_spec
- WikiRPCInterface (XML-RPC), JSPWiki; implemented by MoinMoin and DokuWiki. https://moinmo.in/WikiRpc , https://www.dokuwiki.org/devel:xmlrpc
- The International Symposium on Wikis (WikiSym, 2005–2013) and Open Collaboration (OpenSym, 2014–2022). https://opensym.org/about/

## 5. Engine documentation consulted

Project sites and documentation for the engines in [Appendix A](A-Wiki_Engine_Landscape.md), including: mediawiki.org (Version lifecycle, Help:Links, Help:Export, API:REST_API, Parsoid, Trust and Safety Product/Temporary Accounts); dokuwiki.org (wiki:syntax, devel:jsonrpc, devel:xmlrpc, changes); moinmo.in and moin-20.readthedocs.io; pmwiki.org; twiki.org and the foswiki/distro repository; xwiki.org (XWikiSyntax 2.1, REST API, Realtime WYSIWYG Editor); tiki.org; jspwiki.apache.org; trac.edgewall.org; ikiwiki.info; the gollum, GitHub, GitLab, Gitea, and Azure DevOps wiki documentation; hackage.haskell.org/package/gitit; pukiwiki.sourceforge.io; tiddlywiki.com; github.com/fedwiki and fed.wiki.org; zim-wiki.org; redmine.org; docs.requarks.io; bookstackapp.com; getoutline.com/developers and the outline/outline repository; github.com/docmost/docmost; docs.growi.org and github.com/crowi/crowi; otterwiki.com; docs.silverbullet.md; github.com/TriliumNext/Trilium; docs.foam.md; the dendronhq/dendron repository; confluence.atlassian.com and developer.atlassian.com; developers.notion.com and notion.com/help; scrapbox.io/help and help-jp; esa.io and docs.esa.io; kibe.la and support.kibe.la; docbase.io; help.nuclino.com; gitbook.com/docs; community.fandom.com and meta.miraheze.org; wikidot.com; hedgedoc.org and the etherpad repository; help.obsidian.md and obsidian.md/changelog; github.com/logseq/logseq and logseq/docs; roamresearch.com; github.com/toeverything/AFFiNE; github.com/AppFlowy-IO; anytype.io and developers.anytype.io; github.com/siyuan-note/siyuan; tana.inc; capacities.io; quartz.jzhao.xyz.

---

Previous: [E · Glossary](E-Glossary.md) · Index: [README](../../README.md)
