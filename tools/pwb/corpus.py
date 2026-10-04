"""Run the conformance corpus (corpus/README.md describes the case formats)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

import yaml  # type: ignore

from . import markup
from .resolve import Page, PageIndex

TOOLS = Path(__file__).resolve().parent.parent


def _load_case(case_dir: Path) -> dict:
    cfg = case_dir / "case.yaml"
    return yaml.safe_load(cfg.read_text(encoding="utf-8")) or {} if cfg.exists() else {}


def _index_from(cfg: dict) -> Optional[PageIndex]:
    if not cfg.get("pages"):
        return None
    return PageIndex([Page(p["path"], p.get("title") or Path(p["path"]).stem, p.get("aliases", []), p.get("kind", "page")) for p in cfg["pages"]],
                     namespaces=cfg.get("namespaces", []), interwiki=cfg.get("interwiki", {}), pages_prefix=cfg.get("pages_prefix", ""))


def _compare_json(actual, expected_path: Path, update: bool, results: list, label: str) -> None:
    text = json.dumps(actual, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    if update or not expected_path.exists():
        expected_path.write_text(text, encoding="utf-8")
        results.append(("updated", label, ""))
        return
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    if expected == actual:
        results.append(("pass", label, ""))
    else:
        results.append(("fail", label, _first_diff(json.dumps(expected, ensure_ascii=False, indent=2, sort_keys=False), text)))


def _compare_text(actual: str, expected_path: Path, update: bool, results: list, label: str) -> None:
    if update or not expected_path.exists():
        expected_path.write_text(actual, encoding="utf-8")
        results.append(("updated", label, ""))
        return
    expected = expected_path.read_text(encoding="utf-8")
    if expected == actual:
        results.append(("pass", label, ""))
    else:
        results.append(("fail", label, _first_diff(expected, actual)))


def _first_diff(expected: str, actual: str) -> str:
    e, a = expected.split("\n"), actual.split("\n")
    for i in range(max(len(e), len(a))):
        le = e[i] if i < len(e) else "<missing>"
        la = a[i] if i < len(a) else "<missing>"
        if le != la:
            return f"line {i + 1}: expected {le!r}, got {la!r}"
    return "contents differ"


def run_markup_cases(root: Path, update: bool, results: list) -> None:
    for case_dir in sorted(p for p in (root / "markup").iterdir() if p.is_dir()) if (root / "markup").exists() else []:
        cfg = _load_case(case_dir)
        text = (case_dir / "input.md").read_text(encoding="utf-8")
        label_order = cfg.get("label_order", "target-first")
        scan = markup.scan(text, label_order=label_order)
        _compare_json(scan, case_dir / "expected.scan.json", update, results, f"markup/{case_dir.name}: scan")
        index = _index_from(cfg)
        resolver = (lambda t, f: (lambda r: (r.path, index.title_of(r.path)) if r.path else None)(index.resolve(t, f))) if index else None
        for dst in cfg.get("convert", []):
            notes = markup.Notes()
            out = markup.convert(text, cfg.get("dialect", "portable"), dst, resolver=resolver, from_path=cfg.get("from_path"),
                                 interwiki=cfg.get("interwiki", {}), block_index=cfg.get("block_index"), notes=notes)
            if notes:
                out = out.rstrip("\n") + "\n\n<!-- degradation notes:\n" + "\n".join(f"- {n}" for n in notes) + "\n-->\n"
            _compare_text(out, case_dir / f"expected.{dst}.md", update, results, f"markup/{case_dir.name}: convert to {dst}")


def run_resolution_cases(root: Path, update: bool, results: list) -> None:
    for case_dir in sorted(p for p in (root / "resolution").iterdir() if p.is_dir()) if (root / "resolution").exists() else []:
        cfg = _load_case(case_dir)
        index = _index_from(cfg)
        text = (case_dir / "input.md").read_text(encoding="utf-8")
        scan = markup.scan(text)
        actual = []
        for link in scan["links"]:
            r = index.resolve(link["target"], cfg.get("from_path"))
            actual.append({"raw": link["raw"], "target": link["target"], **r.to_dict()})
        _compare_json({"from_path": cfg.get("from_path"), "links": actual}, case_dir / "expected.json", update, results, f"resolution/{case_dir.name}")


def run_bundle_cases(root: Path, update: bool, results: list) -> None:
    validator = TOOLS / "validate_bundle.py"
    valid = root / "bundles" / "valid"
    invalid = root / "bundles" / "invalid"
    for b in sorted(p for p in valid.iterdir() if p.is_dir()) if valid.exists() else []:
        proc = subprocess.run([sys.executable, str(validator), str(b), "--quiet"], capture_output=True, text=True)
        results.append(("pass" if proc.returncode == 0 else "fail", f"bundles/valid/{b.name}", proc.stdout.strip().split("\n")[0] if proc.returncode else ""))
    for b in sorted(p for p in invalid.iterdir() if p.is_dir()) if invalid.exists() else []:
        proc = subprocess.run([sys.executable, str(validator), str(b), "--quiet"], capture_output=True, text=True)
        expected = [l.strip() for l in (b / "expected-errors.txt").read_text(encoding="utf-8").splitlines() if l.strip()] if (b / "expected-errors.txt").exists() else []
        if proc.returncode == 0:
            results.append(("fail", f"bundles/invalid/{b.name}", "validator accepted a bundle that should be rejected"))
            continue
        missing = [e for e in expected if e not in proc.stdout]
        results.append(("pass" if not missing else "fail", f"bundles/invalid/{b.name}", f"expected message not found: {missing[0]!r}" if missing else ""))


def run(root: Path, update: bool = False) -> list[tuple[str, str, str]]:
    results: list[tuple[str, str, str]] = []
    run_markup_cases(root, update, results)
    run_resolution_cases(root, update, results)
    run_bundle_cases(root, update, results)
    return results
