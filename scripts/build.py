import html
import re
import shutil
from pathlib import Path

import markdown
from markdown.extensions.toc import slugify_unicode
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name
from pygments.util import ClassNotFound

ROOT = Path(__file__).resolve().parent.parent
GUIDES = ROOT / "guides"
ASSETS = ROOT / "site" / "assets"
OUT = ROOT / "_site"

LABELS = {"bash": "терминал", "": "вывод"}
FLOW = ("if|elif|else|for|while|return|assert|with|try|except|finally|raise|"
        "yield|await|break|continue|pass")
KINDS = {
    "bad": '<span class="tag tag-red">Плохо</span>',
    "good": '<span class="tag tag-green">Хорошо</span>',
    "before": '<span class="tag">До</span>',
    "after": '<span class="tag">После</span>',
}
FORMATTER = HtmlFormatter(nowrap=True)
INDEX_TITLE = "Гайды к курсу"
CODES = r'<span class="codes">(?:<span[^>]*>[^<]*</span>)*</span>'

BURGER = (
    '<svg viewBox="0 0 20 20" width="20" height="20" aria-hidden="true">'
    '<path d="M3 5.5h14M3 10h14M3 14.5h14" fill="none" stroke="currentColor" '
    'stroke-width="1.75" stroke-linecap="round"/></svg>'
)
CHEVRON = (
    '<svg viewBox="0 0 16 16" width="12" height="12" aria-hidden="true">'
    '<path d="m6 3.5 4.5 4.5L6 12.5" fill="none" stroke="currentColor" '
    'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>'
    '</svg>'
)
CROSS = (
    '<svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true">'
    '<path d="M5 5l10 10M15 5 5 15" fill="none" stroke="currentColor" '
    'stroke-width="1.75" stroke-linecap="round"/></svg>'
)
ARROW = (
    '<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true">'
    '<path d="M3 8h9M8.5 4.5 12 8l-3.5 3.5" fill="none" '
    'stroke="currentColor" stroke-width="1.75" stroke-linecap="round" '
    'stroke-linejoin="round"/></svg>'
)


def plain(text):
    text = re.sub(r"`([^`]*)`", r"\1", text)
    return re.sub(r"[*_]", "", text).strip()


def split_header(md):
    lines = md.split("\n")
    title = lines[0].lstrip("# ").strip()
    i = 1
    while not lines[i].strip():
        i += 1
    lead = []
    while lines[i].strip():
        lead.append(lines[i])
        i += 1
    body = "\n".join(ln for ln in lines[i:] if ln.strip() != "---")
    return title, " ".join(lead), body


def render_code(lang, attrs, code, kind):
    title = re.search(r"title=(\S+)", attrs)
    label = title.group(1) if title else LABELS.get(lang, lang)
    try:
        lexer = get_lexer_by_name(lang) if lang else TextLexer()
    except ClassNotFound:
        lexer = TextLexer()
    hl = highlight(code.rstrip("\n"), lexer, FORMATTER).rstrip("\n")
    hl = re.sub(rf'<span class="k">({FLOW})</span>',
                r'<span class="kf">\1</span>', hl)
    window = bool(title) and "." in label and lang == "python"
    dots = ('<span class="dots" aria-hidden="true"><i></i><i></i><i></i>'
            '</span>') if window else ""
    cls = "code" + (f" code-{kind}" if kind else "")
    cls += " code-window" if window else ""
    return (
        f'<figure class="{cls} reveal"><figcaption>{dots}'
        f'{KINDS.get(kind, "")}'
        f'<span class="code-label">{html.escape(label)}</span>'
        '<button class="copy" type="button">Копировать</button>'
        f'</figcaption><pre><code>{hl}</code></pre></figure>'
    )


def render_body(body):
    blocks = []

    def grab(match):
        info = match.group(1).strip().split(None, 1)
        lang = info[0] if info else ""
        attrs = info[1] if len(info) > 1 else ""
        blocks.append([lang, attrs, match.group(2), None])
        return f"\n\nCODEBLOCK{len(blocks) - 1}X\n\n"

    body = re.sub(r"```([^\n]*)\n(.*?)```", grab, body, flags=re.S)

    def tag(kind, keep_label=False):
        def apply(match):
            blocks[int(match.group("idx"))][3] = kind
            prefix = f"{match.group('label')}\n\n" if keep_label else ""
            return f"{prefix}CODEBLOCK{match.group('idx')}X"
        return apply

    body = re.sub(r"Плохо:\s*\n+CODEBLOCK(?P<idx>\d+)X", tag("bad"), body)
    body = re.sub(r"Хорошо:\s*\n+CODEBLOCK(?P<idx>\d+)X", tag("good"), body)
    body = re.sub(r"(?m)^До:\s*\n+CODEBLOCK(?P<idx>\d+)X", tag("before"),
                  body)
    body = re.sub(r"(?m)^(?P<label>После[^\n]*:)\s*\n+CODEBLOCK(?P<idx>\d+)X",
                  tag("after", keep_label=True), body)

    rendered = markdown.markdown(
        body,
        extensions=["tables", "toc"],
        extension_configs={"toc": {"slugify": slugify_unicode}},
    )
    rendered = re.sub(r"<p>CODEBLOCK(\d+)X</p>",
                      lambda m: render_code(*blocks[int(m.group(1))]),
                      rendered)

    def badges(match):
        pills = "".join(f'<span class="tag tag-blue">{c}</span>'
                        for c in match.group(1).split(", "))
        return f'<span class="codes">{pills}</span>'

    rendered = re.sub(r"\s\(((?:[EWF]\d{3})(?:, [EWF]\d{3})*)\)(?=</h3>)",
                      badges, rendered)
    rendered = rendered.replace("<table>", '<div class="table reveal"><table>')
    return rendered.replace("</table>", "</table></div>")


def split_sections(rendered):
    sections, toc = [], []
    for part in re.split(r"(?=<h2 )", rendered):
        if not part.strip():
            continue
        m = re.match(r'<h2 id="([^"]+)">(.*?)</h2>', part)
        sid, heading = m.group(1), m.group(2)
        eyebrow = ""
        hm = re.match(r"(Часть \d+)\. (.+)", heading)
        if hm:
            eyebrow, heading = hm.group(1), hm.group(2)
        rest = part[m.end():]
        sections.append(
            f'<section class="part" aria-labelledby="{sid}">'
            '<header class="section-head reveal">'
            + (f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else "")
            + f'<h2 id="{sid}">{heading}</h2></header>{rest}</section>'
        )
        subs = [(s, re.sub(CODES, "", t).strip()) for s, t in
                re.findall(r'<h3 id="([^"]+)">(.*?)</h3>', rest)]
        toc.append((sid, eyebrow, heading, subs))
    return "".join(sections), toc


def toc_list(toc):
    items = []
    for sid, eyebrow, heading, subs in toc:
        item = (f'<li><a href="#{sid}" class="toc-h2">'
                + (f"<span>{eyebrow}</span>" if eyebrow else "")
                + f"{heading}</a>")
        if subs:
            item += "<ol>" + "".join(f'<li><a href="#{s}">{t}</a></li>'
                                     for s, t in subs) + "</ol>"
        items.append(item + "</li>")
    return "".join(items)


def page(title, description, prefix, body, script=True):
    js = (f'<script src="{prefix}assets/guide.js" defer></script>\n'
          if script else "")
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{prefix}assets/style.css">
{js}</head>
<body>
<div class="ambient" aria-hidden="true"></div>
{body}
</body>
</html>
"""


def build_guide(path):
    title, lead, body = split_header(path.read_text(encoding="utf-8"))
    course = re.search(r"«([^»]+)»", lead)
    course = course.group(1) if course else ""
    lead_text = re.sub(r"^Курс «[^»]+»\.\s*", "", lead)
    lead_html = markdown.markdown(lead_text).replace(
        "<p>", '<p class="lead">', 1) if lead_text else ""
    sections, toc = split_sections(render_body(body))
    nav = toc_list(toc)
    short = title.split(":")[0].strip()
    crumbs = (
        '<nav class="crumbs" aria-label="Навигация по сайту"><ol>'
        f'<li><a href="../">{INDEX_TITLE}</a>'
        f'<span class="crumbs-sep">{CHEVRON}</span></li>'
        f'<li><span aria-current="page">{short}</span></li>'
        '</ol></nav>'
    )
    burger = ('<button class="burger" type="button" popovertarget="drawer" '
              f'aria-label="Открыть содержание">{BURGER}</button>')
    close = ('<button class="drawer-close" type="button" '
             'popovertarget="drawer" popovertargetaction="hide" '
             f'aria-label="Закрыть содержание">{CROSS}</button>')
    content = f"""{burger}
<aside class="drawer" id="drawer" popover aria-label="Содержание">
<div class="drawer-head">
<p class="sidebar-title">Содержание</p>
{close}
</div>
<nav><ol class="toc">{nav}</ol></nav>
</aside>
<div class="layout">
<aside class="sidebar">
<nav aria-label="Содержание">
<p class="sidebar-title">Содержание</p>
<ol class="toc">{nav}</ol>
</nav>
</aside>
<main>
<header class="hero">
{crumbs}
<h1>{title}</h1>
{lead_html}
</header>
{sections}
</main>
</div>"""
    target = OUT / path.stem / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    description = plain(lead_text) or plain(title)
    target.write_text(page(short, description, "../", content),
                      encoding="utf-8")
    return {"slug": path.stem, "title": plain(title), "course": course}


def build_index(guides):
    course = next((g["course"] for g in guides if g["course"]), "")
    items = "".join(
        f'<li><a class="guide-link" href="{g["slug"]}/">'
        f'<span class="guide-title">{html.escape(g["title"])}</span>'
        f'<span class="guide-go">{ARROW}</span></a></li>'
        for g in guides
    )
    content = f"""<div class="layout layout-single">
<main>
<header class="hero">
<p class="eyebrow">{course}</p>
<h1>{INDEX_TITLE}</h1>
</header>
<ul class="guides">{items}</ul>
</main>
</div>"""
    (OUT / "index.html").write_text(
        page(INDEX_TITLE, f"Шпаргалки к лабам курса «{course}»", "",
             content, script=False),
        encoding="utf-8",
    )


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ASSETS, OUT / "assets")
    guides = [build_guide(p) for p in sorted(GUIDES.glob("*.md"))]
    build_index(guides)
    print(f"{len(guides)} guide(s) -> {OUT}")


if __name__ == "__main__":
    main()
