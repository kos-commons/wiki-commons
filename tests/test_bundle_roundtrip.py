import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from helpers import EXAMPLE_BUNDLE, TOOLS
from pwb.bundle import build_bundle, unbundle
from pwb.okf import bundle_to_okf, okf_to_bundle

VALIDATOR = TOOLS / "validate_bundle.py"


def validate(path: Path):
    proc = subprocess.run([sys.executable, str(VALIDATOR), str(path), "--quiet"], capture_output=True, text=True)
    return proc.returncode, proc.stdout


def git(repo: Path, *args, author="Aiko Tanaka"):
    subprocess.run(["git", "-C", str(repo), "-c", f"user.name={author}", "-c", "user.email=x@example.org", *args],
                   check=True, capture_output=True)


class VaultRoundTrip(unittest.TestCase):
    def test_obsidian_vault_with_git_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            (vault / "Guides").mkdir(parents=True)
            (vault / "assets").mkdir()
            git(vault, "init", "-q")
            (vault / "Edit Conflicts.md").write_text("---\ntags: [history]\naliases: [Edit conflict]\n---\n# Edit Conflicts\n\nSee [[Guides/Getting Started|guide]] and [[Glossary#^opt]]. %%note%%\n\n![[pic.png|200]]\n\nPara. ^cid\n", encoding="utf-8")
            (vault / "Guides" / "Getting Started.md").write_text("---\ntitle: Getting Started\ndate: 2024-04-01\ndraft: true\n---\nRead [[Edit Conflicts]].\n", encoding="utf-8")
            (vault / "Glossary.md").write_text("- term ^opt\n", encoding="utf-8")
            (vault / "assets" / "pic.png").write_bytes(b"PNG")
            git(vault, "add", "-A"); git(vault, "commit", "-q", "-m", "Add pages")
            (vault / "Edit Conflicts.md").write_text((vault / "Edit Conflicts.md").read_text() + "More.\n", encoding="utf-8")
            git(vault, "add", "-A"); git(vault, "commit", "-q", "-m", "Expand", author="Ben")
            git(vault, "mv", "Glossary.md", "Terms.md"); git(vault, "commit", "-q", "-m", "Rename", author="Ben")

            out = Path(tmp) / "bundle"
            report = build_bundle(vault, out, dialect="obsidian", history=True, id_mode="stable", name="Test", license="CC-BY-4.0",
                                  source_url="https://wiki.example.org/{path}")
            self.assertEqual((report["pages"], report["attachments"], report["history"]), (3, 1, True))
            code, output = validate(out)
            self.assertEqual(code, 0, output)

            ec = (out / "pages" / "Edit Conflicts.md").read_text(encoding="utf-8")
            fm = yaml.safe_load(ec.split("---")[1])
            self.assertEqual(fm["title"], "Edit Conflicts")
            self.assertEqual(fm["aliases"], ["Edit conflict"])
            self.assertEqual(fm["ext"]["obsidian"], {}) if "obsidian" in fm.get("ext", {}) else None
            self.assertEqual([c["name"] for c in fm["contributors"]], ["Aiko Tanaka", "Ben"])
            self.assertEqual(fm["source"], "https://wiki.example.org/Edit%20Conflicts")
            self.assertIn("![pic.png](../attachments/assets/pic.png)", ec)
            self.assertIn("<!--note-->", ec)
            self.assertIn("Para. ^cid", ec)

            terms = yaml.safe_load((out / "pages" / "Terms.md").read_text(encoding="utf-8").split("---")[1])
            self.assertEqual(terms["aliases"], ["Glossary"])  # alias from the git rename
            hist = [json.loads(l) for l in (out / "history" / f"{terms['id']}.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual([r["type"] for r in hist], ["create", "rename", "edit"])
            self.assertEqual((hist[1]["from"], hist[1]["to"]), ("Glossary.md", "Terms.md"))
            self.assertTrue((out / "attachments" / "assets" / "pic.png.meta.yaml").exists())
            self.assertTrue((out / "users.yaml").exists())

            gs = yaml.safe_load((out / "pages" / "Guides" / "Getting Started.md").read_text(encoding="utf-8").split("---")[1])
            self.assertEqual((gs["status"], gs["created"]), ("draft", "2024-04-01"))

            # unbundle to a static site: alias makes the renamed page resolve
            static = Path(tmp) / "static"
            unbundle(out, static, dialect="static")
            text = (static / "Edit Conflicts.md").read_text(encoding="utf-8")
            self.assertIn("[guide](Guides/Getting%20Started.md)", text)
            self.assertIn("[Terms](Terms.md)", text)
            self.assertNotIn("^cid", text)
            self.assertIn("attachments/assets/pic.png", text)
            # and back to Obsidian
            obs = Path(tmp) / "obs"
            unbundle(out, obs, dialect="obsidian")
            self.assertIn("%%note%%", (obs / "Edit Conflicts.md").read_text(encoding="utf-8"))

    def test_logseq_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            graph = Path(tmp) / "graph"
            (graph / "pages").mkdir(parents=True)
            (graph / "pages" / "page a.md").write_text("title:: Page A\nalias:: Alpha, First Page\ntags:: demo\n\n- First\n  id:: 64f1a2b3-0000-4000-8000-000000000001\n- ((64f1a2b3-0000-4000-8000-000000000001)) and [l]([[page b]])\n", encoding="utf-8")
            (graph / "pages" / "page b.md").write_text("- Back to [[Alpha]]\n", encoding="utf-8")
            out = Path(tmp) / "bundle"
            build_bundle(graph, out, dialect="logseq", id_mode="stable")
            self.assertEqual(validate(out)[0], 0)
            fm_text, body = (out / "pages" / "pages" / "page a.md").read_text(encoding="utf-8").split("---\n")[1:]
            fm = yaml.safe_load(fm_text)
            self.assertEqual(fm["aliases"], ["Alpha", "First Page"])
            self.assertIn("[[Page A#^64f1a2b3-0000-4000-8000-000000000001]] and [[page b|l]]", body)
            back = Path(tmp) / "back"
            unbundle(out, back, dialect="logseq")
            text = (back / "pages" / "page a.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("title:: Page A\nalias:: Alpha, First Page\ntags:: demo\n"))
            self.assertIn("((64f1a2b3-0000-4000-8000-000000000001)) and [l]([[page b]])", text)


class OKFRoundTrip(unittest.TestCase):
    def test_example_bundle_to_okf_and_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            okf = Path(tmp) / "okf"
            report = bundle_to_okf(EXAMPLE_BUNDLE, okf)
            self.assertEqual(report["concepts"], 8)
            root_index = (okf / "index.md").read_text(encoding="utf-8")
            self.assertTrue(root_index.startswith("---\nokf_version: '0.2'\n---\n"))
            self.assertIn("* [Edit Conflicts](Edit%20Conflicts.md) - ", root_index)
            self.assertIn("* [Decisions](Decisions/) - 1 concept", root_index)
            self.assertTrue((okf / "log.md").exists())
            for f in okf.rglob("*.md"):
                if f.name in ("index.md", "log.md"):
                    continue
                fm = yaml.safe_load(f.read_text(encoding="utf-8").split("---")[1])
                self.assertTrue(fm.get("type"), f)
            ec = yaml.safe_load((okf / "Edit Conflicts.md").read_text(encoding="utf-8").split("---")[1])
            self.assertEqual(ec["type"], "Wiki Page")
            self.assertEqual(ec["generated"], {"by": "human:aiko", "at": "2026-07-14T15:50:00Z"})
            self.assertEqual(ec["verified"][0]["by"], "human:docs-team")
            body = (okf / "Edit Conflicts.md").read_text(encoding="utf-8").split("---", 2)[2]
            self.assertIn("[Glossary](/Glossary.md)", body)
            self.assertIn("](/attachments/conflict-diagram.svg)", body)
            self.assertNotIn("^conflict-ui", body)
            redirect = yaml.safe_load((okf / "Editing Collisions.md").read_text(encoding="utf-8").split("---")[1])
            self.assertEqual(redirect["type"], "Redirect")
            glossary = yaml.safe_load((okf / "Glossary.md").read_text(encoding="utf-8").split("---")[1])
            self.assertEqual((glossary["status"], glossary["wiki_status"]), ("draft", "wip"))

            back = Path(tmp) / "back"
            okf_to_bundle(okf, back, name="Example Project Wiki")
            self.assertEqual(validate(back)[0], 0)
            fm = yaml.safe_load((back / "pages" / "Edit Conflicts.md").read_text(encoding="utf-8").split("---")[1])
            self.assertEqual(fm["status"] if "status" in fm else "stable", "stable")
            self.assertEqual(fm["review"]["by"], "Docs team")
            self.assertEqual([c["name"] for c in fm["contributors"]][0], "Aiko Tanaka")
            self.assertEqual(fm["ext"]["okf"]["type"], "Wiki Page")
            back_body = (back / "pages" / "Edit Conflicts.md").read_text(encoding="utf-8")
            self.assertIn("[[Glossary]]", back_body)
            self.assertIn("](../attachments/conflict-diagram.svg)", back_body)
            g = yaml.safe_load((back / "pages" / "Glossary.md").read_text(encoding="utf-8").split("---")[1])
            self.assertEqual(g["status"], "wip")
            self.assertEqual(yaml.safe_load((back / "pages" / "Editing Collisions.md").read_text(encoding="utf-8").split("---")[1])["kind"], "redirect")


if __name__ == "__main__":
    unittest.main()
