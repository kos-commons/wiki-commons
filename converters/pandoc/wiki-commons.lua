--[=[
wiki-commons.lua: a Pandoc Lua filter for the Portable Wiki Markdown profile
(Wiki Commons guidelines, chapter 08). Optional tooling.

Read the profile with Pandoc's wikilink extension, then apply the filter:

    pandoc -f commonmark_x+wikilinks_title_after_pipe --lua-filter wiki-commons.lua input.md -t html
    pandoc -f commonmark_x+wikilinks_title_after_pipe --lua-filter wiki-commons.lua input.md -t mediawiki
    pandoc -f commonmark_x+wikilinks_title_after_pipe --lua-filter wiki-commons.lua input.md -t dokuwiki

What it does:
  * [[Target]], [[Target|Label]], [[Target#Heading]], [[Target#^block-id]], [[prefix:Title]]:
    resolves the target (see options), sets the href, adds class "wikilink" and, when the
    target is unknown, "wikilink-missing" (rendered as a span); heading fragments become
    GitHub-style anchors; block fragments become "#block-id".
  * ![[Target]] embeds (a "!" before a wikilink): image targets become images, others become
    links with class "wiki-embed".
  * A trailing "^block-id" on a paragraph wraps it in a Div with that id and class "wiki-block".
  * "> [!NOTE] Title" block quotes become Divs with classes "callout" and "callout-note".
  * When writing MediaWiki or DokuWiki, wikilinks are emitted as [[Target|Label]] so the
    free-link form survives (Pandoc's DokuWiki writer would otherwise drop unlabelled ones).

Options (metadata, e.g. -M wiki-commons-index=index.json):
  wiki-commons-index       path to a JSON object mapping lowercased titles to hrefs
  wiki-commons-interwiki   path to a JSON object mapping prefixes to URL templates with {title}
  wiki-commons-separator   hierarchy separator in targets (default "/")
  wiki-commons-extension   extension appended to unresolved targets when no index is given (default ".html")
]=]

local index, interwiki = nil, {}
local separator, extension = "/", ".html"
local FORMAT = FORMAT or ""

local function read_json(path)
  local f = io.open(path, "r")
  if not f then return nil end
  local text = f:read("a"); f:close()
  return pandoc.json.decode(text)
end

local function read_options(meta)
  local function str(v) return v and pandoc.utils.stringify(v) or nil end
  if meta["wiki-commons-index"] then index = read_json(str(meta["wiki-commons-index"])) or {} end
  if meta["wiki-commons-interwiki"] then interwiki = read_json(str(meta["wiki-commons-interwiki"])) or {} end
  separator = str(meta["wiki-commons-separator"]) or separator
  extension = str(meta["wiki-commons-extension"]) or extension
  return meta
end

local function github_anchor(text)
  text = text:gsub("`([^`]*)`", "%1"):gsub("[*_~]+", ""):lower()
  local out = {}
  for _, cp in utf8.codes(text) do
    local ch = utf8.char(cp)
    if ch == " " then out[#out + 1] = "-"
    elseif ch == "-" or ch == "_" or ch:match("[%w]") or cp > 127 then out[#out + 1] = ch end
  end
  return table.concat(out)
end

local function url_encode(s)
  return (s:gsub("[^%w%-%._~/]", function(c) return string.format("%%%02X", c:byte()) end))
end

local function parse_target(raw)
  local target, fragment, kind = raw, nil, nil
  local hash = raw:find("#", 1, true)
  if hash then
    target = raw:sub(1, hash - 1)
    local frag = raw:sub(hash + 1)
    if frag:sub(1, 1) == "^" and #frag > 1 then fragment, kind = frag:sub(2), "block"
    elseif frag ~= "" and frag ~= "^" then fragment, kind = frag, "heading" end
  end
  target = target:gsub("^%s+", ""):gsub("%s+$", "")
  local prefix = nil
  local colon = target:find(":", 1, true)
  if colon and not target:match("^[./]") then
    local cand = target:sub(1, colon - 1)
    if cand ~= "" and not cand:find(" ") then prefix = cand end
  end
  return target, fragment, kind, prefix
end

local function resolve(target, prefix)
  if prefix and interwiki[prefix] then
    local title = target:sub(#prefix + 2):gsub("^%s+", "")
    return interwiki[prefix]:gsub("{title}", url_encode(title)), true, true
  end
  if target == "" then return "", true, false end
  if index then
    local href = index[target:lower()]
    if href then return href, true, false end
    return nil, false, false
  end
  return url_encode(target) .. extension, nil, false
end

local function is_wikilink(el)
  return el and el.t == "Link" and el.classes:includes("wikilink")
end

local function emit(link, embed)
  local target, fragment, kind, prefix = parse_target(link.target)
  local label = pandoc.utils.stringify(link.content)
  local raw_label = label
  if label == link.target then raw_label = nil end
  if FORMAT == "mediawiki" or FORMAT == "dokuwiki" then
    local inner = target
    if kind == "block" then inner = inner .. "#^" .. fragment elseif kind == "heading" then inner = inner .. "#" .. fragment end
    if raw_label then inner = inner .. "|" .. raw_label end
    return pandoc.RawInline(FORMAT, (embed and "!" or "") .. "[[" .. inner .. "]]")
  end
  local is_image = target:lower():match("%.png$") or target:lower():match("%.jpe?g$") or target:lower():match("%.gif$") or target:lower():match("%.svg$") or target:lower():match("%.webp$")
  if embed and is_image then
    local alt = raw_label
    if not alt or alt:match("^%d+x?%d*$") then alt = target:match("([^/]+)$") end
    local src = (index and index[target:lower()]) or target
    return pandoc.Image({pandoc.Str(alt)}, src, "", pandoc.Attr("", {"wiki-embed"}))
  end
  local href, exists, iw = resolve(target, prefix)
  local classes = {embed and "wiki-embed" or "wikilink"}
  if exists == false then classes[#classes + 1] = "wikilink-missing" end
  if iw then classes[#classes + 1] = "wikilink-interwiki" end
  -- attributes as an ordered list so that output is deterministic (a Lua table iterated with pairs is not)
  local attrs = {{"data-wiki-target", target}}
  local shown = raw_label or (target ~= "" and target:match("([^" .. separator:gsub("%p", "%%%0") .. "]+)$") or fragment or "")
  if exists == false then
    attrs[#attrs + 1] = {"aria-label", "page does not exist yet"}
    return pandoc.Span({pandoc.Str(shown)}, pandoc.Attr("", classes, attrs))
  end
  if kind == "heading" then href = href .. "#" .. github_anchor(fragment) elseif kind == "block" then href = href .. "#" .. fragment end
  return pandoc.Link({pandoc.Str(shown)}, href, "", pandoc.Attr("", classes, attrs))
end

-- Inlines: wikilinks and "!" + wikilink embeds
function Inlines(inlines)
  local out = pandoc.Inlines({})
  local i = 1
  while i <= #inlines do
    local el = inlines[i]
    if el.t == "Str" and el.text == "!" and is_wikilink(inlines[i + 1]) then
      out:insert(emit(inlines[i + 1], true)); i = i + 2
    elseif el.t == "Str" and el.text:sub(-1) == "!" and is_wikilink(inlines[i + 1]) then
      out:insert(pandoc.Str(el.text:sub(1, -2))); out:insert(emit(inlines[i + 1], true)); i = i + 2
    elseif is_wikilink(el) then
      out:insert(emit(el, false)); i = i + 1
    else
      out:insert(el); i = i + 1
    end
  end
  return out
end

-- Blocks: trailing ^block-id on paragraphs
function Para(para)
  local last = para.content[#para.content]
  if last and last.t == "Str" then
    local id = last.text:match("^%^([%w][%w_%-]*)$")
    if id and (#para.content == 1 or para.content[#para.content - 1].t == "Space") then
      para.content:remove(#para.content)
      if #para.content > 0 and para.content[#para.content].t == "Space" then para.content:remove(#para.content) end
      if FORMAT == "mediawiki" then
        para.content:insert(pandoc.RawInline("mediawiki", '<span id="' .. id .. '"></span>'))
        return para
      elseif FORMAT == "dokuwiki" then
        return para
      end
      return pandoc.Div({para}, pandoc.Attr(id, {"wiki-block"}))
    end
  end
  return para
end

-- Blocks: callouts
function BlockQuote(bq)
  local first = bq.content[1]
  if not first or first.t ~= "Para" or #first.content == 0 then return bq end
  local head = first.content[1]
  if head.t ~= "Str" then return bq end
  local ctype, fold = head.text:match("^%[!([%a][%w_%-]*)%]([+-]?)$")
  if not ctype then return bq end
  if FORMAT == "mediawiki" or FORMAT == "dokuwiki" then return bq end
  first.content:remove(1)
  if #first.content > 0 and first.content[1].t == "Space" then first.content:remove(1) end
  -- the rest of the first line is the title
  local title = {}
  while #first.content > 0 and first.content[1].t ~= "SoftBreak" and first.content[1].t ~= "LineBreak" do
    title[#title + 1] = first.content:remove(1)
  end
  if #first.content > 0 then first.content:remove(1) end
  local blocks = pandoc.Blocks({})
  local title_text = #title > 0 and pandoc.utils.stringify(title) or ctype:upper()
  blocks:insert(pandoc.Para({pandoc.Strong({pandoc.Str(title_text)})}, pandoc.Attr("", {"callout-title"})))
  if #first.content > 0 then blocks:insert(first) end
  for i = 2, #bq.content do blocks:insert(bq.content[i]) end
  local attrs = {["data-callout"] = ctype:lower()}
  if fold ~= "" then attrs["data-callout-fold"] = fold end
  return pandoc.Div(blocks, pandoc.Attr("", {"callout", "callout-" .. ctype:lower()}, attrs))
end

return {
  { Meta = read_options },
  { Inlines = Inlines, Para = Para, BlockQuote = BlockQuote },
}
