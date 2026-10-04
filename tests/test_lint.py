"""Tests for the linter with suggestions (AUTH-13): never blocking, safe fixes on request."""
import tempfile
import unittest
from pathlib import Path

import helpers  # noqa: F401
from pwb.lint import lint_path, lint_text, format_text, format_json, LEVELS

BAD = ("﻿---\ntitle: Bad\nsummary: Old key\ncreated: 2026-06-01\ntags: [alpha]\nstatus: yes\n---\n"
       "# Different Title\n\n### Skipped\n\nText %%hidden%% ![](pic.png) [click here](x.md) [[Target|]] [[#^nope]] #inline\n\n"
       ":::tip\nbody\n:::\n\n<!-- wiki:snapshot kind=\"macro\" name=\"x\" -->\nPara. ^dup\n\nPara. ^dup")


class LintText(unittest.TestCase):
    def codes(self, result):
        return {f.code for f in result.findings}

    def test_findings(self):
        res, _ = lint_text(BAD, "bad.md")
        codes = self.codes(res)
        for expected in ["MKUP-19-bom", "MKUP-19-newline", "META-deprecated-key", "META-3-coerced", "META-yaml-bool",
                         "MKUP-8-h1", "A11Y-3-heading-skip", "MKUP-11-percent", "A11Y-6-alt", "A11Y-2-link-text",
                         "MKUP-4-empty-label", "MKUP-9-missing-block", "MKUP-14-tags", "MKUP-15-container",
                         "EXT-4-unclosed", "MKUP-9-duplicate"]:
            self.assertIn(expected, codes)
        self.assertTrue(all(f.guideline for f in res.findings), "every finding names its guideline")
        self.assertIn("warning(s)", format_text(res))
        self.assertIn('"findings"', format_json(res))

    def test_fix_is_safe_and_textual(self):
        res, fixed = lint_text(BAD, "bad.md", fix=True)
        self.assertTrue(fixed.startswith("---\n"))
        self.assertIn("description: Old key", fixed)
        self.assertIn('created: "2026-06-01"', fixed)
        self.assertIn('status: "yes"', fixed)           # quoting preserved, not re-dumped as `true`
        self.assertIn("tags: [alpha, inline]", fixed)
        self.assertIn("<!--hidden-->", fixed)
        self.assertIn("> [!TIP]\n> body", fixed)
        self.assertIn("[[Target]]", fixed)
        self.assertTrue(fixed.endswith("\n"))
        # unsafe things are left alone
        self.assertIn("### Skipped", fixed)
        self.assertEqual(fixed.count("^dup"), 2)
        res2, _ = lint_text(fixed, "bad.md")
        self.assertFalse({"MKUP-19-bom", "META-deprecated-key", "META-3-coerced", "META-yaml-bool",
                          "MKUP-11-percent", "MKUP-15-container", "MKUP-4-empty-label", "MKUP-14-tags"} & self.codes(res2))

    def test_clean_page_is_quiet(self):
        text = "---\ntitle: Clean\ndescription: Fine\ntags: [a]\n---\n\n## Section\n\nA paragraph with a #a tag and [[Other|a link]].\n"
        res, _ = lint_text(text, "clean.md")
        self.assertEqual([f.code for f in res.findings], [])


class LintBundle(unittest.TestCase):
    def test_example_bundle(self):
        res = lint_path(helpers.EXAMPLE_BUNDLE)
        self.assertFalse([f for f in res.findings if f.level == "warning"], [f.message for f in res.findings])
        self.assertTrue(any(f.code == "NAV-3-dangling" for f in res.findings))

    def test_folder_with_resolution_hints(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Edit Conflicts.md").write_text("---\ntitle: Edit Conflicts\n---\n\nSee [[Merge|Edit Conflicts]] and [[edit conflicts]] and [[wp:Wiki]].\n\nBlock. ^b1\n", encoding="utf-8")
            (root / "Other.md").write_text("---\ntitle: Other\n---\n\n[[Edit Conflicts#^b1]] ok, [[Edit Conflicts#^zz]] missing.\n", encoding="utf-8")
            res = lint_path(root)
            codes = {f.code for f in res.findings}
            self.assertIn("MKUP-6-order", codes)           # label resolves, target does not
            self.assertIn("MKUP-9-missing-block", codes)
            self.assertNotIn("META-2-id", codes)           # ids are only suggested inside bundles
            self.assertTrue(max(LEVELS[f.level] for f in res.findings) <= LEVELS["warning"])


if __name__ == "__main__":
    unittest.main()
