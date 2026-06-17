#!/usr/bin/env python3
"""
Recreate the reference GIF exactly:
  - macOS-style title bar (traffic light dots)
  - LEFT: Cursor IDE with sidebar, file tree, editor with code typing, outline, status bar
  - RIGHT: Dark card — large white/cyan headline + gray mono bullets (STATIC)
  - No phases, no reveals — just code typing on the left, card always visible on right
  - 3 colour-theme variants
"""

from PIL import Image, ImageDraw, ImageFont
import os, re

OUT = "/home/user/write-like-me/post_assets"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1080   # square, social-ready
HALF = W // 2        # 540 — left / right split

# ── fonts ─────────────────────────────────────────────────────────────────────
def F(path, size):
    try:    return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

MONO   = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS   = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

f_ui     = F(MONO,   11)
f_ui_b   = F(MONO_B, 11)
f_code   = F(MONO,   13)
f_head   = F(SANS_B, 56)   # headline font — matches reference
f_bullet = F(MONO,   21)   # bullet font  — matches reference

# ── themes ────────────────────────────────────────────────────────────────────
THEMES = {
    "tokyo": {
        # IDE colours — Tokyo Night (matches the reference screenshot)
        "ide_bg":      "#1a1b26",
        "sidebar_bg":  "#16161e",
        "tabbar_bg":   "#13131a",
        "titlebar_bg": "#1f2335",
        "status_bg":   "#7aa2f7",
        "status_fg":   "#1a1b26",
        "gutter_bg":   "#16161e",
        "ln_fg":       "#3b4261",
        "select_bg":   "#283457",
        "text":        "#c0caf5",
        "comment":     "#565f89",
        "keyword":     "#bb9af7",
        "func":        "#7dcfff",
        "string":      "#9ece6a",
        "number":      "#ff9e64",
        "type":        "#f7768e",
        "punct":       "#89ddff",
        "dim":         "#3b4261",
        "folder":      "#e0af68",
        "tab_dot":     "#f7768e",
        # Card colours — right side (matches reference exactly)
        "card_bg":     "#0d0e17",
        "card_white":  "#ffffff",
        "card_cyan":   "#2ac3de",
        "card_body":   "#7982a9",
        "card_div":    "#2ac3de",
    },
    "dracula": {
        "ide_bg":      "#282a36",
        "sidebar_bg":  "#21222c",
        "tabbar_bg":   "#191a21",
        "titlebar_bg": "#191a21",
        "status_bg":   "#bd93f9",
        "status_fg":   "#191a21",
        "gutter_bg":   "#21222c",
        "ln_fg":       "#6272a4",
        "select_bg":   "#44475a",
        "text":        "#f8f8f2",
        "comment":     "#6272a4",
        "keyword":     "#ff79c6",
        "func":        "#50fa7b",
        "string":      "#f1fa8c",
        "number":      "#bd93f9",
        "type":        "#ffb86c",
        "punct":       "#ff79c6",
        "dim":         "#44475a",
        "folder":      "#ffb86c",
        "tab_dot":     "#ff79c6",
        "card_bg":     "#13131f",
        "card_white":  "#f8f8f2",
        "card_cyan":   "#bd93f9",
        "card_body":   "#6272a4",
        "card_div":    "#bd93f9",
    },
    "github": {
        "ide_bg":      "#0d1117",
        "sidebar_bg":  "#010409",
        "tabbar_bg":   "#010409",
        "titlebar_bg": "#010409",
        "status_bg":   "#1f6feb",
        "status_fg":   "#ffffff",
        "gutter_bg":   "#010409",
        "ln_fg":       "#30363d",
        "select_bg":   "#1c2128",
        "text":        "#e6edf3",
        "comment":     "#8b949e",
        "keyword":     "#ff7b72",
        "func":        "#79c0ff",
        "string":      "#a5d6ff",
        "number":      "#79c0ff",
        "type":        "#ffa657",
        "punct":       "#ff7b72",
        "dim":         "#30363d",
        "folder":      "#e3b341",
        "tab_dot":     "#ffa657",
        "card_bg":     "#010409",
        "card_white":  "#e6edf3",
        "card_cyan":   "#58a6ff",
        "card_body":   "#8b949e",
        "card_div":    "#58a6ff",
    },
}

# ── syntax highlighter ────────────────────────────────────────────────────────
KW = {"__global__","__shared__","__device__","__syncthreads","float","int",
      "void","auto","for","if","else","return","import","def","class","not",
      "in","double","char","True","False","None","from","with","as"}

def tokenise(line, T):
    if re.match(r'\s*(#|//)', line):
        return [(line, T["comment"])]
    pat = re.compile(
        r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'
        r'|(\b(?:' + '|'.join(re.escape(k) for k in KW) + r')\b)'
        r'|(\b\d+\.?\d*(?:e[+-]?\d+)?[fF]?\b)'
        r'|([A-Za-z_]\w*(?=\s*\())'
        r'|([^\w\s])'
        r'|(\w+)|(\s+)'
    )
    out = []
    for m in pat.finditer(line):
        s, kw, num, fn, pu, _, ws = m.groups()
        t = m.group(0)
        if ws:    c = T["text"]
        elif s:   c = T["string"]
        elif kw:  c = T["keyword"]
        elif num: c = T["number"]
        elif fn:  c = T["func"]
        elif pu:  c = T["punct"]
        else:     c = T["text"]
        out.append((t, c))
    return out or [(line, T["text"])]


# ── render the LEFT IDE half ──────────────────────────────────────────────────
#   dimensions tuned to match the reference screenshot layout
TITLE_H = 38    # macOS title bar
AB_W    = 0     # no activity bar strip (reference doesn't show one clearly)
SB_W    = 210   # sidebar width
TAB_H   = 30    # editor tab strip
STAT_H  = 22    # status bar
GUT_W   = 38    # line-number gutter
OL_H    = 190   # outline panel height
LH      = 18    # code line height
SLH     = 17    # sidebar row height

def render_left(T, filename, file_tree, code_lines, cursor_li, outline, branch, lang):
    img  = Image.new("RGB", (HALF, H), T["ide_bg"])
    draw = ImageDraw.Draw(img)

    # ── macOS title bar ──
    draw.rectangle([0, 0, HALF, TITLE_H], fill=T["titlebar_bg"])
    # traffic light dots
    draw.ellipse([ 14, 12, 26, 24], fill="#ff5f57")
    draw.ellipse([ 32, 12, 44, 24], fill="#febc2e")
    draw.ellipse([ 50, 12, 62, 24], fill="#28c840")
    # title text centred
    title = f"{filename} — write-like-me — Cursor"
    tw    = draw.textlength(title, font=f_ui)
    draw.text(((HALF - tw) / 2, (TITLE_H - 11) / 2), title,
              fill="#808080", font=f_ui)

    # ── sidebar ──
    draw.rectangle([0, TITLE_H, SB_W, H - STAT_H], fill=T["sidebar_bg"])
    draw.text((8, TITLE_H + 8), "EXPLORER", fill=T["dim"], font=f_ui_b)

    ty = TITLE_H + 26
    for ind, name, is_dir, active in file_tree:
        if ty > H - OL_H - STAT_H - 2:
            break
        if active:
            draw.rectangle([0, ty - 1, SB_W, ty + SLH], fill=T["select_bg"])
        fx  = 6 + ind * 12
        ico = "▾ " if is_dir else "  "
        col = T["folder"] if is_dir else (T["text"] if active else T["dim"])
        draw.text((fx, ty), ico + name, fill=col, font=f_ui)
        ty += SLH

    # outline panel
    OLY = H - OL_H - STAT_H
    draw.rectangle([0, OLY, SB_W, H - STAT_H], fill=T["tabbar_bg"])
    draw.line([0, OLY, SB_W, OLY], fill=T["dim"])
    draw.text((8, OLY + 5), "OUTLINE", fill=T["dim"], font=f_ui_b)
    oy = OLY + 20
    for ind, label, sec in outline:
        if oy > H - STAT_H - 2:
            break
        col = T["func"] if sec else T["comment"]
        draw.text((6 + ind * 10, oy), label, fill=col, font=f_ui)
        oy += SLH

    # ── editor ──
    EDX = SB_W
    draw.rectangle([EDX, TITLE_H, HALF, H - STAT_H], fill=T["ide_bg"])

    # tab strip
    draw.rectangle([EDX, TITLE_H, HALF, TITLE_H + TAB_H], fill=T["tabbar_bg"])
    tab_end = EDX + min(len(filename) * 8 + 36, 220)
    draw.rectangle([EDX, TITLE_H, tab_end, TITLE_H + TAB_H], fill=T["ide_bg"])
    draw.line([tab_end, TITLE_H, tab_end, TITLE_H + TAB_H], fill=T["dim"])
    draw.ellipse([EDX + 7, TITLE_H + TAB_H//2 - 5,
                  EDX + 17, TITLE_H + TAB_H//2 + 5], fill=T["tab_dot"])
    draw.text((EDX + 21, TITLE_H + (TAB_H - 11)//2),
              filename, fill=T["text"], font=f_ui)

    # gutter
    draw.rectangle([EDX, TITLE_H + TAB_H, EDX + GUT_W, H - STAT_H],
                   fill=T["gutter_bg"])

    # code lines
    CODE_X   = EDX + GUT_W
    code_top = TITLE_H + TAB_H + 4
    code_bot = H - STAT_H - OL_H
    max_vis  = (code_bot - code_top) // LH

    start = max(0, cursor_li - max_vis + 3)
    for i, line in enumerate(code_lines[start:start + max_vis]):
        ali = start + i
        cy  = code_top + i * LH
        draw.text((EDX + 2, cy), f"{ali+1:>3}", fill=T["ln_fg"], font=f_ui)
        if ali == cursor_li:
            draw.rectangle([EDX + GUT_W, cy - 1, HALF, cy + LH - 1],
                           fill=T["select_bg"])
        cx = CODE_X
        for tok, col in tokenise(line, T):
            tw = draw.textlength(tok, font=f_code)
            if cx + tw > HALF - 2:
                break
            draw.text((cx, cy), tok, fill=col, font=f_code)
            cx += tw

    # blinking cursor bar
    vi = cursor_li - start
    if 0 <= vi < max_vis and cursor_li < len(code_lines):
        cy  = code_top + vi * LH
        cx  = CODE_X + draw.textlength(code_lines[cursor_li], font=f_code)
        draw.rectangle([min(cx, HALF - 4), cy,
                        min(cx + 2, HALF - 2), cy + LH - 2], fill=T["text"])

    # ── status bar ──
    draw.rectangle([0, H - STAT_H, HALF, H], fill=T["status_bg"])
    draw.text((8, H - STAT_H + 4),
              f"  {branch}  ↑2 ↓0  {lang}  ·  UTF-8  ·  LF  ·  256 cols",
              fill=T["status_fg"], font=f_ui_b)
    draw.text((HALF - 100, H - STAT_H + 4),
              "GPU: H100 · SM96", fill=T["status_fg"], font=f_ui_b)

    return img


# ── render the RIGHT card (static, matches reference exactly) ─────────────────
def render_card(T, headline_parts, bullets):
    img  = Image.new("RGB", (HALF, H), T["card_bg"])
    draw = ImageDraw.Draw(img)

    px = 48
    cy = 105

    # headline — word-wrap at HALF - px, colour per segment
    lh = 70
    cx = px
    for text, hi in headline_parts:
        col = T["card_cyan"] if hi else T["card_white"]
        for word in text.split():
            tw = draw.textlength(word + " ", font=f_head)
            if cx + tw > HALF - px and cx > px:
                cx  = px
                cy += lh
            draw.text((cx, cy), word, fill=col, font=f_head)
            cx += tw
    cy += lh + 24

    # cyan divider — matches reference
    draw.rectangle([px, cy, px + 118, cy + 4], fill=T["card_div"])
    cy += 28

    # bullets
    for b in bullets:
        draw.text((px, cy), b, fill=T["card_body"], font=f_bullet)
        cy += 38

    return img


# ── composite ─────────────────────────────────────────────────────────────────
def compose(left_img, right_img):
    out = Image.new("RGB", (W, H))
    out.paste(left_img,  (0,    0))
    out.paste(right_img, (HALF, 0))
    return out


# ── GIF builder ───────────────────────────────────────────────────────────────
def build(T, filename, file_tree, code_lines, outline,
          headline_parts, bullets,
          branch="main", lang="CUDA"):

    card   = render_card(T, headline_parts, bullets)
    frames = []

    typed = []
    for li, line in enumerate(code_lines):
        typed.append("")
        for ci, ch in enumerate(line):
            typed[-1] += ch
            if ci % 2 == 0:          # every 2nd char to keep frame count sane
                left = render_left(T, filename, file_tree, list(typed),
                                   li, outline, branch, lang)
                frames.append((compose(left, card), 42))
        # short pause at end of each line
        for _ in range(4):
            left = render_left(T, filename, file_tree, list(typed),
                               li, outline, branch, lang)
            frames.append((compose(left, card), 70))

    # cursor blink at the end
    last = list(typed)
    last_li = len(code_lines) - 1
    for _ in range(5):
        l1 = render_left(T, filename, file_tree, last, last_li,
                         outline, branch, lang)
        l2 = render_left(T, filename, file_tree, last, -1,
                         outline, branch, lang)
        frames.append((compose(l1, card), 400))
        frames.append((compose(l2, card), 400))

    # hold final frame
    final = compose(render_left(T, filename, file_tree, last, last_li,
                                outline, branch, lang), card)
    for _ in range(35):
        frames.append((final, 100))

    return frames


def save(frames, path, colors=96):
    imgs = [f[0].quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
            for f in frames]
    durs = [f[1] for f in frames]
    imgs[0].save(path, save_all=True, append_images=imgs[1:],
                 duration=durs, loop=0, optimize=True)
    print(f"  {path}  {os.path.getsize(path)//1024} KB")


# ══════════════════════════════════════════════════════════════════════════════
#  Content (same across all 3 themes)
# ══════════════════════════════════════════════════════════════════════════════
FILE_TREE = [
    (0, "cuda-kernels-from-scratch", True,  False),
    (1, "src",                       True,  False),
    (2, "01_vector_add.cu",          False, False),
    (2, "02_matmul_naive.cu",        False, False),
    (2, "03_gemm_tiled.cu",          False, True ),
    (2, "04_softmax.cu",             False, False),
    (2, "05_flash_attention.cu",     False, False),
    (1, "bench",                     True,  False),
    (2, "bench.py",                  False, False),
    (1, "notes",                     True,  False),
    (2, "why_kernels_matter.md",     False, False),
    (0, "README.md",                 False, False),
    (0, "Makefile",                  False, False),
]

OUTLINE = [
    (0, "__global__ gemm_tiled",  True),
    (1, "↳ load A tile → smem",   False),
    (1, "↳ load B tile → smem",   False),
    (1, "↳ __syncthreads()",      False),
    (1, "↳ tile-mma accumulate",  False),
    (1, "↳ __syncthreads()",      False),
    (0, "host_launcher()",        True),
]

CODE = [
    "#define TILE 16",
    "",
    "__global__ void gemm_tiled(",
    "    float* A, float* B, float* C,",
    "    int M, int N, int K) {",
    "  __shared__ float As[TILE][TILE];",
    "  __shared__ float Bs[TILE][TILE];",
    "  int row = blockIdx.y*TILE + threadIdx.y;",
    "  int col = blockIdx.x*TILE + threadIdx.x;",
    "  float acc = 0.0f;",
    "  for (int t = 0; t < K/TILE; t++) {",
    "    As[threadIdx.y][threadIdx.x]",
    "      = A[row*K + t*TILE + threadIdx.x];",
    "    Bs[threadIdx.y][threadIdx.x]",
    "      = B[(t*TILE+threadIdx.y)*N + col];",
    "    __syncthreads();",
    "    for (int k = 0; k < TILE; k++)",
    "      acc += As[threadIdx.y][k]*Bs[k][threadIdx.x];",
    "    __syncthreads();",
    "  }",
    "  C[row*N + col] = acc;",
    "}",
]

# Right-card content — matches the reference image exactly
HEADLINE = [
    ("Every AI engineer should learn to write ", False),
    ("exactly one CUDA kernel.", True),        # cyan
]

BULLETS = [
    "→ not because you'll write them at work",
    "→ because the mental model",
    "   changes everything",
    "→ ~200 lines.  one weekend.",
    "→ you'll never look at PyTorch",
    "   the same way again",
]


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    for key, name in [("tokyo","post1.gif"),("dracula","post2.gif"),("github","post3.gif")]:
        T = THEMES[key]
        print(f"\n── {T.get('name', key)} ──")
        frames = build(T, "03_gemm_tiled.cu", FILE_TREE, CODE, OUTLINE,
                       HEADLINE, BULLETS)
        save(frames, f"{OUT}/{name}")
    print("\nDone!")
