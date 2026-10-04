/**
 * markdown-it-wiki-commons: a markdown-it plugin for the Portable Wiki Markdown profile
 * (Wiki Commons guidelines, chapter 08). Optional tooling.
 *
 * Recognizes [[Target]], [[Target|Label]], [[Target#Heading]], [[Target#^block-id]],
 * [[prefix:Title]], ![[...]] embeds, trailing ^block-id tokens, and > [!NOTE] callouts,
 * and renders them with the HTML conventions of MKUP-12.
 *
 * Options: labelOrder ('target-first' | 'label-first'), separator ('/'), interwiki ({prefix: url}),
 * resolve(target, link) -> {href, exists, title} | string | null, embeds ('link' | 'keep'),
 * callouts (true), blockIds (true).
 */

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

const defaultResolve = (target) => (target ? { href: encodeURI(target) + '.md', exists: undefined } : { href: '', exists: true });

export default function wikiCommonsPlugin(md, options = {}) {
  const opts = { labelOrder: 'target-first', separator: '/', interwiki: {}, resolve: defaultResolve, embeds: 'link', callouts: true, blockIds: true, ...options };

  // --- inline rule: [[...]] and ![[...]] ---
  function wikilink(state, silent) {
    const src = state.src, start = state.pos;
    let pos = start, embed = false;
    if (src.charCodeAt(pos) === 0x21 /* ! */ && src.startsWith('[[', pos + 1)) { embed = true; pos += 1; }
    if (!src.startsWith('[[', pos)) return false;
    const end = src.indexOf(']]', pos + 2);
    if (end === -1) return false;
    const inner = src.slice(pos + 2, end);
    if (!inner || /[\[\]\n]/.test(inner)) return false;
    if (!silent) {
      const token = state.push('wikilink', '', 0);
      token.meta = { link: parseInner(inner, opts.labelOrder, embed), raw: src.slice(start, end + 2) };
      token.content = inner;
    }
    state.pos = end + 2;
    return true;
  }
  md.inline.ruler.before('link', 'wikilink', wikilink);

  md.renderer.rules.wikilink = (tokens, idx) => {
    const { link } = tokens[idx].meta;
    const esc = md.utils.escapeHtml;
    const isImage = IMAGE_EXT.test(link.target);
    let resolved;
    if (link.prefix && opts.interwiki[link.prefix]) {
      const title = link.target.slice(link.prefix.length + 1).trim();
      resolved = { href: opts.interwiki[link.prefix].replace('{title}', encodeURIComponent(title)), exists: true, interwiki: true, title };
    } else {
      const r = opts.resolve(link.target, link);
      resolved = typeof r === 'string' ? { href: r, exists: true } : (r || { href: null, exists: false });
    }
    if (link.embed && isImage && opts.embeds !== 'keep') {
      const alt = link.label && !/^\d+(x\d+)?$/.test(link.label) ? link.label : link.target.split('/').pop();
      return `<img src="${esc(resolved.href || link.target)}" alt="${esc(alt)}" class="wiki-embed">`;
    }
    let href = resolved.href || '';
    if (link.fragmentKind === 'heading') href += '#' + githubAnchor(link.fragment);
    else if (link.fragmentKind === 'block') href += '#' + link.fragment;
    const label = link.label || resolved.title || (link.target ? link.target.split(opts.separator).pop() : (link.fragment || ''));
    const classes = [link.embed ? 'wiki-embed' : 'wikilink'];
    if (resolved.exists === false) classes.push('wikilink-missing');
    if (resolved.interwiki) classes.push('wikilink-interwiki');
    const target = link.target ? ` data-wiki-target="${esc(link.target)}"` : '';
    if (resolved.exists === false && !link.embed) {
      return `<span class="${classes.join(' ')}"${target} aria-label="page does not exist yet">${esc(label)}</span>`;
    }
    return `<a class="${classes.join(' ')}"${target} href="${esc(href)}">${esc(label)}</a>`;
  };

  // --- core rule: trailing ^block-id on paragraphs and list items ---
  if (opts.blockIds) {
    md.core.ruler.after('inline', 'wiki_block_id', (state) => {
      const tokens = state.tokens;
      for (let i = 0; i < tokens.length; i++) {
        const t = tokens[i];
        if (t.type !== 'inline' || !t.children || tokens[i - 1]?.type !== 'paragraph_open') continue;
        const last = t.children[t.children.length - 1];
        if (!last || last.type !== 'text') continue;
        const m = BLOCK_ID_RE.exec(last.content);
        if (!m) continue;
        last.content = last.content.slice(0, m.index).replace(/[ \t]+$/, '');
        if (!last.content) t.children.pop();
        const span = new state.Token('html_inline', '', 0);
        span.content = `<span id="${m[1]}" class="wiki-block-id"></span>`;
        t.children.push(span);
        t.content = t.content.slice(0, t.content.lastIndexOf('^' + m[1])).replace(/[ \t]+$/, '');
        const open = tokens[i - 1];
        const carrier = open.hidden ? findListItemOpen(tokens, i - 1) || open : open;
        carrier.attrJoin('class', 'wiki-block');
        if (!open.hidden) open.attrSet('id', m[1]);
      }
    });
  }

  // --- core rule: callouts ---
  if (opts.callouts) {
    md.core.ruler.after('inline', 'wiki_callout', (state) => {
      const tokens = state.tokens;
      for (let i = 0; i < tokens.length; i++) {
        if (tokens[i].type !== 'blockquote_open') continue;
        const pOpen = tokens[i + 1], inline = tokens[i + 2];
        if (!pOpen || pOpen.type !== 'paragraph_open' || !inline || inline.type !== 'inline' || !inline.children?.length) continue;
        const first = inline.children[0];
        if (first.type !== 'text') continue;
        const nl = first.content.indexOf('\n');
        const firstLine = nl === -1 ? first.content : first.content.slice(0, nl);
        const m = CALLOUT_RE.exec(firstLine);
        if (!m) continue;
        const type = m[1].toLowerCase();
        const close = findClose(tokens, i);
        tokens[i].tag = 'div';
        tokens[i].attrSet('class', `callout callout-${type}`);
        tokens[i].attrSet('data-callout', type);
        if (m[2]) tokens[i].attrSet('data-callout-fold', m[2]);
        if (close) close.tag = 'div';
        // strip the marker line from the paragraph
        first.content = nl === -1 ? '' : first.content.slice(nl + 1);
        if (!first.content) {
          inline.children.shift();
          if (inline.children[0]?.type === 'softbreak') inline.children.shift();
        }
        const removeParagraph = inline.children.length === 0;
        const title = m[3].trim() || m[1].toUpperCase();
        const tOpen = new state.Token('paragraph_open', 'p', 1); tOpen.attrSet('class', 'callout-title');
        const tInline = new state.Token('inline', '', 0); tInline.content = title;
        const sOpen = new state.Token('strong_open', 'strong', 1), sText = new state.Token('text', '', 0), sClose = new state.Token('strong_close', 'strong', -1);
        sText.content = title; tInline.children = [sOpen, sText, sClose];
        const tClose = new state.Token('paragraph_close', 'p', -1);
        const insert = [tOpen, tInline, tClose];
        if (removeParagraph) tokens.splice(i + 1, 3, ...insert); else tokens.splice(i + 1, 0, ...insert);
      }
    });
  }

  function findClose(tokens, openIndex) {
    let depth = 0;
    for (let j = openIndex; j < tokens.length; j++) {
      if (tokens[j].type === 'blockquote_open') depth++;
      if (tokens[j].type === 'blockquote_close' && --depth === 0) return tokens[j];
    }
    return null;
  }
  function findListItemOpen(tokens, fromIndex) {
    for (let j = fromIndex; j >= 0; j--) if (tokens[j].type === 'list_item_open') return tokens[j];
    return null;
  }
}
