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


def _write_report(args, out: Path, *, title: str, source: str, direction: str, report: dict, filename: str,
                  frontmatter: dict | None = None) -> None:
    """Write import-report.md / export-report.md beside the result unless --no-report was given (XFER-13)."""
    if getattr(args, "no_report", False):
        return
    from .report import write_report
    import yaml  # type: ignore
    fidelity = None
    manifest_path = out / "wiki-bundle.yaml"
    if manifest_path.exists():
        try:
            fidelity = (yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}).get("fidelity")
        except Exception:  # noqa: BLE001
            fidelity = None
    summary = {k: v for k, v in report.items() if k != "notes" and not isinstance(v, (list, dict))}
    path = write_report(out / filename if out.is_dir() else out.parent / filename, title=title, source=source,
                        destination=str(out), direction=direction, summary=summary, notes=report.get("notes", []), fidelity=fidelity,
                        frontmatter=frontmatter)
    report["report"] = str(path)


def cmd_bundle(args) -> int:
    from .bundle import build_bundle
    out = Path(args.out)
    report = build_bundle(Path(args.src), out, dialect=args.dialect, name=args.name, license=args.license,
                          lang=args.lang, history=args.history, id_mode="stable" if args.stable_ids else "uuid4",
                          source_url=args.source_url)
    _write_report(args, out, title=f"Export report: {args.dialect} folder to Portable Wiki Bundle", source=args.src,
                  direction="export", report=report, filename="export-report.md")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def cmd_unbundle(args) -> int:
    from .bundle import unbundle
    out = Path(args.out)
    report = unbundle(Path(args.bundle), out, dialect=args.dialect)
    _write_report(args, out, title=f"Import report: Portable Wiki Bundle to {args.dialect} folder", source=args.bundle,
                  direction="import", report=report, filename="import-report.md")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def cmd_okf(args) -> int:
    from .okf import bundle_to_okf, okf_to_bundle
    out = Path(args.out)
    if args.direction == "export":
        report = bundle_to_okf(Path(args.src), out, name=args.name, default_type=args.type)
        # inside an OKF bundle every non-reserved .md file needs a type, so the report is itself a concept
        _write_report(args, out, title="Export report: Portable Wiki Bundle to Open Knowledge Format", source=args.src,
                      direction="export", report=report, filename="export-report.md",
                      frontmatter={"type": "Export Report", "title": "Export report",
                                   "description": "What the Wiki Commons tooling degraded or dropped when writing this OKF bundle."})
    else:
        report = okf_to_bundle(Path(args.src), out, name=args.name)
        _write_report(args, out, title="Import report: Open Knowledge Format to Portable Wiki Bundle", source=args.src,
                      direction="import", report=report, filename="import-report.md")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def cmd_bookstack(args) -> int:
    from .bookstack import bookstack_to_bundle, bundle_to_bookstack
    out = Path(args.out)
    if args.direction == "import":
        report = bookstack_to_bundle(Path(args.src), out, name=args.name)
        _write_report(args, out, title="Import report: BookStack Portable ZIP to Portable Wiki Bundle", source=args.src,
                      direction="import", report=report, filename="import-report.md")
    else:
        report = bundle_to_bookstack(Path(args.src), out, name=args.name)
        _write_report(args, out, title="Export report: Portable Wiki Bundle to BookStack Portable ZIP", source=args.src,
                      direction="export", report=report, filename="export-report.md")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def cmd_mediawiki(args) -> int:
    from .mediawiki import bundle_to_mediawiki, mediawiki_to_bundle
    out = Path(args.out)
    if args.direction == "import":
        report = mediawiki_to_bundle(Path(args.src), out, name=args.name, keep_ips=args.keep_ips, history=not args.no_history)
        _write_report(args, out, title="Import report: MediaWiki XML dump to Portable Wiki Bundle", source=args.src,
                      direction="import", report=report, filename="import-report.md")
    else:
        report = bundle_to_mediawiki(Path(args.src), out, sitename=args.name, base=args.base)
        _write_report(args, out, title="Export report: Portable Wiki Bundle to MediaWiki XML dump", source=args.src,
                      direction="export", report=report, filename="export-report.md")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def cmd_lint(args) -> int:
    from .lint import LEVELS, format_json, format_text, lint_path
    result = lint_path(Path(args.path), fix=args.fix)
    print(format_json(result) if args.format == "json" else format_text(result))
    if args.fail_on:
        threshold = LEVELS[args.fail_on]
        return 1 if any(LEVELS[f.level] >= threshold for f in result.findings) else 0
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
    s.add_argument("--no-report", action="store_true", help="do not write import-report.md / export-report.md")
    s.set_defaults(func=cmd_bundle)

    s = sub.add_parser("unbundle", help="write a bundle out as a folder in a dialect")
    s.add_argument("bundle"); s.add_argument("out"); s.add_argument("--dialect", default="obsidian", choices=sorted(markup.DIALECTS))
    s.add_argument("--no-report", action="store_true", help="do not write import-report.md / export-report.md")
    s.set_defaults(func=cmd_unbundle)

    s = sub.add_parser("okf", help="Open Knowledge Format interchange")
    s.add_argument("direction", choices=["export", "import"]); s.add_argument("src"); s.add_argument("out")
    s.add_argument("--name"); s.add_argument("--type", default="Wiki Page", help="OKF concept type for ordinary pages")
    s.add_argument("--no-report", action="store_true", help="do not write import-report.md / export-report.md")
    s.set_defaults(func=cmd_okf)

    s = sub.add_parser("bookstack", help="BookStack Portable ZIP interchange")
    s.add_argument("direction", choices=["import", "export"]); s.add_argument("src", help="zip or extracted directory (import), bundle (export)")
    s.add_argument("out", help="bundle directory (import), zip file (export)"); s.add_argument("--name")
    s.add_argument("--no-report", action="store_true", help="do not write import-report.md / export-report.md")
    s.set_defaults(func=cmd_bookstack)

    s = sub.add_parser("mediawiki", help="MediaWiki XML dump interchange")
    s.add_argument("direction", choices=["import", "export"]); s.add_argument("src", help="dump .xml (import), bundle (export)")
    s.add_argument("out", help="bundle directory (import), .xml file (export)"); s.add_argument("--name", help="wiki name / sitename")
    s.add_argument("--base", help="site URL for the export's <base>")
    s.add_argument("--keep-ips", action="store_true", help="keep anonymous editors' IP addresses instead of pseudonyms")
    s.add_argument("--no-history", action="store_true", help="import only the current revision of each page")
    s.add_argument("--no-report", action="store_true")
    s.set_defaults(func=cmd_mediawiki)

    s = sub.add_parser("lint", help="suggestions for a page, a folder of pages, or a bundle (never blocking by default)")
    s.add_argument("path"); s.add_argument("--fix", action="store_true", help="apply safe fixes in place")
    s.add_argument("--format", choices=["text", "json"], default="text")
    s.add_argument("--fail-on", choices=["warning", "suggestion", "info"], default=None, help="exit 1 when findings at or above this level exist")
    s.set_defaults(func=cmd_lint)

    s = sub.add_parser("validate", help="validate a bundle (same as tools/validate_bundle.py)")
    s.add_argument("bundle"); s.add_argument("--quiet", action="store_true")
    s.set_defaults(func=cmd_validate)

    s = sub.add_parser("corpus", help="run or update the conformance corpus")
    s.add_argument("action", choices=["check", "update"]); s.add_argument("--corpus", default=str(ROOT / "corpus"))
    s.add_argument("-v", "--verbose", action="store_true")
    s.set_defaults(func=cmd_corpus)

    args = p.parse_args(argv)
    return args.func(args)
