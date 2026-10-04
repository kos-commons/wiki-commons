"""Command-line interface for the Wiki Commons reference tooling."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__, markup
from .resolve import Page, PageIndex

ROOT = Path(__file__).resolve().parent.parent.parent


def _index_from_folder(folder: Path, pages_prefix: str = "") -> PageIndex:
    pages = []
    for f in sorted(folder.rglob("*.md")):
        if any(part.startswith(".") for part in f.relative_to(folder).parts):
            continue
        text = f.read_text(encoding="utf-8")
        fm_text, _, _ = markup.split_frontmatter(text)
        fm = markup.parse_frontmatter(fm_text) or {}
        title = str(fm.get("title") or f.stem)
        aliases = fm.get("aliases") or []
        pages.append(Page(f.relative_to(folder).as_posix(), title, [str(a) for a in aliases] if isinstance(aliases, list) else []))
    return PageIndex(pages, pages_prefix=pages_prefix)


def cmd_scan(args) -> int:
    text = Path(args.file).read_text(encoding="utf-8")
    print(json.dumps(markup.scan(text, label_order=args.label_order), ensure_ascii=False, indent=2))
    return 0


def cmd_convert(args) -> int:
    src = Path(args.path)
    notes = markup.Notes()
    if src.is_dir():
        out = Path(args.out) if args.out else None
        if out is None:
            print("--out is required when converting a directory", file=sys.stderr)
            return 2
        index = _index_from_folder(src)
        resolver = lambda t, f: (lambda r: r.path)(index.resolve(t, f))
        for f in sorted(src.rglob("*.md")):
            rel = f.relative_to(src)
            converted = markup.convert(f.read_text(encoding="utf-8"), getattr(args, "from"), args.to, resolver=resolver,
                                       from_path=rel.as_posix(), notes=notes)
            dest = out / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(converted, encoding="utf-8")
    else:
        converted = markup.convert(src.read_text(encoding="utf-8"), getattr(args, "from"), args.to, notes=notes)
        if args.out:
            Path(args.out).write_text(converted, encoding="utf-8")
        else:
            sys.stdout.write(converted)
    for n in notes:
        print(f"note: {n}", file=sys.stderr)
    return 0


def cmd_resolve(args) -> int:
    index = _index_from_folder(Path(args.folder), pages_prefix=args.pages_prefix)
    r = index.resolve(args.target, getattr(args, "from"))
    print(json.dumps(r.to_dict(), ensure_ascii=False))
    return 0 if r.resolved else 1


def cmd_bundle(args) -> int:
    from .bundle import build_bundle
    report = build_bundle(Path(args.src), Path(args.out), dialect=args.dialect, name=args.name, license=args.license,
                          lang=args.lang, history=args.history, id_mode="stable" if args.stable_ids else "uuid4",
                          source_url=args.source_url)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def cmd_unbundle(args) -> int:
    from .bundle import unbundle
    report = unbundle(Path(args.bundle), Path(args.out), dialect=args.dialect)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def cmd_okf(args) -> int:
    from .okf import bundle_to_okf, okf_to_bundle
    if args.direction == "export":
        report = bundle_to_okf(Path(args.src), Path(args.out), name=args.name, default_type=args.type)
    else:
        report = okf_to_bundle(Path(args.src), Path(args.out), name=args.name)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def cmd_validate(args) -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    import validate_bundle  # type: ignore
    return validate_bundle.main(["validate_bundle.py", args.bundle] + (["--quiet"] if args.quiet else []))


def cmd_corpus(args) -> int:
    from .corpus import run
    results = run(Path(args.corpus), update=args.action == "update")
    failed = 0
    for status, label, detail in results:
        if status == "fail":
            failed += 1
            print(f"FAIL  {label}: {detail}")
        elif args.verbose or status == "updated":
            print(f"{status:7} {label}")
    print(f"\n{len(results)} checks, {failed} failed")
    return 1 if failed else 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="wikicommons", description="Wiki Commons reference tooling " + __version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan", help="list the Portable Wiki Markdown constructs in a page as JSON")
    s.add_argument("file"); s.add_argument("--label-order", default="target-first", choices=["target-first", "label-first"])
    s.set_defaults(func=cmd_scan)

    s = sub.add_parser("convert", help="convert a page or folder between dialects")
    s.add_argument("path"); s.add_argument("--from", default="portable", choices=sorted(markup.DIALECTS))
    s.add_argument("--to", default="portable", choices=sorted(markup.DIALECTS)); s.add_argument("--out")
    s.set_defaults(func=cmd_convert)

    s = sub.add_parser("resolve", help="resolve a free-link target against a folder of pages")
    s.add_argument("folder"); s.add_argument("target"); s.add_argument("--from", dest="from", default=None)
    s.add_argument("--pages-prefix", default="")
    s.set_defaults(func=cmd_resolve)

    s = sub.add_parser("bundle", help="build a Portable Wiki Bundle from a folder or vault")
    s.add_argument("src"); s.add_argument("out"); s.add_argument("--dialect", default="obsidian", choices=sorted(markup.DIALECTS))
    s.add_argument("--name"); s.add_argument("--license"); s.add_argument("--lang", default="en")
    s.add_argument("--history", action="store_true", help="replay git history into history/*.jsonl")
    s.add_argument("--stable-ids", action="store_true", help="derive page ids from paths instead of random UUIDs")
    s.add_argument("--source-url", help="URL template for the `source` field, with {path} or {title}")
    s.set_defaults(func=cmd_bundle)

    s = sub.add_parser("unbundle", help="write a bundle out as a folder in a dialect")
    s.add_argument("bundle"); s.add_argument("out"); s.add_argument("--dialect", default="obsidian", choices=sorted(markup.DIALECTS))
    s.set_defaults(func=cmd_unbundle)

    s = sub.add_parser("okf", help="Open Knowledge Format interchange")
    s.add_argument("direction", choices=["export", "import"]); s.add_argument("src"); s.add_argument("out")
    s.add_argument("--name"); s.add_argument("--type", default="Wiki Page", help="OKF concept type for ordinary pages")
    s.set_defaults(func=cmd_okf)

    s = sub.add_parser("validate", help="validate a bundle (same as tools/validate_bundle.py)")
    s.add_argument("bundle"); s.add_argument("--quiet", action="store_true")
    s.set_defaults(func=cmd_validate)

    s = sub.add_parser("corpus", help="run or update the conformance corpus")
    s.add_argument("action", choices=["check", "update"]); s.add_argument("--corpus", default=str(ROOT / "corpus"))
    s.add_argument("-v", "--verbose", action="store_true")
    s.set_defaults(func=cmd_corpus)

    args = p.parse_args(argv)
    return args.func(args)
