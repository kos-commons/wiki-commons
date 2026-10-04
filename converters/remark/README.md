# remark-wiki-commons

A [remark](https://github.com/remarkjs/remark) plugin for the Portable Wiki Markdown profile of the [Wiki Commons guidelines](https://kos-commons.github.io/wiki-commons/guidelines/08-Markup_and_Syntax.html). It is optional tooling for JavaScript toolchains (Docusaurus, Astro, Gatsby, custom unified pipelines); it does not make any engine conform to anything.

It recognizes, outside code: `[[Target]]`, `[[Target|Label]]`, `[[Target#Heading]]`, `[[Target#^block-id]]`, `[[prefix:Title]]` (interwiki), `![[...]]` embeds (pages, headings, blocks, images), trailing `^block-id` tokens, and `> [!NOTE]` callouts. It produces `wikiLink`, `wikiEmbed`, and `wikiBlockId` mdast nodes with `data.hName`/`data.hProperties`, so `remark-rehype` renders them with the HTML conventions of [MKUP-12](https://kos-commons.github.io/wiki-commons/guidelines/08-Markup_and_Syntax.html#mkup-12--rendered-html-conventions) (`class="wikilink"`, `wikilink-missing`, `data-wiki-target`, `id` on identified blocks), and it registers `remark-stringify` handlers so the syntax round-trips.

```js
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkRehype from 'remark-rehype';
import rehypeStringify from 'rehype-stringify';
import remarkWikiCommons from 'remark-wiki-commons';

const pages = { 'edit conflicts': 'edit-conflicts.html' };
const html = await unified()
  .use(remarkParse)
  .use(remarkWikiCommons, {
    labelOrder: 'target-first',                      // or 'label-first' (TiddlyWiki, Gollum, GitLab, Dendron)
    interwiki: { wp: 'https://en.wikipedia.org/wiki/{title}' },
    resolve: (target) => pages[target.toLowerCase()]
      ? { href: pages[target.toLowerCase()], exists: true }
      : { href: null, exists: false },               // rendered as a span with class wikilink-missing
  })
  .use(remarkRehype)
  .use(rehypeStringify)
  .process('See [[Edit Conflicts|the page]] and [[Missing]]. ^para-1');
```

Options: `labelOrder`, `separator`, `interwiki`, `resolve(target, link, file)`, `embeds` (`'link'` renders page embeds as links with class `wiki-embed`; `'keep'` leaves image embeds as links too), `callouts`, `blockIds`.

Test: `npm install && npm test` (Node 20 or later).
