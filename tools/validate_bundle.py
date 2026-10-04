#!/usr/bin/env python3
"""Validate a Portable Wiki Bundle against the Wiki Commons schemas.

Usage:
    python3 tools/validate_bundle.py <bundle-dir> [--schemas <schemas-dir>] [--quiet]

Checks performed:
  * wiki-bundle.yaml against bundle-manifest.schema.json
  * the YAML frontmatter of every pages/**/*.md against page-frontmatter.schema.json
  * every line of history/*.jsonl against history-record.schema.json
  * every line of discussions/*.jsonl against discussion-record.schema.json
  * every attachments/*.meta.yaml (or attachments.yaml) against attachment-meta.schema.json
  * sha256sums.txt (or the file named by the manifest's `checksums`) against the files
  * that targets in links.json and blocks.json exist (dangling links are reported as info)
  * that relative image/attachment paths inside pages exist
  * that `[[Page#^id]]` references point at identifiers that exist

The validator implements the subset of JSON Schema (draft 2020-12) used by the
Wiki Commons schemas: type, required, properties, additionalProperties, items,
enum, const, pattern, minimum, maximum, minLength, anyOf, $ref (local and to a
sibling schema file), and the formats date, date-time, uri (checked loosely).
It needs only the Python standard library plus PyYAML for the YAML files.

Exit status: 0 when no errors were found, 1 otherwise. Warnings and info do not
affect the exit status.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

HERE = Path(__file__).resolve().parent
DEFAULT_SCHEMAS = HERE.parent / "schemas"

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATETIME_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?([Zz]|[+-]\d{2}:\d{2})$"
)
URI_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]|#]+?)(?:#([^\]|]+?))?(?:\|[^\]]*?)?\]\]")
EMBED_RE = re.compile(r"!\[\[([^\]|#]*?)(?:#([^\]|]+?))?(?:\|[^\]]*?)?\]\]")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
BLOCK_ID_RE = re.compile(r"(?:^|\s)\^([A-Za-z0-9][A-Za-z0-9_-]*)\s*$", re.M)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")



def strip_fences(text: str) -> str:
    """Remove fenced code blocks, detecting fences line by line (``` or ~~~)."""
    out, fence = [], None
    for line in text.split("\n"):
        stripped = line.lstrip()
        if fence is None and (stripped.startswith("```") or stripped.startswith("~~~")):
            fence = stripped[:3]
            continue
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            continue
        out.append(line)
    return "\n".join(out)

class Report:
    def __init__(self, quiet: bool = False) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.infos: list[str] = []
        self.quiet = quiet

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def info(self, msg: str) -> None:
        self.infos.append(msg)

    def print(self) -> None:
        for m in self.errors:
            print(f"ERROR   {m}")
        for m in self.warnings:
            print(f"WARNING {m}")
        if not self.quiet:
            for m in self.infos:
                print(f"info    {m}")
        print(
            f"\n{len(self.errors)} error(s), {len(self.warnings)} warning(s), "
            f"{len(self.infos)} informational note(s)"
        )


# --------------------------------------------------------------------------- schema subset
class Validator:
    def __init__(self, schemas_dir: Path) -> None:
        self.schemas_dir = schemas_dir
        self.cache: dict[str, dict] = {}

    def load(self, name: str) -> dict:
        if name not in self.cache:
            with open(self.schemas_dir / name, encoding="utf-8") as f:
                self.cache[name] = json.load(f)
        return self.cache[name]

    def resolve_ref(self, ref: str, root: dict) -> tuple[dict, dict]:
        """Return (schema, root) for a $ref."""
        if ref.startswith("#"):
            target_root = root
            pointer = ref[1:]
        else:
            file_part, _, pointer = ref.partition("#")
            target_root = self.load(Path(file_part).name)
        node: dict = target_root
        for part in [p for p in pointer.split("/") if p]:
            part = part.replace("~1", "/").replace("~0", "~")
            node = node[part]
        return node, target_root

    @staticmethod
    def type_ok(value, t: str) -> bool:
        if t == "object":
            return isinstance(value, dict)
        if t == "array":
            return isinstance(value, list)
        if t == "string":
            return isinstance(value, str)
        if t == "integer":
            return isinstance(value, int) and not isinstance(value, bool)
        if t == "number":
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        if t == "boolean":
            return isinstance(value, bool)
        if t == "null":
            return value is None
        return True

    @staticmethod
    def format_ok(value, fmt: str) -> bool:
        if not isinstance(value, str):
            return True
        if fmt == "date":
            return bool(DATE_RE.match(value))
        if fmt == "date-time":
            return bool(DATETIME_RE.match(value))
        if fmt == "uri":
            return bool(URI_RE.match(value))
        return True

    def validate(self, value, schema: dict, root: dict, path: str, errors: list[str]) -> None:
        if "$ref" in schema:
            target, target_root = self.resolve_ref(schema["$ref"], root)
            self.validate(value, target, target_root, path, errors)
            return
        if "const" in schema and value != schema["const"]:
            errors.append(f"{path}: expected constant {schema['const']!r}, got {value!r}")
            return
        if "enum" in schema and value not in schema["enum"]:
            errors.append(f"{path}: {value!r} is not one of {schema['enum']}")
        if "type" in schema:
            types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
            if not any(self.type_ok(value, t) for t in types):
                errors.append(f"{path}: expected type {'/'.join(types)}, got {type(value).__name__}")
                return
        if "anyOf" in schema:
            sub_errors_all = []
            for sub in schema["anyOf"]:
                sub_errors: list[str] = []
                self.validate(value, sub, root, path, sub_errors)
                if not sub_errors:
                    break
                sub_errors_all.append(sub_errors)
            else:
                errors.append(f"{path}: value matches none of the alternatives ({value!r})")
        if isinstance(value, str):
            if "pattern" in schema and not re.search(schema["pattern"], value):
                errors.append(f"{path}: {value!r} does not match pattern {schema['pattern']}")
            if "minLength" in schema and len(value) < schema["minLength"]:
                errors.append(f"{path}: string shorter than {schema['minLength']}")
            if "format" in schema and not self.format_ok(value, schema["format"]):
                errors.append(f"{path}: {value!r} is not a valid {schema['format']}")
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if "minimum" in schema and value < schema["minimum"]:
                errors.append(f"{path}: {value} < minimum {schema['minimum']}")
            if "maximum" in schema and value > schema["maximum"]:
                errors.append(f"{path}: {value} > maximum {schema['maximum']}")
        if isinstance(value, dict):
            for req in schema.get("required", []):
                if req not in value:
                    errors.append(f"{path}: missing required key {req!r}")
            props = schema.get("properties", {})
            for k, v in value.items():
                if k in props:
                    self.validate(v, props[k], root, f"{path}.{k}", errors)
                else:
                    ap = schema.get("additionalProperties", True)
                    if ap is False:
                        errors.append(f"{path}: unexpected key {k!r}")
                    elif isinstance(ap, dict):
                        self.validate(v, ap, root, f"{path}.{k}", errors)
        if isinstance(value, list) and "items" in schema:
            for i, item in enumerate(value):
                self.validate(item, schema["items"], root, f"{path}[{i}]", errors)


# --------------------------------------------------------------------------- helpers
def load_yaml(path: Path, report: Report):
    if yaml is None:
        report.warn(f"{path}: PyYAML not installed; YAML files were not checked")
        return None
    with open(path, encoding="utf-8") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as exc:  # type: ignore[attr-defined]
            report.error(f"{path}: YAML parse error: {exc}")
            return None


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if text.startswith("---\n") or text.startswith("---\r\n"):
        end = re.search(r"\n---[ \t]*(\r?\n|$)", text[3:])
        if end:
            fm = text[4 : 3 + end.start() + 1]
            body = text[3 + end.end() :]
            return fm, body
    return None, text


def strip_code(body: str) -> str:
    body = strip_fences(body)
    body = INLINE_CODE_RE.sub("", body)
    return body


def title_key(s: str) -> str:
    import unicodedata

    s = unicodedata.normalize("NFC", s).strip()
    s = re.sub(r"[\s_-]+", " ", s)
    return s.casefold()


# --------------------------------------------------------------------------- main checks
def main(argv: list[str]) -> int:
    quiet = "--quiet" in argv
    argv = [a for a in argv if a != "--quiet"]
    schemas_dir = DEFAULT_SCHEMAS
    if "--schemas" in argv:
        i = argv.index("--schemas")
        schemas_dir = Path(argv[i + 1])
        del argv[i : i + 2]
    if len(argv) != 2:
        print(__doc__)
        return 2
    bundle = Path(argv[1]).resolve()
    report = Report(quiet=quiet)
    v = Validator(schemas_dir)

    # manifest
    manifest_path = bundle / "wiki-bundle.yaml"
    manifest = None
    if not manifest_path.exists():
        report.error("wiki-bundle.yaml is missing")
    else:
        manifest = load_yaml(manifest_path, report)
        if manifest is not None:
            errs: list[str] = []
            v.validate(manifest, v.load("bundle-manifest.schema.json"), v.load("bundle-manifest.schema.json"), "manifest", errs)
            report.errors.extend(f"wiki-bundle.yaml: {e}" for e in errs)

    interwiki = (manifest or {}).get("interwiki", {}) if isinstance(manifest, dict) else {}
    namespaces = (manifest or {}).get("namespaces", []) if isinstance(manifest, dict) else []

    # pages
    pages_dir = bundle / "pages"
    titles: dict[str, Path] = {}
    aliases: dict[str, Path] = {}
    block_ids: dict[tuple[str, str], Path] = {}
    page_bodies: dict[Path, str] = {}
    page_count = 0
    fm_schema = v.load("page-frontmatter.schema.json")
    for md in sorted(pages_dir.rglob("*.md")) if pages_dir.exists() else []:
        page_count += 1
        rel = md.relative_to(bundle)
        text = md.read_text(encoding="utf-8")
        if text.startswith("﻿"):
            report.warn(f"{rel}: starts with a byte-order mark (MKUP-19)")
        if not text.endswith("\n"):
            report.warn(f"{rel}: no trailing newline (MKUP-19)")
        fm_text, body = split_frontmatter(text)
        fm: dict = {}
        if fm_text is None:
            report.warn(f"{rel}: no frontmatter; title taken from file name")
            title = md.stem
        else:
            parsed = load_yaml_text(fm_text, rel, report)
            if isinstance(parsed, dict):
                fm = parsed
                errs = []
                v.validate(fm, fm_schema, fm_schema, "frontmatter", errs)
                report.errors.extend(f"{rel}: {e}" for e in errs)
            elif parsed is not None:
                report.error(f"{rel}: frontmatter is not a mapping")
            title = fm.get("title") or md.stem
            if "title" not in fm:
                report.warn(f"{rel}: frontmatter has no title (META-2)")
        page_bodies[rel] = body
        # register titles: full path form and bare title
        path_title = str(rel.relative_to("pages").with_suffix("")).replace(os.sep, "/")
        for key in {title_key(title), title_key(path_title)}:
            if key in titles and titles[key] != rel:
                report.warn(f"{rel}: title {title!r} collides with {titles[key]}")
            titles[key] = rel
        for a in fm.get("aliases", []) or []:
            aliases[title_key(str(a))] = rel
        if fm.get("kind") == "redirect" and not fm.get("redirect"):
            report.error(f"{rel}: kind is redirect but no redirect target")
        if fm.get("redirect") and body.strip():
            report.warn(f"{rel}: redirect page has a body")
        for m in BLOCK_ID_RE.finditer(strip_code(body)):
            block_ids[(str(rel), m.group(1))] = rel
        # relative images
        for m in IMAGE_RE.finditer(strip_code(body)):
            target = m.group(1)
            if URI_RE.match(target) or target.startswith("#"):
                continue
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                report.error(f"{rel}: image/attachment path not found: {target}")

    if manifest and isinstance(manifest, dict):
        declared = (manifest.get("contents") or {}).get("pages")
        if declared is not None and declared != page_count:
            report.warn(f"manifest declares {declared} pages but {page_count} page files were found")

    # link resolution (informational for dangling links)
    def resolve_title(t: str) -> bool:
        k = title_key(t)
        return k in titles or k in aliases

    for rel, body in page_bodies.items():
        clean = strip_code(body)
        for m in list(WIKILINK_RE.finditer(clean)) + list(EMBED_RE.finditer(clean)):
            target, frag = m.group(1).strip(), m.group(2)
            if target == "":
                target_rel = rel  # same-page link
            else:
                prefix, _, rest = target.partition(":")
                if _ and prefix in interwiki:
                    continue
                if _ and prefix not in namespaces and prefix not in interwiki and rest and not resolve_title(target):
                    report.info(f"{rel}: link target {target!r} has an undeclared prefix {prefix!r}; treated as a title")
                if not resolve_title(target):
                    report.info(f"{rel}: dangling link to {target!r}")
                    continue
                k = title_key(target)
                target_rel = titles.get(k) or aliases.get(k)
            if frag and frag.startswith("^") and target_rel is not None:
                if (str(target_rel), frag[1:]) not in block_ids:
                    report.error(f"{rel}: block reference {target!r}#{frag} not found")

    # attachments
    att_dir = bundle / "attachments"
    att_schema = v.load("attachment-meta.schema.json")
    att_count = 0
    if att_dir.exists():
        index = att_dir / "attachments.yaml"
        entries = []
        if index.exists():
            data = load_yaml(index, report)
            if isinstance(data, list):
                entries = [(index, e) for e in data]
        for side in sorted(att_dir.rglob("*.meta.yaml")):
            entries.append((side, load_yaml(side, report)))
        for f in att_dir.rglob("*"):
            if f.is_file() and not f.name.endswith(".meta.yaml") and f.name != "attachments.yaml":
                att_count += 1
                if not (att_dir / (str(f.relative_to(att_dir)) + ".meta.yaml")).exists() and not index.exists():
                    report.warn(f"{f.relative_to(bundle)}: no sidecar metadata (XFER-4)")
        for src, entry in entries:
            if not isinstance(entry, dict):
                continue
            errs = []
            v.validate(entry, att_schema, att_schema, "attachment", errs)
            report.errors.extend(f"{src.relative_to(bundle)}: {e}" for e in errs)
            fn = entry.get("filename")
            if fn:
                target = (src.parent if src.name.endswith(".meta.yaml") else att_dir) / fn
                if not target.exists():
                    report.error(f"{src.relative_to(bundle)}: filename {fn!r} not found")
                else:
                    if "sha256" in entry:
                        actual = hashlib.sha256(target.read_bytes()).hexdigest()
                        if actual != entry["sha256"]:
                            report.error(f"{src.relative_to(bundle)}: sha256 mismatch for {fn}")
                    if "size" in entry and entry["size"] != target.stat().st_size:
                        report.error(f"{src.relative_to(bundle)}: size mismatch for {fn}")
    if manifest and isinstance(manifest, dict):
        declared = (manifest.get("contents") or {}).get("attachments")
        if declared is not None and declared != att_count:
            report.warn(f"manifest declares {declared} attachments but {att_count} were found")

    # history and discussions
    for sub, schema_name, required_first in (
        ("history", "history-record.schema.json", True),
        ("discussions", "discussion-record.schema.json", False),
    ):
        d = bundle / sub
        if not d.exists():
            continue
        schema = v.load(schema_name)
        for jl in sorted(d.glob("*.jsonl")):
            rel = jl.relative_to(bundle)
            seen: set[str] = set()
            last_at = None
            for n, line in enumerate(jl.read_text(encoding="utf-8").splitlines(), 1):
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError as exc:
                    report.error(f"{rel}:{n}: invalid JSON: {exc}")
                    continue
                errs = []
                v.validate(rec, schema, schema, f"line {n}", errs)
                report.errors.extend(f"{rel}: {e}" for e in errs)
                if sub == "history":
                    rid = rec.get("rev")
                    if rid in seen:
                        report.error(f"{rel}:{n}: duplicate rev {rid!r}")
                    seen.add(rid)
                    parent = rec.get("parent")
                    if n > 1 and parent is not None and parent not in seen:
                        report.warn(f"{rel}:{n}: parent {parent!r} not seen earlier in the file")
                    if required_first and n == 1 and parent is not None:
                        report.warn(f"{rel}: first record has a parent; history may be partial")
                    if "content" in rec and "sha256" in rec:
                        actual = hashlib.sha256(rec["content"].encode("utf-8")).hexdigest()
                        if actual != rec["sha256"]:
                            report.error(f"{rel}:{n}: sha256 does not match content")
                    if rec.get("suppressed") and ("content" in rec or "summary" in rec and "summary" in rec.get("suppressed", [])):
                        report.error(f"{rel}:{n}: suppressed fields must be omitted")
                    at = rec.get("at")
                    if last_at and at and at < last_at:
                        report.warn(f"{rel}:{n}: records are not in chronological order")
                    last_at = at or last_at

    # users
    users_path = bundle / "users.yaml"
    if users_path.exists():
        users = load_yaml(users_path, report)
        if isinstance(users, list):
            for u in users:
                if isinstance(u, dict) and "email" in u:
                    report.warn("users.yaml: contains email addresses (PRIV-3, XFER-8)")
                    break

    # blocks.json and links.json
    bj = bundle / "blocks.json"
    if bj.exists():
        data = json.loads(bj.read_text(encoding="utf-8"))
        for bid, path in data.items():
            if not (bundle / path).exists():
                report.error(f"blocks.json: {bid!r} points at missing file {path}")
            elif (path, bid) not in block_ids:
                report.error(f"blocks.json: block ^{bid} not found in {path}")
    lj = bundle / "links.json"
    if lj.exists():
        data = json.loads(lj.read_text(encoding="utf-8"))
        for edge in data:
            src = edge.get("from")
            if src and not (bundle / src).exists():
                report.error(f"links.json: source {src} does not exist")
            if edge.get("resolved") and edge.get("kind") in ("link", "embed", "redirect", "attachment"):
                to = edge.get("to", "")
                if not (bundle / to).exists():
                    report.error(f"links.json: resolved target {to} does not exist")

    # checksums
    sums_name = (manifest or {}).get("checksums", "sha256sums.txt") if isinstance(manifest, dict) else "sha256sums.txt"
    sums = bundle / sums_name
    if sums.exists():
        for n, line in enumerate(sums.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                digest, path = line.split(None, 1)
            except ValueError:
                report.error(f"{sums_name}:{n}: malformed line")
                continue
            path = path.strip()
            if path.startswith("*"):
                path = path[1:]
            f = bundle / path
            if not f.exists():
                report.error(f"{sums_name}:{n}: {path} does not exist")
                continue
            if hashlib.sha256(f.read_bytes()).hexdigest() != digest:
                report.error(f"{sums_name}:{n}: checksum mismatch for {path}")
    else:
        report.info(f"no {sums_name}; checksums not verified")

    report.print()
    return 1 if report.errors else 0


def load_yaml_text(text: str, rel, report: Report):
    if yaml is None:
        report.warn(f"{rel}: PyYAML not installed; frontmatter was not checked")
        return None
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as exc:  # type: ignore[attr-defined]
        report.error(f"{rel}: frontmatter YAML parse error: {exc}")
        return None


if __name__ == "__main__":
    sys.exit(main(sys.argv))
