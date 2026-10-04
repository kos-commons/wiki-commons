"""Scan and convert Portable Wiki Markdown (guidelines chapter 08).

The scanner recognizes the Layer 2 constructs of the profile outside code
spans, fenced code blocks, frontmatter, and HTML comments: free links and
embeds, block identifiers, headings (with GitHub-style anchors), inline tags,
callouts, generic directives, snapshot envelopes, and property envelopes.

The converter re-emits a document in another dialect: it flips label order,
maps hierarchy separators, converts embed and comment syntaxes, resolves
links for static-site output, and records what it had to degrade.
"""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Callable, Optional
from urllib.parse import quote

try:  # PyYAML is optional for scanning; required for frontmatter contents
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif", ".bmp", ".tiff", ".tif"}

FENCE_RE = re.compile(r"^(\s{0,3})(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
SNAPSHOT_OPEN_RE = re.compile(r"<!--\s*wiki:snapshot\b(.*?)-->", re.S)
SNAPSHOT_CLOSE_RE = re.compile(r"<!--\s*/wiki:snapshot\s*-->")
PROPS_RE = re.compile(r"<!--\s*wiki:props\s+(\{.*?\})\s*-->", re.S)
ATTR_RE = re.compile(r"""([A-Za-z_][\w-]*)\s*=\s*(?:"((?:[^"\\]|\\.)*)"|'((?:[^'\\]|\\.)*)'|([^\s"']+))""")
WIKILINK_RE = re.compile(r"(?<!\\)(!?)\[\[([^\[\]\n]+?)\]\]")
PERCENT_COMMENT_RE = re.compile(r"%%(.*?)%%", re.S)
BLOCK_ID_RE = re.compile(r"(?:^|(?<=[ \t]))\^([A-Za-z0-9][A-Za-z0-9_-]*)[ \t]*$")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
CALLOUT_RE = re.compile(r"^[ \t]{0,3}>[ \t]*\[!([A-Za-z][\w-]*)\]([+-]?)[ \t]*(.*)$")
DIRECTIVE_OPEN_RE = re.compile(r"^:::[ \t]*([A-Za-z][\w-]*)[ \t]*(.*)$")
DIRECTIVE_CLOSE_RE = re.compile(r"^:::[ \t]*$")
INLINE_DIRECTIVE_RE = re.compile(r"(?<![:\w]):([A-Za-z][\w-]*)\[([^\]]*)\]\{([^}]*)\}")
TAG_RE = re.compile(r"(?<![\w#/&:])#(\w[^\s#\[\]()<>{},.!?;:\"'`|\\]*)")
MD_LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
URL_RE = re.compile(r"\bhttps?://\S+")
LOGSEQ_REF_RE = re.compile(r"\(\(([0-9a-fA-F-]{8,})\)\)")
LOGSEQ_ID_LINE_RE = re.compile(r"^[ \t]*id::[ \t]*([0-9a-fA-F-]{8,})[ \t]*$", re.M)
LOGSEQ_LABEL_LINK_RE = re.compile(r"\[([^\]]+)\]\(\[\[([^\[\]]+?)\]\]\)")
LOGSEQ_BLOCK_RE = re.compile(r"^([ \t]*(?:-[ \t]+)?)#\+BEGIN_([A-Z]+)[ \t]*\n(.*?)^[ \t]*#\+END_\2[ \t]*$", re.S | re.M)
CONTAINER_RE = re.compile(r"^:::[ \t]*([A-Za-z][\w-]*)[ \t]*(.*?)\n(.*?)^:::[ \t]*$", re.S | re.M)
ALERT_TYPES = {"note", "tip", "important", "warning", "caution"}
CALLOUT_ALIASES = {
    "info": "NOTE", "hint": "TIP", "success": "TIP", "check": "TIP", "done": "TIP",
    "danger": "CAUTION", "error": "CAUTION", "failure": "CAUTION", "fail": "CAUTION", "bug": "CAUTION",
    "attention": "WARNING", "question": "NOTE", "help": "NOTE", "faq": "NOTE", "example": "NOTE",
    "quote": "NOTE", "cite": "NOTE", "abstract": "NOTE", "summary": "NOTE", "tldr": "NOTE", "todo": "IMPORTANT",
    "pinned": "IMPORTANT",
}


# --------------------------------------------------------------------------- dialects
@dataclass(frozen=True)
class Dialect:
    name: str
    label_order: str = "target-first"      # or "label-first"
    separator: str = "/"                   # hierarchy separator in link targets
    link_style: str = "wikilink"           # or "markdown" (static sites)
    embed_images: bool = False             # ![[image.png]] is the native image syntax
    comment_style: str = "html"            # "html", "percent" (Obsidian %% %%), "org" (Logseq #+BEGIN_COMMENT)
    block_ids: bool = True                 # trailing ^id tokens are meaningful
    embeds: bool = True                    # ![[Page]] transclusion is meaningful
    callouts: str = "alert"                # "alert" (> [!NOTE]), "org" (#+BEGIN_NOTE), "container" (:::note)
    description: str = ""


DIALECTS: dict[str, Dialect] = {
    "portable": Dialect("portable", description="Portable Wiki Markdown (guidelines chapter 08)"),
    "obsidian": Dialect("obsidian", embed_images=True, comment_style="percent",
                        description="Obsidian Flavored Markdown; also read by Quartz and most vault tools"),
    "foam": Dialect("foam", embed_images=True, description="Foam (VS Code)"),
    "logseq": Dialect("logseq", comment_style="org", callouts="org",
                      description="Logseq file graphs: ((block refs)), id:: properties, #+BEGIN_NOTE blocks, [label]([[Page]])"),
    "dendron": Dialect("dendron", label_order="label-first", separator=".", embed_images=True,
                       description="Dendron: dot hierarchy, label-first links"),
    "gollum": Dialect("gollum", label_order="label-first", block_ids=False, embeds=False,
                      description="Gollum, the GitHub wiki, and GitLab wikis: label-first links"),
    "static": Dialect("static", link_style="markdown", block_ids=False, embeds=False,
                      description="Plain CommonMark for static site generators: wikilinks become relative Markdown links"),
}


@dataclass
class Link:
    raw: str
    target: str
    label: Optional[str]
    fragment: Optional[str]
    fragment_kind: Optional[str]   # "heading" | "block" | None
    prefix: Optional[str]          # text before the first ":" in the target, if any
    embed: bool
    line: int
    start: int = 0
    end: int = 0

    def to_dict(self) -> dict:
        return {
            "raw": self.raw, "target": self.target, "label": self.label, "fragment": self.fragment,
            "fragment_kind": self.fragment_kind, "prefix": self.prefix, "embed": self.embed, "line": self.line,
        }


# --------------------------------------------------------------------------- helpers
def github_anchor(text: str) -> str:
    """GitHub-style heading anchor (also what mdBook 0.5 produces)."""
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[\[([^\]|]*)(?:\|([^\]]*))?\]\]", lambda m: m.group(2) or m.group(1), text)
    text = re.sub(r"[*_~]+", "", text)
    text = unicodedata.normalize("NFC", text).lower()
    out = []
    for ch in text:
        if ch == " ":
            out.append("-")
        elif ch == "-" or ch == "_" or ch.isalnum() or unicodedata.category(ch).startswith(("L", "N", "M")):
            out.append(ch)
    return "".join(out)


def split_frontmatter(text: str) -> tuple[Optional[str], str, int]:
    """Return (frontmatter text or None, body, body start offset)."""
    if text.startswith("---\n") or text.startswith("---\r\n"):
        m = re.search(r"\n---[ \t]*(\r?\n|$)", text[3:])
        if m:
            fm = text[4: 3 + m.start() + 1]
            start = 3 + m.end()
            return fm, text[start:], start
    return None, text, 0


def parse_frontmatter(fm_text: Optional[str]) -> Optional[dict]:
    if fm_text is None:
        return None
    if yaml is None:
        return {"_raw": fm_text}
    try:
        data = yaml.safe_load(fm_text)
    except Exception as exc:  # noqa: BLE001
        return {"_error": str(exc), "_raw": fm_text}
    return data if isinstance(data, dict) else {"_value": data}


def jsonable(value):
    """Make parsed YAML JSON-serializable, marking values YAML coerced into dates (a frontmatter pitfall)."""
    import datetime as _dt
    if isinstance(value, _dt.datetime):
        return {"$type": "datetime", "iso": value.isoformat()}
    if isinstance(value, _dt.date):
        return {"$type": "date", "iso": value.isoformat()}
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def parse_attrs(s: str) -> dict:
    attrs: dict = {}
    for m in ATTR_RE.finditer(s):
        key = m.group(1)
        val = next(v for v in m.groups()[1:] if v is not None)
        val = val.replace('\\"', '"').replace("\\'", "'").replace("&quot;", '"').replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")
        attrs[key] = val
    return attrs


def _blank(s: str) -> str:
    """Replace every non-newline character with a space (keeps offsets and line numbers)."""
    return re.sub(r"[^\n]", " ", s)


def mask_code(text: str) -> str:
    """Blank out fenced code blocks and inline code spans, preserving offsets."""
    lines = text.split("\n")
    out, fence = [], None
    for line in lines:
        m = FENCE_RE.match(line)
        if fence is None and m:
            fence = m.group(2)[0]
            out.append(_blank(line))
            continue
        if fence is not None:
            out.append(_blank(line))
            if m and m.group(2)[0] == fence and line.strip() == m.group(2):
                fence = None
            elif m and m.group(2)[0] == fence and line.strip().rstrip(fence) == "":
                fence = None
            continue
        out.append(INLINE_CODE_RE.sub(lambda mm: _blank(mm.group(0)), line))
    return "\n".join(out)


def _mask_spans(text: str, spans) -> str:
    chars = list(text)
    for a, b in spans:
        for i in range(a, b):
            if chars[i] != "\n":
                chars[i] = " "
    return "".join(chars)


def _line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def parse_link_inner(inner: str, label_order: str = "target-first", embed: bool = False) -> dict:
    """Parse the text between [[ and ]] into target, label, fragment, prefix."""
    if "|" in inner:
        a, b = inner.split("|", 1)
        if label_order == "label-first":
            label, target_part = a, b
        else:
            target_part, label = a, b
        label = label.strip()
        if label == "":
            label = None
    else:
        target_part, label = inner, None
    target_part = target_part.strip()
    fragment = fragment_kind = None
    if "#" in target_part:
        target_part, frag = target_part.split("#", 1)
        target_part = target_part.strip()
        frag = frag.strip()
        if frag.startswith("^") and len(frag) > 1:
            fragment, fragment_kind = frag[1:], "block"
        elif frag and frag != "^":
            fragment, fragment_kind = frag, "heading"
    prefix = None
    if ":" in target_part and not target_part.startswith(("/", ".")):
        cand = target_part.split(":", 1)[0]
        if cand and " " not in cand:
            prefix = cand
    return {"target": target_part, "label": label, "fragment": fragment, "fragment_kind": fragment_kind,
            "prefix": prefix, "embed": embed}


# --------------------------------------------------------------------------- scanning
def scan(text: str, label_order: str = "target-first") -> dict:
    """Return the constructs found in a page, as a JSON-serializable dict."""
    fm_text, body, body_start = split_frontmatter(text)
    frontmatter = parse_frontmatter(fm_text)

    masked = mask_code(text)
    if body_start:
        masked = _blank(masked[:body_start]) + masked[body_start:]

    # envelopes and props live in HTML comments outside code
    envelopes, props = [], []
    opens = [(m.start(), m.end(), parse_attrs(m.group(1))) for m in SNAPSHOT_OPEN_RE.finditer(masked)]
    closes = [(m.start(), m.end()) for m in SNAPSHOT_CLOSE_RE.finditer(masked)]
    events = sorted([(s, "open", e, a) for s, e, a in opens] + [(s, "close", e, None) for s, e in closes])
    stack = []
    for pos, kind, end, attrs in events:
        if kind == "open":
            stack.append((pos, end, attrs))
        elif stack:
            opos, oend, oattrs = stack.pop()
            body_text = text[oend:pos].strip("\n")
            params = oattrs.get("params")
            if params:
                try:
                    params = json.loads(params)
                except ValueError:
                    pass
            envelopes.append({
                "line": _line_of(text, opos), "kind": oattrs.get("kind"), "name": oattrs.get("name"),
                "engine": oattrs.get("engine"), "src": oattrs.get("src"), "params": params,
                "at": oattrs.get("at"), "target": oattrs.get("target"), "id": oattrs.get("id"),
                "depth": len(stack), "body": body_text,
            })
    for opos, oend, oattrs in stack:
        envelopes.append({"line": _line_of(text, opos), "kind": oattrs.get("kind"), "name": oattrs.get("name"),
                          "engine": oattrs.get("engine"), "unclosed": True})
    envelopes.sort(key=lambda e: e["line"])
    for m in PROPS_RE.finditer(masked):
        try:
            data = json.loads(m.group(1))
        except ValueError:
            data = {"_raw": m.group(1)}
        props.append({"line": _line_of(text, m.start()), "props": data})

    # hide all HTML comments from the content scan
    masked = _mask_spans(masked, [(m.start(), m.end()) for m in HTML_COMMENT_RE.finditer(masked)])

    links: list[Link] = []
    for m in WIKILINK_RE.finditer(masked):
        d = parse_link_inner(m.group(2), label_order, embed=m.group(1) == "!")
        links.append(Link(raw=text[m.start():m.end()], line=_line_of(text, m.start()), start=m.start(), end=m.end(), **d))

    headings, block_ids, callouts, directives = [], [], [], []
    seen_anchor: dict[str, int] = {}
    pos = 0
    depth = 0
    for line in masked.split("\n"):
        line_no = _line_of(text, pos)
        h = HEADING_RE.match(line)
        if h:
            raw = text[pos: pos + len(line)]
            hm = HEADING_RE.match(raw)
            htext = hm.group(2) if hm else h.group(2)
            a = github_anchor(htext)
            if a in seen_anchor:
                seen_anchor[a] += 1
                anchor = f"{a}-{seen_anchor[a]}"
            else:
                seen_anchor[a] = 0
                anchor = a
            headings.append({"line": line_no, "level": len(h.group(1)), "text": htext, "anchor": anchor})
        else:
            b = BLOCK_ID_RE.search(line)
            if b and line.strip() != "":
                block_ids.append({"line": line_no, "id": b.group(1)})
        c = CALLOUT_RE.match(line)
        if c:
            callouts.append({"line": line_no, "type": c.group(1).upper(), "fold": c.group(2) or None,
                             "title": c.group(3).strip() or None})
        if DIRECTIVE_CLOSE_RE.match(line) and depth > 0:
            depth -= 1
        else:
            d = DIRECTIVE_OPEN_RE.match(line)
            if d:
                directives.append({"line": line_no, "name": d.group(1), "attrs": parse_attrs(d.group(2)), "inline": False})
                depth += 1
        pos += len(line) + 1
    for m in INLINE_DIRECTIVE_RE.finditer(masked):
        directives.append({"line": _line_of(text, m.start()), "name": m.group(1), "text": m.group(2),
                           "attrs": parse_attrs(m.group(3)), "inline": True})
    directives.sort(key=lambda d: d["line"])

    # tags: mask links and URLs first
    tag_masked = _mask_spans(masked, [(l.start, l.end) for l in links])
    tag_masked = _mask_spans(tag_masked, [(m.start(), m.end()) for m in MD_LINK_RE.finditer(tag_masked)])
    tag_masked = _mask_spans(tag_masked, [(m.start(), m.end()) for m in URL_RE.finditer(tag_masked)])
    inline_tags = []
    for m in TAG_RE.finditer(tag_masked):
        t = m.group(1).rstrip("/")
        if t.isdigit() or t.startswith("^"):
            continue
        if m.start() > 0 and tag_masked[m.start() - 1] not in " \t\n(" and m.start() != 0:
            continue
        inline_tags.append(t)
    fm_tags = []
    if isinstance(frontmatter, dict):
        raw_tags = frontmatter.get("tags")
        if isinstance(raw_tags, str):
            fm_tags = [t.strip() for t in re.split(r"[,\s]+", raw_tags) if t.strip()]
        elif isinstance(raw_tags, list):
            fm_tags = [str(t) for t in raw_tags]

    return {
        "frontmatter": jsonable(frontmatter),
        "headings": headings,
        "links": [l.to_dict() for l in links],
        "block_ids": block_ids,
        "tags": {"frontmatter": fm_tags, "inline": inline_tags},
        "callouts": callouts,
        "directives": directives,
        "envelopes": envelopes,
        "props": props,
    }


# --------------------------------------------------------------------------- conversion
class Notes(list):
    """Degradation notes collected during a conversion."""

    def add(self, msg: str) -> None:
        self.append(msg)


def map_separator(target: str, src: Dialect, dst: Dialect) -> str:
    if src.separator == dst.separator or not target:
        return target
    if dst.separator != "/" and target.startswith("/"):
        target = target.lstrip("/")
    if src.separator == "." and "." in target and not target.startswith("."):
        target = target.replace(".", "/")
    elif src.separator != "/" and src.separator in target:
        target = target.replace(src.separator, "/")
    if dst.separator != "/" and "/" in target:
        target = target.replace("/", dst.separator)
    return target


UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


def emit_wikilink(link: dict, dst: Dialect) -> str:
    target = link["target"]
    frag = ""
    if link.get("fragment"):
        frag = "#^" + link["fragment"] if link.get("fragment_kind") == "block" else "#" + link["fragment"]
    label = link.get("label")
    if dst.name == "logseq":
        # Logseq: ((uuid)) block references, [label]([[Page]]) for labelled links, {{embed ...}} for embeds
        if link.get("fragment_kind") == "block" and UUID_RE.match(link["fragment"]):
            ref = "((" + link["fragment"] + "))"
            if link.get("embed"):
                return "{{embed " + ref + "}}"
            return f"[{label}]({ref})" if label else ref
        inner = "[[" + target + frag + "]]"
        if link.get("embed"):
            return "{{embed " + inner + "}}"
        return f"[{label}]({inner})" if label else inner
    inner = target + frag
    if label:
        inner = f"{label}|{inner}" if dst.label_order == "label-first" else f"{inner}|{label}"
    return ("!" if link.get("embed") else "") + "[[" + inner + "]]"


def convert(
    text: str,
    src: str | Dialect = "portable",
    dst: str | Dialect = "portable",
    *,
    resolver: Optional[Callable[[str, Optional[str]], Optional[str]]] = None,
    from_path: Optional[str] = None,
    interwiki: Optional[dict] = None,
    block_index: Optional[dict] = None,
    link_rewriter: Optional[Callable[[str, bool], Optional[str]]] = None,
    notes: Optional[Notes] = None,
    absolute_links: bool = False,
) -> str:
    """Convert `text` from one dialect to another.

    resolver(target, from_path) -> path of the target page (relative to the content root, e.g.
    "guides/Getting Started.md"), or a (path, title) tuple, or None when dangling; only needed for
    the static dialect. The title, when given, is the default label of unlabelled links.
    link_rewriter(href, is_image) -> replacement href for standard Markdown links and images with
    relative targets (used to relocate attachments), or None to keep.
    absolute_links=True makes static links bundle-absolute ("/path.md"), as OKF recommends.
    block_index maps block identifiers (e.g. Logseq UUIDs) to page titles.
    """
    src_d = DIALECTS[src] if isinstance(src, str) else src
    dst_d = DIALECTS[dst] if isinstance(dst, str) else dst
    notes = notes if notes is not None else Notes()
    interwiki = interwiki or {}
    fm_text, body, body_start = split_frontmatter(text)
    head = text[:body_start]

    # --- source-dialect normalizations on the body ---
    if src_d.name == "logseq":
        # id:: <uuid> property lines become a trailing ^uuid on the previous line
        lines = body.split("\n")
        out_lines: list[str] = []
        for line in lines:
            m = LOGSEQ_ID_LINE_RE.match(line)
            if m and out_lines:
                i = len(out_lines) - 1
                while i >= 0 and out_lines[i].strip() == "":
                    i -= 1
                if i >= 0:
                    out_lines[i] = out_lines[i].rstrip() + " ^" + m.group(1)
                    continue
            out_lines.append(line)
        body = "\n".join(out_lines)
        # [label]([[Page]]) -> [[Page|label]]
        body = LOGSEQ_LABEL_LINK_RE.sub(lambda m: f"[[{m.group(2)}|{m.group(1)}]]", body)
        # ((uuid)) -> [[Page#^uuid]] when the block index knows the page
        def _ref(m):
            uid = m.group(1)
            page = (block_index or {}).get(uid)
            if page:
                return f"[[{page}#^{uid}]]"
            notes.add(f"unresolved Logseq block reference (({uid})) kept as text")
            return m.group(0)
        body = re.sub(r"\{\{embed\s+\[\[([^\[\]]+?)\]\]\s*\}\}", lambda m: "![[" + m.group(1) + "]]", body)
        body = re.sub(r"\{\{embed\s+\(\(([0-9a-fA-F-]{8,})\)\)\s*\}\}",
                      lambda m: ("![[" + (block_index or {}).get(m.group(1), "") + "#^" + m.group(1) + "]]") if (block_index or {}).get(m.group(1)) else m.group(0), body)
        body = LOGSEQ_REF_RE.sub(_ref, body)
        # #+BEGIN_NOTE ... #+END_NOTE -> callouts
        def _org_block(m):
            prefix, kind = m.group(1), m.group(2)
            indent = re.sub(r"\S", " ", prefix)
            raw_lines = m.group(3).rstrip("\n").split("\n")
            common = min((len(l) - len(l.lstrip()) for l in raw_lines if l.strip()), default=0)
            content = [l[common:] if l.strip() else "" for l in raw_lines]
            if kind == "COMMENT":
                return prefix + "<!--\n" + "\n".join(indent + l for l in content) + "\n" + indent + "-->"
            if kind in ("QUOTE", "VERSE"):
                return "\n".join((prefix if i == 0 else indent) + "> " + l for i, l in enumerate(content))
            ctype = kind if kind.lower() in ALERT_TYPES else CALLOUT_ALIASES.get(kind.lower(), "NOTE")
            return prefix + "> [!" + ctype + "]\n" + "\n".join(indent + "> " + l for l in content)
        body = LOGSEQ_BLOCK_RE.sub(_org_block, body)
    if src_d.comment_style == "percent":
        body = PERCENT_COMMENT_RE.sub(lambda m: "<!--" + m.group(1) + "-->", body)
    # ::: container -> callout, when the container name is an admonition type
    def _container(m):
        name = m.group(1).lower()
        if name in ALERT_TYPES or name in CALLOUT_ALIASES:
            ctype = name.upper() if name in ALERT_TYPES else CALLOUT_ALIASES[name]
            title = m.group(2).strip()
            first = "> [!" + ctype + "]" + (" " + title if title else "")
            return first + "\n" + "\n".join("> " + l for l in m.group(3).rstrip("\n").split("\n"))
        return m.group(0)
    body = CONTAINER_RE.sub(_container, body)

    # --- links and block ids, driven by the masked view ---
    masked = mask_code(body)
    masked = _mask_spans(masked, [(m.start(), m.end()) for m in HTML_COMMENT_RE.finditer(masked)])
    edits: list[tuple[int, int, str]] = []

    def rel_href(target_path: str) -> str:
        """Relative href from from_path's directory to target_path (both content-root relative)."""
        if not from_path:
            return quote(target_path)
        src_parts = from_path.split("/")[:-1]
        tgt_parts = target_path.split("/")
        i = 0
        while i < len(src_parts) and i < len(tgt_parts) - 1 and src_parts[i] == tgt_parts[i]:
            i += 1
        rel = [".."] * (len(src_parts) - i) + tgt_parts[i:]
        return quote("/".join(rel))

    for m in WIKILINK_RE.finditer(masked):
        d = parse_link_inner(m.group(2), src_d.label_order, embed=m.group(1) == "!")
        target = d["target"]
        is_image = any(target.lower().endswith(ext) for ext in IMAGE_EXT)
        prefix = d["prefix"]
        if prefix and prefix in interwiki:
            url = interwiki[prefix].replace("{title}", quote(target.split(":", 1)[1].strip()))
            label = d["label"] or target.split(":", 1)[1].strip()
            if dst_d.link_style == "markdown":
                edits.append((m.start(), m.end(), f"[{label}]({url})"))
            continue  # wikilink dialects keep the prefix form
        if is_image and d["embed"] and not dst_d.embed_images:
            alt = d["label"] or target.rsplit("/", 1)[-1]
            alt = re.sub(r"^\d+(x\d+)?$", "", alt) or target.rsplit("/", 1)[-1]
            href = target
            if link_rewriter:
                href = link_rewriter(target, True) or target
            edits.append((m.start(), m.end(), f"![{alt}]({href})"))
            continue
        d["target"] = map_separator(target, src_d, dst_d)
        if dst_d.link_style == "wikilink":
            if d["embed"] and not dst_d.embeds and not is_image:
                d["embed"] = False
                notes.add(f"embed of {target!r} degraded to a link")
            if d["fragment_kind"] == "block" and not dst_d.block_ids:
                notes.add(f"block reference to {target!r}#^{d['fragment']} degraded to a page link")
                d["fragment"] = d["fragment_kind"] = None
            edits.append((m.start(), m.end(), emit_wikilink(d, dst_d)))
            continue
        # static: resolve to a relative Markdown link
        if not target:  # same-page link
            label = d["label"] or d["fragment"] or ""
            if d["fragment_kind"] == "block":
                notes.add(f"same-page block reference ^{d['fragment']} degraded to text")
                edits.append((m.start(), m.end(), label))
            else:
                frag = "#" + github_anchor(d["fragment"]) if d["fragment_kind"] == "heading" else ""
                edits.append((m.start(), m.end(), f"[{label}]({frag})"))
            continue
        resolved = resolver(target, from_path) if resolver else None
        title = None
        if isinstance(resolved, tuple):
            resolved, title = resolved
        label = d["label"] or title or target.rsplit("/", 1)[-1]
        if resolved is None and resolver is not None:
            notes.add(f"dangling link to {target!r} degraded to text")
            edits.append((m.start(), m.end(), d["label"] or target.rsplit("/", 1)[-1]))
            continue
        if resolved and absolute_links:
            href = "/" + quote(resolved)
        else:
            href = rel_href(resolved) if resolved else quote(target + ".md")
        if d["fragment_kind"] == "heading":
            href += "#" + github_anchor(d["fragment"])
        elif d["fragment_kind"] == "block":
            notes.add(f"block reference {target!r}#^{d['fragment']} degraded to a page link")
        if d["embed"]:
            notes.add(f"embed of {target!r} degraded to a link")
        edits.append((m.start(), m.end(), f"[{label}]({href})"))

    if not dst_d.block_ids:
        pos = 0
        for line in masked.split("\n"):
            b = BLOCK_ID_RE.search(line)
            if b and line.strip() != "" and not HEADING_RE.match(line):
                start = pos + b.start()
                if line[: b.start()].strip() == "":
                    edits.append((start, pos + len(line), ""))  # identifier-only line
                else:
                    edits.append((start - 1 if start > pos and line[b.start() - 1] in " \t" else start, pos + len(line), ""))
                notes.add(f"block identifier ^{b.group(1)} removed")
            pos += len(line) + 1

    if link_rewriter:
        for m in MD_LINK_RE.finditer(masked):
            href = m.group(3)
            if URL_RE.match(href) or href.startswith(("#", "mailto:", "/")):
                continue
            new = link_rewriter(href, m.group(1) == "!")
            if new and new != href:
                edits.append((m.start(3), m.end(3), new))

    edits.sort(key=lambda e: e[0])
    out, last = [], 0
    for a, b, rep in edits:
        if a < last:
            continue
        out.append(body[last:a]); out.append(rep); last = b
    out.append(body[last:])
    body = "".join(out)

    # --- destination-dialect comment and callout syntax ---
    if dst_d.comment_style == "percent":
        body = re.sub(r"<!--(?!\s*/?wiki:)(.*?)-->", lambda m: "%%" + m.group(1) + "%%", body, flags=re.S)
    if dst_d.callouts == "org":
        lines, out_lines, i = body.split("\n"), [], 0
        while i < len(lines):
            c = CALLOUT_RE.match(lines[i])
            if c:
                block = []
                i += 1
                while i < len(lines) and lines[i].lstrip().startswith(">"):
                    block.append(re.sub(r"^[ \t]{0,3}>[ \t]?", "", lines[i])); i += 1
                kind = c.group(1).upper()
                if kind not in ("NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION"):
                    kind = "NOTE"
                title = c.group(3).strip()
                out_lines.append(f"#+BEGIN_{kind}")
                if title:
                    out_lines.append(f"**{title}**")
                out_lines.extend(block)
                out_lines.append(f"#+END_{kind}")
                continue
            out_lines.append(lines[i]); i += 1
        body = "\n".join(out_lines)
    return head + body
