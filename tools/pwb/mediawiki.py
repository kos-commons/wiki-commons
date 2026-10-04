"""MediaWiki XML dump interchange (optional tooling).

`mediawiki_to_bundle` reads an XML dump (export-0.10/0.11 schema, as written by Special:Export and
dumpBackup.php) into a Portable Wiki Bundle with full revision history. Wikitext is converted to
Markdown with Pandoc when it is installed, otherwise with a small built-in converter that handles
headings, emphasis, lists, links, categories, redirects, references, and external links, and keeps
templates and tables as source inside snapshot envelopes. `bundle_to_mediawiki` writes a bundle as an
XML dump that Special:Import accepts. The mapping is documented in
guidelines/appendices/H-BookStack_and_MediaWiki_Alignment.md.
"""
from __future__ import annotations

import hashlib
import html
import json
import posixpath
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional
from xml.sax.saxutils import escape

import yaml  # type: ignore

from . import __version__, markup
from .bundle import (as_list, default_manifest, dump_frontmatter, load_bundle_pages, order_keys, read_manifest,
                     write_checksums, write_page)
from .external import markdown_to_wikitext, pandoc_available, wikitext_to_markdown
from .history import slug
from .resolve import strip_md

NS_KIND = {1: "discussion", 2: "user", 3: "discussion", 4: "help", 5: "discussion", 6: "page", 7: "discussion",
           8: "system", 9: "discussion", 10: "template", 11: "discussion", 12: "help", 13: "discussion",
           14: "category", 15: "discussion"}
CANONICAL_NS = {"Talk": 1, "User": 2, "User talk": 3, "Project": 4, "Project talk": 5, "File": 6, "File talk": 7,
                "MediaWiki": 8, "MediaWiki talk": 9, "Template": 10, "Template talk": 11, "Help": 12, "Help talk": 13,
                "Category": 14, "Category talk": 15}
CATEGORY_RE = re.compile(r"\[\[\s*(?:Category|category)\s*:\s*([^\]|]+?)\s*(?:\|[^\]]*)?\]\]\s*\n?")
REDIRECT_RE = re.compile(r"^\s*#REDIRECT\s*:?\s*\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", re.I)
TEMPLATE_RE = re.compile(r"\{\{(?!#)([^{}|]+?)(\|(?:[^{}]|\{\{[^{}]*\}\})*)?\}\}", re.S)
PARSERFUNC_RE = re.compile(r"\{\{#[^{}]*(?:\{\{[^{}]*\}\}[^{}]*)*\}\}", re.S)
TABLE_RE = re.compile(r"^\{\|.*?^\|\}", re.S | re.M)
REF_RE = re.compile(r"<ref(?:\s[^>]*)?>(.*?)</ref>", re.S)
REF_SELF_RE = re.compile(r"<ref\s[^>]*/>")
EXT_LINK_RE = re.compile(r"\[((?:https?|ftp|mailto):[^\s\]]+)(?:\s+([^\]]+))?\]")


def _tag(el: ET.Element) -> str:
    return el.tag.split("}", 1)[-1]


def _find(el: ET.Element, name: str) -> Optional[ET.Element]:
    for child in el:
        if _tag(child) == name:
            return child
    return None


def _text(el: Optional[ET.Element]) -> str:
    return (el.text or "") if el is not None else ""


# --------------------------------------------------------------------------- built-in wikitext conversion
def builtin_wikitext_to_markdown(text: str, notes: markup.Notes, page: str) -> str:
    out = text.replace("\r\n", "\n")
    # tables and templates: keep source inside snapshot envelopes (not expanded on import)
    def table(m):
        notes.add(f"{page}: wikitext table kept as source (not converted)")
        return ("<!-- wiki:snapshot kind=\"unknown\" name=\"table\" engine=\"mediawiki\" -->\n```wikitext\n" + m.group(0)
                + "\n```\n<!-- /wiki:snapshot -->")
    out = TABLE_RE.sub(table, out)
    # references -> footnotes
    refs: list[str] = []
    def ref(m):
        refs.append(m.group(1).strip())
        return f"[^{len(refs)}]"
    out = REF_RE.sub(ref, out)
    out = REF_SELF_RE.sub("", out)
    out = re.sub(r"<references\s*/?>", "", out)
    # lists (before headings, so that the produced "## " lines are not mistaken for numbered items)
    def listline(m):
        marks, rest = m.group(1), m.group(2)
        depth = len(marks) - 1
        bullet = "1." if marks[-1] == "#" else "-"
        return "  " * depth + bullet + " " + rest
    out = re.sub(r"^([*#]+)\s*(.*)$", listline, out, flags=re.M)
    # headings
    def heading(m):
        level = len(m.group(1))
        return "#" * min(level, 6) + " " + m.group(2).strip() + "\n"
    out = re.sub(r"^(={1,6})\s*(.+?)\s*\1\s*$", heading, out, flags=re.M)
    # emphasis
    out = re.sub(r"'''''(.+?)'''''", r"***\1***", out)
    out = re.sub(r"'''(.+?)'''", r"**\1**", out)
    out = re.sub(r"''(.+?)''", r"*\1*", out)
    out = re.sub(r"^;\s*(.+?)\s*:\s*(.+)$", r"**\1**: \2", out, flags=re.M)
    out = re.sub(r"^:\s*(.*)$", r"> \1", out, flags=re.M)
    # external links
    out = EXT_LINK_RE.sub(lambda m: f"[{m.group(2) or m.group(1)}]({m.group(1)})", out)
    # file/image links -> standard images (files themselves are not in XML dumps)
    def image(m):
        parts = [p.strip() for p in m.group(1).split("|")]
        fname = parts[0]
        caption = parts[-1] if len(parts) > 1 and not re.match(r"^(thumb|frame|left|right|center|\d+px|upright.*|border|frameless)$", parts[-1]) else fname
        notes.add(f"{page}: media file {fname!r} referenced but not included in the dump")
        return f"![{caption}]({fname})"
    out = re.sub(r"\[\[\s*(?:File|Image|file|image)\s*:\s*([^\]]+?)\]\]", image, out)
    out = re.sub(r"<nowiki>(.*?)</nowiki>", r"`\1`", out, flags=re.S)
    out = re.sub(r"<(/?)(code|pre|tt)>", lambda m: "`" if m.group(2) != "pre" else ("```\n" if not m.group(1) else "\n```"), out)
    out = re.sub(r"<br\s*/?>", "  \n", out)
    out = re.sub(r"__(NO|FORCE)?TOC__", "", out)
    out = re.sub(r"__[A-Z]+__", "", out)
    if refs:
        out = out.rstrip("\n") + "\n\n" + "\n".join(f"[^{i}]: {r}" for i, r in enumerate(refs, 1)) + "\n"
    return out


def extract_templates(text: str, notes: markup.Notes, page: str) -> str:
    """Replace templates and parser functions with snapshot envelopes that keep the source (EXT-6)."""
    def envelope(name: str, src: str) -> str:
        notes.add(f"{page}: template {{{{{name}}}}} not expanded")
        esc = src.replace('"', "&quot;").replace("-->", "--&gt;")
        return (f'<!-- wiki:snapshot kind="template" name="{html.escape(name, quote=True)}" engine="mediawiki" src="{esc}" -->'
                f"*[template {name} not expanded]*<!-- /wiki:snapshot -->")
    text = PARSERFUNC_RE.sub(lambda m: envelope(m.group(0)[2:].split(":", 1)[0].split("|", 1)[0].strip(), m.group(0)), text)
    return TEMPLATE_RE.sub(lambda m: envelope(m.group(1).strip(), m.group(0)), text)


def wikitext_to_portable(text: str, notes: markup.Notes, page: str) -> tuple[str, list[str], Optional[str], bool]:
    """Return (markdown body, categories, redirect target, used_pandoc)."""
    m = REDIRECT_RE.match(text)
    if m:
        return "", [], m.group(1).strip().replace("_", " "), False
    categories = [c.strip().replace("_", " ") for c in CATEGORY_RE.findall(text)]
    text = CATEGORY_RE.sub("", text)
    text = extract_templates(text, notes, page)
    if pandoc_available():
        # Pandoc's mediawiki reader drops HTML comments, so envelopes travel as placeholders
        envelopes: list[str] = []
        def hold(m):
            envelopes.append(m.group(0))
            return f"WCENVELOPE{len(envelopes) - 1}X"
        protected = re.sub(r"<!-- wiki:snapshot .*?<!-- /wiki:snapshot -->", hold, text, flags=re.S)
        converted = wikitext_to_markdown(protected)
        if converted is not None:
            for i, env in enumerate(envelopes):
                converted = converted.replace(f"WCENVELOPE{i}X", env)
            return converted, categories, None, True
    return builtin_wikitext_to_markdown(text, notes, page), categories, None, False


# --------------------------------------------------------------------------- import
def mediawiki_to_bundle(dump: Path, out: Path, *, name: Optional[str] = None, keep_ips: bool = False,
                        history: bool = True) -> dict:
    dump, out = dump.resolve(), out.resolve()
    if out.exists():
        shutil.rmtree(out)
    (out / "pages").mkdir(parents=True)
    notes = markup.Notes()
    site: dict = {}
    namespaces: dict[int, str] = {}
    pages: list[dict] = []
    users: dict = {}
    used_pandoc = False

    for event, el in ET.iterparse(str(dump), events=("end",)):
        tag = _tag(el)
        if tag == "siteinfo":
            site = {"sitename": _text(_find(el, "sitename")), "base": _text(_find(el, "base")), "generator": _text(_find(el, "generator"))}
            ns_el = _find(el, "namespaces")
            if ns_el is not None:
                for n in ns_el:
                    try:
                        namespaces[int(n.get("key", "0"))] = (n.text or "").strip()
                    except ValueError:
                        pass
            el.clear()
        elif tag == "page":
            title = _text(_find(el, "title")).strip()
            ns = int(_text(_find(el, "ns")) or 0)
            pid = _text(_find(el, "id")).strip()
            redirect_el = _find(el, "redirect")
            revisions = []
            for rev in el:
                if _tag(rev) != "revision":
                    continue
                contrib = _find(rev, "contributor")
                username = _text(_find(contrib, "username")).strip() if contrib is not None else ""
                ip = _text(_find(contrib, "ip")).strip() if contrib is not None else ""
                text_el = _find(rev, "text")
                revisions.append({
                    "id": _text(_find(rev, "id")).strip(), "parent": _text(_find(rev, "parentid")).strip() or None,
                    "at": _text(_find(rev, "timestamp")).strip(), "username": username, "ip": ip,
                    "minor": _find(rev, "minor") is not None, "comment": _text(_find(rev, "comment")),
                    "text": _text(text_el), "text_deleted": text_el is not None and text_el.get("deleted") is not None,
                    "comment_deleted": (_find(rev, "comment") is not None and _find(rev, "comment").get("deleted") is not None),
                    "contributor_deleted": contrib is not None and contrib.get("deleted") is not None,
                })
            pages.append({"title": title, "ns": ns, "id": pid, "redirect": redirect_el.get("title") if redirect_el is not None else None,
                          "revisions": revisions})
            el.clear()

    def page_path(title: str, ns: int) -> str:
        prefix = namespaces.get(ns, "")
        rest = title.split(":", 1)[1] if prefix and title.startswith(prefix + ":") else title
        parts = [p.strip() for p in rest.split("/")]
        safe = "/".join(re.sub(r'[\\:*?"<>|]', "-", p) or "-" for p in parts)
        return ("pages/" + prefix + "/" + safe + ".md") if prefix else ("pages/" + safe + ".md")

    def author_of(rev: dict) -> dict:
        if rev["contributor_deleted"]:
            return {"anonymous": True, "label": "suppressed"}
        if rev["username"]:
            uid = slug(rev["username"])
            users.setdefault(uid, {"id": uid, "name": rev["username"], "kind": "person"})
            return {"id": uid, "name": rev["username"]}
        if rev["ip"]:
            if keep_ips:
                return {"anonymous": True, "label": rev["ip"]}
            return {"anonymous": True, "label": "~ip-" + hashlib.sha256(rev["ip"].encode()).hexdigest()[:10]}
        return {"anonymous": True, "label": "anonymous"}

    aliases: dict[str, list[str]] = {}
    for p in pages:
        if p["redirect"]:
            aliases.setdefault(p["redirect"].replace("_", " "), []).append(p["title"])
    titles = {p["title"] for p in pages}
    counts = {"templates": 0, "tables": 0}
    hist_dir = out / "history"
    for p in pages:
        if not p["revisions"]:
            continue
        current = p["revisions"][-1]
        path = page_path(p["title"], p["ns"])
        page_notes = markup.Notes()
        body, categories, redirect, pandoc_used = wikitext_to_portable(current["text"], page_notes, path)
        used_pandoc = used_pandoc or pandoc_used
        counts["templates"] += sum(1 for n in page_notes if "not expanded" in n)
        counts["tables"] += sum(1 for n in page_notes if "table kept" in n)
        notes.extend(n for n in page_notes if "media file" in n or "not expanded" in n or "table kept" in n)
        fm: dict = {"id": f"mw:{p['id']}" if p["id"] else None, "title": p["title"]}
        kind = NS_KIND.get(p["ns"], "page")
        if redirect or p["redirect"]:
            fm["kind"] = "redirect"
            fm["redirect"] = (redirect or p["redirect"]).replace("_", " ")
        elif kind != "page":
            fm["kind"] = kind
        if p["title"] in aliases:
            fm["aliases"] = aliases[p["title"]]
        if categories:
            fm["tags"] = categories
        if kind == "discussion":
            fm["about"] = p["title"].split(":", 1)[1] if ":" in p["title"] else p["title"]
        contributors: list[dict] = []
        for rev in p["revisions"]:
            a = author_of(rev)
            if a.get("id") and all(c.get("id") != a["id"] for c in contributors):
                contributors.append({"name": a["name"], "id": a["id"]})
        if contributors:
            fm["contributors"] = contributors
        if p["revisions"][0]["at"]:
            fm["created"] = p["revisions"][0]["at"]
        if current["at"]:
            fm["updated"] = current["at"]
        fm["source"] = (site.get("base") or "").rsplit("/", 1)[0] + "/" + p["title"].replace(" ", "_") if site.get("base") else None
        fm["ext"] = {"mediawiki": {"page_id": int(p["id"]) if p["id"].isdigit() else p["id"], "namespace": p["ns"]}}
        if not pandoc_used and not redirect:
            fm["ext"]["mediawiki"]["wikitext_converter"] = "builtin"
        write_page(out / path, order_keys({k: v for k, v in fm.items() if v is not None}), body)
        if history and len(p["revisions"]) >= 1:
            hist_dir.mkdir(exist_ok=True)
            records = []
            prev = None
            for i, rev in enumerate(p["revisions"]):
                rid = f"r{rev['id']}" if rev["id"] else f"r{i + 1}"
                rec: dict = {"rev": rid, "parent": (f"r{rev['parent']}" if rev["parent"] else prev), "type": "create" if i == 0 else "edit",
                             "at": rev["at"], "author": author_of(rev)}
                if rev["minor"]:
                    rec["minor"] = True
                suppressed = []
                if rev["text_deleted"]:
                    suppressed.append("content")
                if rev["comment_deleted"]:
                    suppressed.append("summary")
                if rev["contributor_deleted"]:
                    suppressed.append("author")
                    rec.pop("author", None)
                if suppressed:
                    rec["suppressed"] = suppressed
                    rec["reason"] = "revision-deleted-in-source"
                else:
                    if rev["comment"]:
                        rec["summary"] = rev["comment"]
                    rbody, rcats, rredirect, _ = wikitext_to_portable(rev["text"], markup.Notes(), path)
                    rfm = {"title": p["title"]}
                    if rcats:
                        rfm["tags"] = rcats
                    if rredirect:
                        rfm["kind"], rfm["redirect"] = "redirect", rredirect
                    content = dump_frontmatter(rfm) + ("\n" + rbody.lstrip("\n") if rbody.strip() else "")
                    rec["content"] = content
                    rec["sha256"] = hashlib.sha256(content.encode("utf-8")).hexdigest()
                records.append(rec)
                prev = rid
            hist_name = fm["id"] if fm.get("id") else strip_md(path[len("pages/"):]).replace("/", "__")
            (hist_dir / f"{hist_name}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")
    if users:
        (out / "users.yaml").write_text(yaml.safe_dump(list(users.values()), sort_keys=False, allow_unicode=True), encoding="utf-8")

    manifest = default_manifest(name=name or site.get("sitename") or dump.stem, engine="mediawiki", url=(site.get("base") or "").rsplit("/", 1)[0] or None,
                                native_format="text/x-wiki", native_separator="/")
    if site.get("generator"):
        manifest["source"]["engine_version"] = site["generator"]
    manifest["namespaces"] = sorted({v for k, v in namespaces.items() if k != 0 and v})
    manifest["contents"].update({"pages": len([p for p in pages if p["revisions"]]), "history": history and bool(pages), "users": bool(users)})
    manifest["fidelity"]["level"] = 3 if history else 2
    degraded = [{"construct": "templates and parser functions", "count": counts["templates"], "how": "kept as source in snapshot envelopes; not expanded"}]
    if used_pandoc:
        degraded.append({"construct": "wikitext", "how": "converted to Markdown with Pandoc (mediawiki reader)"})
    else:
        degraded.append({"construct": "wikitext", "how": "converted with the built-in minimal converter; tables kept as source"})
        if counts["tables"]:
            degraded.append({"construct": "tables", "count": counts["tables"], "how": "kept as wikitext source in snapshot envelopes"})
    manifest["fidelity"]["degraded"] = degraded
    manifest["fidelity"]["dropped"] = [{"construct": "media files", "how": "XML dumps do not contain uploads; File: description pages are kept"},
                                       {"construct": "IP addresses of anonymous editors", "how": "replaced by stable pseudonyms" if not keep_ips else "kept (--keep-ips)"}]
    (out / "wiki-bundle.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
    write_checksums(out)
    return {"pages": len(pages), "users": len(users), "pandoc": used_pandoc, "notes": list(dict.fromkeys(notes))}


# --------------------------------------------------------------------------- export
def _sha1_base36(text: str) -> str:
    n = int(hashlib.sha1(text.encode("utf-8")).hexdigest(), 16)
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    while n:
        n, r = divmod(n, 36)
        out = digits[r] + out
    return (out or "0").rjust(31, "0")


def _mw_title(path: str, manifest: dict) -> tuple[str, int]:
    rel = strip_md(path[len("pages/"):])
    parts = rel.split("/")
    namespaces = set(manifest.get("namespaces", []))
    if len(parts) > 1 and parts[0] in namespaces:
        return parts[0] + ":" + "/".join(parts[1:]), CANONICAL_NS.get(parts[0], 0)
    return rel, 0


def bundle_to_mediawiki(bundle: Path, out_xml: Path, *, sitename: Optional[str] = None, base: Optional[str] = None) -> dict:
    bundle, out_xml = bundle.resolve(), out_xml.resolve()
    manifest = read_manifest(bundle)
    pages = load_bundle_pages(bundle)
    notes = markup.Notes()
    sitename = sitename or (manifest.get("source") or {}).get("name") or bundle.name
    base = base or (manifest.get("source") or {}).get("url") or "https://example.org/wiki"
    if not re.search(r"/[^/]+_[^/]+$|\.php", base):
        base = base.rstrip("/") + "/Main_Page"
    pandoc = pandoc_available()

    def to_wikitext(fm: dict, body: str) -> str:
        if fm.get("kind") == "redirect" and fm.get("redirect"):
            return f"#REDIRECT [[{fm['redirect']}]]"
        text = markup.convert(body, "portable", "portable")
        # snapshot envelopes that came from MediaWiki carry the original template call: restore it
        restored: list[str] = []
        def restore(m):
            attrs = markup.parse_attrs(m.group(1))
            if attrs.get("engine") == "mediawiki" and attrs.get("src"):
                restored.append(attrs["src"])
                return f"WCRESTORE{len(restored) - 1}X"
            return m.group(2)  # other engines: keep the snapshot body
        text = re.sub(r"<!-- wiki:snapshot\b(.*?)-->(.*?)<!-- /wiki:snapshot -->", restore, text, flags=re.S)
        text = re.sub(r"```wikitext\n(.*?)\n```", r"\1", text, flags=re.S)  # tables kept as source
        wt = markdown_to_wikitext(text) if pandoc else None
        if wt is None:
            notes.add("Markdown kept as-is in <text> " + ("(Pandoc failed on this page)" if pandoc else "(Pandoc not available)")
                      + "; MediaWiki will not render it as wikitext")
            wt = text
        wt = re.sub(r'<span id="[^"]*"></span>\n?', "", wt)
        for i, src in enumerate(restored):
            wt = wt.replace(f"WCRESTORE{i}X", src)
        for tag in as_list(fm.get("tags")):
            wt = wt.rstrip("\n") + f"\n[[Category:{tag}]]"
        return wt

    parts = ['<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.11/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
             'xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.11/ http://www.mediawiki.org/xml/export-0.11.xsd" version="0.11" xml:lang="'
             + escape(str(manifest.get("lang", "en"))) + '">',
             "  <siteinfo>", f"    <sitename>{escape(sitename)}</sitename>", f"    <base>{escape(base)}</base>",
             f"    <generator>wiki-commons-tools {__version__}</generator>", "    <case>first-letter</case>", "    <namespaces>",
             '      <namespace key="0" case="first-letter" />']
    for ns_name, key in sorted(CANONICAL_NS.items(), key=lambda kv: kv[1]):
        parts.append(f'      <namespace key="{key}" case="first-letter">{escape(ns_name)}</namespace>')
    parts += ["    </namespaces>", "  </siteinfo>"]
    rev_counter = 1
    page_counter = 1
    for p in pages:
        title, ns = _mw_title(p["path"], manifest)
        fm = p["fm"]
        parts += ["  <page>", f"    <title>{escape(title)}</title>", f"    <ns>{ns}</ns>", f"    <id>{page_counter}</id>"]
        if fm.get("kind") == "redirect" and fm.get("redirect"):
            parts.append(f'    <redirect title="{escape(str(fm["redirect"]), {chr(34): "&quot;"})}" />')
        page_counter += 1
        revisions = []
        hist = bundle / "history" / f"{fm.get('id')}.jsonl" if fm.get("id") else None
        if hist and hist.exists():
            for line in hist.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                r = json.loads(line)
                if "content" not in r or r.get("suppressed"):
                    continue
                fm_text, rbody, _ = markup.split_frontmatter(r["content"])
                rfm = markup.parse_frontmatter(fm_text) or {}
                revisions.append({"at": r.get("at", ""), "author": r.get("author") or {}, "comment": r.get("summary", ""),
                                  "minor": r.get("minor", False), "text": to_wikitext(rfm, rbody)})
        if not revisions:
            revisions.append({"at": str(fm.get("updated") or fm.get("created") or "1970-01-01T00:00:00Z"),
                              "author": (fm.get("contributors") or [{}])[-1] if fm.get("contributors") else {},
                              "comment": "Imported from a Portable Wiki Bundle", "minor": False, "text": to_wikitext(fm, p["body"])})
        prev_id = None
        for r in revisions:
            at = str(r["at"])
            if not at.endswith("Z") and "+" not in at[10:] and len(at) <= 19:
                at = at + "Z"
            parts += ["    <revision>", f"      <id>{rev_counter}</id>"]
            if prev_id:
                parts.append(f"      <parentid>{prev_id}</parentid>")
            parts.append(f"      <timestamp>{escape(at)}</timestamp>")
            a = r["author"] if isinstance(r["author"], dict) else {"name": str(r["author"])}
            if a.get("anonymous"):
                parts += ["      <contributor>", f"        <ip>{escape(str(a.get('label', '0.0.0.0')))}</ip>", "      </contributor>"]
            else:
                parts += ["      <contributor>", f"        <username>{escape(str(a.get('name') or a.get('id') or 'Imported'))}</username>", "      </contributor>"]
            if r.get("minor"):
                parts.append("      <minor />")
            if r.get("comment"):
                parts.append(f"      <comment>{escape(str(r['comment']))}</comment>")
            text = r["text"]
            parts += [f"      <origin>{rev_counter}</origin>", "      <model>wikitext</model>", "      <format>text/x-wiki</format>",
                      f'      <text bytes="{len(text.encode("utf-8"))}" xml:space="preserve">{escape(text)}</text>',
                      f"      <sha1>{_sha1_base36(text)}</sha1>", "    </revision>"]
            prev_id = rev_counter
            rev_counter += 1
        parts.append("  </page>")
    parts.append("</mediawiki>")
    out_xml.parent.mkdir(parents=True, exist_ok=True)
    out_xml.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return {"pages": len(pages), "revisions": rev_counter - 1, "pandoc": pandoc, "notes": list(dict.fromkeys(notes))}
