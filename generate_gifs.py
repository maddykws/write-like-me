#!/usr/bin/env python3
"""
Exact match to reference GIF screenshots:

Phase 1 : Split view  — IDE (left half) + Post card (right half), static, ~2 s
Phase 2 : Full-width IDE — code types in line by line
Phase 3 : Cyan-bordered overlay box appears over the code:
            "AFTER YOU WRITE IT, YOU UNDERSTAND:" (cyan)
            ✓ bullets (yellow)
            CTA question (yellow)
            hashtags (cyan)

3 colour themes: Tokyo Night, Dracula, GitHub Dark
"""

from PIL import Image, ImageDraw, ImageFont
import os, re

OUT = "/home/user/write-like-me/post_assets"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1080
HALF = W // 2

# ── fonts ─────────────────────────────────────────────────────────────────────
def F(path, size):
    try:    return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

MONO   = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# split-view card fonts
f_head   = F(SANS_B, 56)
f_bullet = F(MONO,   21)

# full-width IDE fonts — slightly larger to match screenshots
f_code   = F(MONO,   15)
f_ui     = F(MONO,   11)
f_ui_b   = F(MONO_B, 11)

# overlay box fonts
f_ov_h   = F(MONO_B, 16)   # "AFTER YOU WRITE IT…"
f_ov_b   = F(MONO,   15)   # bullets / CTA / hashtags

# ── themes ────────────────────────────────────────────────────────────────────
THEMES = {
    "tokyo": {
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
        # card (split view right half)
        "card_bg":     "#0d0e17",
        "card_white":  "#ffffff",
        "card_cyan":   "#2ac3de",
        "card_body":   "#7982a9",
        "card_div":    "#2ac3de",
        # overlay box
        "ov_border":   "#2ac3de",
        "ov_bg":       "#1a1b26",
        "ov_head":     "#2ac3de",
        "ov_check":    "#e0af68",
        "ov_cta":      "#e0af68",
        "ov_hash":     "#2ac3de",
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
        "ov_border":   "#bd93f9",
        "ov_bg":       "#282a36",
        "ov_head":     "#bd93f9",
        "ov_check":    "#ffb86c",
        "ov_cta":      "#ffb86c",
        "ov_hash":     "#bd93f9",
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
        "ov_border":   "#58a6ff",
        "ov_bg":       "#0d1117",
        "ov_head":     "#58a6ff",
        "ov_check":    "#e3b341",
        "ov_cta":      "#e3b341",
        "ov_hash":     "#58a6ff",
    },
}

# ── syntax highlighter ────────────────────────────────────────────────────────
KW = {"__global__","__shared__","__device__","__syncthreads","float","int",
      "void","auto","for","if","else","return","const","double","char",
      "include","define","pragma","unsigned","short","long"}

def tokenise(line, T):
    if re.match(r'\s*(//)', line):
        return [(line, T["comment"])]
    if re.match(r'\s*#\s*(include|define|pragma)', line):
        # keep # as keyword colour, rest as text/string
        parts = []
        m = re.match(r'(\s*#\s*\w+)(.*)', line)
        if m:
            parts.append((m.group(1), T["keyword"]))
            rest = m.group(2)
            if rest:
                parts.append((rest, T["string"] if "<" in rest or '"' in rest
                               else T["number"] if rest.strip().isdigit()
                               else T["text"]))
            return parts
    pat = re.compile(
        r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|<[^>]+>)'
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


# ── shared content ────────────────────────────────────────────────────────────
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

# Exact code from reference screenshots
CODE = [
    "// tiny GEMM with shared-memory tiling — your starter kernel",
    "// goal: 200 lines, weekend project, changes how you think.",
    "",
    "#include <cuda_runtime.h>",
    "",
    "#define BM 128",
    "#define BN 128",
    "#define BK 16",
    "",
    "__global__ void gemm_tiled(const float* A,",
    "                           const float* B,  float* C,",
    "                           int M, int N, int K) {",
    "  __shared__ float As[BM][BK];",
    "  __shared__ float Bs[BK][BN];",
    "",
    "  int tx = threadIdx.x, ty = threadIdx.y;",
    "  int row = blockIdx.y*BM + ty;",
    "  int col = blockIdx.x*BN + tx;",
    "",
    "  float acc = 0.0f;",
    "  for (int t = 0; t < K; t += BK) {",
    "    // stage A,B tiles into shared memory",
    "    As[ty][tx] = A[row*K + t + tx];",
    "    Bs[ty][tx] = B[(t + ty)*N + col];",
    "    __syncthreads();",
    "",
    "    // matrix-multiply the tile, fully cached",
    "    #pragma unroll",
    "    for (int k = 0; k < BK; ++k)",
    "        acc += As[ty][k] * Bs[k][tx];",
    "    __syncthreads();",
    "  }",
    "  C[row*N + col] = acc;",
    "}",
]

# Right card (split view) — matches reference screenshot
HEADLINE = [
    ("Every AI engineer should learn to write ", False),
    ("exactly one CUDA kernel.", True),
]
CARD_BULLETS = [
    "→ not because you'll write them at work",
    "→ because the mental model changes everything",
    "→ ~200 lines.  one weekend.",
    "→ you'll never look at PyTorch the same way again",
]

# Overlay box content — matches final screenshot exactly
OV_LINES = [
    ("AFTER YOU WRITE IT, YOU UNDERSTAND:", "head"),
    ("", None),
    ("✓   why batch size matters",           "check"),
    ("✓   why FP8 helps",                    "check"),
    ("✓   why fused kernels exist",          "check"),
    ("✓   what 'memory access pattern' means","check"),
    ("✓   flash attention papers, actually", "check"),
    ("", None),
    ("have you written a CUDA kernel? what did it teach you?", "cta"),
    ("", None),
    ("#CUDA  #GPU  #AIInfrastructure  #LearnToCode", "hash"),
]


# ── IDE layout constants (full-width) ─────────────────────────────────────────
TITLE_H = 38
SB_W    = 258
TAB_H   = 30
STAT_H  = 22
GUT_W   = 48
OL_H    = 185
LH      = 22    # line height — matches screenshots
SLH     = 17


# ── render helpers ────────────────────────────────────────────────────────────

def draw_titlebar(draw, T, width, filename):
    draw.rectangle([0, 0, width, TITLE_H], fill=T["titlebar_bg"])
    draw.ellipse([ 14, 12, 26, 24], fill="#ff5f57")
    draw.ellipse([ 32, 12, 44, 24], fill="#febc2e")
    draw.ellipse([ 50, 12, 62, 24], fill="#28c840")
    title = f"{filename} — write-like-me — Cursor"
    tw = draw.textlength(title, font=f_ui)
    draw.text(((width - tw) / 2, (TITLE_H - 11) / 2), title,
              fill="#808080", font=f_ui)

def draw_sidebar(draw, T, width, height, file_tree, outline):
    """Sidebar + outline into a rectangle [0, TITLE_H, SB_W, height-STAT_H]."""
    draw.rectangle([0, TITLE_H, SB_W, height - STAT_H], fill=T["sidebar_bg"])
    draw.text((8, TITLE_H + 8), "EXPLORER", fill=T["dim"], font=f_ui_b)
    ty = TITLE_H + 26
    for ind, name, is_dir, active in file_tree:
        if ty > height - OL_H - STAT_H - 2:
            break
        if active:
            draw.rectangle([0, ty - 1, SB_W, ty + SLH], fill=T["select_bg"])
        fx  = 6 + ind * 12
        ico = "▾ " if is_dir else "  "
        col = T["folder"] if is_dir else (T["text"] if active else T["dim"])
        draw.text((fx, ty), ico + name, fill=col, font=f_ui)
        ty += SLH
    # outline
    OLY = height - OL_H - STAT_H
    draw.rectangle([0, OLY, SB_W, height - STAT_H], fill=T["tabbar_bg"])
    draw.line([0, OLY, SB_W, OLY], fill=T["dim"])
    draw.text((8, OLY + 5), "OUTLINE", fill=T["dim"], font=f_ui_b)
    oy = OLY + 20
    for ind, label, sec in outline:
        if oy > height - STAT_H - 2:
            break
        col = T["func"] if sec else T["comment"]
        draw.text((6 + ind * 10, oy), label, fill=col, font=f_ui)
        oy += SLH

def draw_editor_chrome(draw, T, width, height, filename):
    """Tab strip + gutter."""
    EDX = SB_W
    draw.rectangle([EDX, TITLE_H, width, TITLE_H + TAB_H], fill=T["tabbar_bg"])
    te = EDX + min(len(filename) * 8 + 36, 220)
    draw.rectangle([EDX, TITLE_H, te, TITLE_H + TAB_H], fill=T["ide_bg"])
    draw.line([te, TITLE_H, te, TITLE_H + TAB_H], fill=T["dim"])
    draw.ellipse([EDX + 7,  TITLE_H + TAB_H//2 - 5,
                  EDX + 17, TITLE_H + TAB_H//2 + 5], fill=T["tab_dot"])
    draw.text((EDX + 21, TITLE_H + (TAB_H - 11)//2),
              filename, fill=T["text"], font=f_ui)
    draw.rectangle([EDX, TITLE_H + TAB_H, EDX + GUT_W, height - STAT_H],
                   fill=T["gutter_bg"])

def draw_status(draw, T, width, height, branch, lang):
    draw.rectangle([0, height - STAT_H, width, height], fill=T["status_bg"])
    draw.text((8, height - STAT_H + 4),
              f"  {branch}  ↑2 ↓0  {lang}  ·  UTF-8  ·  LF  ·  256 cols",
              fill=T["status_fg"], font=f_ui_b)
    draw.text((width - 115, height - STAT_H + 4),
              "GPU: H100 · SM96", fill=T["status_fg"], font=f_ui_b)

def draw_code(draw, T, width, height, code_lines, cursor_li):
    CODE_X   = SB_W + GUT_W
    code_top = TITLE_H + TAB_H + 4
    code_bot = height - STAT_H - OL_H
    max_vis  = (code_bot - code_top) // LH
    start    = max(0, cursor_li - max_vis + 3)
    for i, line in enumerate(code_lines[start:start + max_vis]):
        ali = start + i
        cy  = code_top + i * LH
        draw.text((SB_W + 2, cy), f"{ali+1:>3}", fill=T["ln_fg"], font=f_ui)
        if ali == cursor_li:
            draw.rectangle([SB_W + GUT_W, cy - 1, width, cy + LH - 1],
                           fill=T["select_bg"])
        cx = CODE_X
        for tok, col in tokenise(line, T):
            tw = draw.textlength(tok, font=f_code)
            if cx + tw > width - 2:
                break
            draw.text((cx, cy), tok, fill=col, font=f_code)
            cx += tw
    # cursor
    vi = cursor_li - start
    if 0 <= vi < max_vis and cursor_li < len(code_lines):
        cy  = code_top + vi * LH
        cx  = CODE_X + draw.textlength(code_lines[cursor_li], font=f_code)
        draw.rectangle([min(cx, width - 4), cy,
                        min(cx + 2, width - 2), cy + LH - 2], fill=T["text"])


# ── Phase 1: split-view frame ─────────────────────────────────────────────────
def make_split_frame(T, filename):
    """IDE left half + post card right half."""
    img  = Image.new("RGB", (W, H), T["ide_bg"])
    draw = ImageDraw.Draw(img)

    # LEFT IDE (half-width) ─ abbreviated, no code yet
    draw_titlebar(draw, T, HALF, filename)
    # sidebar scaled to half-width
    draw.rectangle([0, TITLE_H, SB_W, H - STAT_H], fill=T["sidebar_bg"])
    draw.text((8, TITLE_H + 8), "EXPLORER", fill=T["dim"], font=f_ui_b)
    ty = TITLE_H + 26
    for ind, name, is_dir, active in FILE_TREE:
        if ty > H - OL_H - STAT_H - 2:
            break
        if active:
            draw.rectangle([0, ty - 1, SB_W, ty + SLH], fill=T["select_bg"])
        fx  = 6 + ind * 12
        ico = "▾ " if is_dir else "  "
        col = T["folder"] if is_dir else (T["text"] if active else T["dim"])
        draw.text((fx, ty), ico + name, fill=col, font=f_ui)
        ty += SLH
    OLY = H - OL_H - STAT_H
    draw.rectangle([0, OLY, SB_W, H - STAT_H], fill=T["tabbar_bg"])
    draw.line([0, OLY, SB_W, OLY], fill=T["dim"])
    draw.text((8, OLY + 5), "OUTLINE", fill=T["dim"], font=f_ui_b)
    oy = OLY + 20
    for ind, label, sec in OUTLINE:
        if oy > H - STAT_H - 2: break
        draw.text((6 + ind * 10, oy), label,
                  fill=T["func"] if sec else T["comment"], font=f_ui)
        oy += SLH
    # editor chrome (left half)
    EDX = SB_W
    draw.rectangle([EDX, TITLE_H, HALF, TITLE_H + TAB_H], fill=T["tabbar_bg"])
    te = EDX + min(len(filename) * 8 + 36, 180)
    draw.rectangle([EDX, TITLE_H, te, TITLE_H + TAB_H], fill=T["ide_bg"])
    draw.ellipse([EDX+7, TITLE_H+TAB_H//2-5, EDX+17, TITLE_H+TAB_H//2+5],
                 fill=T["tab_dot"])
    draw.text((EDX+21, TITLE_H+(TAB_H-11)//2), filename, fill=T["text"], font=f_ui)
    draw.rectangle([EDX, TITLE_H+TAB_H, EDX+GUT_W, H-STAT_H], fill=T["gutter_bg"])
    draw_status(draw, T, HALF, H, "main", "CUDA")

    # RIGHT card
    cx0 = HALF
    draw.rectangle([cx0, 0, W, H], fill=T["card_bg"])
    px = cx0 + 48
    cy = 105
    lh = 70
    cx = px
    for text, hi in HEADLINE:
        col = T["card_cyan"] if hi else T["card_white"]
        for word in text.split():
            tw = draw.textlength(word + " ", font=f_head)
            if cx + tw > W - 48 and cx > px:
                cx = px; cy += lh
            draw.text((cx, cy), word, fill=col, font=f_head)
            cx += tw
    cy += lh + 22
    draw.rectangle([px, cy, px + 118, cy + 4], fill=T["card_div"])
    cy += 28
    for b in CARD_BULLETS:
        draw.text((px, cy), b, fill=T["card_body"], font=f_bullet)
        cy += 38

    return img


# ── Phase 2: full-width IDE frame (with code typed so far) ────────────────────
def make_full_frame(T, filename, code_lines, cursor_li):
    img  = Image.new("RGB", (W, H), T["ide_bg"])
    draw = ImageDraw.Draw(img)
    draw_titlebar(draw, T, W, filename)
    draw_sidebar(draw, T, W, H, FILE_TREE, OUTLINE)
    draw.rectangle([SB_W, TITLE_H, W, H], fill=T["ide_bg"])
    draw_editor_chrome(draw, T, W, H, filename)
    draw_code(draw, T, W, H, code_lines, cursor_li)
    draw_status(draw, T, W, H, "main", "CUDA")
    return img


# ── Phase 3: overlay box on top of final code frame ──────────────────────────
def make_overlay_frame(T, base_img):
    img  = base_img.copy()
    draw = ImageDraw.Draw(img)

    # Box dimensions — covers roughly lines 22-34 area in the editor
    CODE_X   = SB_W + GUT_W
    code_top = TITLE_H + TAB_H + 4
    # position box starting at line 21 (0-indexed → row 20)
    box_y1 = code_top + 20 * LH - 6
    box_y2 = H - STAT_H - OL_H - 6
    box_x1 = SB_W + GUT_W - 8
    box_x2 = W - 8

    # dark fill + border
    draw.rectangle([box_x1, box_y1, box_x2, box_y2], fill=T["ov_bg"])
    draw.rectangle([box_x1, box_y1, box_x2, box_y2],
                   outline=T["ov_border"], width=2)

    tx = box_x1 + 16
    ty = box_y1 + 12
    lh_ov = 26

    for text, kind in OV_LINES:
        if kind is None:
            ty += lh_ov // 2
            continue
        col = {
            "head":  T["ov_head"],
            "check": T["ov_check"],
            "cta":   T["ov_cta"],
            "hash":  T["ov_hash"],
        }[kind]
        font = f_ov_h if kind == "head" else f_ov_b
        draw.text((tx, ty), text, fill=col, font=font)
        ty += lh_ov

    return img


# ── GIF builder ───────────────────────────────────────────────────────────────
def build(T, filename="03_gemm_tiled.cu"):
    frames = []

    # Phase 1: split view — hold ~2 s
    split = make_split_frame(T, filename)
    for _ in range(20):
        frames.append((split, 100))

    # Phase 2: full-width, code types in
    typed = []
    for li, line in enumerate(CODE):
        typed.append("")
        for ci, ch in enumerate(line):
            typed[-1] += ch
            if ci % 2 == 0:
                frames.append((make_full_frame(T, filename, list(typed), li), 42))
        for _ in range(4):
            frames.append((make_full_frame(T, filename, list(typed), li), 70))

    last    = list(typed)
    last_li = len(CODE) - 1

    # cursor blink
    for _ in range(4):
        frames.append((make_full_frame(T, filename, last, last_li), 400))
        frames.append((make_full_frame(T, filename, last, -1),      400))

    # Phase 3: overlay appears, hold
    base = make_full_frame(T, filename, last, last_li)
    ov   = make_overlay_frame(T, base)
    for _ in range(40):
        frames.append((ov, 100))

    return frames


def save(frames, path, colors=96):
    imgs = [f[0].quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
            for f in frames]
    durs = [f[1] for f in frames]
    imgs[0].save(path, save_all=True, append_images=imgs[1:],
                 duration=durs, loop=0, optimize=True)
    print(f"  {path}  {os.path.getsize(path)//1024} KB  ({len(frames)} frames)")


if __name__ == "__main__":
    for key, name in [("tokyo","post1.gif"),("dracula","post2.gif"),("github","post3.gif")]:
        print(f"\n── {key} ──")
        frames = build(THEMES[key])
        save(frames, f"{OUT}/{name}")
    print("\nDone!")
