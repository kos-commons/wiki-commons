# markdown-it-wiki-commons

A [markdown-it](https://github.com/markdown-it/markdown-it) plugin for the Portable Wiki Markdown profile of the [Wiki Commons guidelines](https://kos-commons.github.io/wiki-commons/guidelines/08-Markup_and_Syntax.html). Optional tooling for markdown-it based sites and engines (VitePress, Eleventy, Obsidian-style previewers, Docmost-like editors); it does not make any engine conform to anything.

It adds an inline rule for `[[Target]]`, `[[Target|Label]]`, `[[Target#Heading]]`, `[[Target#^block-id]]`, `[[prefix:Title]]`, and `![[...]]` embeds, and two core rules for trailing `^block-id` tokens (on paragraphs and list items) and `> [!NOTE]` callouts. Output follows [MKUP-12](https://kos-commons.github.io/wiki-commons/guidelines/08-Markup_and_Syntax.html#mkup-12--rendered-html-conventions): `class="wikilink"`, `wikilink-missing` spans with an accessible label, `data-wiki-target`, `id` on identified blocks, `div.callout.callout-<type>`.

```js
import MarkdownIt from 'markdown-it';
import wikiCommons from 'markdown-it-wiki-commons';

const pages = { 'edit conflicts': 'edit-conflicts.html' };
const md = new MarkdownIt().use(wikiCommons, {
  labelOrder: 'target-first',                        // or 'label-first'
  interwiki: { wp: 'https://en.wikipedia.org/wiki/{title}' },
  resolve: (target) => pages[target.toLowerCase()]
    ? { href: pages[target.toLowerCase()], exists: true }
    : { href: null, exists: false },
});
md.render('See [[Edit Conflicts|the page]] and [[Missing]]. ^para-1');
```

Options: `labelOrder`, `separator`, `interwiki`, `resolve(target, link)`, `embeds` (`'link'` | `'keep'`), `callouts`, `blockIds`.

Test: `npm install && npm test` (Node 20 or later).
