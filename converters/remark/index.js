/**
 * remark-wiki-commons: a remark plugin for the Portable Wiki Markdown profile
 * (Wiki Commons guidelines, chapter 08). Optional tooling; it does not make any
 * engine conform to anything.
 *
 * Recognizes, in text nodes outside code:
 *   [[Target]], [[Target|Label]], [[Target#Heading]], [[Target#^block-id]], [[prefix:Title]]
 *   ![[Target]] embeds (pages, headings, blocks, images)
 *   trailing ^block-id tokens on paragraphs and list items
 *   > [!NOTE] callouts (GitHub alerts / Obsidian callouts)
 *
 * It produces `wikiLink`, `wikiEmbed`, and `wikiBlockId` mdast nodes carrying `data.hName`
 * and `data.hProperties`, so remark-rehype renders them without further plugins, and it
 * registers to-markdown handlers so remark-stringify writes them back as [[...]] syntax.
 *
 * Options:
 *   labelOrder:   'target-first' (default) | 'label-first'
 *   separator:    hierarchy separator used in targets (default '/')
 *   interwiki:    { prefix: 'https://host/wiki/{title}' }
 *   resolve(target, link) -> { href, exists, title } | string | null
 *                 default: href = encodeURI(target) + '.md' (+ '#anchor'); exists unknown
 *   embeds:       'link' (default: render as a link with class wiki-embed) | 'keep'
 *   callouts:     true (default) | false
 *   blockIds:     true (default) | false
 */

const WIKILINK_RE = /(?<!\\)(!?)\[\[([^\[\]\n]+?)\]\]/g;
const BLOCK_ID_RE = /(?:^|[ \t])\^([A-Za-z0-9][A-Za-z0-9_-]*)[ \t]*$/;
const CALLOUT_RE = /^\[!([A-Za-z][\w-]*)\]([+-]?)[ \t]*(.*)$/;
const IMAGE_EXT = /\.(png|jpe?g|gif|svg|webp|avif|bmp|tiff?)$/i;

export function githubAnchor(text) {
  let s = String(text).replace(/`([^`]*)`/g, '$1').replace(/!?\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/[*_~]+/g, '');
  s = s.normalize('NFC').toLowerCase();
  let out = '';
  for (const ch of s) {
    if (ch === ' ') out += '-';
    else if (ch === '-' || ch === '_' || /[\p{L}\p{N}\p{M}]/u.test(ch)) out += ch;
  }
  return out;
}

export function parseInner(inner, labelOrder = 'target-first', embed = false) {
  let targetPart = inner, label = null;
  if (inner.includes('|')) {
    const i = inner.indexOf('|');
    const a = inner.slice(0, i), b = inner.slice(i + 1);
    if (labelOrder === 'label-first') { label = a; targetPart = b; } else { targetPart = a; label = b; }
    label = label.trim() || null;
  }
  targetPart = targetPart.trim();
  let fragment = null, fragmentKind = null;
  if (targetPart.includes('#')) {
    const i = targetPart.indexOf('#');
    const frag = targetPart.slice(i + 1).trim();
    targetPart = targetPart.slice(0, i).trim();
    if (frag.startsWith('^') && frag.length > 1) { fragment = frag.slice(1); fragmentKind = 'block'; }
    else if (frag && frag !== '^') { fragment = frag; fragmentKind = 'heading'; }
  }
  let prefix = null;
  if (targetPart.includes(':') && !/^[./]/.test(targetPart)) {
    const cand = targetPart.split(':')[0];
    if (cand && !cand.includes(' ')) prefix = cand;
  }
  return { target: targetPart, label, fragment, fragmentKind, prefix, embed };
}

function defaultResolve(target, link) {
  if (!target) return { href: '', exists: true };
  return { href: encodeURI(target) + '.md', exists: undefined, title: null };
}

function visit(node, parent, index, fn) {
  const r = fn(node, parent, index);
  if (r === 'skip') return;
  if (node.children) {
    for (let i = 0; i < node.children.length; i++) {
      const before = node.children.length;
      visit(node.children[i], node, i, fn);
      i += node.children.length - before; // account for replacements
    }
  }
}

export default function remarkWikiCommons(options = {}) {
  const opts = {
    labelOrder: 'target-first', separator: '/', interwiki: {}, resolve: defaultResolve,
    embeds: 'link', callouts: true, blockIds: true, ...options,
  };
  const data = this.data();
  const toMarkdownExtensions = data.toMarkdownExtensions || (data.toMarkdownExtensions = []);
  toMarkdownExtensions.push({
    handlers: {
      wikiLink: (node) => serialize(node, opts),
      wikiEmbed: (node) => serialize(node, opts),
      wikiBlockId: (node) => ' ^' + node.value,
    },
    unsafe: [{ character: '[', inConstruct: 'phrasing', after: '\\[' }],
  });

  return (tree, file) => {
    // 1. wikilinks and embeds inside text nodes (code and inlineCode are separate node types)
    visit(tree, null, null, (node, parent, index) => {
      if (node.type === 'code' || node.type === 'inlineCode' || node.type === 'html') return 'skip';
      if (node.type !== 'text' || !parent) return;
      const pieces = [];
      let last = 0, m;
      WIKILINK_RE.lastIndex = 0;
      while ((m = WIKILINK_RE.exec(node.value)) !== null) {
        if (m.index > last) pieces.push({ type: 'text', value: node.value.slice(last, m.index) });
        pieces.push(makeNode(parseInner(m[2], opts.labelOrder, m[1] === '!'), m[0], opts, file));
        last = m.index + m[0].length;
      }
      if (!pieces.length) return;
      if (last < node.value.length) pieces.push({ type: 'text', value: node.value.slice(last) });
      parent.children.splice(index, 1, ...pieces);
    });
    // 2. trailing block identifiers
    if (opts.blockIds) {
      visit(tree, null, null, (node) => {
        if (node.type !== 'paragraph' && node.type !== 'heading') return;
        if (node.type === 'heading') return;
        const lastChild = node.children && node.children[node.children.length - 1];
        if (!lastChild || lastChild.type !== 'text') return;
        const m = BLOCK_ID_RE.exec(lastChild.value);
        if (!m) return;
        lastChild.value = lastChild.value.slice(0, m.index).replace(/[ \t]+$/, '');
        if (!lastChild.value) node.children.pop();
        node.children.push({ type: 'wikiBlockId', value: m[1], data: { hName: 'span', hProperties: { id: m[1], className: ['wiki-block-id'] } } });
        node.data = node.data || {};
        node.data.hProperties = { ...(node.data.hProperties || {}), className: ['wiki-block'] };
      });
    }
    // 3. callouts
    if (opts.callouts) {
      visit(tree, null, null, (node) => {
        if (node.type !== 'blockquote' || !node.children?.length) return;
        const first = node.children[0];
        if (first.type !== 'paragraph' || !first.children?.length || first.children[0].type !== 'text') return;
        const text = first.children[0];
        const nl = text.value.indexOf('\n');
        const firstLine = nl === -1 ? text.value : text.value.slice(0, nl);
        const m = CALLOUT_RE.exec(firstLine);
        if (!m) return;
        const type = m[1].toLowerCase();
        node.data = node.data || {};
        node.data.hName = 'div';
        node.data.hProperties = { className: ['callout', 'callout-' + type], 'data-callout': type, 'data-callout-fold': m[2] || undefined };
        const title = m[3].trim();
        text.value = nl === -1 ? '' : text.value.slice(nl + 1);
        if (!text.value) first.children.shift();
        if (!first.children.length) node.children.shift();
        node.children.unshift({ type: 'paragraph', data: { hProperties: { className: ['callout-title'] } },
          children: [{ type: 'strong', children: [{ type: 'text', value: title || m[1].toUpperCase() }] }] });
      });
    }
  };
}

function makeNode(link, raw, opts, file) {
  const isImage = IMAGE_EXT.test(link.target);
  let resolved = null;
  if (link.prefix && opts.interwiki[link.prefix]) {
    const title = link.target.slice(link.prefix.length + 1).trim();
    resolved = { href: opts.interwiki[link.prefix].replace('{title}', encodeURIComponent(title)), exists: true, interwiki: true, title };
  } else {
    const r = opts.resolve(link.target, link, file);
    resolved = typeof r === 'string' ? { href: r, exists: true } : (r || { href: null, exists: false });
  }
  let href = resolved.href || '';
  if (link.fragmentKind === 'heading') href += '#' + githubAnchor(link.fragment);
  else if (link.fragmentKind === 'block') href += '#' + link.fragment;
  const label = link.label || resolved.title || (link.target ? link.target.split(opts.separator).pop() : (link.fragment || ''));
  const className = [link.embed ? 'wiki-embed' : 'wikilink'];
  if (resolved.exists === false) className.push('wikilink-missing');
  if (resolved.interwiki) className.push('wikilink-interwiki');
  const props = { className, 'data-wiki-target': link.target || undefined };
  if (link.embed && isImage && opts.embeds !== 'keep') {
    return { type: 'wikiEmbed', link, raw, data: { hName: 'img', hProperties: { src: resolved.href || link.target, alt: link.label && !/^\d+(x\d+)?$/.test(link.label) ? link.label : link.target.split('/').pop(), className: ['wiki-embed'] } } };
  }
  const hProperties = resolved.exists === false && !link.embed ? { ...props, 'aria-label': 'page does not exist yet' } : props;
  if (href) hProperties.href = href;
  return { type: link.embed ? 'wikiEmbed' : 'wikiLink', link, raw, data: { hName: hProperties.href ? 'a' : 'span', hProperties }, children: [{ type: 'text', value: label }] };
}

function serialize(node, opts) {
  const l = node.link;
  let inner = l.target;
  if (l.fragmentKind === 'block') inner += '#^' + l.fragment;
  else if (l.fragmentKind === 'heading') inner += '#' + l.fragment;
  if (l.label) inner = opts.labelOrder === 'label-first' ? l.label + '|' + inner : inner + '|' + l.label;
  return (l.embed ? '!' : '') + '[[' + inner + ']]';
}
