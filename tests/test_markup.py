import unittest

from helpers import ROOT  # noqa: F401
from pwb import markup


class ScanTests(unittest.TestCase):
    def test_links_and_fragments(self):
        s = markup.scan("See [[A|lbl]] [[B#Head]] [[C#^blk]] ![[D]] [[wp:X]] and `[[code]]`.")
        targets = [(l["target"], l["label"], l["fragment"], l["fragment_kind"], l["prefix"], l["embed"]) for l in s["links"]]
        self.assertEqual(targets, [("A", "lbl", None, None, None, False), ("B", None, "Head", "heading", None, False),
                                   ("C", None, "blk", "block", None, False), ("D", None, None, None, None, True),
                                   ("wp:X", None, None, None, "wp", False)])

    def test_label_first_parsing(self):
        s = markup.scan("[[shown|Target]]", label_order="label-first")
        self.assertEqual((s["links"][0]["target"], s["links"][0]["label"]), ("Target", "shown"))

    def test_code_fences_and_comments_are_ignored(self):
        text = "```\n[[x]] ^id\n```\n<!-- [[y]] -->\n[[z]] ^real\n"
        s = markup.scan(text)
        self.assertEqual([l["target"] for l in s["links"]], ["z"])
        self.assertEqual([b["id"] for b in s["block_ids"]], ["real"])

    def test_headings_anchors_github_style(self):
        s = markup.scan("## 2.1 Numbered\n## Merging\n## Merging\n## Cunningham's Law & more\n## 編集の競合\n")
        self.assertEqual([h["anchor"] for h in s["headings"]], ["21-numbered", "merging", "merging-1", "cunninghams-law--more", "編集の競合"])

    def test_tags(self):
        s = markup.scan("---\ntags: [a]\n---\n#one #漢字 not #1, C#sharp, https://x/#f, #+BEGIN_TIP, (#paren) #end.\n# Heading\n")
        self.assertEqual(s["tags"], {"frontmatter": ["a"], "inline": ["one", "漢字", "paren", "end"]})

    def test_callouts_directives_envelopes(self):
        text = ("> [!tip]- Title\n> body\n\n::: toc depth=2\n:::\n\nInline :kbd[Ctrl]{}\n\n"
                "<!-- wiki:snapshot kind=\"macro\" name=\"toc\" -->\n- x\n<!-- /wiki:snapshot -->\n<!-- wiki:props {\"a\": 1} -->\n")
        s = markup.scan(text)
        self.assertEqual(s["callouts"][0], {"line": 1, "type": "TIP", "fold": "-", "title": "Title"})
        self.assertEqual([d["name"] for d in s["directives"]], ["toc", "kbd"])
        self.assertEqual(s["envelopes"][0]["name"], "toc")
        self.assertEqual(s["envelopes"][0]["body"], "- x")
        self.assertEqual(s["props"][0]["props"], {"a": 1})

    def test_frontmatter_date_coercion_is_visible(self):
        s = markup.scan("---\nd: 2026-06-01\nq: \"2026-06-01\"\n---\n")
        self.assertEqual(s["frontmatter"]["d"], {"$type": "date", "iso": "2026-06-01"})
        self.assertEqual(s["frontmatter"]["q"], "2026-06-01")


class ConvertTests(unittest.TestCase):
    def test_label_order_flip_and_separator(self):
        out = markup.convert("[[Guides/Start|Begin]] [[A]]", "portable", "dendron")
        self.assertEqual(out, "[[Begin|Guides.Start]] [[A]]")
        back = markup.convert(out, "dendron", "portable")
        self.assertEqual(back, "[[Guides/Start|Begin]] [[A]]")

    def test_gollum_round_trip(self):
        src = "[[Target|Label]] [[Only]]"
        self.assertEqual(markup.convert(markup.convert(src, "portable", "gollum"), "gollum", "portable"), src)

    def test_static_links(self):
        pages = {"target": ("Target.md", "The Target"), "deep": ("ns/Deep.md", "Deep")}
        res = lambda t, f: pages.get(t.lower())
        out = markup.convert("[[Target]] [[Deep|d]] [[Target#Sec One]] [[Missing]] [[Target#^b]] ^id", "portable", "static",
                             resolver=res, from_path="ns/Here.md", notes=(n := markup.Notes()))
        self.assertEqual(out, "[The Target](../Target.md) [d](Deep.md) [The Target](../Target.md#sec-one) Missing [The Target](../Target.md)")
        self.assertIn("dangling link to 'Missing' degraded to text", n)
        self.assertIn("block identifier ^id removed", n)

    def test_absolute_static_links(self):
        out = markup.convert("[[Target]]", "portable", "static", resolver=lambda t, f: ("Target.md", "T"), from_path="a/b.md", absolute_links=True)
        self.assertEqual(out, "[T](/Target.md)")

    def test_interwiki_static(self):
        out = markup.convert("[[wp:Edit conflict|art]]", "portable", "static", interwiki={"wp": "https://en.wikipedia.org/wiki/{title}"})
        self.assertEqual(out, "[art](https://en.wikipedia.org/wiki/Edit%20conflict)")

    def test_obsidian_to_portable_and_back(self):
        src = "Text %%c%% ![[img.png|200]] [[N|x]]"
        out = markup.convert(src, "obsidian", "portable")
        self.assertEqual(out, "Text <!--c--> ![img.png](img.png) [[N|x]]")
        self.assertEqual(markup.convert(out, "portable", "obsidian"), "Text %%c%% ![img.png](img.png) [[N|x]]")

    def test_logseq_both_ways(self):
        idx = {"64f1a2b3-0000-4000-8000-000000000001": "Page A"}
        out = markup.convert("- A\n  id:: 64f1a2b3-0000-4000-8000-000000000001\n- ((64f1a2b3-0000-4000-8000-000000000001)) [l]([[B]])\n- #+BEGIN_TIP\n  t\n  #+END_TIP\n",
                             "logseq", "portable", block_index=idx)
        self.assertEqual(out, "- A ^64f1a2b3-0000-4000-8000-000000000001\n- [[Page A#^64f1a2b3-0000-4000-8000-000000000001]] [[B|l]]\n- > [!TIP]\n  > t\n")
        back = markup.convert("[[Page A|l]] [[Page A#^64f1a2b3-0000-4000-8000-000000000001]] ![[B]]", "portable", "logseq")
        self.assertEqual(back, "[l]([[Page A]]) ((64f1a2b3-0000-4000-8000-000000000001)) {{embed [[B]]}}")

    def test_container_to_callout(self):
        out = markup.convert(":::note Title\nBody\n:::\n", "portable", "portable")
        self.assertEqual(out, "> [!NOTE] Title\n> Body\n")

    def test_code_untouched(self):
        src = "`[[x]]` and\n```\n[[y]] ^z\n```\n"
        self.assertEqual(markup.convert(src, "portable", "static", resolver=lambda t, f: None), src)


if __name__ == "__main__":
    unittest.main()
