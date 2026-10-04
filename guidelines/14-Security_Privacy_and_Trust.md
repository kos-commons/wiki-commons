# 14 · Security, Privacy and Trust

> **Part III — Interoperability Guidelines** · **Status:** Working Draft 0.1 (October 2026)
> Previous: [13 · Accessibility, Internationalization and Web Standards](13-Accessibility_Internationalization_and_Web_Standards.md) · Next: [15 · Licensing and Attribution](15-Licensing_and_Attribution.md)

**In one sentence:** A wiki renders text from strangers, imports bundles from other systems, runs other people's plugins, and remembers everything forever; these guidelines cover the security practices that follow from that, the privacy of contributors and readers, and the signals that let people trust what they read.

Recommendations carry the prefixes `SEC-` (security), `PRIV-` (privacy), and `TRUST-` (provenance and trust). Access-control *models* remain out of scope; what is in scope is how an engine protects itself, its users, and its content regardless of model.

---

## 1. Security

### Rendering untrusted content

#### SEC-1 · Sanitize everything that is rendered

User content, imported bundles, pasted HTML, and plugin output **should** all pass through an allowlist-based HTML sanitizer before reaching a browser. Raw HTML in Markdown ([MKUP-17](08-Markup_and_Syntax.md)) **should** be reduced to a documented safe subset. Uploaded SVG **should** be sanitized or served in a way that prevents script execution; uploads **should** be served with `X-Content-Type-Options: nosniff` and correct media types, and **should** be served from a separate origin where the deployment allows it, as large public wikis do.

#### SEC-2 · Browser-side defences

Engines **should** ship a strict Content Security Policy (nonce- or hash-based, no inline script by default), **should** set `Referrer-Policy`, frame protections, and `SameSite` cookies, **should** serve only over HTTPS with HSTS, and **are encouraged** to adopt Trusted Types where their front end allows. Third-party scripts **should** be avoided on reading pages; where unavoidable, Subresource Integrity **should** be used.

#### SEC-3 · State changes need intent

Every state-changing request **should** be protected against cross-site request forgery (tokens or same-site cookies plus origin checks). Sensitive actions (changing email, granting rights, bulk deletion) **should** require re-authentication. Session expiry **should never** discard an edit in progress ([AUTH-8](05-Authoring_and_Participation.md#auth-8--never-lose-a-draft)).

### Accounts and abuse

#### SEC-4 · Modern authentication

Engines **should** support passkeys (WebAuthn) and time-based one-time passwords as second factors, **should** avoid arbitrary password composition rules in favour of length and breach checks, **should** offer OpenID Connect and, for enterprises, SAML, **should** rate-limit authentication, and **should** make account recovery safe.

#### SEC-5 · Abuse resistance that starts soft

Following [COLL-6](07-Collaboration_Awareness_and_Governance.md#coll-6--soft-security), engines **should** make reversion and visibility excellent first, then add friction progressively: rate limits, upload type restrictions, `rel="nofollow ugc"` on external links, honeypot fields, challenge–response only when anomalies are detected, temporary and explained blocks. Every protective action **should** be logged. Automated filters **should** be reviewable by people and **should** explain themselves to the affected contributor ([COLL-7](07-Collaboration_Awareness_and_Governance.md#coll-7--assume-good-faith-by-default)).

### Extensions and imports

#### SEC-6 · Sandbox what executes

Scripting inside content (Lua modules, template languages, embedded widgets) **should** run in a sandbox with resource limits and no ambient access to the host; the sandbox **should** be documented. Plugins **should** declare the permissions they need and operators **should** see them before enabling ([EXT-13](12-Extensibility_Macros_and_Dynamic_Content.md)). Plugin output is user content for sanitization purposes. Engines **should** practise supply-chain hygiene: pinned dependencies, signed releases, reproducible builds where feasible.

#### SEC-7 · Imported bundles are untrusted input

Importers **should** defend against path traversal in archive entries, symbolic links, oversized or deeply nested archives, and attachments whose content does not match their declared type; **should** sanitize Markdown and HTML on import as on save; **should** quarantine attachments until scanned where policy requires; **should** verify checksums when present; **should** never execute scripts or fetch remote resources named in a bundle without explicit operator consent ([EXT-8](12-Extensibility_Macros_and_Dynamic_Content.md), [EXT-9](12-Extensibility_Macros_and_Dynamic_Content.md)); and **should** offer a dry run ([XFER-13](10-Interchange_and_Portability.md)).

### Operations

#### SEC-8 · Secrets stay out of content

API tokens, credentials, and configuration **should not** appear in pages, frontmatter, or bundles ([META-14](09-Metadata_and_Frontmatter.md)). Tokens **should** be scoped, expiring, and revocable; webhook payloads **should** be signed.

#### SEC-9 · Backups, integrity, and recovery

History is a security feature only if it survives. Engines **should** document backup and restore, **should** make restore drills easy, **should** store history append-only where the architecture allows, and **should** treat the portable export ([Chapter 10](10-Interchange_and_Portability.md)) as part of disaster recovery rather than a separate feature.

#### SEC-10 · Responsible disclosure

Projects **should** publish a security policy (a `SECURITY.md` and a `security.txt`), **should** issue advisories for fixed vulnerabilities, and **should** keep dependencies current. Operators **should** be able to see the versions they run and whether updates are available.

## 2. Privacy

Wikis differ from most web applications in two ways that matter for privacy: contributors leave a permanent, attributed, public record, and readers of public wikis are often researching sensitive topics. Both deserve protection.

### PRIV-1 · Collect little, track nothing by default

Engines **should** default to no third-party trackers, no advertising scripts, and no external fonts or CDNs that leak visitor data; assets **should** be self-hosted. Analytics, if any, **should** be self-hosted and aggregated, and operators **should** be able to see exactly what is collected. Large public wikis have shown that this is practical at any scale.

### PRIV-2 · Say what you keep

Operators **should** be able to publish, and engines **should** help them publish, a plain statement of what is logged (addresses, user agents, timing), for how long, who can see contribution histories and emails, and how to ask for data or deletion.

### PRIV-3 · Protect contributor identity

- IP addresses of anonymous contributors **should not** be published; a temporary pseudonym shown publicly with the address restricted to a trusted role is the model large wikis have adopted. Engines that still publish addresses **should** treat this as a defect to fix.
- Pseudonymous participation **should** be possible; whether real names are required is the operator's choice, and engines **should not** force it.
- Email addresses **should** be private by default, never exported ([XFER-8](10-Interchange_and_Portability.md)), and used only for the purposes the user agreed to.
- Exports **should** offer pseudonymization of contributor identities while preserving attribution structure, and the manifest **should** record its use.

### PRIV-4 · Do not fetch on the reader's behalf without consent

Embedded third-party content (videos, maps, badges, remote images) tells third parties who is reading what. Engines **should** offer click-to-load or server-side proxying for embeds, **should not** hotlink remote images by default ([AUTH-7](05-Authoring_and_Participation.md#auth-7--effortless-media)), and **should** fetch link previews server-side with care for the target's own privacy.

### PRIV-5 · Users' rights over their data

Users **should** be able to export their own data (profile, preferences, contributions list) in a portable form, which aligns with data-portability rights in several jurisdictions. Account deletion **should** be possible; because contributions remain licensed to the community, engines **should** document how deletion affects attribution (replacing the name with a stable pseudonym is the common practice) rather than silently removing history. Where content must be removed for legal reasons, [HIST-12](06-Temporal_Design_and_Revision_History.md#hist-12--suppression-without-erasure) reconciles the duty to remove with the integrity of the record.

### PRIV-6 · Notifications leak

Emails and push notifications **should not** contain content the recipient could not otherwise access and **should** be minimal by default ([COLL-9](07-Collaboration_Awareness_and_Governance.md#coll-9--notifications-with-restraint)). Unsubscribing **should** be one step.

### PRIV-7 · Private wikis stay private

Search, feeds, APIs, sitemaps, and link previews **should** respect access controls; private wikis **should** send `noindex` signals and **should** not expose titles of restricted pages through backlinks, search suggestions, or feeds to those who may not read them ([COLL-10](07-Collaboration_Awareness_and_Governance.md#coll-10--open-by-default-narrow-with-care)).

### PRIV-8 · Crawling and machine reuse

Public wikis **should** publish `robots.txt` and a sitemap and **should** state their content license machine-readably ([LIC-1](15-Licensing_and_Attribution.md)); the license, not a technical block, governs reuse. Public knowledge wikis are **encouraged** to remain archivable by public archives, since archives are a form of portability. Emerging machine-readable preferences for text and data mining (such as the W3C TDM reservation protocol and work in the IETF on AI preferences) **may** be exposed; this is *exploratory* and evolving.

## 3. Trust and provenance

Trust in a wiki comes from being able to see where things came from.

### TRUST-1 · Provenance is visible

Attribution ([HIST-4](06-Temporal_Design_and_Revision_History.md#hist-4--attribution-per-revision)), history ([HIST-1](06-Temporal_Design_and_Revision_History.md#hist-1--non-destructive-history)), review states ([COLL-14](07-Collaboration_Awareness_and_Governance.md#coll-14--review-as-an-overlay-not-a-gate)), imported-content markers, generated-content markers ([EXT-4](12-Extensibility_Macros_and_Dynamic_Content.md)), and machine-assistance markers ([AUTH-14](05-Authoring_and_Participation.md#auth-14--machine-assistance-human-authorship)) **should** all be visible to readers, not only to administrators.

### TRUST-2 · Integrity of what moves

Bundles **should** carry checksums ([XFER-1](10-Interchange_and_Portability.md)); history records using patches **should** carry content hashes ([XFER-7](10-Interchange_and_Portability.md)). Exporters **may** sign bundles (detached signatures with widely used tooling) so that an importer can verify origin; this is *exploratory*.

### TRUST-3 · Transparent moderation

Protective and administrative actions **should** be logged where the community can see them ([COLL-8](07-Collaboration_Awareness_and_Governance.md#coll-8--visible-activity-and-contribution-history)), **should** carry reasons, and **should** have a path of appeal that the software makes findable. Suppressed content leaves a tombstone, never a hole ([HIST-12](06-Temporal_Design_and_Revision_History.md#hist-12--suppression-without-erasure)).

### TRUST-4 · Honest degradation

A page that has lost something in transit says so ([PR-17](02-Guiding_Principles.md)). Import reports, snapshot envelopes, and fidelity declarations are trust features as much as engineering ones.

## 4. Observed in

Large public wikis demonstrate most of this chapter at scale: strict sanitization of wikitext and uploads, uploads on a separate origin, no third-party trackers or fonts, published privacy and data-retention policies, revision suppression with logs, and the recent move from public IP addresses to temporary accounts. Sandboxed Lua for templates shows that scripting in content can be made safe. Smaller engines vary widely: flat-file and git-backed wikis have small attack surfaces but often weaker CSRF and upload handling; enterprise tools integrate identity providers well but sometimes embed third-party content freely. Local-first tools sidestep server privacy problems and inherit the file system's; their sync services then raise the same questions again.

---

Previous: [13 · Accessibility, Internationalization and Web Standards](13-Accessibility_Internationalization_and_Web_Standards.md) · Next: [15 · Licensing and Attribution](15-Licensing_and_Attribution.md)
