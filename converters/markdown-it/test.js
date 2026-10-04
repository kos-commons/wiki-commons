import { test } from 'node:test';
import assert from 'node:assert/strict';
import MarkdownIt from 'markdown-it';
import wikiCommons, { parseInner } from './index.js';

const pages = { 'edit conflicts': 'Edit Conflicts.md', 'guides/getting started': 'Guides/Getting Started.md' };
const resolve = (target) => pages[target.toLowerCase()] ? { href: encodeURI(pages[target.toLowerCase()]), exists: true } : { href: null, exists: false };
const md = new MarkdownIt({ html: true }).use(wikiCommons, { resolve, interwiki: { wp: 'https://en.wikipedia.org/wiki/{title}' } });

test('parseInner', () => {
  assert.deepEqual(parseInner('Label|Target#^b1', 'label-first'), { target: 'Target', label: 'Label', fragment: 'b1', fragmentKind: 'block', prefix: null, embed: false });
});

test('links', () => {
  const out = md.render('See [[Edit Conflicts|the page]], [[Guides/Getting Started#Install]], [[Missing]], and [[wp:Wiki]].');
  assert.match(out, /<a class="wikilink" data-wiki-target="Edit Conflicts" href="Edit%20Conflicts.md">the page<\/a>/);
  assert.match(out, /href="Guides\/Getting%20Started.md#install">Getting Started<\/a>/);
  assert.match(out, /<span class="wikilink wikilink-missing" data-wiki-target="Missing" aria-label="page does not exist yet">Missing<\/span>/);
  assert.match(out, /<a class="wikilink wikilink-interwiki" data-wiki-target="wp:Wiki" href="https:\/\/en.wikipedia.org\/wiki\/Wiki">Wiki<\/a>/);
});

test('code and escapes are left alone', () => {
  const out = md.render('`[[x]]` and \\[[y]] and\n\n```\n[[z]] ^id\n```\n');
  assert.doesNotMatch(out, /wikilink/);
  assert.match(out, /<code>\[\[x\]\]<\/code>/);
  assert.match(out, /\[\[y\]\]/);
});

test('embeds, images, block ids, callouts', () => {
  const out = md.render('![[Edit Conflicts#^b]] ![[diagram.png|200]]\n\nA paragraph. ^para-1\n\n- item ^item-1\n\n> [!NOTE]- Title\n> body\n');
  assert.match(out, /<a class="wiki-embed" data-wiki-target="Edit Conflicts" href="Edit%20Conflicts.md#b">Edit Conflicts<\/a>/);
  assert.match(out, /<img src="diagram.png" alt="diagram.png" class="wiki-embed">/);
  assert.match(out, /<p class="wiki-block" id="para-1">A paragraph.<span id="para-1" class="wiki-block-id"><\/span><\/p>/);
  assert.match(out, /<li class="wiki-block">item<span id="item-1" class="wiki-block-id"><\/span><\/li>/);
  assert.match(out, /<div class="callout callout-note" data-callout="note" data-callout-fold="-">/);
  assert.match(out, /<p class="callout-title"><strong>Title<\/strong><\/p>/);
  assert.match(out, /<p>body<\/p>/);
});

test('label-first option', () => {
  const lf = new MarkdownIt().use(wikiCommons, { labelOrder: 'label-first', resolve });
  assert.match(lf.render('[[the page|Edit Conflicts]]'), /href="Edit%20Conflicts.md">the page<\/a>/);
});
