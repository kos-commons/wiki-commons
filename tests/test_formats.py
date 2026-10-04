"""BookStack Portable ZIP and MediaWiki XML dump interchange, and the report writer."""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import yaml

from helpers import EXAMPLE_BUNDLE, TOOLS
from pwb import external
from pwb.bookstack import bookstack_to_bundle, bundle_to_bookstack
from pwb.mediawiki import bundle_to_mediawiki, mediawiki_to_bundle, builtin_wikitext_to_markdown
from pwb import markup
from pwb.report import render_report, categorize

VALIDATOR = TOOLS / "validate_bundle.py"
HAS_PANDOC = external.pandoc_available()


def validate(path: Path):
    proc = subprocess.run([sys.executable, str(VALIDATOR), str(path), "--quiet"], capture_output=True, text=True)
    return proc.returncode, proc.stdout


def write_portable_zip(path: Path) -> None:
    svg = b'<svg xmlns="http://www.w3.org/2000/svg" width="4" height="4"/>'
    data = {
        "instance": {"id": "inst-1", "version": "v26.09.1"}, "exported_at": "2026-10-04T00:00:00Z",
        "book": {"id": 8, "name": "Handbook", "description_html": "<p>Team handbook</p>", "tags": [{"name": "team", "value": ""}],
                 "chapters": [{"id": 2, "name": "Onboarding", "priority": 1, "description_html": "<p>Start here</p>", "pages": [
                     {"id": 40, "name": "First Day", "priority": 1,
                      "markdown": "Welcome! See [the setup page]([[bsexport:page:41]]) and ![diagram]([[bsexport:image:22]]).\n\nDownload [the PDF]([[bsexport:attachment:55]]).\n",
                      "tags": [{"name": "status", "value": "draft"}], "images": [{"id": 22, "name": "Diagram", "file": "abc123.png", "type": "gallery"}],
                      "attachments": [{"id": 55, "name": "Policy", "file": "doc1.pdf"}, {"id": 56, "name": "Intranet", "link": "https://intranet.example"}]},
                     {"id": 41, "name": "Setup", "priority": 2, "html": "<h2>Laptop</h2><p>Ask <a href=\"[[bsexport:page:40]]\">First Day</a> owner.</p>"}]}],
                 "pages": [{"id": 42, "name": "Index", "priority": 0, "markdown": "Links to [[bsexport:chapter:2]] and [[bsexport:book:8]].\n"}]}}
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("data.json", json.dumps(data))
        zf.writestr("files/abc123.png", svg)
        zf.writestr("files/doc1.pdf", b"%PDF-1.4 fake")


DUMP = """<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.11/" version="0.11" xml:lang="en">
  <siteinfo><sitename>Demo Wiki</sitename><base>https://demo.example.org/wiki/Main_Page</base><generator>MediaWiki 1.46.1</generator>
    <namespaces><namespace key="0" case="first-letter" /><namespace key="1" case="first-letter">Talk</namespace><namespace key="14" case="first-letter">Category</namespace></namespaces></siteinfo>
  <page><title>Edit conflicts</title><ns>0</ns><id>12</id>
    <revision><id>100</id><timestamp>2024-03-02T01:15:00Z</timestamp><contributor><username>Aiko</username><id>3</id></contributor><comment>stub</comment><origin>100</origin><model>wikitext</model><format>text/x-wiki</format><text xml:space="preserve">An '''edit conflct''' happens.</text><sha1>a</sha1></revision>
    <revision><id>101</id><parentid>100</parentid><timestamp>2024-03-05T00:02:11Z</timestamp><contributor><ip>203.0.113.7</ip></contributor><minor /><comment>typo</comment><origin>101</origin><model>wikitext</model><format>text/x-wiki</format><text xml:space="preserve">== Overview ==
An '''edit conflict''' happens when two people save.&lt;ref&gt;Leuf 2001&lt;/ref&gt; See [[Revision history|history]] and [[Glossary]].
{{Infobox|type=concept}}
* one
** nested
[[Category:Collaboration]]</text><sha1>b</sha1></revision>
  </page>
  <page><title>Editing collisions</title><ns>0</ns><id>13</id><redirect title="Edit conflicts" />
    <revision><id>102</id><timestamp>2025-01-10T12:00:00Z</timestamp><contributor><username>Aiko</username><id>3</id></contributor><origin>102</origin><model>wikitext</model><format>text/x-wiki</format><text xml:space="preserve">#REDIRECT [[Edit conflicts]]</text><sha1>c</sha1></revision>
  </page>
  <page><title>Talk:Edit conflicts</title><ns>1</ns><id>14</id>
    <revision><id>103</id><timestamp>2026-02-01T10:00:00Z</timestamp><contributor><username>Ben</username><id>4</id></contributor><origin>103</origin><model>wikitext</model><format>text/x-wiki</format><text xml:space="preserve">Should we mention merging?</text><sha1>d</sha1></revision>
  </page>
</mediawiki>
"""


class BookStackTests(unittest.TestCase):
    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            zip_path = Path(tmp) / "handbook.zip"
            write_portable_zip(zip_path)
            out = Path(tmp) / "bundle"
            report = bookstack_to_bundle(zip_path, out)
            self.assertEqual((report["pages"], report["attachments"]), (5, 2))
            self.assertEqual(validate(out)[0], 0)
            first = (out / "pages" / "Handbook" / "Onboarding" / "First Day.md").read_text(encoding="utf-8")
            fm = yaml.safe_load(first.split("---")[1])
            self.assertEqual((fm["id"], fm["tags"], fm["properties"]), ("bookstack:page:40", ["status"], {"status": "draft"}))
            self.assertIn("[[Setup|the setup page]]", first)
            self.assertIn("![diagram](../../../attachments/abc123.png)", first)
            self.assertIn("[the PDF](../../../attachments/doc1.pdf)", first)
            index_page = (out / "pages" / "Handbook" / "Index.md").read_text(encoding="utf-8")
            self.assertIn("[[Handbook/Onboarding]] and [[Handbook]]", index_page)
            book = yaml.safe_load((out / "pages" / "Handbook.md").read_text(encoding="utf-8").split("---")[1])
            self.assertEqual((book["kind"], book["description"]), ("category", "Team handbook"))
            setup = (out / "pages" / "Handbook" / "Onboarding" / "Setup.md").read_text(encoding="utf-8")
            if HAS_PANDOC:
                self.assertIn("[[First Day]]", setup)
                self.assertIn("## Laptop", setup)
            else:
                self.assertIn("format: text/html", setup)
                self.assertIn('href="First Day"', setup)
            back = Path(tmp) / "back.zip"
            report2 = bundle_to_bookstack(out, back)
            self.assertEqual(report2["chapters"], 1)
            with zipfile.ZipFile(back) as zf:
                data = json.loads(zf.read("data.json"))
                self.assertIn("files/abc123.png", zf.namelist())
            b = data["book"]
            self.assertEqual(b["name"], "Handbook")
            self.assertEqual([c["name"] for c in b["chapters"]], ["Onboarding"])
            self.assertEqual(b["chapters"][0]["description_html"], "<p>Start here</p>")
            self.assertEqual(sorted(p["name"] for p in b["chapters"][0]["pages"]), ["First Day", "Setup"])
            self.assertEqual([p["name"] for p in b["pages"]], ["Index"])
            first_day = next(p for p in b["chapters"][0]["pages"] if p["name"] == "First Day")
            self.assertEqual(first_day["tags"], [{"name": "status", "value": "draft"}])
            self.assertIn("[the setup page]([[bsexport:page:", first_day["markdown"])
            self.assertEqual(len(first_day["images"]), 1)


class MediaWikiTests(unittest.TestCase):
    def _import(self, tmp: Path, **kw):
        dump = tmp / "dump.xml"
        dump.write_text(DUMP, encoding="utf-8")
        out = tmp / "bundle"
        report = mediawiki_to_bundle(dump, out, **kw)
        return out, report

    def test_import_with_history_and_redirect(self):
        with tempfile.TemporaryDirectory() as tmp:
            out, report = self._import(Path(tmp))
            self.assertEqual(report["pages"], 3)
            self.assertEqual(validate(out)[0], 0)
            manifest = yaml.safe_load((out / "wiki-bundle.yaml").read_text(encoding="utf-8"))
            self.assertEqual(manifest["source"]["engine"], "mediawiki")
            self.assertEqual(manifest["namespaces"], ["Category", "Talk"])
            self.assertEqual(manifest["fidelity"]["level"], 3)
            page = (out / "pages" / "Edit conflicts.md").read_text(encoding="utf-8")
            fm = yaml.safe_load(page.split("---")[1])
            self.assertEqual(fm["id"], "mw:12")
            self.assertEqual(fm["aliases"], ["Editing collisions"])      # from the redirect page
            self.assertEqual(fm["tags"], ["Collaboration"])              # from [[Category:...]]
            self.assertEqual(fm["source"], "https://demo.example.org/wiki/Edit_conflicts")
            body = page.split("---\n", 2)[2]
            self.assertIn("## Overview", body)
            self.assertIn("**edit conflict**", body)
            self.assertIn("[[Revision history|history]] and [[Glossary]]", body)
            self.assertIn('<!-- wiki:snapshot kind="template" name="Infobox" engine="mediawiki" src="{{Infobox|type=concept}}" -->', body)
            self.assertIn("[^1]: Leuf 2001", body)
            self.assertIn("- one\n  - nested", body)
            redirect = yaml.safe_load((out / "pages" / "Editing collisions.md").read_text(encoding="utf-8").split("---")[1])
            self.assertEqual((redirect["kind"], redirect["redirect"]), ("redirect", "Edit conflicts"))
            talk = yaml.safe_load((out / "pages" / "Talk" / "Edit conflicts.md").read_text(encoding="utf-8").split("---")[1])
            self.assertEqual((talk["kind"], talk["about"]), ("discussion", "Edit conflicts"))
            hist = [json.loads(l) for l in (out / "history" / "mw:12.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual([r["rev"] for r in hist], ["r100", "r101"])
            self.assertEqual(hist[1]["parent"], "r100")
            self.assertTrue(hist[1]["minor"])
            self.assertTrue(hist[1]["author"]["anonymous"])
            self.assertTrue(hist[1]["author"]["label"].startswith("~ip-"))   # IP replaced by a pseudonym
            users = yaml.safe_load((out / "users.yaml").read_text(encoding="utf-8"))
            self.assertEqual(sorted(u["name"] for u in users), ["Aiko", "Ben"])

    def test_keep_ips_option(self):
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = self._import(Path(tmp), keep_ips=True)
            hist = [json.loads(l) for l in (out / "history" / "mw:12.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(hist[1]["author"]["label"], "203.0.113.7")

    def test_export_and_reimport(self):
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = self._import(Path(tmp))
            xml = Path(tmp) / "export.xml"
            report = bundle_to_mediawiki(out, xml)
            self.assertEqual(report["pages"], 3)
            text = xml.read_text(encoding="utf-8")
            self.assertIn('version="0.11"', text)
            self.assertIn("<base>https://demo.example.org/wiki/Main_Page</base>", text)
            self.assertIn('<redirect title="Edit conflicts" />', text)
            self.assertIn("[[Category:Collaboration]]", text)
            self.assertIn("<username>Aiko</username>", text)
            self.assertRegex(text, r"<sha1>[0-9a-z]{31}</sha1>")
            if HAS_PANDOC:
                self.assertIn("== Overview ==", text)
                self.assertIn("{{Infobox|type=concept}}", text)   # template call restored from its envelope
                self.assertIn("'''edit conflict'''", text)
            back = Path(tmp) / "back"
            r2 = mediawiki_to_bundle(xml, back)
            self.assertEqual(r2["pages"], 3)
            self.assertEqual(validate(back)[0], 0)
            body = (back / "pages" / "Edit conflicts.md").read_text(encoding="utf-8")
            self.assertIn("[[Revision history|history]]", body)
            if HAS_PANDOC:
                self.assertIn("## Overview", body)
                self.assertIn('name="Infobox"', body)

    def test_builtin_converter_details(self):
        notes = markup.Notes()
        out = builtin_wikitext_to_markdown("== H ==\n'''b''' ''i'' [https://x.y lbl] [[File:Pic.png|thumb|A caption]]\n# one\n## two\n{| class=\"wikitable\"\n| x\n|}\n", notes, "p.md")
        self.assertIn("## H", out)
        self.assertIn("**b** *i* [lbl](https://x.y) ![A caption](Pic.png)", out)
        self.assertIn("1. one\n  1. two", out)
        self.assertIn("```wikitext", out)
        self.assertTrue(any("table kept" in n for n in notes))


class ReportTests(unittest.TestCase):
    def test_categorize_and_render(self):
        self.assertEqual(categorize("dangling link to 'X' degraded to text"), "dangling")
        self.assertEqual(categorize("block identifier ^a removed"), "degraded")
        self.assertEqual(categorize("OKF index.md listings were not imported"), "dropped")
        text = render_report(title="T", source="s", destination="d", direction="import", summary={"pages": 3},
                             notes=["dangling link to 'X' degraded to text", "dangling link to 'X' degraded to text", "something else"],
                             fidelity={"level": 2, "degraded": [{"construct": "c", "count": 2, "how": "h"}]})
        self.assertIn("| pages | 3 |", text)
        self.assertIn("### Links left dangling (2)", text)
        self.assertIn("(×2)", text)
        self.assertIn("- c (2×): h", text)
        self.assertIn("XFER-13", text)

    def test_cli_writes_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "okf"
            subprocess.run([sys.executable, str(TOOLS / "wikicommons.py"), "okf", "export", str(EXAMPLE_BUNDLE), str(out)], check=True, capture_output=True)
            self.assertTrue((out / "export-report.md").exists())
            back = Path(tmp) / "back"
            subprocess.run([sys.executable, str(TOOLS / "wikicommons.py"), "okf", "import", str(out), str(back)], check=True, capture_output=True)
            report = (back / "import-report.md").read_text(encoding="utf-8")
            self.assertIn("| pages | 9 |", report)
            self.assertIn("Level reached:** 2", report)
            self.assertEqual(validate(back)[0], 0)   # the report file does not disturb validation
            subprocess.run([sys.executable, str(TOOLS / "wikicommons.py"), "okf", "import", str(out), str(back), "--no-report"], check=True, capture_output=True)
            self.assertFalse((back / "import-report.md").exists())


if __name__ == "__main__":
    unittest.main()
