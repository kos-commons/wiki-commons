import { test } from 'node:test';
import assert from 'node:assert/strict';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkStringify from 'remark-stringify';
import remarkRehype from 'remark-rehype';
import rehypeStringify from 'rehype-stringify';
import remarkWikiCommons, { parseInner, githubAnchor } from './index.js';

const pages = { 'edit conflicts': 'Edit Conflicts.md', 'guides/getting started': 'Guides/Getting Started.md' };
const resolve = (target) => pages[target.toLowerCase()] ? { href: encodeURI(pages[target.toLowerCase()]), exists: true } : { href: null, exists: false };

async function html(md, options = {}) {
  const file = await unified().use(remarkParse).use(remarkWikiCommons, { resolve, interwiki: { wp: 'https://en.wikipedia.org/wiki/{title}' }, ...options })
    .use(remarkRehype).use(rehypeStringify).process(md);
  return String(file);
}
async function roundtrip(md, options = {}) {
  const file = await unified().use(remarkParse).use(remarkWikiCommons, options).use(remarkStringify, { bullet: '-' }).process(md);
  return String(file);
}

test('parseInner', () => {
  assert.deepEqual(parseInner('Target|Label'), { target: 'Target', label: 'Label', fragment: null, fragmentKind: null, prefix: null, embed: false });
  assert.deepEqual(parseInner('Label|Target#^b1', 'label-first'), { target: 'Target', label: 'Label', fragment: 'b1', fragmentKind: 'block', prefix: null, embed: false });
  assert.equal(parseInner('wp:Wiki').prefix, 'wp');
  assert.equal(githubAnchor("Cunningham's Law & more"), 'cunninghams-law--more');
  assert.equal(githubAnchor('編集の競合'), '編集の競合');
});

test('links render with classes and resolution', async () => {
  const out = await html('See [[Edit Conflicts|the page]], [[Guides/Getting Started#Install]], [[Missing]], and [[wp:Wiki]].');
  assert.match(out, /<a class="wikilink" data-wiki-target="Edit Conflicts" href="Edit%20Conflicts.md">the page<\/a>/);
  assert.match(out, /href="Guides\/Getting%20Started.md#install">Getting Started<\/a>/);
  assert.match(out, /<span class="wikilink wikilink-missing" data-wiki-target="Missing" aria-label="page does not exist yet">Missing<\/span>/);
  assert.match(out, /class="wikilink wikilink-interwiki" data-wiki-target="wp:Wiki" href="https:\/\/en.wikipedia.org\/wiki\/Wiki">Wiki<\/a>/);
});

test('code is left alone', async () => {
  const out = await html('`[[x]]` and\n\n```\n[[y]] ^z\n```\n');
  assert.doesNotMatch(out, /wikilink/);
  assert.match(out, /<code>\[\[x\]\]<\/code>/);
});

test('embeds, images, block ids, callouts', async () => {
  const out = await html('![[Edit Conflicts#^b]] ![[diagram.png|200]]\n\nA paragraph. ^para-1\n\n> [!NOTE]- Title\n> body\n');
  assert.match(out, /<a class="wiki-embed" data-wiki-target="Edit Conflicts" href="Edit%20Conflicts.md#b">Edit Conflicts<\/a>/);
  assert.match(out, /<img src="diagram.png" alt="diagram.png" class="wiki-embed">/);
  assert.match(out, /<p class="wiki-block">A paragraph.<span id="para-1" class="wiki-block-id"><\/span><\/p>/);
  assert.match(out, /<div class="callout callout-note" data-callout="note" data-callout-fold="-">/);
  assert.match(out, /<p class="callout-title"><strong>Title<\/strong><\/p>/);
});

test('stringify round trip', async () => {
  const src = 'See [[Target|Label]] and ![[Page#^id]] and [[A#Head]]. ^blk\n';
  assert.equal(await roundtrip(src), src);
  assert.equal(await roundtrip('[[Label|Target]]\n', { labelOrder: 'label-first' }), '[[Label|Target]]\n');
});
