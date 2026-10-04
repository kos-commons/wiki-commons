# 11 · APIs and Discovery

> **Part III — Interoperability Guidelines** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [10 · Interchange and Portability](10-Interchange_and_Portability.md) · Next: [12 · Extensibility, Macros and Dynamic Content](12-Extensibility_Macros_and_Dynamic_Content.md)

**In one sentence:** There is no "Wiki API Protocol" and this chapter does not propose one; instead it lists the *capabilities* a wiki's API is encouraged to expose and shows how to express each with existing web standards (HTTP semantics, Web Linking, OpenAPI, Atom, OpenSearch, OAuth) so that generic tools can work with any wiki that follows them.

Recommendations in this chapter carry the prefix `API-`. The site description document's schema is `schemas/site-description.schema.json`.

---

## 1. Why capabilities, not a protocol

The source report notes that no unified API exists for fetching pages, history, or metadata. That is true, and the history of the field suggests why a single protocol is unlikely to win: engines differ in data model (document, block, line, tiddler), in transport taste (REST, GraphQL, JSON-RPC, XML-RPC, plain JSON files), and in their notion of identity and permission. Early in the 2000s a shared XML-RPC interface was implemented by several engines and then faded as each grew its own.

What generic tools actually need is smaller than a protocol. A converter needs to enumerate pages and fetch their source. An archiver needs history. A search aggregator needs a feed. A client library needs to know where the API is and how it is described. Each of these can be provided with standards that already exist. The recommendations below name the capability, then the conventional way to expose it. Engines keep their own transport and their own paths.

## 2. Recommendations

### Describing yourself

#### API-1 · Publish a machine-readable description

- REST APIs **should** be described with an OpenAPI document; GraphQL APIs **should** allow schema introspection or publish the schema; RPC-style APIs **should** publish a method list with types.
- The description **should** be discoverable from any page through Web Linking: `<link rel="service-desc" href="/api/openapi.json">` for the machine-readable description and `rel="service-doc"` for human documentation (both relations are registered for exactly this purpose).
- The wiki **should** also publish a **site description document**, a small JSON document discoverable with `<link rel="describedby" type="application/json" href="...">` (and, exploratorily, at `/.well-known/wiki`), containing at least: the wiki's name, engine and version, default language and license, the markup profile and native format, API roots and their description URLs, feed URLs, the interwiki map, the search description URL, and any conformance profiles the operator declares ([Chapter 16](16-Conformance_Profiles_and_Self_Assessment.md)). Example:

```json
{
  "format": "wiki-site-description",
  "version": "0.1",
  "name": "Example Project Wiki",
  "url": "https://wiki.example.org/",
  "engine": {"name": "examplewiki", "version": "4.2.0", "url": "https://example.org/examplewiki"},
  "lang": ["en", "ja"],
  "license": "CC-BY-SA-4.0",
  "markup": {"profile": "portable-wiki-markdown/2", "native_format": "text/markdown; variant=GFM", "link_label_order": "target-first"},
  "api": [{"kind": "rest", "root": "https://wiki.example.org/api/v1/", "description": "https://wiki.example.org/api/v1/openapi.json"}],
  "feeds": {"recent_changes": "https://wiki.example.org/feeds/changes.atom"},
  "search": "https://wiki.example.org/opensearch.xml",
  "sitemap": "https://wiki.example.org/sitemap.xml",
  "interwiki": {"wikipedia": "https://en.wikipedia.org/wiki/{title}"},
  "export": {"bundle": "https://wiki.example.org/api/v1/export/bundle"},
  "conformance": ["portable-content", "connected-wiki"]
}
```

### Reading

#### API-2 · Every page has a raw source URL

The single most valuable API is the simplest: a URL that returns one page as plain text in the portable profile ([Chapter 08](08-Markup_and_Syntax.md)) with its frontmatter ([Chapter 09](09-Metadata_and_Frontmatter.md)).
- Engines **should** serve it through content negotiation on the page's own URL (`Accept: text/markdown`) and/or a documented raw URL, with the response typed `text/markdown; charset=UTF-8` plus a `variant` parameter where one fits, and **should** advertise it in the HTML head: `<link rel="alternate" type="text/markdown" href="...">`.
- The native format, if different, **should** also be available (`text/x-wiki` for wikitext, `application/json` for block or JSON pages) and advertised the same way.
- Responses **should** carry `ETag` and `Last-Modified` and honour conditional requests, and **should** include `Link` headers for `edit`, `version-history`, `latest-version`, `license`, and `canonical` so that a client holding only the source can find everything else.
- The rendered HTML **should** be available too, as a complete page and, where feasible, as a fragment without site chrome.

#### API-3 · Enumerate pages

Clients **should** be able to list pages with cursor-based pagination and filters for namespace or space, tag, kind, and modification time. Each item **should** include title, path, stable identifier, last-modified time, and links to the page's source, HTML, and history. A full enumeration is what makes archiving and migration possible; it **should** be available to anyone who can read the wiki.

#### API-4 · History, revisions, and diffs

- A page's history **should** be listable with the fields of the portable history record ([XFER-7](10-Interchange_and_Portability.md)): revision identifier, parent, time, author, summary, flags.
- A single revision **should** be fetchable as source and as HTML, with `Link` relations `predecessor-version`, `successor-version`, `latest-version`, and `version-history` (all registered relations from the versioning vocabulary of RFC 5829).
- A diff between two revisions **should** be fetchable, at least as a unified text diff, optionally as HTML or a structured change list.
- Revision identifiers **should** be the same ones that appear in permalinks and exports ([HIST-5](06-Temporal_Design_and_Revision_History.md#hist-5--permalinks-to-revisions)).

#### API-5 · The graph and its health

Clients **should** be able to fetch, for a page, its backlinks and outgoing links (with resolution status), and, for the wiki, wanted pages, orphans, dead ends, and broken redirects ([NAV-4](04-Discovery_Navigation_and_Topology.md#nav-4--backlinks-what-links-here), [NAV-15](04-Discovery_Navigation_and_Topology.md#nav-15--health-views-orphans-wanted-dead-ends)). Engines with block identifiers **should** expose block references the same way.

#### API-6 · Changes as feeds

- Recent changes **should** be available as an Atom feed for the whole wiki, and are **encouraged** per namespace, per tag, and per page. Each entry **should** carry the page title, author, summary, time, and links to the page and to the diff. RSS and JSON Feed **may** be offered in addition.
- Feeds **should** be advertised in HTML (`<link rel="alternate" type="application/atom+xml">`), and the site description **should** list them.
- Real-time delivery (WebSub via `rel="hub"`, server-sent events, WebSockets) **may** be offered; the feed remains the portable baseline.

#### API-7 · Search and sitemaps

- A search endpoint **should** exist and **should** be described with an OpenSearch description document advertised as `<link rel="search" type="application/opensearchdescription+xml">`, so that browsers and aggregators can query the wiki without custom code. Results **should** include title, URL, snippet, and last-modified time.
- Public wikis **should** publish a sitemap (`sitemap.xml`) and a `robots.txt`.

#### API-8 · Attachments

Attachments **should** be listable and fetchable with their metadata ([XFER-4](10-Interchange_and_Portability.md)), and the page API **should** report which attachments a page uses.

#### API-9 · Interwiki map

The interwiki map (prefix → URL template) **should** be published in the site description document and **may** be available at its own endpoint ([NAV-13](04-Discovery_Navigation_and_Topology.md#nav-13--interwiki-links)).

#### API-10 · Bulk export

A bundle export ([Chapter 10](10-Interchange_and_Portability.md)) **should** be requestable through the API, for the whole wiki or a scope, as an archive or as a streamed sequence of files, so that migration never requires server access.

### Writing

#### API-11 · Create and update with optimistic concurrency

- Writes **should** be based on the revision the client read: either `If-Match` with the page's `ETag` or an explicit base revision identifier in the request. A stale base **should** produce a conflict response (HTTP 409 or 412) that includes the current revision and, where the engine can compute it, a merge attempt ([HIST-9](06-Temporal_Design_and_Revision_History.md#hist-9--gentle-conflict-resolution)).
- A write **should** accept a summary and a minor flag, **should** create an ordinary revision attributed to the authenticated principal, and **should** return the new revision identifier.
- Rename, soft delete, restore, and revert **should** be available as explicit operations that produce history events like their UI counterparts.
- Engines with real-time collaboration **may** expose their sync protocol; a plain revision-based write path **should** still exist for tools.

#### API-12 · Discussions and users (optional)

Where discussions exist, they **should** be readable through the API in the portable discussion shape ([XFER-10](10-Interchange_and_Portability.md)). Minimal user information for attribution (display name, profile URL, kind) **should** be available; contact details **should not** be ([PRIV-3](14-Security_Privacy_and_Trust.md)). A user's contributions **should** be listable ([COLL-8](07-Collaboration_Awareness_and_Governance.md#coll-8--visible-activity-and-contribution-history)).

### Mechanics

#### API-13 · Authentication and authorization

- Public wikis **should** allow anonymous read access to the API, with CORS headers permitting browser clients to read.
- For authenticated access, OAuth 2.0 (authorization code with PKCE for interactive clients; client credentials or personal access tokens as Bearer tokens for bots and scripts) is **recommended**; OpenID Connect is **recommended** for login federation. Scopes **should** be coarse and understandable (`read`, `write`, `history`, `upload`, `moderate`).
- Tokens **should** be revocable and listable by their owner.

#### API-14 · HTTP hygiene

JSON (UTF-8) as the default representation; RFC 3339 timestamps; BCP 47 language tags; cursor pagination with `Link: <...>; rel="next"`; `ETag` and conditional requests; problem-detail error bodies (RFC 9457); rate limiting communicated with the emerging standard `RateLimit` headers and `Retry-After`; API versioning in the path or media type with a documented deprecation policy using the `Deprecation` and `Sunset` headers.

#### API-15 · Events and webhooks (optional)

Engines **may** offer webhooks for page events (created, updated, renamed, deleted, uploaded, commented). Payloads **should** use the portable history record shape, **should** be signed, and **should** be retried with backoff.

## 3. Link relations in the page head

A reader's browser is also a client. The relations below, placed in the HTML `<head>` of every page, let tools discover a wiki's capabilities from any page without documentation. All are registered in the IANA link relations registry.

| Relation | Points to |
|---|---|
| `alternate` (+ `type="text/markdown"`) | The page's portable source ([API-2](#api-2--every-page-has-a-raw-source-url)) |
| `alternate` (+ `type="application/atom+xml"`) | A feed of changes to this page or the wiki ([API-6](#api-6--changes-as-feeds)) |
| `alternate` (+ `hreflang`) | The same page in another language ([I18N-6](13-Accessibility_Internationalization_and_Web_Standards.md)) |
| `canonical` | The preferred URL of this page |
| `bookmark` | A permalink to this revision ([HIST-5](06-Temporal_Design_and_Revision_History.md#hist-5--permalinks-to-revisions)) |
| `edit`, `edit-form` | Where to edit the page, by API or by form |
| `version-history` | The history view or API |
| `latest-version`, `predecessor-version`, `successor-version` | Navigation between revisions, on revision pages |
| `license` | The license of the content ([LIC-1](15-Licensing_and_Attribution.md)) |
| `author` | The contributors view or a person |
| `replies` | The discussion for this page ([COLL-3](07-Collaboration_Awareness_and_Governance.md#coll-3--talk-beside-content)) |
| `search` (+ OpenSearch type) | The search description ([API-7](#api-7--search-and-sitemaps)) |
| `service-desc`, `service-doc` | The API description and its documentation ([API-1](#api-1--publish-a-machine-readable-description)) |
| `describedby` (+ `type="application/json"`) | The site description document |
| `hub` | A WebSub hub for the feeds, if any |
| `via` | For forked pages, the page this one was forked from ([COLL-13](07-Collaboration_Awareness_and_Governance.md#coll-13--fork-instead-of-fight)) |
| `related` | Hand-curated or computed related pages ([NAV-12](04-Discovery_Navigation_and_Topology.md#nav-12--related-pages-and-the-two-hop-neighborhood)) |

## 4. Toward federation (exploratory)

The capabilities above make a wiki legible to tools. A few further steps, all using existing standards, would let wikis talk to each other.

- **Cross-wiki backlinks with Webmention.** When a page on wiki A links to a page on wiki B, A **may** send a Webmention to B's advertised endpoint; B **may** then show the link among its backlinks, labelled as external. This is the open web's existing answer to "what links here" across sites.
- **Change notifications with ActivityPub.** A wiki **may** publish page updates as ActivityStreams activities so that other wikis, feed readers, and social software can follow it. Several projects have experimented with wikis as ActivityPub actors.
- **Neighbourhoods and forking.** Federated Wiki's design, in which each site publishes `sitemap.json` and every page is fetchable as `/slug.json`, shows how little is needed for cross-site discovery and forking: a list of pages, a stable page representation, and provenance. The bundle and site description above are deliberately compatible with that idea.
- **Identity across wikis.** WebFinger and OpenID Connect allow a contributor to be recognized across sites without a central directory; Decentralized Identifiers are a further option.
- **An interwiki registry.** A community-maintained list of common prefixes and URL templates would let every engine ship the same defaults ([17 · Roadmap](17-Roadmap_and_Open_Questions.md)).
- **Agent interfaces.** By 2026 a number of engines expose their content to software agents through Model Context Protocol servers or agent-oriented command-line tools in addition to, or instead of, REST. These are a new kind of client, not a new kind of wiki; the capabilities listed above are what such interfaces end up wrapping, and engines are **encouraged** to build them on the same page, history, and search operations rather than on a parallel model.

None of this is required for a good wiki. All of it becomes possible once the ordinary capabilities above exist.

## 5. Observed in

- **MediaWiki** offers an Action API and a REST API, the latter with a served OpenAPI description; XML dumps and Atom feeds have existed for two decades; OAuth is available through an extension.
- **DokuWiki** exposes XML-RPC and, since its 2024 release, JSON-RPC with a generated OpenAPI 3.1 document and token authentication.
- **XWiki** provides a REST API over wikis, spaces, pages, objects, and classes, with a downloadable OpenAPI description.
- **Wiki.js** and **Kibela** use GraphQL; **BookStack** (self-documented at a `/api/docs` endpoint), **Outline** (with an OpenAPI description and OAuth 2.0), **Trilium** (an OpenAPI-described REST interface), **GROWI**, **Redmine**, **Confluence** (REST v2 with an OpenAPI description), **Notion**, and **esa.io** offer REST APIs with documented resources and tokens; **GitLab** exposes wikis through its general API.
- **Federated Wiki** serves every page as JSON and every site's page list as `sitemap.json`, which is an API without a specification.
- **TiddlyWiki** in server mode exposes a small HTTP interface descended from TiddlyWeb; **Gollum**, **ikiwiki**, and other git-backed wikis have no API beyond the repository itself, which is a complete read/write interface of its own.
- In the early 2000s a shared XML-RPC "WikiRPCInterface", defined by JSPWiki and implemented by MoinMoin and DokuWiki (whose XML-RPC API still exposes its `wiki.*` methods), was the closest thing to a common wiki API that has existed; its fate is a caution against over-specifying.

---

Previous: [10 · Interchange and Portability](10-Interchange_and_Portability.md) · Next: [12 · Extensibility, Macros and Dynamic Content](12-Extensibility_Macros_and_Dynamic_Content.md)
