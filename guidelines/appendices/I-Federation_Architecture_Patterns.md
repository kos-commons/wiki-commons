# Appendix I · Federation Architecture Patterns

> **Appendices** · **Status:** Working Draft 0.4 (October 2026) · **Maturity:** Exploratory throughout
> Previous: [H · BookStack and MediaWiki Alignment](H-BookStack_and_MediaWiki_Alignment.md) · Index: [README](../../README.md)

**In one sentence:** Fourteen exploratory patterns, in the format of Part II, for wikis that want to see, cite, copy, and notify each other across site boundaries, built on the portable pieces this suite already has and on standards the web already offers.

Everything here is optional direction. No pattern in this appendix is required for a good wiki, and none is required for any conformance profile. They are written down because several engines are moving this way independently and because the mistakes are easier to avoid when the trade-offs are named.

---

## 1. Why federation, and why now

A wiki is a community's shared memory, and communities overlap. The classic answers to overlap were interwiki links (cite across sites) and consensus (one page per topic, argued into shape). Federated Wiki, Ward Cunningham's second wiki design, proposed a third: every author owns a site, pages are copied between sites with their provenance, and readers browse a neighbourhood of sites rather than one. Meanwhile the open web grew standards for exactly the cross-site primitives wikis need: Webmention for "you linked to me", WebSub and ActivityPub for "I changed", WebFinger and OpenID Connect for "this is who I am", and content-addressed archives for "this is exactly what I had". The patterns below put these pieces together without inventing a protocol.

Two warnings up front. Federation multiplies every privacy and licensing question by the number of sites involved ([Chapter 14](../14-Security_Privacy_and_Trust.md), [Chapter 15](../15-Licensing_and_Attribution.md)). And federation is not a substitute for portability: a federated wiki whose pages cannot leave as a bundle is still locked in.

## 2. Topologies

Federation is not one architecture. Four shapes recur:

| Topology | Shape | Examples | Strength | Weakness |
|---|---|---|---|---|
| **Farm** | Many wikis under one operator, sharing accounts, interwiki tables, and software | Wikimedia projects, Fandom, Miraheze | Shared identity and tooling; cheap cross-links | One operator; one policy; one point of failure |
| **Peer federation** | Independent sites that discover each other, fork pages, and keep provenance | Federated Wiki | No centre; plural truth; durable copies | Convergence is work; discovery is bounded by what you have seen |
| **Pull mirroring** | Sites periodically fetch each other's bundles or feeds and keep local copies | Static mirrors, archive crawlers, "planet" aggregators | Simple; works with any engine that exports | Staleness; no backchannel |
| **Push notification** | Sites announce changes to subscribers who decide what to do | Feeds with WebSub, ActivityPub actors, webhooks | Timely; subscribers choose | Needs endpoints that stay up; spam surface |

Most real deployments mix them: a farm whose wikis also publish feeds, or peer sites that also pull bundles for safekeeping. The patterns are written to be combined.

## 3. The patterns

Format as in [03 · Pattern Language Overview](../03-Pattern_Language_Overview.md#2-pattern-format). Maturity is *Exploratory* for all fourteen, so the field is omitted and every guidance block is labelled accordingly. Codes are `FED-n`; they are stable once released.

---

### FED-1 · Site as the Unit of Trust

**Also known as:** one site, one steward; origin.

**Context.** Content crosses site boundaries; readers need to know whom they are trusting.

**Tension.** A single global namespace is easy to cite and impossible to govern; a web of independent sites is easy to govern and hard to keep consistent. Trust attaches naturally to a site and its stewards, not to a page floating free.

**Guidance (exploratory).**
- A federated page **should** always be shown with its site of origin, and provenance **should** name sites, not only people ([COLL-13](../07-Collaboration_Awareness_and_Governance.md#coll-13--fork-instead-of-fight)).
- Each site **should** publish a site description document ([API-1](../11-APIs_and_Discovery.md)) stating its name, license, engine, feeds, and contact, so that trust decisions have something to read.
- Policies (who may edit, what is reviewed) **may** differ per site and **should** be visible from the site description rather than assumed.

**Observed in.** Federated Wiki (each site has one owner; the flag identifies the site everywhere); Wikipedia language editions (each with its own policies and interlanguage links); farms, where the operator is the trust boundary.

**Interchange.** `source`, `forked_from.site`, and the manifest's `source` block carry the site.

---

### FED-2 · Neighbourhood Discovery

**Also known as:** sitemap-driven discovery; who do I know.

**Context.** A site needs to learn what pages exist on the sites it works with, without a central registry.

**Tension.** Crawling the whole web is impossible; a registry is a centre; asking the user to type URLs is friction.

**Guidance (exploratory).**
- Sites **should** publish a machine-readable list of their pages (a sitemap, a page enumeration endpoint, or Federated Wiki's `sitemap.json`) ([API-3](../11-APIs_and_Discovery.md), [API-7](../11-APIs_and_Discovery.md)).
- A reader's neighbourhood **should** grow organically: the sites they visit, the sites pages were forked from, the sites referenced in interwiki links. Engines **may** seed it from a configured list.
- Discovery results **should** be cached and refreshed, and a site that cannot be reached **should** be shown as such rather than dropped ([FED-12](#fed-12--graceful-absence)).

**Observed in.** Federated Wiki's neighbourhood built from visited and referenced sites; interwiki tables as a configured neighbourhood; `.well-known` conventions and WebFinger in the social web.

**Interchange.** Site description documents and sitemaps; the manifest's `interwiki` map.

---

### FED-3 · Fork with Provenance

**Also known as:** copy, do not edit; profligate copying.

**Context.** Someone wants to build on a page they do not control.

**Tension.** Editing in place requires permission and forces agreement; copying without a record creates orphans that drift silently.

**Guidance (exploratory).**
- Copying a page from another site **should** record the source site, page, and revision ([`forked_from`](../09-Metadata_and_Frontmatter.md), [COLL-13](../07-Collaboration_Awareness_and_Governance.md#coll-13--fork-instead-of-fight)) and **should** keep the copied history where the license permits.
- The copy **should** show its lineage, and the original **may** show that it has been forked (a kind of backlink, [FED-5](#fed-5--cross-site-backlinks)).
- Changes **should** be mergeable back by ordinary editing tools: a forked page is a bundle of one page plus history, and the import report says what differs ([XFER-13](../10-Interchange_and_Portability.md)).

**Observed in.** Federated Wiki's fork action with its journal entry; git-based wikis forking repositories; the many Wikipedia mirrors that copy without provenance, and the confusion they cause.

**Interchange.** `forked_from`, `history/` records with `type: fork`.

---

### FED-4 · Twin Pages

**Also known as:** sister sites; same title elsewhere.

**Context.** Several sites in a neighbourhood have a page with the same title.

**Tension.** Showing every twin clutters the page; hiding them loses the chorus. Titles collide by accident as well as by intent.

**Guidance (exploratory).**
- When a page has twins in the neighbourhood, the engine **should** make them discoverable from the page (icons, a list, a panel), labelled with their sites.
- Twins **should** be matched by normalized title ([MKUP-5](../08-Markup_and_Syntax.md)) and **may** be matched by shared `id` or `forked_from` lineage for precision.
- Readers **should** be able to compare twins (a cross-site diff) and to fork the one they prefer.

**Observed in.** Federated Wiki's twin-page flags; MeatballWiki's SisterSites and TwinPages, which placed icons for sibling wikis at the bottom of pages two decades ago.

**Interchange.** Titles and `id`s in bundles; no new fields.

---

### FED-5 · Cross-Site Backlinks

**Also known as:** federated what-links-here; mentions.

**Context.** A page on site A links to a page on site B; B's readers would benefit from knowing.

**Tension.** B cannot see A's content; A has no reason to tell B unless there is a cheap, standard way; unsolicited notifications are a spam vector.

**Guidance (exploratory).**
- Sites **may** send a Webmention when they publish a link to a page on another site, and **may** accept Webmentions, verifying that the source really links before listing it ([Chapter 11 §4](../11-APIs_and_Discovery.md#4-toward-federation-exploratory)).
- Accepted mentions **should** be shown separately from local backlinks ([NAV-4](../04-Discovery_Navigation_and_Topology.md#nav-4--backlinks-what-links-here)), labelled with the source site, and moderation **should** be possible.
- Interwiki links in bundles **should** survive export so that mentions can be reconstructed ([MKUP-13](../08-Markup_and_Syntax.md)).

**Observed in.** Webmention across personal sites and blogs (the IndieWeb); no wiki engine implements it natively yet, which is why this is exploratory.

**Interchange.** Received mentions **may** be stored as discussion records with `kind: mention`.

---

### FED-6 · Change Notification

**Also known as:** federated recent changes; subscribe to a site.

**Context.** A site wants to know when pages it cares about change elsewhere.

**Tension.** Polling is simple and late; push needs endpoints and trust; a global firehose is noise.

**Guidance (exploratory).**
- Every site **should** publish Atom feeds of changes ([API-6](../11-APIs_and_Discovery.md)); that alone makes pull-based federation possible with no new software.
- Sites **may** offer WebSub hubs for timely push, and **may** act as ActivityPub actors publishing updates as activities, so that other wikis and social software can follow them.
- Subscribers **should** be able to scope subscriptions (a page, a namespace, a tag, a site) and **should** treat notifications as invitations to look, not as instructions to copy.

**Observed in.** Feeds in every classic engine; Federated Wiki's neighbourhood recent changes assembled from sitemaps; experiments with wikis as ActivityPub actors.

**Interchange.** Feeds and activities carry the fields of the history record ([XFER-7](../10-Interchange_and_Portability.md)).

---

### FED-7 · Shared Interwiki Vocabulary

**Also known as:** intermap; prefix registry.

**Context.** Sites link to common destinations (encyclopedias, documentation, each other) with prefixes that each site defines separately.

**Tension.** Local maps are flexible and inconsistent; a central registry is consistent and a centre.

**Guidance (exploratory).**
- Sites **should** publish their interwiki map ([API-9](../11-APIs_and_Discovery.md)) and **should** import maps from the bundles they receive, so that prefixes travel with content.
- A community-maintained list of common prefixes ([17 · Roadmap](../17-Roadmap_and_Open_Questions.md)) **may** be used as a default; local overrides **should** remain possible.
- Neighbours **may** treat each other's site names as prefixes automatically (a site called *Gardening* resolves `[[gardening:Compost]]`).

**Observed in.** Meatball's InterMap lists, MediaWiki's interwiki table, DokuWiki's `interwiki.conf`, PmWiki's InterMap page: the same idea, never shared.

**Interchange.** Manifest `interwiki`; site description `interwiki`.

---

### FED-8 · Portable Identity

**Also known as:** who wrote this, across sites.

**Context.** Attribution must survive when content moves between sites with different account systems.

**Tension.** Centralized identity is convenient and a single point of control; purely local accounts make the same person unrecognizable elsewhere; exposing identities widely raises privacy stakes.

**Guidance (exploratory).**
- A contributor **should** be representable by a profile URL that is theirs (on their home wiki or elsewhere), which is enough to recognize them across sites ([Q5](../17-Roadmap_and_Open_Questions.md)).
- Sites **may** support WebFinger addresses and OpenID Connect so that a person can log in to a neighbour with their home identity; decentralized identifiers are a further option.
- Pseudonymization **should** be available when content is shared ([PRIV-3](../14-Security_Privacy_and_Trust.md), [XFER-8](../10-Interchange_and_Portability.md)), and the actor convention of the Open Knowledge Format ([Appendix G](G-Open_Knowledge_Format_Alignment.md)) **may** be used to distinguish people, processes, and groups.

**Observed in.** Wikimedia's unified login across its farm; OpenID Connect in enterprise wikis; WebFinger in the fediverse; Federated Wiki, which avoids the question by binding identity to the site.

**Interchange.** `contributors[].url`, `users.yaml`, the `pseudonymized` manifest flag.

---

### FED-9 · Plural Truth with Paths to Convergence

**Also known as:** chorus of voices; agree later.

**Context.** Sites hold different versions of the same topic.

**Tension.** Forcing one version produces edit wars or silence; accepting many produces fragmentation and reader confusion.

**Guidance (exploratory).**
- Federated engines **should** present divergent twins as legitimate ([FED-4](#fed-4--twin-pages)) and **should** make the differences visible rather than ranking one as canonical.
- Convergence **should** be possible by choice: a maintainer merges a twin's changes through an ordinary import with a report, and records the merge in history (`type: merge`, [XFER-7](../10-Interchange_and_Portability.md)).
- Communities **should** be able to declare, per page or per namespace, whether they seek convergence (an encyclopedia) or plurality (a commonplace book), and engines **should** honour the declaration in what they suggest.

**Observed in.** Federated Wiki's design intent; Wikipedia's language editions as long-running, loosely converging forks; documentation wikis that mirror each other and drift.

**Interchange.** History `merge` and `fork` events; `forked_from`.

---

### FED-10 · Content Integrity Across Sites

**Also known as:** know what you got.

**Context.** Content arrives from another site, possibly through intermediaries.

**Tension.** Trusting transport is fragile; signing everything is heavy; readers rarely check.

**Guidance (exploratory).**
- Bundles exchanged between sites **should** carry checksums ([XFER-1](../10-Interchange_and_Portability.md)) and **may** be signed by the exporting site; receivers **should** verify and **should** show provenance ([TRUST-2](../14-Security_Privacy_and_Trust.md)).
- Revision hashes in history records **should** be preserved so that two sites can agree they hold the same revision without comparing text.
- Content-addressed storage (hashes as names) **may** be used for attachments to deduplicate across a neighbourhood.

**Observed in.** Git-backed wikis, where every revision is content-addressed; checksums in bundles; signed releases in software ecosystems, which wikis have not yet copied.

**Interchange.** `sha256` on history records and attachments; `checksums` in the manifest.

---

### FED-11 · Pull-Based Mirroring

**Also known as:** keep a copy; archive your neighbours.

**Context.** A community depends on pages hosted elsewhere and wants them to survive that site's fate.

**Tension.** Mirroring without permission raises licensing questions; mirroring with stale copies misleads; not mirroring loses knowledge when sites die.

**Guidance (exploratory).**
- Sites **should** make their content mirrorable by exposing bundles ([API-10](../11-APIs_and_Discovery.md)) and incremental exports ([Q8](../17-Roadmap_and_Open_Questions.md)), and **should** state the license plainly so that mirrors know their obligations ([LIC-1](../15-Licensing_and_Attribution.md)).
- Mirrors **should** be labelled as mirrors, dated, and linked to the origin; they **should** keep attribution and license ([LIC-4](../15-Licensing_and_Attribution.md)).
- A mirror **may** become a fork ([FED-3](#fed-3--fork-with-provenance)) when the origin disappears; the provenance record makes the transition honest.

**Observed in.** Static mirrors of documentation wikis; archive crawlers; Federated Wiki's practice of forking pages one wants to keep.

**Interchange.** Bundles; `source` and `forked_from`.

---

### FED-12 · Graceful Absence

**Also known as:** the remote site is down.

**Context.** A page depends on another site (a twin, a transclusion, a mention, a remote link) and that site is unreachable or gone.

**Tension.** Failing loudly breaks pages that are otherwise fine; failing silently hides the loss.

**Guidance (exploratory).**
- Remote dependencies **should** degrade like any other dynamic content: a cached snapshot with a dated marker, or a visible placeholder, never a broken page ([EXT-8](../12-Extensibility_Macros_and_Dynamic_Content.md), [Chapter 08 §4](../08-Markup_and_Syntax.md#4-the-degradation-ladder)).
- Links to unreachable sites **should** remain links; the engine **may** annotate them and **may** offer an archived copy.
- Neighbourhood lists **should** keep absent sites for a while, marked, before forgetting them.

**Observed in.** The web's own practice of link rot and archive links; Federated Wiki's ghost pages for unreachable sites.

**Interchange.** Snapshot envelopes with `kind="embed"` and `target`.

---

### FED-13 · Visible Boundaries

**Also known as:** know where you are.

**Context.** Readers move between sites without noticing, and sites differ in license, policy, and trustworthiness.

**Tension.** Seamless federation feels like one wiki, which is pleasant and misleading; heavy-handed boundaries make federation feel like leaving.

**Guidance (exploratory).**
- The current site **should** always be identifiable ([NAV-11](../04-Discovery_Navigation_and_Topology.md#nav-11--spatial-orientation)), and remote content (twins, transclusions, mentions) **should** be visibly attributed to its site.
- License and policy differences **should** be surfaced at the moment they matter: when forking, when merging, when quoting ([LIC-5](../15-Licensing_and_Attribution.md)).
- Private sites **should not** leak page titles or existence into neighbourhoods they have not joined ([PRIV-7](../14-Security_Privacy_and_Trust.md)).

**Observed in.** Federated Wiki's per-site flags on every page; Wikipedia's interwiki icons and "from another project" notices.

**Interchange.** Not applicable.

---

### FED-14 · Minimal Protocol Surface

**Also known as:** the smallest federated wiki.

**Context.** Engines want to federate without committing to a large protocol they may not keep up with.

**Tension.** A rich protocol enables rich features and excludes small engines; a tiny one includes everyone and does less.

**Guidance (exploratory).**
- Federation **should** be built from pieces that already exist and already pay for themselves locally: raw page access ([API-2](../11-APIs_and_Discovery.md)), page enumeration ([API-3](../11-APIs_and_Discovery.md)), feeds ([API-6](../11-APIs_and_Discovery.md)), bundles ([Chapter 10](../10-Interchange_and_Portability.md)), and a site description ([API-1](../11-APIs_and_Discovery.md)). An engine that has these can federate with a few hundred lines of code.
- Richer mechanisms (Webmention, WebSub, ActivityPub, WebFinger) **should** be layered on, each optional, each a registered standard, none invented here.
- Anything that would require every engine to adopt one new wire format **should** be treated with suspicion; the history of wiki standardization ([01 §9](../01-Core_Concepts_and_Landscape.md#9-lessons-from-earlier-standardization-attempts)) is a history of such proposals failing.

**Observed in.** Federated Wiki, whose entire protocol is "GET a page as JSON, GET a sitemap, PUT if you own the site"; the fediverse, where the heavy protocol took a decade to spread.

**Interchange.** Everything in Part III.

## 4. Putting it together: a minimal federation

Two wikis on different engines can federate today with the pieces above, in this order of effort:

1. Both publish a site description, raw page access, page enumeration, and Atom feeds (Chapter 11). Readers can now follow each other's changes with any feed reader. (*FED-2, FED-6, FED-14*)
2. Both export and import bundles (Chapter 10). A page can be copied with its history and provenance, and merged back later with a report. (*FED-3, FED-9, FED-10, FED-11*)
3. Both declare each other in their interwiki maps and show twins by normalized title. (*FED-4, FED-7, FED-13*)
4. Optionally, both send and accept Webmentions, publish WebSub or ActivityPub, and recognize each other's contributors by profile URL. (*FED-5, FED-6, FED-8*)
5. Throughout, remote dependencies degrade gracefully and boundaries stay visible. (*FED-1, FED-12, FED-13*)

Nothing in steps 1 to 3 requires software that does not already exist in most engines; that is the point.

## 5. Open questions specific to federation

These extend [Q5](../17-Roadmap_and_Open_Questions.md) and [Q6](../17-Roadmap_and_Open_Questions.md) in the roadmap.

- Is a minimal "wiki activity" vocabulary for ActivityPub (page created, edited, forked, merged) worth specifying, or do the generic *Create* and *Update* activities with a link to the history record suffice?
- How should twins be matched when titles differ across languages: by `translations`, by `id` lineage, by Wikidata-style concept identifiers, or not at all?
- What does a federation-aware license check look like when a merge brings together pages under different licenses ([LIC-5](../15-Licensing_and_Attribution.md))?
- Can suppression ([HIST-12](../06-Temporal_Design_and_Revision_History.md#hist-12--suppression-without-erasure)) propagate to forks and mirrors, and should it?

---

Previous: [H · BookStack and MediaWiki Alignment](H-BookStack_and_MediaWiki_Alignment.md) · Index: [README](../../README.md)
