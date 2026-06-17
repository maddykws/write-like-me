#!/usr/bin/env python3
"""
Split-layout GIFs — fixed:
  Phase 1: IDE left, RIGHT side dark/empty — code types out
  Phase 2: Right card REVEALS after code done (fade-in)
  Phase 3: Hold split view
  Phase 4: Full-width "understanding" end card

3 themes: Tokyo Night (original), Dracula, GitHub Dark
"""

from PIL import Image, ImageDraw, ImageFont
import os, re, textwrap

OUT = "/home/user/write-like-me/post_assets"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1080
HALF = W // 2

# ── fonts ─────────────────────────────────────────────────────────────────────
def load(path, size):
    try:    return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

MONO   = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANS   = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

F_CODE  = load(MONO,   13)
F_UI    = load(MONO,   11)
F_UI_B  = load(MONO_B, 11)
F_HEAD1 = load(SANS_B, 54)
F_HEAD2 = load(SANS_B, 46)
F_BODY  = load(MONO,   21)
F_END_H = load(SANS_B, 62)
F_END_B = load(SANS,   26)

# ── themes ────────────────────────────────────────────────────────────────────
THEMES = {
    "tokyo": {
        "name":       "Tokyo Night",
        "bg":         "#1a1b26",
        "sidebar":    "#16161e",
        "tab_bar":    "#13131a",
        "status_bg":  "#7aa2f7",
        "ln":         "#3b4261",
        "select":     "#283457",
        "text":       "#c0caf5",
        "comment":    "#565f89",
        "keyword":    "#bb9af7",
        "func":       "#7dcfff",
        "string":     "#9ece6a",
        "number":     "#ff9e64",
        "type":       "#f7768e",
        "punct":      "#89ddff",
        "dim":        "#3b4261",
        "folder":     "#e0af68",
        "accent":     "#2ac3de",     # cyan — card highlight
        "card_bg":    "#0d0e14",
        "card_text":  "#c0caf5",
        "divider":    "#2ac3de",
        "end_bg":     "#13131a",
        "end_accent": "#7aa2f7",
    },
    "dracula": {
        "name":       "Dracula",
        "bg":         "#282a36",
        "sidebar":    "#21222c",
        "tab_bar":    "#191a21",
        "status_bg":  "#bd93f9",
        "ln":         "#6272a4",
        "select":     "#44475a",
        "text":       "#f8f8f2",
        "comment":    "#6272a4",
        "keyword":    "#ff79c6",
        "func":       "#50fa7b",
        "string":     "#f1fa8c",
        "number":     "#bd93f9",
        "type":       "#ffb86c",
        "punct":      "#ff79c6",
        "dim":        "#44475a",
        "folder":     "#ffb86c",
        "accent":     "#bd93f9",     # purple
        "card_bg":    "#191a21",
        "card_text":  "#f8f8f2",
        "divider":    "#bd93f9",
        "end_bg":     "#21222c",
        "end_accent": "#ff79c6",
    },
    "github": {
        "name":       "GitHub Dark",
        "bg":         "#0d1117",
        "sidebar":    "#010409",
        "tab_bar":    "#010409",
        "status_bg":  "#388bfd",
        "ln":         "#30363d",
        "select":     "#1f2937",
        "text":       "#e6edf3",
        "comment":    "#8b949e",
        "keyword":    "#ff7b72",
        "func":       "#79c0ff",
        "string":     "#a5d6ff",
        "number":     "#79c0ff",
        "type":       "#ffa657",
        "punct":      "#ff7b72",
        "dim":        "#30363d",
        "folder":     "#e3b341",
        "accent":     "#58a6ff",     # blue
        "card_bg":    "#010409",
        "card_text":  "#e6edf3",
        "divider":    "#58a6ff",
        "end_bg":     "#0d1117",
        "end_accent": "#3fb950",
    },
}

KEYWORDS_SET = {
    "__global__","__shared__","__device__","__syncthreads","float","int",
    "void","auto","for","if","else","return","import","from","def","class",
    "with","as","True","False","None","and","or","not","in","double",
}

def hl_tokens(line, T):
    if re.match(r'\s*(#|//)', line):
        return [(line, T["comment"])]
    pattern = re.compile(
        r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'
        r'|(\b(?:' + '|'.join(re.escape(k) for k in KEYWORDS_SET) + r')\b)'
        r'|(\b\d+\.?\d*(?:e[+-]?\d+)?[fF]?\b)'
        r'|([A-Za-z_]\w*(?=\s*\())'
        r'|([^\w\s])'
        r'|(\w+)'
        r'|(\s+)'
    )
    tokens = []
    for m in pattern.finditer(line):
        s, kw, num, fn, pu, ident, ws = m.groups()
        txt = m.group(0)
        if ws:    col = T["text"]
        elif s:   col = T["string"]
        elif kw:  col = T["keyword"]
        elif num: col = T["number"]
        elif fn:  col = T["func"]
        elif pu:  col = T["punct"]
        else:     col = T["text"]
        tokens.append((txt, col))
    return tokens or [(line, T["text"])]


# ── IDE renderer ──────────────────────────────────────────────────────────────
AB_W = 36    # activity bar
SB_W = 196   # sidebar
TAB_H = 32
STATUS_H = 24
OUTLINE_H = 175
GUTTER_W = 36
LH = 18      # line height in editor
LH_SB = 17   # sidebar line height

def render_ide(T, filename, file_tree, code_lines, cursor_li, outline_items,
               branch="main", lang="CUDA"):
    """Render the left-half IDE panel into a new 540×1080 image."""
    img  = Image.new("RGB", (HALF, H), T["bg"])
    draw = ImageDraw.Draw(img)

    # ── activity bar ──
    draw.rectangle([0, 0, AB_W, H], fill=T["tab_bar"])
    for ay in [55, 110, 165, 220, 275]:
        draw.rectangle([6, ay, AB_W-6, ay+22], fill=T["dim"])

    # ── sidebar ──
    SB_X = AB_W
    draw.rectangle([SB_X, 0, SB_X+SB_W, H], fill=T["sidebar"])
    draw.text((SB_X+8, 10), "EXPLORER", fill=T["comment"], font=F_UI_B)
    ty = 30
    for indent, name, is_folder, is_active in file_tree:
        if ty > H - OUTLINE_H - STATUS_H - 10:
            break
        fx = SB_X + 6 + indent * 11
        if is_active:
            draw.rectangle([SB_X, ty-1, SB_X+SB_W, ty+LH_SB], fill=T["select"])
        icon = "▾ " if is_folder else "  "
        col  = T["folder"] if is_folder else (T["text"] if is_active else T["dim"])
        draw.text((fx, ty), icon + name, fill=col, font=F_UI)
        ty += LH_SB

    # ── outline panel ──
    OL_Y = H - OUTLINE_H - STATUS_H
    draw.rectangle([SB_X, OL_Y, SB_X+SB_W, H-STATUS_H], fill=T["tab_bar"])
    draw.line([SB_X, OL_Y, SB_X+SB_W, OL_Y], fill=T["dim"], width=1)
    draw.text((SB_X+8, OL_Y+5), "OUTLINE", fill=T["comment"], font=F_UI_B)
    oy = OL_Y + 20
    for indent, label, is_sec in outline_items:
        if oy > H - STATUS_H - 3:
            break
        ox = SB_X + 6 + indent*10
        col = T["accent"] if is_sec else T["comment"]
        draw.text((ox, oy), label, fill=col, font=F_UI)
        oy += LH_SB

    # ── editor ──
    ED_X = SB_X + SB_W
    ED_W = HALF - ED_X

    # tab bar
    draw.rectangle([ED_X, 0, HALF, TAB_H], fill=T["tab_bar"])
    tab_end = ED_X + min(len(filename)*8+36, 220)
    draw.rectangle([ED_X, 0, tab_end, TAB_H], fill=T["bg"])
    draw.line([tab_end, 0, tab_end, TAB_H], fill=T["dim"])
    dot = T["type"] if cursor_li >= 0 else T["comment"]
    draw.ellipse([ED_X+7, TAB_H//2-5, ED_X+17, TAB_H//2+5], fill=dot)
    draw.text((ED_X+21, (TAB_H-11)//2), filename, fill=T["text"], font=F_UI)

    # gutter
    draw.rectangle([ED_X, TAB_H, ED_X+GUTTER_W, H-STATUS_H], fill=T["sidebar"])

    # code area — FIX: never scroll, just show from line 0, clip at bottom
    CODE_X = ED_X + GUTTER_W
    code_top = TAB_H + 5
    code_bot = H - STATUS_H - OUTLINE_H - 2   # stop before outline area
    max_vis  = (code_bot - code_top) // LH

    # scroll so cursor stays in view
    start = max(0, cursor_li - max_vis + 3)

    for i, line in enumerate(code_lines[start:start + max_vis]):
        abs_li = start + i
        cy = code_top + i * LH
        # line number
        draw.text((ED_X+2, cy), f"{abs_li+1:>3}", fill=T["ln"], font=F_UI)
        # active line highlight
        if abs_li == cursor_li:
            draw.rectangle([ED_X+GUTTER_W, cy-1, HALF, cy+LH-1], fill=T["select"])
        # tokens
        cx = CODE_X
        for tok, col in hl_tokens(line, T):
            tw = draw.textlength(tok, font=F_CODE)
            if cx + tw > HALF - 2:
                break
            draw.text((cx, cy), tok, fill=col, font=F_CODE)
            cx += tw

    # cursor
    vis_i = cursor_li - start
    if 0 <= vis_i < max_vis and cursor_li < len(code_lines):
        cur_y = code_top + vis_i * LH
        cur_x = CODE_X + draw.textlength(code_lines[cursor_li], font=F_CODE)
        cur_x = min(cur_x, HALF - 4)
        draw.rectangle([cur_x, cur_y, cur_x+2, cur_y+LH-2], fill=T["text"])

    # status bar
    draw.rectangle([0, H-STATUS_H, HALF, H], fill=T["status_bg"])
    draw.text((AB_W+6, H-STATUS_H+5),
              f"  {branch}  ↑2 ↓0  {lang}  ·  UTF-8  ·  LF",
              fill=T["bg"], font=F_UI_B)
    draw.text((HALF-70, H-STATUS_H+5), "GPU: H100", fill=T["bg"], font=F_UI_B)

    return img


# ── right card renderer ────────────────────────────────────────────────────────
def render_card(T, headline_parts, bullets, alpha=255):
    """Render right-half post card. alpha 0=invisible 255=full."""
    img  = Image.new("RGBA", (HALF, H), T["card_bg"] + "ff")
    draw = ImageDraw.Draw(img)

    px = 52
    cy = 115

    # headline
    line_h = 68
    cx = px
    for text, hi in headline_parts:
        col  = T["accent"] if hi else "#ffffff"
        font = F_HEAD1
        for word in text.split():
            tw = draw.textlength(word + " ", font=font)
            if cx + tw > HALF - px and cx > px:
                cx  = px
                cy += line_h
            draw.text((cx, cy), word, fill=col, font=font)
            cx += tw
    cy += line_h + 18

    # divider
    draw.rectangle([px, cy, px+110, cy+4], fill=T["divider"])
    cy += 26

    # bullets
    for b in bullets:
        draw.text((px, cy), b, fill=T["card_text"], font=F_BODY)
        cy += 36

    # apply alpha
    if alpha < 255:
        mask = Image.new("L", (HALF, H), alpha)
        img.putalpha(mask)

    return img


def render_end_card(T, headline, sub_bullets):
    """Full-width end card."""
    img  = Image.new("RGB", (W, H), T["end_bg"])
    draw = ImageDraw.Draw(img)

    # top accent bar
    draw.rectangle([0, 0, W, 6], fill=T["end_accent"])

    cx, cy = 80, 160
    line_h = 78
    for word in headline.split():
        tw = draw.textlength(word + " ", font=F_END_H)
        # line break hints via '|'
        if word == "|":
            cx  = 80
            cy += line_h
            continue
        if cx + tw > W - 80 and cx > 80:
            cx  = 80
            cy += line_h
        col = T["end_accent"] if word.startswith("*") and word.endswith("*") \
              else "#ffffff"
        word_clean = word.strip("*")
        draw.text((cx, cy), word_clean, fill=col, font=F_END_H)
        cx += draw.textlength(word_clean + " ", font=F_END_H)

    cy += line_h + 30
    draw.rectangle([80, cy, 80+160, cy+5], fill=T["end_accent"])
    cy += 30

    for b in sub_bullets:
        draw.text((80, cy), b, fill=T["card_text"] if "card_text" in T else "#c0caf5",
                  font=F_END_B)
        cy += 44

    return img


# ── main GIF builder ──────────────────────────────────────────────────────────
def build_gif(T, filename, file_tree, code_lines, outline_items,
              headline_parts, bullets,
              end_headline, end_bullets,
              branch="main", lang="CUDA",
              char_delay=45, line_pause=5,
              reveal_steps=18, hold=28, end_hold=35):

    frames = []
    typed = []

    def compose(typed_lines, cursor_li, card_alpha=0):
        ide_img  = render_ide(T, filename, file_tree, typed_lines,
                               cursor_li, outline_items, branch, lang)
        full = Image.new("RGB", (W, H), T["card_bg"])
        full.paste(ide_img, (0, 0))
        if card_alpha > 0:
            card = render_card(T, headline_parts, bullets, alpha=card_alpha)
            # paste with alpha
            base = Image.new("RGB", (HALF, H), T["card_bg"])
            card_rgb = card.convert("RGB")
            blended = Image.blend(base, card_rgb, card_alpha / 255)
            full.paste(blended, (HALF, 0))
        return full

    # ── Phase 1: type code, right side dark ──
    for li, line in enumerate(code_lines):
        typed.append("")
        for ci, ch in enumerate(line):
            typed[-1] += ch
            if ci % 2 == 0:
                frames.append((compose(list(typed), li, 0), char_delay))
        for _ in range(line_pause):
            frames.append((compose(list(typed), li, 0), 70))

    last_typed = list(typed)
    last_li    = len(code_lines) - 1

    # cursor blink pause before reveal
    for _ in range(3):
        frames.append((compose(last_typed, last_li, 0), 350))
        frames.append((compose(last_typed, -1,      0), 350))

    # ── Phase 2: card reveals ──
    for step in range(reveal_steps + 1):
        a = int(255 * step / reveal_steps)
        frames.append((compose(last_typed, last_li, a), 35))

    # ── Phase 3: hold split view ──
    split_final = compose(last_typed, last_li, 255)
    for _ in range(hold):
        frames.append((split_final, 100))

    # ── Phase 4: full-width end card ──
    end_img = render_end_card(T, end_headline, end_bullets)
    for _ in range(end_hold):
        frames.append((end_img, 100))

    return frames


def save_gif(frames, path, colors=96):
    imgs = [f[0].quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
            for f in frames]
    durs = [f[1] for f in frames]
    imgs[0].save(path, save_all=True, append_images=imgs[1:],
                 duration=durs, loop=0, optimize=True)
    print(f"Saved {path}  ({os.path.getsize(path)//1024} KB, {len(frames)} frames)")


# ══════════════════════════════════════════════════════════════════════════════
#  Shared content
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
    "      acc += As[threadIdx.y][k]",
    "           * Bs[k][threadIdx.x];",
    "    __syncthreads();",
    "  }",
    "  C[row*N + col] = acc;",
    "}",
]

HEADLINE = [
    ("Every AI engineer should learn to write ", False),
    ("exactly one CUDA kernel.", True),
]

BULLETS = [
    "→ not because you'll write them at work",
    "→ because the mental model changes everything",
    "→ ~200 lines.  one weekend.",
    "→ you'll never look at PyTorch the same way",
]

END_HEADLINE = (
    "After you write it | you *understand* | everything."
)

END_BULLETS = [
    "→  why batch size is the first perf knob",
    "→  why FP8 doubles throughput",
    "→  why fused kernels exist",
    "→  how to read a profiler trace",
    "→  why Flash Attention matters",
    "",
    "   Suggested start: GEMM with tiling.  ~200 lines.",
]


# ══════════════════════════════════════════════════════════════════════════════
#  Generate 3 themes
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    for theme_key, out_name in [
        ("tokyo",   "post1.gif"),
        ("dracula", "post2.gif"),
        ("github",  "post3.gif"),
    ]:
        T = THEMES[theme_key]
        print(f"\n── {T['name']} ──")
        frames = build_gif(
            T, "03_gemm_tiled.cu", FILE_TREE, CODE, OUTLINE,
            HEADLINE, BULLETS,
            END_HEADLINE, END_BULLETS,
        )
        save_gif(frames, f"{OUT}/{out_name}")

    print("\nDone!")
