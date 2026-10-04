import unittest

from helpers import ROOT  # noqa: F401
from pwb.resolve import Page, PageIndex


class ResolveTests(unittest.TestCase):
    def setUp(self):
        self.idx = PageIndex([
            Page("pages/Edit Conflicts.md", "Edit Conflicts", ["Edit conflict"]),
            Page("pages/Guides/Getting Started.md", "Getting Started"),
            Page("pages/Admin/Getting Started.md", "Getting Started"),
            Page("pages/Café.md", "Café"),
        ], pages_prefix="pages", interwiki={"wp": "https://en.wikipedia.org/wiki/{title}"}, namespaces=["Talk"])

    def via(self, target, frm=None):
        r = self.idx.resolve(target, frm)
        return r.path, r.via

    def test_order(self):
        self.assertEqual(self.via("Edit Conflicts"), ("pages/Edit Conflicts.md", "exact"))
        self.assertEqual(self.via("Edit conflict"), ("pages/Edit Conflicts.md", "alias"))
        self.assertEqual(self.via("edit conflicts"), ("pages/Edit Conflicts.md", "case"))
        self.assertEqual(self.via("edit_conflicts"), ("pages/Edit Conflicts.md", "normalized"))
        self.assertEqual(self.via("Guides/Getting Started"), ("pages/Guides/Getting Started.md", "exact"))
        self.assertEqual(self.via("pages/Guides/Getting Started"), ("pages/Guides/Getting Started.md", "exact"))

    def test_hierarchy_and_ambiguity(self):
        self.assertEqual(self.via("Getting Started", "pages/Guides/Intro.md"), ("pages/Guides/Getting Started.md", "exact"))
        r = self.idx.resolve("Getting Started", "pages/Home.md")
        self.assertEqual(r.via, "ambiguous")
        self.assertEqual(len(r.candidates), 2)

    def test_nfc_relative_interwiki_self(self):
        self.assertEqual(self.via("Café"), ("pages/Café.md", "exact"))
        self.assertEqual(self.via("../Edit Conflicts", "pages/Guides/Intro.md"), ("pages/Edit Conflicts.md", "relative"))
        r = self.idx.resolve("wp:Wiki")
        self.assertEqual((r.via, r.url), ("interwiki", "https://en.wikipedia.org/wiki/Wiki"))
        self.assertEqual(self.via("", "pages/X.md"), ("pages/X.md", "self"))
        self.assertEqual(self.via("Nope"), (None, "dangling"))


if __name__ == "__main__":
    unittest.main()
