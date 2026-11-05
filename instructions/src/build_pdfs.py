#!/usr/bin/env python3
"""
build_pdfs.py -- turn the tutorial Markdown files in this folder into PDFs.

Usage (from anywhere):
    python build_pdfs.py            # build every *.md in this folder
    python build_pdfs.py banksys    # build just banksys.md

Needs:  pip install reportlab markdown-it-py pygments
Fonts:  Arial + Menlo from macOS (edit the paths below on another OS).

Markdown features supported: front matter (title/subtitle/project), # ## ###
headings, paragraphs, **bold**, *italic*, `code`, bullet/numbered lists, tables,
fenced code blocks, and "> **Tip:** ..." style call-out boxes (Tip, Note,
Warning, Checkpoint, Concept, Stuck?, Why).

Special code fence:  ```python include=solutions/banksys/art_styles.py::get_style_description
pulls the *tested* source of a function (or top-level variable) out of the
solutions folder, so the tutorial can never drift from working code.
  include=file.py::name            a def / class / top-level assignment
  include=file.py::LEVELS.variables   one key of a top-level dict
Add  file="art_styles.py"  to show a file-name label above a code block.
"""

import ast
import os
import re
import sys

from markdown_it import MarkdownIt
from pygments import lex
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.token import Token
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table,
                                TableStyle, XPreformatted, NextPageTemplate,
                                HRFlowable, ListFlowable, ListItem, Flowable)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.dirname(HERE)

# ---------------------------------------------------------------- fonts
FONT_DIR = "/System/Library/Fonts/Supplemental/"
pdfmetrics.registerFont(TTFont("Body", FONT_DIR + "Arial.ttf"))
pdfmetrics.registerFont(TTFont("Body-Bold", FONT_DIR + "Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("Body-Italic", FONT_DIR + "Arial Italic.ttf"))
pdfmetrics.registerFont(TTFont("Body-BoldItalic", FONT_DIR + "Arial Bold Italic.ttf"))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold",
                              italic="Body-Italic", boldItalic="Body-BoldItalic")
pdfmetrics.registerFont(TTFont("Mono", "/System/Library/Fonts/Menlo.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("Mono-Bold", "/System/Library/Fonts/Menlo.ttc", subfontIndex=1))
pdfmetrics.registerFontFamily("Mono", normal="Mono", bold="Mono-Bold",
                              italic="Mono", boldItalic="Mono-Bold")

# ---------------------------------------------------------------- palette
INK = colors.HexColor("#1f2933")
MUTED = colors.HexColor("#5f6c7b")
ACCENT = colors.HexColor("#2b59c3")
ACCENT_LIGHT = colors.HexColor("#e8eefc")
CODE_BG = colors.HexColor("#f5f6f8")
CODE_BORDER = colors.HexColor("#d9dde3")
RULE = colors.HexColor("#d9dde3")

CALLOUTS = {  # label -> (bar colour, background)
    "tip": (colors.HexColor("#2f9e6b"), colors.HexColor("#eaf7f0")),
    "note": (colors.HexColor("#2b59c3"), colors.HexColor("#eaf0fc")),
    "concept": (colors.HexColor("#7b4fc9"), colors.HexColor("#f2edfb")),
    "why": (colors.HexColor("#7b4fc9"), colors.HexColor("#f2edfb")),
    "warning": (colors.HexColor("#d9822b"), colors.HexColor("#fdf1e3")),
    "stuck?": (colors.HexColor("#d9822b"), colors.HexColor("#fdf1e3")),
    "checkpoint": (colors.HexColor("#c2384a"), colors.HexColor("#fceaed")),
}

# ---------------------------------------------------------------- styles
def S(name, **kw):
    base = dict(fontName="Body", fontSize=10.2, leading=14.6, textColor=INK,
                alignment=TA_LEFT)
    base.update(kw)
    return ParagraphStyle(name, **base)

ST = {
    "body": S("body", spaceAfter=6),
    "h1": S("h1", fontName="Body-Bold", fontSize=21, leading=26, textColor=ACCENT,
            spaceBefore=4, spaceAfter=10),
    "h2": S("h2", fontName="Body-Bold", fontSize=15, leading=19, textColor=INK,
            spaceBefore=14, spaceAfter=6, keepWithNext=1),
    "h3": S("h3", fontName="Body-Bold", fontSize=11.5, leading=15, textColor=ACCENT,
            spaceBefore=10, spaceAfter=4, keepWithNext=1),
    "step": S("step", fontName="Body-Bold", fontSize=14, leading=18,
              textColor=colors.white, leftIndent=8, spaceBefore=0, spaceAfter=0),
    "li": S("li", spaceAfter=2),
    "cell": S("cell", fontSize=9, leading=12),
    "cellh": S("cellh", fontName="Body-Bold", fontSize=9, leading=12),
    "call": S("call", fontSize=9.6, leading=13.6, spaceAfter=3),
    "callh": S("callh", fontName="Body-Bold", fontSize=8.6, leading=11,
               textColor=MUTED, spaceAfter=2),
    "file": S("file", fontName="Mono-Bold", fontSize=8, leading=10, textColor=MUTED,
              spaceBefore=4, spaceAfter=0),
    "code": ParagraphStyle("code", fontName="Mono", fontSize=7.9, leading=10.4,
                           textColor=INK, backColor=CODE_BG, borderColor=CODE_BORDER,
                           borderWidth=0.5, borderPadding=(5, 6, 5, 6), leftIndent=6,
                           rightIndent=6, spaceBefore=4, spaceAfter=9),
    "cover_t": S("cover_t", fontName="Body-Bold", fontSize=34, leading=40, textColor=ACCENT),
    "cover_s": S("cover_s", fontSize=14, leading=20, textColor=MUTED),
    "toc1": S("toc1", fontName="Body-Bold", fontSize=10.5, leading=16),
    "toc2": S("toc2", fontSize=9.5, leading=14, leftIndent=18, textColor=MUTED),
}

MAX_CODE_COLS = 98


# ---------------------------------------------------------------- code
def extract_source(spec):
    """spec = 'solutions/x.py::name' or 'solutions/x.py::DICT.key'."""
    path, _, target = spec.partition("::")
    full = os.path.join(HERE, path)
    text = open(full, encoding="utf-8").read()
    tree = ast.parse(text)
    lines = text.splitlines()
    dotted = target.split(".")
    for node in tree.body:
        name = None
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            name = node.name
        elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
        if name != dotted[0]:
            continue
        if len(dotted) == 1:
            return "\n".join(lines[node.lineno - 1:node.end_lineno])
        for k, v in zip(node.value.keys, node.value.values):
            if isinstance(k, ast.Constant) and k.value == dotted[1]:
                seg = "\n".join(lines[k.lineno - 1:v.end_lineno])
                return seg.rstrip().rstrip(",") + ","
    raise SystemExit(f"include target not found: {spec}")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


TOKEN_COLORS = [
    (Token.Comment, "#6a737d"), (Token.Keyword, "#c2185b"), (Token.Name.Builtin, "#1565c0"),
    (Token.Name.Function, "#6a1b9a"), (Token.Name.Class, "#6a1b9a"),
    (Token.Literal.String, "#2e7d32"), (Token.Literal.Number, "#e65100"),
    (Token.Operator.Word, "#c2185b"),
]


def highlight(code, lang):
    try:
        lexer = get_lexer_by_name(lang) if lang else TextLexer()
    except Exception:
        lexer = TextLexer()
    out = []
    for ttype, value in lex(code, lexer):
        color = None
        for base, c in TOKEN_COLORS:
            if ttype in base:
                color = c
                break
        v = esc(value)
        out.append(f'<font color="{color}">{v}</font>' if color and v.strip() else v)
    return "".join(out).rstrip("\n")


def wrap_long_lines(code):
    out = []
    for line in code.split("\n"):
        while len(line) > MAX_CODE_COLS:
            cut = line.rfind(" ", 0, MAX_CODE_COLS)
            if cut < 20:
                cut = MAX_CODE_COLS
            out.append(line[:cut])
            indent = len(line) - len(line.lstrip())
            line = " " * (indent + 4) + line[cut:].lstrip()
        out.append(line)
    return "\n".join(out)


def code_flowables(code, lang, filename=None):
    code = wrap_long_lines(code.rstrip("\n").replace("\t", "    "))
    flow = []
    if filename:
        flow.append(Paragraph(esc(filename), ST["file"]))
    # chunk very tall blocks so they can break across pages gracefully
    lines = code.split("\n")
    chunks = [lines[i:i + 38] for i in range(0, len(lines), 38)] or [[""]]
    for i, chunk in enumerate(chunks):
        style = ST["code"]
        flow.append(XPreformatted(highlight("\n".join(chunk), lang), style))
    # keep a short block together with its file label
    if len(lines) <= 38:
        return [KeepTogether(flow)]
    return flow


# ---------------------------------------------------------------- inline
def inline(tokens):
    out = []
    for t in tokens:
        k = t.type
        if k == "text":
            out.append(esc(t.content))
        elif k == "code_inline":
            out.append(f'<font face="Mono" size="8.6" backColor="#eef0f3">&nbsp;{esc(t.content)}&nbsp;</font>')
        elif k == "strong_open":
            out.append("<b>")
        elif k == "strong_close":
            out.append("</b>")
        elif k == "em_open":
            out.append("<i>")
        elif k == "em_close":
            out.append("</i>")
        elif k == "softbreak":
            out.append(" ")
        elif k == "hardbreak":
            out.append("<br/>")
        elif k == "link_open":
            href = dict(t.attrs).get("href", "")
            out.append(f'<link href="{esc(href)}" color="#2b59c3"><u>')
        elif k == "link_close":
            out.append("</u></link>")
        elif k == "image":
            out.append(esc(t.content))
        elif k == "html_inline":
            out.append(esc(t.content))
    return "".join(out)


# ---------------------------------------------------------------- doc
class StepBar(Flowable):
    """Coloured banner that introduces each numbered step."""

    def __init__(self, text, width):
        super().__init__()
        self.p = Paragraph(esc(text), ST["step"])
        self.w = width
        self.p.wrap(width - 16, 100)
        self.h = self.p.height + 12

    def wrap(self, aw, ah):
        return self.w, self.h

    def draw(self):
        c = self.canv
        c.setFillColor(ACCENT)
        c.roundRect(0, 0, self.w, self.h, 4, stroke=0, fill=1)
        self.p.drawOn(c, 0, 6)


class Doc(BaseDocTemplate):
    def __init__(self, filename, title, header, **kw):
        super().__init__(filename, pagesize=letter, title=title,
                         author="MITES", **kw)
        self.header = header
        w, h = letter
        m = 0.85 * inch
        frame = Frame(m, 0.8 * inch, w - 2 * m, h - 1.65 * inch, id="f",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[Frame(m, 0.8 * inch, w - 2 * m, h - 1.6 * inch, id="c")],
                         onPage=self.cover_page),
            PageTemplate(id="main", frames=[frame], onPage=self.main_page),
        ])
        self._bookmark_n = 0

    def cover_page(self, canv, doc):
        w, h = letter
        canv.saveState()
        canv.setFillColor(ACCENT)
        canv.rect(0, h - 0.45 * inch, w, 0.45 * inch, stroke=0, fill=1)
        canv.restoreState()

    def main_page(self, canv, doc):
        w, h = letter
        canv.saveState()
        canv.setFont("Body", 8)
        canv.setFillColor(MUTED)
        canv.drawString(0.85 * inch, h - 0.55 * inch, self.header)
        canv.drawRightString(w - 0.85 * inch, 0.5 * inch, f"Page {doc.page}")
        canv.setStrokeColor(RULE)
        canv.line(0.85 * inch, h - 0.62 * inch, w - 0.85 * inch, h - 0.62 * inch)
        canv.restoreState()

    def handle_documentBegin(self):
        self._bookmark_n = 0  # keys must be identical on every multiBuild pass
        super().handle_documentBegin()

    def afterFlowable(self, fl):
        if isinstance(fl, Paragraph) and getattr(fl, "_toc", None):
            level, text = fl._toc
            key = f"h{self._bookmark_n}"
            self._bookmark_n += 1
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=False)
            self.notify("TOCEntry", (level, text, self.page, key))


class Builder:
    def __init__(self, width):
        self.width = width

    # -- block rendering ---------------------------------------------------
    def render(self, tokens, i=0, stop=None, pstyle=None):
        pstyle = pstyle or ST["body"]
        flow = []
        while i < len(tokens):
            t = tokens[i]
            if stop and t.type == stop:
                return flow, i
            k = t.type
            if k == "heading_open":
                level = int(t.tag[1])
                text = inline(tokens[i + 1].children)
                plain = "".join(c.content for c in tokens[i + 1].children
                                if c.type in ("text", "code_inline"))
                if level == 1:
                    flow.append(PageBreak())
                    p = Paragraph(text, ST["h1"])
                    p._toc = (0, plain)
                    flow += [p, HRFlowable(width="100%", color=RULE, thickness=0.8,
                                           spaceAfter=8)]
                elif level == 2 and re.match(r"^Step \d+", plain):
                    if not (flow and isinstance(flow[-1], HRFlowable)):
                        flow.append(PageBreak())  # not right after a section title
                    bar = StepBar(plain, self.width)
                    bar_wrap = KeepTogether([bar])
                    marker = Paragraph("", ST["body"])
                    marker._toc = (1, plain)
                    flow += [bar_wrap, marker, Spacer(1, 6)]
                elif level == 2:
                    p = Paragraph(text, ST["h2"])
                    p._toc = (1, plain)
                    flow.append(p)
                else:
                    flow.append(Paragraph(text, ST["h3"]))
                i += 3
            elif k == "paragraph_open":
                flow.append(Paragraph(inline(tokens[i + 1].children), pstyle))
                i += 3
            elif k == "fence":
                info = t.info.strip()
                lang = info.split()[0] if info else ""
                code = t.content
                filename = None
                m = re.search(r'file="([^"]+)"', info)
                if m:
                    filename = m.group(1)
                m = re.search(r"include=(\S+)", info)
                if m:
                    code = extract_source(m.group(1))
                flow += code_flowables(code, lang, filename)
                i += 1
            elif k in ("bullet_list_open", "ordered_list_open"):
                items, i = self.render_list(tokens, i, k)
                flow.append(items)
            elif k == "blockquote_open":
                inner, j = self.render(tokens, i + 1, stop="blockquote_close", pstyle=ST["call"])
                flow.append(self.callout(inner))
                i = j + 1
            elif k == "table_open":
                tbl, i = self.render_table(tokens, i)
                flow.extend(tbl)
            elif k == "hr":
                flow.append(HRFlowable(width="100%", color=RULE, spaceBefore=6, spaceAfter=6))
                i += 1
            else:
                i += 1
        return flow, i

    def render_list(self, tokens, i, open_type):
        ordered = open_type == "ordered_list_open"
        close = open_type.replace("open", "close")
        start = int(dict(tokens[i].attrs).get("start", 1)) if ordered else 1
        i += 1
        items = []
        while tokens[i].type != close:
            if tokens[i].type == "list_item_open":
                inner, j = self.render(tokens, i + 1, stop="list_item_close", pstyle=ST["li"])
                if not inner:
                    inner = [Paragraph("", ST["li"])]
                items.append(ListItem(inner, leftIndent=18))
                i = j + 1
            else:
                i += 1
        lf = ListFlowable(items, bulletType="1" if ordered else "bullet", start=start if ordered else "•",
                          bulletFontName="Body-Bold" if ordered else "Body",
                          bulletFontSize=9.5, leftIndent=18, bulletColor=ACCENT,
                          bulletFormat="%s." if ordered else None)
        return lf, i + 1

    def render_table(self, tokens, i):
        rows, row, header_rows = [], [], 0
        i += 1
        while tokens[i].type != "table_close":
            t = tokens[i]
            if t.type == "tr_open":
                row = []
            elif t.type in ("th_open", "td_open"):
                is_h = t.type == "th_open"
                cell = Paragraph(inline(tokens[i + 1].children), ST["cellh" if is_h else "cell"])
                row.append(cell)
                i += 2
            elif t.type == "tr_close":
                rows.append(row)
            elif t.type == "thead_close":
                header_rows = len(rows)
            i += 1
        ncol = max(len(r) for r in rows)
        total = self.width
        weights = [0] * ncol
        for r in rows:
            for c, cell in enumerate(r):
                plain = re.sub(r"<[^>]+>", "", cell.text).replace("&nbsp;", " ")
                longest_word = max([len(w) for w in plain.split()] or [1])
                weights[c] = max(weights[c], min(max(len(plain), longest_word + 4), 70))
        weights = [max(w, 8) ** 0.8 for w in weights]
        widths = [total * w / sum(weights) for w in weights]
        tbl = Table(rows, colWidths=widths, repeatRows=header_rows)
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, header_rows - 1), ACCENT_LIGHT),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ]))
        return [Spacer(1, 2), tbl, Spacer(1, 8)], i + 1

    def callout(self, inner):
        label, (bar, bg) = "Note", CALLOUTS["note"]
        body = []
        for n, f in enumerate(inner):
            if n == 0 and isinstance(f, Paragraph):
                m = re.match(r"^<b>([^<]+?):?</b>:?\s*", f.text)
                if m and m.group(1).strip().lower().rstrip(":") in CALLOUTS:
                    label = m.group(1).strip().rstrip(":")
                    bar, bg = CALLOUTS[label.lower()]
                    f = Paragraph(f.text[m.end():], ST["call"])
            body.append(f)
        cell = [Paragraph(esc(label.upper()), ST["callh"])] + body
        t = Table([[cell]], colWidths=[self.width])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), bg),
            ("LINEBEFORE", (0, 0), (0, -1), 3, bar),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        return KeepTogether([Spacer(1, 2), t, Spacer(1, 8)])


def parse_front_matter(text):
    meta = {}
    if text.startswith("---"):
        _, fm, rest = text.split("---", 2)
        for line in fm.strip().splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
        text = rest
    return meta, text


def build(md_path):
    text = open(md_path, encoding="utf-8").read()
    meta, body = parse_front_matter(text)
    name = os.path.splitext(os.path.basename(md_path))[0]
    if os.path.basename(os.path.dirname(md_path)) == "answer_key":
        out = os.path.join(OUT_DIR, "answer_key", f"{name}_answer_key.pdf")
    else:
        out = os.path.join(OUT_DIR, f"{name}_instructions.pdf")
    doc = Doc(out, meta.get("title", name), meta.get("project", name))
    width = letter[0] - 2 * 0.85 * inch

    md = MarkdownIt("commonmark").enable("table")
    tokens = md.parse(body)
    flow, _ = Builder(width).render(tokens)

    story = [Spacer(1, 1.6 * inch),
             Paragraph(esc(meta.get("title", name)), ST["cover_t"]), Spacer(1, 10),
             Paragraph(esc(meta.get("subtitle", "")), ST["cover_s"]), Spacer(1, 30),
             HRFlowable(width="40%", color=ACCENT, thickness=2, hAlign="LEFT"),
             Spacer(1, 14),
             Paragraph("Student tutorial: follow the steps in order and build the project as you read.",
                       ST["cover_s"]),
             NextPageTemplate("main"), PageBreak()]
    toc = TableOfContents()
    toc.levelStyles = [ST["toc1"], ST["toc2"]]
    toc.dotsMinLevel = 0
    story += [Paragraph("Contents", ST["h1"]),
              HRFlowable(width="100%", color=RULE, thickness=0.8, spaceAfter=8), toc]
    # the first '# ' heading emits its own PageBreak, which we want after the TOC
    story += flow
    doc.multiBuild(story)
    print("wrote", out)
    return out


if __name__ == "__main__":
    wanted = sys.argv[1:]
    for sub in ("", "answer_key"):  # student tutorials, then teacher answer keys
        folder = os.path.join(HERE, sub)
        for fn in sorted(os.listdir(folder)):
            if fn.endswith(".md") and (not wanted or fn[:-3] in wanted or sub in wanted):
                build(os.path.join(folder, fn))
