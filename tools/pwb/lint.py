"""A linter with suggestions for Portable Wiki Markdown pages and bundles.

In the spirit of AUTH-13 (gentle guidance) and Cunningham's *Tolerant*, the linter never refuses
anything: every finding is a suggestion, a warning, or a note, the exit status is 0 unless the
caller asks otherwise, and safe fixes are applied only with --fix. Rules point at the guideline
they come from.
"""
from __future__ import annotations

import datetime as dt
import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

import yaml  # type: ignore

from . import markup
from .resolve import Page, PageIndex, strip_md

LEVELS = {"warning": 2, "suggestion": 1, "info": 0}
RFC3339_RE = re.compile(r"^\d{4}-\d{2}-\d{2}([Tt ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?([Zz]|[+-]\d{2}:\d{2}))?$")
LANG_RE = re.compile(r"^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$")
STATUS_VALUES = {"draft", "wip", "stable", "deprecated", "archived", "deleted", "seedling", "budding", "evergreen"}
DEPRECATED_KEYS = {"summary": "description", "desc": "description", "alias": "aliases", "tag": "tags", "cssclass": "ext.obsidian.cssclasses"}
SECRET_KEY_RE = re.compile(r"(token|secret|password|api[_-]?key|private[_-]?key)", re.I)
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
POOR_LINK_TEXT = {"here", "click here", "this", "link", "this link", "read more", "more"}
RAW_HTML_RE = re.compile(r"<(?!!--)(/?)([A-Za-z][A-Za-z0-9-]*)(\s[^>]*)?>")
CONTAINER_RE = re.compile(r"^:::\s*(note|tip|important|warning|caution|info|hint|danger|error)\b", re.I | re.M)
PERCENT_RE = re.compile(r"%%.*?%%", re.S)


@dataclass
class Finding:
    level: str
    code: str
    message: str
    path: str
    line: Optional[int] = None
    guideline: Optional[str] = None
    fixable: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LintResult:
    findings: list[Finding] = field(default_factory=list)
    fixed: list[str] = field(default_factory=list)

    def add(self, level: str, code: str, message: str, path: str, line: Optional[int] = None,
            guideline: Optional[str] = None, fixable: bool = False) -> None:
        self.findings.append(Finding(level, code, message, path, line, guideline, fixable))


# --------------------------------------------------------------------------- frontmatter fixes
def _fix_frontmatter_text(fm_text: str) -> tuple[str, list[str]]:
    """Apply safe textual fixes to a frontmatter block: rename deprecated keys, quote bare dates/times."""
    changes: list[str] = []
    out_lines = []
    for line in fm_text.split("\n"):
        m = re.match(r"^(\s*)([A-Za-z_][\w-]*):(\s*)(.*)$", line)
        if m and not m.group(1):
            key = m.group(2)
            if key in DEPRECATED_KEYS and "." not in DEPRECATED_KEYS[key] and not re.search(rf"^{DEPRECATED_KEYS[key]}:", fm_text, re.M):
                line = f"{m.group(1)}{DEPRECATED_KEYS[key]}:{m.group(3)}{m.group(4)}"
                changes.append(f"renamed `{key}` to `{DEPRECATED_KEYS[key]}`")
        m2 = re.match(r"^(\s*[A-Za-z_][\w-]*:\s*)(\d{4}-\d{2}-\d{2}(?:[Tt ]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:[Zz]|[+-]\d{2}:\d{2})?)?)\s*$", line)
        if m2:
            line = f'{m2.group(1)}"{m2.group(2)}"'
            changes.append(f"quoted the date/time value on `{m2.group(1).strip()}`")
        m3 = re.match(r"^((?:status|visibility|kind|lang):\s*)(yes|no|on|off|true|false|y|n)\s*$", line, re.I)
        if m3:
            line = f'{m3.group(1)}"{m3.group(2)}"'
            changes.append(f"quoted the value on `{m3.group(1).strip()}` so YAML does not read it as a boolean")
        out_lines.append(line)
    return "\n".join(out_lines), changes


def _add_tags_textually(fm_text: str, tags: list[str]) -> Optional[str]:
    """Add tags to a frontmatter block without re-serializing it (which would lose quoting)."""
    lines = fm_text.split("\n")
    for i, line in enumerate(lines):
        m = re.match(r"^tags:\s*(.*)$", line)
        if not m:
            continue
        rest = m.group(1).strip()
        if rest.startswith("[") and rest.endswith("]"):
            inner = rest[1:-1].strip()
            items = [x.strip() for x in inner.split(",") if x.strip()] if inner else []
            lines[i] = "tags: [" + ", ".join(items + tags) + "]"
            return "\n".join(lines)
        if rest and not rest.startswith("#"):
            lines[i] = "tags: [" + ", ".join([rest.strip("'\"")] + tags) + "]"
            return "\n".join(lines)
        j = i + 1
        indent = None
        while j < len(lines) and re.match(r"^\s*-\s", lines[j]):
            indent = re.match(r"^(\s*)-", lines[j]).group(1); j += 1
        indent = "  " if indent is None and j == i + 1 else (indent or "")
        for t in tags:
            lines.insert(j, f"{indent}- {t}"); j += 1
        return "\n".join(lines)
    while lines and not lines[-1].strip():
        lines.pop()
    lines.append("tags:")
    lines.extend(f"- {t}" for t in tags)
    return "\n".join(lines)


# --------------------------------------------------------------------------- page linting
def lint_text(text: str, path: str, *, index: Optional[PageIndex] = None, manifest: Optional[dict] = None,
              fix: bool = False) -> tuple[LintResult, str]:
    """Lint one page. Returns (result, possibly fixed text)."""
    res = LintResult()
    original = text
    # --- text conventions (MKUP-19) ---
    if text.startswith("﻿"):
        res.add("warning", "MKUP-19-bom", "file starts with a byte-order mark", path, 1, "MKUP-19", fixable=True)
        if fix:
            text = text.lstrip("﻿"); res.fixed.append("removed the byte-order mark")
    if "\r\n" in text:
        res.add("suggestion", "MKUP-19-crlf", "CRLF line endings; LF is recommended for exported files", path, None, "MKUP-19", fixable=True)
        if fix:
            text = text.replace("\r\n", "\n"); res.fixed.append("normalized line endings to LF")
    if text and not text.endswith("\n"):
        res.add("suggestion", "MKUP-19-newline", "no trailing newline", path, None, "MKUP-19", fixable=True)
        if fix:
            text += "\n"; res.fixed.append("added a trailing newline")

    text = text.lstrip("\ufeff") if fix else text
    atext = text.lstrip("\ufeff")  # analyse without the BOM even when not fixing
    fm_text, body, body_start = markup.split_frontmatter(atext)
    fm = markup.parse_frontmatter(fm_text) if fm_text is not None else None
    body_line0 = atext[:body_start].count("\n") + 1 if body_start else 1

    # --- frontmatter (chapter 09) ---
    if fm_text is None:
        res.add("suggestion", "META-1-missing", "no frontmatter; a `title` block makes the page portable", path, 1, "META-1")
    elif isinstance(fm, dict) and ("_error" in fm):
        res.add("warning", "META-1-parse", f"frontmatter does not parse as YAML: {fm['_error'].splitlines()[0]}", path, 1, "META-1")
    elif isinstance(fm, dict):
        if not fm.get("title"):
            res.add("suggestion", "META-2-title", "frontmatter has no `title`", path, 1, "META-2")
        for key, repl in DEPRECATED_KEYS.items():
            if key in fm:
                res.add("suggestion", "META-deprecated-key", f"`{key}` is a legacy key; use `{repl}`", path, 1, "META-4" if repl == "aliases" else "META-5" if repl == "tags" else "META-6", fixable="." not in repl)
        for key in ("created", "updated"):
            val = fm.get(key)
            if isinstance(val, (dt.date, dt.datetime)):
                res.add("warning", "META-3-coerced", f"`{key}` is unquoted and was coerced by YAML into a date object; quote it", path, 1, "META-3", fixable=True)
            elif isinstance(val, str) and not RFC3339_RE.match(val):
                res.add("warning", "META-3-format", f"`{key}: {val}` is not an RFC 3339 timestamp", path, 1, "META-3")
        for key in fm:
            v = fm[key]
            if isinstance(v, (dt.date, dt.datetime)) and key not in ("created", "updated"):
                res.add("suggestion", "META-yaml-date", f"`{key}` was coerced by YAML into a date; quote date-like strings", path, 1, "Appendix C §7", fixable=True)
            if isinstance(v, bool) and key in ("status", "visibility", "kind", "lang"):
                res.add("warning", "META-yaml-bool", f"`{key}` was coerced by YAML into a boolean (yes/no/on/off); quote it", path, 1, "Appendix C §7", fixable=True)
        if "tags" in fm and not isinstance(fm["tags"], list):
            res.add("suggestion", "META-5-list", "`tags` should be a list of strings", path, 1, "META-5")
        if "aliases" in fm and not isinstance(fm["aliases"], list):
            res.add("suggestion", "META-4-list", "`aliases` should be a list of strings", path, 1, "META-4")
        if "status" in fm and str(fm["status"]) not in STATUS_VALUES:
            res.add("info", "META-6-status", f"`status: {fm['status']}` is not one of the recommended values; importers will treat it as stable", path, 1, "META-6")
        if "lang" in fm and not LANG_RE.match(str(fm["lang"])):
            res.add("warning", "META-10-lang", f"`lang: {fm['lang']}` is not a BCP 47 tag", path, 1, "META-10")
        if "visibility" in fm and str(fm["visibility"]) not in ("public", "internal", "restricted"):
            res.add("warning", "META-13-visibility", f"`visibility: {fm['visibility']}` is not public, internal, or restricted", path, 1, "META-13")
        if fm.get("kind") == "redirect" and not fm.get("redirect"):
            res.add("warning", "META-7-redirect", "kind is redirect but there is no `redirect` target", path, 1, "META-7")
        for key in fm:
            if SECRET_KEY_RE.search(str(key)):
                res.add("warning", "META-14-secret", f"frontmatter key `{key}` looks like a credential; metadata is content", path, 1, "META-14")
        if fix and fm_text is not None:
            new_fm, changes = _fix_frontmatter_text(fm_text)
            if changes:
                text = text[:4] + new_fm + text[3 + len(fm_text) + 1:]
                res.fixed.extend(changes)
                fm_text, body, body_start = markup.split_frontmatter(text)
                fm = markup.parse_frontmatter(fm_text)

    # --- body constructs (chapter 08) ---
    scan = markup.scan(text)
    line_of = lambda off: body_line0 + body[:off].count("\n")  # noqa: E731
    seen_ids: dict[str, int] = {}
    for b in scan["block_ids"]:
        if b["id"] in seen_ids:
            res.add("warning", "MKUP-9-duplicate", f"block identifier ^{b['id']} appears more than once (first at line {seen_ids[b['id']]})", path, b["line"], "MKUP-9")
        else:
            seen_ids[b["id"]] = b["line"]
    for e in scan["envelopes"]:
        if e.get("unclosed"):
            res.add("warning", "EXT-4-unclosed", f"snapshot envelope `{e.get('name')}` is never closed", path, e["line"], "EXT-4")
    for c in scan["callouts"]:
        if c["type"].lower() not in markup.ALERT_TYPES and c["type"].lower() not in markup.CALLOUT_ALIASES:
            res.add("info", "MKUP-15-callout", f"callout type `{c['type']}` is not one of the five shared types; renderers will show a generic callout", path, c["line"], "MKUP-15")
    masked = markup.mask_code(body)
    for m in CONTAINER_RE.finditer(masked):
        res.add("suggestion", "MKUP-15-container", f"`:::{m.group(1).lower()}` container; the shared callout form is `> [!{m.group(1).upper()}]`", path, line_of(m.start()), "MKUP-15", fixable=True)
    for m in PERCENT_RE.finditer(masked):
        res.add("suggestion", "MKUP-11-percent", "Obsidian `%% %%` comment; the portable form is an HTML comment", path, line_of(m.start()), "MKUP-11", fixable=True)
    html_tags = {m.group(2).lower() for m in RAW_HTML_RE.finditer(markup._mask_spans(masked, [(mm.start(), mm.end()) for mm in markup.HTML_COMMENT_RE.finditer(masked)]))}
    html_tags -= {"br", "sup", "sub", "kbd", "mark", "details", "summary", "span", "abbr", "a", "img"}
    if html_tags:
        res.add("info", "MKUP-17-html", f"raw HTML ({', '.join(sorted(html_tags))}); importers sanitize HTML most aggressively", path, None, "MKUP-17")
    if "\t" in masked:
        res.add("suggestion", "MKUP-19-tabs", "tab characters outside code", path, line_of(masked.index("\t")), "MKUP-19")
    # headings
    levels = [h["level"] for h in scan["headings"]]
    if levels:
        if levels[0] == 1 and isinstance(fm, dict) and fm.get("title") and scan["headings"][0]["text"] != str(fm["title"]):
            res.add("suggestion", "MKUP-8-h1", "a level-1 heading that differs from the frontmatter title; body headings should begin at level 2", path, scan["headings"][0]["line"], "MKUP-8")
        prev = levels[0]
        for h in scan["headings"][1:]:
            if h["level"] > prev + 1:
                res.add("suggestion", "A11Y-3-heading-skip", f"heading level jumps from {prev} to {h['level']}", path, h["line"], "A11Y-3")
            prev = h["level"]
    texts = [h["text"] for h in scan["headings"]]
    for t in {t for t in texts if texts.count(t) > 1}:
        res.add("info", "MKUP-8-duplicate-heading", f"heading `{t}` appears more than once; anchors are disambiguated with -1, -2", path, None, "MKUP-8")
    # tags
    fm_tags = set(scan["tags"]["frontmatter"])
    missing_tags = [t for t in dict.fromkeys(scan["tags"]["inline"]) if t not in fm_tags]
    if missing_tags:
        res.add("suggestion", "MKUP-14-tags", f"inline tags not listed in frontmatter `tags`: {', '.join(missing_tags)}", path, None, "MKUP-14", fixable=isinstance(fm, dict) and fm_text is not None)
    # images and link text (A11Y-6, AUTH-12)
    for m in IMAGE_RE.finditer(masked):
        if not m.group(1).strip():
            res.add("suggestion", "A11Y-6-alt", f"image `{m.group(2)}` has no alternative text", path, line_of(m.start()), "A11Y-6")
    for m in markup.MD_LINK_RE.finditer(masked):
        if m.group(1) == "!":
            continue
        label = m.group(2).strip().lower()
        if label in POOR_LINK_TEXT or re.match(r"^https?://", label):
            res.add("suggestion", "A11Y-2-link-text", f"link text `{m.group(2)}` does not describe its target", path, line_of(m.start()), "AUTH-12")
    # links
    for l in scan["links"]:
        if l["raw"].endswith("|]]"):
            res.add("suggestion", "MKUP-4-empty-label", f"`{l['raw']}` has an empty label", path, l["line"], "MKUP-4", fixable=True)
        if not l["target"] and l["fragment"] is None:
            res.add("warning", "MKUP-4-empty", f"`{l['raw']}` has no target", path, l["line"], "MKUP-4")
        if l["fragment_kind"] == "block" and not l["target"] and l["fragment"] not in seen_ids:
            res.add("warning", "MKUP-9-missing-block", f"same-page block reference ^{l['fragment']} does not exist", path, l["line"], "MKUP-9")
        if index is not None and l["target"]:
            r = index.resolve(l["target"], path)
            if r.via == "dangling":
                prefix = l.get("prefix")
                if prefix and manifest and prefix not in (manifest.get("interwiki") or {}) and prefix not in (manifest.get("namespaces") or []):
                    res.add("info", "MKUP-13-prefix", f"`{l['raw']}` has an undeclared prefix `{prefix}`; declare it in the manifest or it is read as a title", path, l["line"], "MKUP-13")
                elif l.get("label") and index.resolve(l["label"], path).via != "dangling":
                    res.add("suggestion", "MKUP-6-order", f"`{l['raw']}`: the label resolves and the target does not; the source may be label-first", path, l["line"], "MKUP-6")
                else:
                    res.add("info", "NAV-3-dangling", f"`{l['raw']}` points at a page that does not exist (an invitation, not an error)", path, l["line"], "NAV-3")
            elif r.via == "ambiguous":
                res.add("warning", "MKUP-5-ambiguous", f"`{l['raw']}` matches several pages: {', '.join(r.candidates)}", path, l["line"], "MKUP-5")
            elif l["fragment_kind"] == "block" and r.path and index.block_ids is not None and l["fragment"] not in index.block_ids.get(r.path, set()):
                res.add("warning", "MKUP-9-missing-block", f"`{l['raw']}` refers to a block identifier that does not exist in {r.path}", path, l["line"], "MKUP-9")

    # --- safe body fixes ---
    if fix:
        new_body = body
        def _container(m):
            name = m.group(1).lower()
            ctype = name.upper() if name in markup.ALERT_TYPES else markup.CALLOUT_ALIASES.get(name, "NOTE")
            title = m.group(2).strip()
            first = "> [!" + ctype + "]" + (" " + title if title else "")
            return first + "\n" + "\n".join("> " + ln for ln in m.group(3).rstrip("\n").split("\n"))
        new_body2 = markup.CONTAINER_RE.sub(_container, new_body)
        if new_body2 != new_body:
            res.fixed.append("converted container admonitions to `> [!TYPE]` callouts"); new_body = new_body2
        new_body2 = PERCENT_RE.sub(lambda m: "<!--" + m.group(0)[2:-2] + "-->", new_body)
        if new_body2 != new_body:
            res.fixed.append("converted `%% %%` comments to HTML comments"); new_body = new_body2
        new_body2 = re.sub(r"\[\[([^\[\]|]+)\|\]\]", r"[[\1]]", new_body)
        if new_body2 != new_body:
            res.fixed.append("removed empty link labels"); new_body = new_body2
        if missing_tags and isinstance(fm, dict) and fm_text is not None:
            new_fm = _add_tags_textually(fm_text, missing_tags)
            if new_fm is not None:
                text = "---\n" + new_fm.rstrip("\n") + "\n---\n" + text[body_start:]
                res.fixed.append("added inline tags to frontmatter `tags`")
                fm_text, body, body_start = markup.split_frontmatter(text)
        text = text[:body_start] + new_body if new_body != body else text
    return res, text if fix and text != original else original


# --------------------------------------------------------------------------- folders and bundles
def _index_with_blocks(root: Path, pages: list[Path], manifest: Optional[dict]) -> PageIndex:
    is_bundle = (root / "wiki-bundle.yaml").exists()
    idx = PageIndex(namespaces=(manifest or {}).get("namespaces", []), interwiki=(manifest or {}).get("interwiki", {}),
                    pages_prefix="pages" if is_bundle else "")
    idx.block_ids = {}  # type: ignore[attr-defined]
    for f in pages:
        rel = f.relative_to(root).as_posix()
        text = f.read_text(encoding="utf-8", errors="replace")
        fm_text, body, _ = markup.split_frontmatter(text)
        fm = markup.parse_frontmatter(fm_text) or {}
        aliases = fm.get("aliases") if isinstance(fm, dict) else None
        idx.add(Page(rel, str(fm.get("title") if isinstance(fm, dict) and fm.get("title") else strip_md(f.name)),
                     [str(a) for a in aliases] if isinstance(aliases, list) else [], str(fm.get("kind", "page")) if isinstance(fm, dict) else "page"))
        idx.block_ids[rel] = {b["id"] for b in markup.scan(text)["block_ids"]}  # type: ignore[attr-defined]
    return idx


def lint_path(target: Path, *, fix: bool = False) -> LintResult:
    target = target.resolve()
    total = LintResult()
    if target.is_file():
        text = target.read_text(encoding="utf-8", errors="replace")
        res, new = lint_text(text, target.name, fix=fix)
        if fix and new != text:
            target.write_text(new, encoding="utf-8")
        total.findings.extend(res.findings); total.fixed.extend(f"{target.name}: {x}" for x in res.fixed)
        return total
    manifest = None
    root = target
    if (target / "wiki-bundle.yaml").exists():
        manifest = yaml.safe_load((target / "wiki-bundle.yaml").read_text(encoding="utf-8")) or {}
        pages_root = target / "pages"
        declared = (manifest.get("contents") or {}).get("pages")
    else:
        pages_root = target
        declared = None
    pages = sorted(p for p in pages_root.rglob("*.md") if not any(part.startswith(".") or part in ("node_modules", "book") for part in p.relative_to(target).parts)
                   and p.name not in ("import-report.md", "export-report.md"))
    if declared is not None and declared != len(pages):
        total.add("warning", "XFER-1-count", f"manifest declares {declared} pages but {len(pages)} page files exist", "wiki-bundle.yaml", None, "XFER-1")
    index = _index_with_blocks(root, pages, manifest)
    for f in pages:
        rel = f.relative_to(root).as_posix()
        text = f.read_text(encoding="utf-8", errors="replace")
        res, new = lint_text(text, rel, index=index, manifest=manifest, fix=fix)
        if manifest is not None and isinstance(markup.parse_frontmatter(markup.split_frontmatter(text)[0]), dict) and "id" not in (markup.parse_frontmatter(markup.split_frontmatter(text)[0]) or {}):
            res.add("suggestion", "META-2-id", "page has no stable `id`; identifiers survive renames", rel, 1, "META-2")
        if fix and new != text:
            f.write_text(new, encoding="utf-8")
        total.findings.extend(res.findings); total.fixed.extend(f"{rel}: {x}" for x in res.fixed)
    return total


def format_text(result: LintResult) -> str:
    lines = []
    by_path: dict[str, list[Finding]] = {}
    for f in result.findings:
        by_path.setdefault(f.path, []).append(f)
    for path, fs in by_path.items():
        lines.append(path)
        for f in sorted(fs, key=lambda x: (x.line or 0, -LEVELS[x.level])):
            loc = f"  line {f.line}" if f.line else "  (file)"
            tag = f" [{f.guideline}]" if f.guideline else ""
            lines.append(f"{loc:>12}  {f.level:<10} {f.code:<24} {f.message}{tag}" + (" (fixable)" if f.fixable else ""))
    counts = {lvl: sum(1 for f in result.findings if f.level == lvl) for lvl in ("warning", "suggestion", "info")}
    lines.append("")
    lines.append(f"{counts['warning']} warning(s), {counts['suggestion']} suggestion(s), {counts['info']} note(s)")
    if result.fixed:
        lines.append(f"{len(result.fixed)} fix(es) applied:")
        lines.extend(f"  - {x}" for x in result.fixed)
    return "\n".join(lines)


def format_json(result: LintResult) -> str:
    return json.dumps({"findings": [f.to_dict() for f in result.findings], "fixed": result.fixed}, ensure_ascii=False, indent=2)
