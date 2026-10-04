"""Open Knowledge Format (OKF) interchange.

OKF (https://github.com/GoogleCloudPlatform/open-knowledge-format, version 0.2) is a directory
of Markdown concept documents with YAML frontmatter, a required `type`, optional `index.md`
listings and `log.md` histories, and standard Markdown links (bundle-absolute `/path.md`
recommended). `bundle_to_okf` writes a Portable Wiki Bundle as an OKF bundle; `okf_to_bundle`
imports one. The field mapping is documented in guidelines/appendices/G-Open_Knowledge_Format_Alignment.md.
"""
from __future__ import annotations

import datetime as dt
import json
import posixpath
import re
import shutil
from pathlib import Path
from typing import Optional
from urllib.parse import quote, unquote

import yaml  # type: ignore

from . import markup
from .bundle import (as_list, attachment_meta, default_manifest, dump_frontmatter, load_bundle_pages,
                     bundle_index, order_keys, read_manifest, write_checksums, write_page)
from .resolve import Page, PageIndex, strip_md

OKF_VERSION = "0.2"
RESERVED = {"index.md", "log.md"}
KIND_TO_TYPE = {"page": "Wiki Page", "category": "Category", "template": "Template", "help": "Help Page",
                "system": "System Page", "discussion": "Discussion", "user": "User Page", "redirect": "Redirect"}
TYPE_TO_KIND = {v.lower(): k for k, v in KIND_TO_TYPE.items()}
STATUS_TO_OKF = {"draft": "draft", "wip": "draft", "stable": "stable", "deprecated": "deprecated",
                 "archived": "deprecated", "deleted": "deprecated"}
OKF_FAMILIES = ("sources", "usage_window", "verified", "stale_after", "runtime", "parameters", "computation",
                "executor", "attester", "timestamp")
LOG_TYPES = {"create": "Creation", "edit": "Update", "rename": "Rename", "delete": "Deletion", "restore": "Restoration",
             "revert": "Revert", "upload": "Upload", "merge": "Merge", "fork": "Fork", "review": "Review", "protect": "Update"}


def actor_for(person: Optional[dict], fallback: str) -> str:
    if not person:
        return fallback
    kind = person.get("kind", "person")
    ident = str(person.get("id") or re.sub(r"[^a-z0-9]+", "-", str(person.get("name", "")).casefold()).strip("-") or "unknown")
    if kind == "bot":
        return f"process:{ident}"
    if kind == "group":
        return f"team:{ident}"
    return f"human:{ident}"


def person_from_actor(actor: str) -> dict:
    actor = str(actor)
    if actor.startswith("human:"):
        ident = actor[6:]
        return {"name": ident, "id": ident, "kind": "person"}
    if actor.startswith("process:"):
        ident = actor[8:]
        return {"name": ident, "id": ident, "kind": "bot"}
    if actor.startswith("team:"):
        ident = actor[5:]
        return {"name": ident, "id": ident, "kind": "group"}
    name = actor.split("/", 1)[0]
    return {"name": actor, "id": re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-"), "kind": "bot"}


def latest_author(bundle: Path, page_id: Optional[str]) -> Optional[dict]:
    """Author of the most recent history record for a page, when history is present."""
    if not page_id:
        return None
    jl = bundle / "history" / f"{page_id}.jsonl"
    if not jl.exists():
        return None
    last = None
    for line in jl.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            if rec.get("author"):
                last = rec["author"]
    if last and last.get("anonymous"):
        return {"name": last.get("label", "anonymous"), "id": last.get("label", "anonymous"), "kind": "person"}
    return last


def attachment_dest(rel: str) -> str:
    """Bundle path for an OKF non-Markdown file (an existing attachments/ prefix is not doubled)."""
    return rel if rel.startswith("attachments/") else "attachments/" + rel


def safe_concept_name(rel: str) -> str:
    base = posixpath.basename(rel)
    if base.lower() in RESERVED:
        rel = posixpath.join(posixpath.dirname(rel), strip_md(base) + "-page.md")
    return rel


# --------------------------------------------------------------------------- export
def bundle_to_okf(bundle: Path, out: Path, *, name: Optional[str] = None, default_type: str = "Wiki Page") -> dict:
    bundle, out = bundle.resolve(), out.resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    manifest = read_manifest(bundle)
    name = name or (manifest.get("source") or {}).get("name") or bundle.name
    engine = (manifest.get("source") or {}).get("engine") or "wiki"
    pages = load_bundle_pages(bundle)
    index = bundle_index(bundle, pages)
    notes = markup.Notes()
    okf_paths = {p["path"]: safe_concept_name(p["path"][len("pages/"):]) for p in pages}

    def resolver(target: str, from_path: Optional[str]):
        r = index.resolve(target, "pages/" + from_path if from_path else None)
        return (okf_paths[r.path], index.title_of(r.path)) if r.path and r.path in okf_paths else None

    entries: dict[str, list[dict]] = {}
    for p in pages:
        fm, body = dict(p["fm"]), p["body"]
        okf_rel = okf_paths[p["path"]]
        page_dir = posixpath.dirname(p["path"])

        def rewrite(href: str, is_image: bool, page_dir=page_dir) -> Optional[str]:
            target = posixpath.normpath(posixpath.join(page_dir, unquote(href.split("#")[0])))
            if target.startswith("attachments/"):
                return "/" + quote(target)
            return None

        body = markup.convert(body, "portable", "static", resolver=resolver, from_path=okf_rel,
                              interwiki=manifest.get("interwiki", {}), link_rewriter=rewrite, notes=notes,
                              absolute_links=True)
        concept: dict = {"type": KIND_TO_TYPE.get(str(fm.pop("kind", "page")), default_type) if default_type == "Wiki Page" else default_type,
                         "title": p["title"]}
        fm.pop("title", None)
        desc = fm.pop("description", None) or fm.pop("summary", None)
        if desc:
            concept["description"] = re.sub(r"\s+", " ", str(desc)).strip()
        resource = fm.pop("canonical", None) or fm.get("source")
        if resource:
            concept["resource"] = resource
        if "tags" in fm:
            concept["tags"] = as_list(fm.pop("tags"))
        status = STATUS_TO_OKF.get(str(fm.pop("status", "stable")), "stable")
        if status != "stable":
            concept["status"] = status
        contributors = fm.get("contributors") or []
        last = contributors[-1] if contributors else None
        if isinstance(last, str):
            last = {"name": last}
        latest = latest_author(bundle, fm.get("id"))
        if latest:
            last = latest
        at = fm.get("updated")
        if at:
            concept["generated"] = {"by": actor_for(last, f"process:{engine}"), "at": str(at)}
        review = fm.get("review")
        if isinstance(review, dict) and review.get("state") in ("reviewed", "verified") and review.get("at"):
            by = review.get("by")
            concept["verified"] = [{"by": by if isinstance(by, str) and ":" in by else f"human:{re.sub(r'[^a-z0-9]+', '-', str(by or 'reviewer').casefold()).strip('-')}", "at": str(review["at"])}]
        original_status = p["fm"].get("status")
        if original_status and STATUS_TO_OKF.get(str(original_status)) != original_status:
            concept["wiki_status"] = original_status
        source = fm.get("source")
        if source:
            concept["sources"] = [{"id": "origin", "resource": source, "title": f"Original page in {name}"}]
        # remaining portable keys travel as extension keys (OKF §4.1 permits additional keys)
        for key, value in fm.items():
            if key not in concept:
                concept[key] = value
        dest = out / okf_rel
        write_page(dest, concept, body)
        entries.setdefault(posixpath.dirname(okf_rel), []).append({"title": p["title"], "path": posixpath.basename(okf_rel), "description": concept.get("description")})

    # attachments
    att = bundle / "attachments"
    if att.exists():
        for f in att.rglob("*"):
            if f.is_file() and not f.name.endswith(".meta.yaml") and f.name != "attachments.yaml":
                dest = out / "attachments" / f.relative_to(att)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
    # keep the original manifest for round-trips (not a .md file, so not a concept)
    if (bundle / "wiki-bundle.yaml").exists():
        shutil.copy2(bundle / "wiki-bundle.yaml", out / "wiki-bundle.yaml")

    # index.md files (§8): root carries okf_version; each directory lists its concepts and subdirectories
    all_dirs = set(entries)
    for d in list(all_dirs):
        while d:
            d = posixpath.dirname(d)
            all_dirs.add(d)
    for d in sorted(all_dirs):
        lines = []
        if d == "":
            lines.append(dump_frontmatter({"okf_version": OKF_VERSION}))
            lines.append(f"# {name}\n")
            lines.append(f"Exported from a Portable Wiki Bundle by wiki-commons-tools; the bundle manifest is kept as `wiki-bundle.yaml`. See the Wiki Commons guidelines, Appendix G, for the field mapping.\n")
        else:
            lines.append(f"# {posixpath.basename(d)}\n")
        concepts = sorted(entries.get(d, []), key=lambda e: e["title"].casefold())
        if concepts:
            lines.append("## Concepts\n")
            for e in concepts:
                link = f"[{e['title']}]({quote(e['path'])})"
                lines.append(f"* {link} - {e['description']}" if e.get("description") else f"* {link}")
            lines.append("")
        subdirs = sorted({posixpath.relpath(x, d) if d else x for x in all_dirs if x and posixpath.dirname(x) == d})
        subdirs = [s for s in subdirs if s and "/" not in s]
        if subdirs:
            lines.append("## Directories\n")
            for s in subdirs:
                count = sum(1 for k, v in entries.items() if (k == posixpath.join(d, s) if d else k == s) or k.startswith((posixpath.join(d, s) if d else s) + "/") for _ in v)
                lines.append(f"* [{s}]({quote(s)}/) - {count} concept{'s' if count != 1 else ''}")
            lines.append("")
        (out / d / "index.md").write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")

    # log.md (§9) from history
    hist = bundle / "history"
    if hist.exists():
        by_date: dict[str, list[str]] = {}
        titles = {p["fm"].get("id"): (p["title"], okf_paths[p["path"]]) for p in pages if p["fm"].get("id")}
        for jl in sorted(hist.glob("*.jsonl")):
            title, path = titles.get(jl.stem, (jl.stem, None))
            link = f"[{title}](/{quote(path)})" if path else title
            for line in jl.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                r = json.loads(line)
                day = str(r.get("at", ""))[:10]
                label = LOG_TYPES.get(r.get("type", "edit"), "Update")
                summary = r.get("summary")
                if r.get("suppressed"):
                    text = f"* **Suppression**: Revision {r['rev']} of {link} was suppressed ({r.get('reason', 'no reason given')})."
                elif r.get("type") == "rename":
                    text = f"* **Rename**: {link} renamed from {r.get('from')} to {r.get('to')}."
                else:
                    text = f"* **{label}**: {link}" + (f": {summary}" if summary else "") + "."
                by_date.setdefault(day, []).append(text)
        if by_date:
            lines = ["# Update Log", ""]
            for day in sorted(by_date, reverse=True):
                lines.append(f"## {day}")
                lines.extend(by_date[day])
                lines.append("")
            (out / "log.md").write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")
    return {"concepts": len(pages), "notes": list(notes)}


# --------------------------------------------------------------------------- import
def okf_to_bundle(okf: Path, out: Path, *, name: Optional[str] = None) -> dict:
    okf, out = okf.resolve(), out.resolve()
    if out.exists():
        shutil.rmtree(out)
    (out / "pages").mkdir(parents=True)
    notes = markup.Notes()
    name = name or okf.name
    concepts, logs, others = [], [], []
    for f in sorted(okf.rglob("*")):
        if not f.is_file() or any(part.startswith(".") for part in f.relative_to(okf).parts):
            continue
        rel = f.relative_to(okf).as_posix()
        if f.suffix.lower() == ".md":
            if f.name.lower() == "index.md":
                continue
            if f.name.lower() == "log.md":
                logs.append(rel)
            else:
                concepts.append(rel)
        elif f.name != "wiki-bundle.yaml":
            others.append(rel)
    okf_version = None
    root_index = okf / "index.md"
    if root_index.exists():
        fm_text, _, _ = markup.split_frontmatter(root_index.read_text(encoding="utf-8"))
        fm = markup.parse_frontmatter(fm_text) or {}
        okf_version = fm.get("okf_version")
    notes.add("OKF index.md listings were not imported; they are regenerated on export")

    pages = []
    for rel in concepts:
        text = (okf / rel).read_text(encoding="utf-8")
        fm_text, body, _ = markup.split_frontmatter(text)
        fm = markup.parse_frontmatter(fm_text) or {}
        if not fm_text:
            notes.add(f"{rel}: no frontmatter (OKF requires `type`); imported as a plain page")
        pages.append({"rel": rel, "fm": fm, "body": body, "new_path": "pages/" + rel,
                      "title": str(fm.get("title") or strip_md(posixpath.basename(rel)))})
    for rel in logs:
        text = (okf / rel).read_text(encoding="utf-8")
        d = posixpath.dirname(rel)
        pages.append({"rel": rel, "fm": {"type": "Update Log", "title": "Update Log" if not d else f"Update Log ({d})"},
                      "body": text, "new_path": "pages/" + (posixpath.join(d, "Update Log.md") if d else "Update Log.md"),
                      "title": "Update Log" if not d else f"Update Log ({d})", "is_log": True})
    index = PageIndex([Page(p["new_path"], p["title"], as_list(p["fm"].get("aliases"))) for p in pages], pages_prefix="pages")
    path_to_new = {p["rel"]: p["new_path"] for p in pages}
    headings_cache: dict[str, dict] = {}

    def heading_text(new_path: str, slug: str) -> Optional[str]:
        if new_path not in headings_cache:
            page = next(p for p in pages if p["new_path"] == new_path)
            headings_cache[new_path] = {h["anchor"]: h["text"] for h in markup.scan(page["body"])["headings"]}
        return headings_cache[new_path].get(slug)

    for p in pages:
        body = p["body"]
        concept_dir = posixpath.dirname(p["rel"])
        masked = markup.mask_code(body)
        edits = []
        for m in markup.MD_LINK_RE.finditer(masked):
            href = m.group(3)
            if markup.URL_RE.match(href) or href.startswith(("mailto:", "#")):
                continue
            path_part, _, frag = unquote(href).partition("#")
            target = path_part.lstrip("/") if path_part.startswith("/") else posixpath.normpath(posixpath.join(concept_dir, path_part))
            if target.startswith("../"):
                continue  # points outside the bundle; leave as written
            is_image = m.group(1) == "!"
            if target.lower().endswith(".md") and not is_image:
                new = path_to_new.get(target)
                if new is None:
                    # OKF tolerates broken links; keep as a dangling free link to the file stem
                    title = strip_md(posixpath.basename(target))
                    edits.append((m.start(), m.end(), f"[[{title}|{m.group(2)}]]" if m.group(2) and m.group(2) != title else f"[[{title}]]"))
                    notes.add(f"{p['rel']}: link to missing concept {target!r} kept as a dangling free link")
                    continue
                title = index.title_of(new) or strip_md(posixpath.basename(target))
                inner = title
                if frag:
                    text_frag = heading_text(new, frag)
                    inner += "#" + (text_frag or frag)
                label = m.group(2)
                if label and label != title:
                    inner += "|" + label
                edits.append((m.start(), m.end(), f"[[{inner}]]"))
            elif target in others:
                new_dir = posixpath.dirname(p["new_path"])
                edits.append((m.start(3), m.end(3), posixpath.relpath(attachment_dest(target), new_dir)))
        edits.sort(key=lambda e: e[0])
        pieces, last = [], 0
        for a, b, rep in edits:
            pieces.append(body[last:a]); pieces.append(rep); last = b
        pieces.append(body[last:])
        p["body"] = "".join(pieces)

        fm = dict(p["fm"])
        out_fm: dict = {"title": p["title"]}
        fm.pop("title", None)
        okf_type = fm.pop("type", None)
        kind = TYPE_TO_KIND.get(str(okf_type).lower(), "page") if okf_type else "page"
        if p.get("is_log"):
            kind = "system"
        if kind != "page":
            out_fm["kind"] = kind
        if "description" in fm:
            out_fm["description"] = str(fm.pop("description"))
        if "tags" in fm:
            out_fm["tags"] = as_list(fm.pop("tags"))
        if "aliases" in fm:
            out_fm["aliases"] = as_list(fm.pop("aliases"))
        if "id" in fm:
            out_fm["id"] = str(fm.pop("id"))
        resource = fm.pop("resource", None)
        if resource and markup.URL_RE.match(str(resource)):
            out_fm["canonical"] = str(resource)
        elif resource:
            fm.setdefault("ext", {}).setdefault("okf", {})["resource"] = resource
        status = fm.pop("status", None)
        if status:
            out_fm["status"] = str(status)
        generated = fm.pop("generated", None)
        timestamp = fm.pop("timestamp", None)
        if isinstance(generated, dict):
            if generated.get("at"):
                out_fm["updated"] = str(generated["at"])
            if generated.get("by"):
                out_fm["contributors"] = [person_from_actor(generated["by"])]
        elif timestamp:
            out_fm["updated"] = str(timestamp)
        if "created" in fm:
            out_fm["created"] = str(fm.pop("created"))
        if "updated" in fm and "updated" not in out_fm:
            out_fm["updated"] = str(fm.pop("updated"))
        verified = fm.pop("verified", None)
        if verified:
            events = verified if isinstance(verified, list) else [verified]
            events = [e for e in events if isinstance(e, dict)]
            if events:
                latest = max(events, key=lambda e: str(e.get("at", "")))
                out_fm["review"] = {"state": "verified", "by": str(latest.get("by", "")), "at": str(latest.get("at", ""))}
                fm.setdefault("ext", {}).setdefault("okf", {})["verified"] = events
        ext_okf = fm.setdefault("ext", {}).setdefault("okf", {})
        if okf_type:
            ext_okf["type"] = okf_type
        for key in OKF_FAMILIES:
            if key in fm:
                ext_okf[key] = fm.pop(key)
        if not ext_okf:
            fm["ext"].pop("okf", None)
        if not fm.get("ext"):
            fm.pop("ext", None)
        # keys written by a Wiki Commons exporter are richer than what OKF's own fields can carry
        for key in ("status", "review", "contributors", "created", "updated", "canonical"):
            src_key = "wiki_status" if key == "status" else key
            if src_key in fm:
                out_fm[key] = fm.pop(src_key)
        fm.pop("wiki_status", None)
        for key, value in fm.items():
            out_fm.setdefault(key, value)
        write_page(out / p["new_path"], order_keys(out_fm), p["body"])

    for rel in others:
        dest = out / attachment_dest(rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(okf / rel, dest)
        dest.with_name(dest.name + ".meta.yaml").write_text(yaml.safe_dump(attachment_meta(okf / rel, rel), sort_keys=False, allow_unicode=True), encoding="utf-8")

    manifest = default_manifest(name=name, engine="okf", native_format="text/markdown; charset=UTF-8")
    manifest["source"]["engine_version"] = f"okf {okf_version}" if okf_version else "okf"
    manifest["contents"].update({"pages": len(pages), "attachments": len(others)})
    manifest["fidelity"]["degraded"] = [
        {"construct": "OKF index.md listings", "how": "not imported; regenerated on export"},
        {"construct": "OKF log.md histories", "count": len(logs), "how": "imported as pages of kind system"},
    ]
    counts: dict[str, int] = {}
    for n in notes:
        if "missing concept" in n:
            counts["links to missing concepts"] = counts.get("links to missing concepts", 0) + 1
    for k, v in counts.items():
        manifest["fidelity"]["degraded"].append({"construct": k, "count": v, "how": "kept as dangling free links"})
    (out / "wiki-bundle.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
    write_checksums(out)
    return {"pages": len(pages), "attachments": len(others), "okf_version": okf_version, "notes": list(notes)}
