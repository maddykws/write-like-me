#!/usr/bin/env python3
"""
GIF flow:
  1. Post text types out in the LEFT editor (like drafting the idea)
  2. RIGHT card is VISIBLE from frame 1 (static, always shown)
  3. Editor transitions to CUDA code typing
  4. Full-width end card (post card summary)

Colors match the reference Cursor screenshot exactly.
3 theme variants: Tokyo Night, Dracula, GitHub Dark
"""

from PIL import Image, ImageDraw, ImageFont
import os, re

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
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS   = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

F_CODE  = load(MONO,   13)
F_UI    = load(MONO,   11)
F_UI_B  = load(MONO_B, 11)
# card fonts — match reference: large bold sans for headline, mono for bullets
F_HEAD  = load(SANS_B, 55)
F_BODY  = load(MONO,   21)
F_END_H = load(SANS_B, 56)
F_END_B = load(SANS,   25)

# ── themes — tuned to match reference image exactly ───────────────────────────
THEMES = {
    # Reference image is Tokyo Night — these values match it pixel-perfect
    "tokyo": {
        "name":      "Tokyo Night",
        # IDE
        "bg":        "#1a1b26",
        "sidebar":   "#16161e",
        "tab_bar":   "#13131a",
        "status_bg": "#7aa2f7",
        "status_fg": "#1a1b26",
        "ln":        "#3b4261",
        "select":    "#283457",
        "text":      "#c0caf5",
        "comment":   "#565f89",
        "keyword":   "#bb9af7",
        "func":      "#7dcfff",
        "string":    "#9ece6a",
        "number":    "#ff9e64",
        "type":      "#f7768e",
        "punct":     "#89ddff",
        "dim":       "#3b4261",
        "folder":    "#e0af68",
        # card (right side) — dark panel, white + cyan, matches reference
        "card_bg":   "#0d0e17",
        "card_h1":   "#ffffff",
        "card_hi":   "#2ac3de",   # cyan — "exactly one CUDA kernel."
        "card_body": "#7982a9",   # muted for bullets
        "divider":   "#2ac3de",
        # end card
        "end_bg":    "#13131a",
        "end_accent":"#7aa2f7",
        "end_hi":    "#2ac3de",
    },
    "dracula": {
        "name":      "Dracula",
        "bg":        "#282a36",
        "sidebar":   "#21222c",
        "tab_bar":   "#191a21",
        "status_bg": "#bd93f9",
        "status_fg": "#191a21",
        "ln":        "#6272a4",
        "select":    "#44475a",
        "text":      "#f8f8f2",
        "comment":   "#6272a4",
        "keyword":   "#ff79c6",
        "func":      "#50fa7b",
        "string":    "#f1fa8c",
        "number":    "#bd93f9",
        "type":      "#ffb86c",
        "punct":     "#ff79c6",
        "dim":       "#44475a",
        "folder":    "#ffb86c",
        "card_bg":   "#191a21",
        "card_h1":   "#f8f8f2",
        "card_hi":   "#bd93f9",
        "card_body": "#6272a4",
        "divider":   "#bd93f9",
        "end_bg":    "#21222c",
        "end_accent":"#ff79c6",
        "end_hi":    "#bd93f9",
    },
    "github": {
        "name":      "GitHub Dark",
        "bg":        "#0d1117",
        "sidebar":   "#010409",
        "tab_bar":   "#010409",
        "status_bg": "#388bfd",
        "status_fg": "#ffffff",
        "ln":        "#30363d",
        "select":    "#1c2128",
        "text":      "#e6edf3",
        "comment":   "#8b949e",
        "keyword":   "#ff7b72",
        "func":      "#79c0ff",
        "string":    "#a5d6ff",
        "number":    "#79c0ff",
        "type":      "#ffa657",
        "punct":     "#ff7b72",
        "dim":       "#30363d",
        "folder":    "#e3b341",
        "card_bg":   "#010409",
        "card_h1":   "#e6edf3",
        "card_hi":   "#58a6ff",
        "card_body": "#8b949e",
        "divider":   "#58a6ff",
        "end_bg":    "#0d1117",
        "end_accent":"#3fb950",
        "end_hi":    "#58a6ff",
    },
}

# ── syntax highlighter ────────────────────────────────────────────────────────
KW = {"__global__","__shared__","__device__","__syncthreads","float","int",
      "void","auto","for","if","else","return","import","from","def","class",
      "with","as","True","False","None","and","or","not","in","double","char"}

def tokenise(line, T):
    if re.match(r'\s*(#|//)', line):
        return [(line, T["comment"])]
    pat = re.compile(
        r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'
        r'|(\b(?:' + '|'.join(re.escape(k) for k in KW) + r')\b)'
        r'|(\b\d+\.?\d*(?:e[+-]?\d+)?[fF]?\b)'
        r'|([A-Za-z_]\w*(?=\s*\())'
        r'|([^\w\s])'
        r'|(\w+)'
        r'|(\s+)'
    )
    out = []
    for m in pat.finditer(line):
        s, kw, num, fn, pu, _, ws = m.groups()
        txt = m.group(0)
        if ws:    c = T["text"]
        elif s:   c = T["string"]
        elif kw:  c = T["keyword"]
        elif num: c = T["number"]
        elif fn:  c = T["func"]
        elif pu:  c = T["punct"]
        else:     c = T["text"]
        out.append((txt, c))
    return out or [(line, T["text"])]


# ── IDE renderer ──────────────────────────────────────────────────────────────
AB   = 36     # activity bar width
SB   = 194    # sidebar width
TAB  = 32     # tab bar height
STAT = 24     # status bar height
GUT  = 36     # gutter width
OL_H = 172    # outline panel height
LH   = 18     # code line height
SLH  = 16     # sidebar line height

def draw_ide(T, filename, file_tree, code_lines, cursor_li, outline, branch, lang):
    img  = Image.new("RGB", (HALF, H), T["bg"])
    draw = ImageDraw.Draw(img)

    # activity bar
    draw.rectangle([0, 0, AB, H], fill=T["tab_bar"])
    for ay in [52, 104, 156, 208, 260]:
        draw.rectangle([7, ay, AB-7, ay+20], fill=T["dim"])

    # sidebar bg
    SBX = AB
    draw.rectangle([SBX, 0, SBX+SB, H], fill=T["sidebar"])
    draw.text((SBX+8, 9), "EXPLORER", fill=T["comment"], font=F_UI_B)

    # file tree
    ty = 28
    for ind, name, is_dir, active in file_tree:
        if ty > H - OL_H - STAT - 4:
            break
        fx = SBX + 5 + ind * 11
        if active:
            draw.rectangle([SBX, ty-1, SBX+SB, ty+SLH], fill=T["select"])
        ico = "▾ " if is_dir else "  "
        col = T["folder"] if is_dir else (T["text"] if active else T["dim"])
        draw.text((fx, ty), ico + name, fill=col, font=F_UI)
        ty += SLH

    # outline panel
    OLY = H - OL_H - STAT
    draw.rectangle([SBX, OLY, SBX+SB, H-STAT], fill=T["tab_bar"])
    draw.line([SBX, OLY, SBX+SB, OLY], fill=T["dim"])
    draw.text((SBX+8, OLY+5), "OUTLINE", fill=T["comment"], font=F_UI_B)
    oy = OLY + 20
    for ind, label, sec in outline:
        if oy > H - STAT - 2:
            break
        draw.text((SBX+5+ind*10, oy), label,
                  fill=T["func"] if sec else T["comment"], font=F_UI)
        oy += SLH

    # editor area
    EDX = SBX + SB
    draw.rectangle([EDX, 0, HALF, H], fill=T["bg"])

    # tab bar
    draw.rectangle([EDX, 0, HALF, TAB], fill=T["tab_bar"])
    tw = min(len(filename)*8+34, 210)
    draw.rectangle([EDX, 0, EDX+tw, TAB], fill=T["bg"])
    draw.line([EDX+tw, 0, EDX+tw, TAB], fill=T["dim"])
    draw.ellipse([EDX+7, TAB//2-5, EDX+17, TAB//2+5],
                 fill=T["type"] if cursor_li >= 0 else T["comment"])
    draw.text((EDX+21, (TAB-11)//2), filename, fill=T["text"], font=F_UI)

    # gutter
    draw.rectangle([EDX, TAB, EDX+GUT, H-STAT], fill=T["sidebar"])

    # code
    CODE_X  = EDX + GUT
    code_top = TAB + 4
    code_bot = H - STAT - OL_H
    max_vis  = (code_bot - code_top) // LH

    start = max(0, cursor_li - max_vis + 3)
    for i, line in enumerate(code_lines[start:start+max_vis]):
        ali = start + i
        cy  = code_top + i * LH
        draw.text((EDX+2, cy), f"{ali+1:>3}", fill=T["ln"], font=F_UI)
        if ali == cursor_li:
            draw.rectangle([EDX+GUT, cy-1, HALF, cy+LH-1], fill=T["select"])
        cx = CODE_X
        for tok, col in tokenise(line, T):
            tw2 = draw.textlength(tok, font=F_CODE)
            if cx + tw2 > HALF - 2:
                break
            draw.text((cx, cy), tok, fill=col, font=F_CODE)
            cx += tw2

    # cursor
    vi = cursor_li - start
    if 0 <= vi < max_vis and cursor_li < len(code_lines):
        cy  = code_top + vi * LH
        cx  = CODE_X + draw.textlength(code_lines[cursor_li], font=F_CODE)
        draw.rectangle([min(cx, HALF-4), cy, min(cx+2, HALF-2), cy+LH-2],
                       fill=T["text"])

    # status bar
    draw.rectangle([0, H-STAT, HALF, H], fill=T["status_bg"])
    draw.text((AB+6, H-STAT+5),
              f"  {branch}  ↑2 ↓0  {lang}  ·  UTF-8  ·  LF",
              fill=T["status_fg"], font=F_UI_B)
    draw.text((HALF-70, H-STAT+5), "GPU: H100",
              fill=T["status_fg"], font=F_UI_B)

    return img


# ── right card renderer (STATIC — always visible) ─────────────────────────────
def draw_card(T, headline_parts, bullets):
    """Right half post card — matches reference screenshot."""
    img  = Image.new("RGB", (HALF, H), T["card_bg"])
    draw = ImageDraw.Draw(img)

    px = 50
    cy = 110

    # headline — word-wrap, colour per segment
    line_h = 70
    cx = px
    for text, hi in headline_parts:
        col = T["card_hi"] if hi else T["card_h1"]
        for word in text.split():
            tw = draw.textlength(word + " ", font=F_HEAD)
            if cx + tw > HALF - px and cx > px:
                cx  = px
                cy += line_h
            draw.text((cx, cy), word, fill=col, font=F_HEAD)
            cx += tw
    cy += line_h + 22

    # divider — matches reference
    draw.rectangle([px, cy, px+115, cy+4], fill=T["divider"])
    cy += 30

    # bullets
    for b in bullets:
        draw.text((px, cy), b, fill=T["card_body"], font=F_BODY)
        cy += 38

    return img


# ── full-width end card ────────────────────────────────────────────────────────
def draw_end_card(T, lines):
    """Full 1080×1080 ending post card."""
    img  = Image.new("RGB", (W, H), T["end_bg"])
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 6], fill=T["end_accent"])

    px = 80
    cy = 140
    lh = 72
    for line in lines:
        if line == "":
            cy += 20
            continue
        if line.startswith("──"):
            draw.rectangle([px, cy, px+140, cy+4], fill=T["end_hi"])
            cy += 24
            continue
        hi = line.startswith("*")
        col = T["end_hi"] if hi else ("#ffffff" if not line.startswith("→") else T["card_body"] if "card_body" in T else "#7982a9")
        text = line.lstrip("*").rstrip("*")
        font = F_END_H if hi else F_END_B
        draw.text((px, cy), text, fill=col, font=font)
        cy += lh if hi else 44

    return img


# ── frame assembler ───────────────────────────────────────────────────────────
def compose(ide_img, card_img):
    out = Image.new("RGB", (W, H))
    out.paste(ide_img,  (0,    0))
    out.paste(card_img, (HALF, 0))
    return out


def build_gif(T, filename, file_tree, post_lines, code_lines, outline,
              headline_parts, bullets, end_lines,
              branch="main", lang="CUDA"):
    frames = []

    # Pre-render card (always visible)
    card = draw_card(T, headline_parts, bullets)

    typed = []

    def frame(lines, cursor_li, delay):
        ide = draw_ide(T, filename, file_tree, lines, cursor_li, outline, branch, lang)
        frames.append((compose(ide, card), delay))

    # ── Phase 1: post text types in the editor ──
    for li, line in enumerate(post_lines):
        typed.append("")
        for ci, ch in enumerate(line):
            typed[-1] += ch
            if ci % 2 == 0:
                frame(list(typed), li, 45)
        for _ in range(4):
            frame(list(typed), li, 70)

    # brief pause + cursor blink
    last_post = list(typed)
    for _ in range(3):
        frame(last_post, len(post_lines)-1, 350)
        frame(last_post, -1, 350)

    # ── Phase 2: CUDA code types in the editor ──
    typed = []
    for li, line in enumerate(code_lines):
        typed.append("")
        for ci, ch in enumerate(line):
            typed[-1] += ch
            if ci % 2 == 0:
                frame(list(typed), li, 42)
        for _ in range(4):
            frame(list(typed), li, 70)

    last_code = list(typed)
    for _ in range(4):
        frame(last_code, len(code_lines)-1, 350)
        frame(last_code, -1, 350)

    # hold final split
    final_split = compose(
        draw_ide(T, filename, file_tree, last_code, len(code_lines)-1,
                 outline, branch, lang),
        card
    )
    for _ in range(20):
        frames.append((final_split, 100))

    # ── Phase 3: full-width end card ──
    end = draw_end_card(T, end_lines)
    for _ in range(38):
        frames.append((end, 100))

    return frames


def save_gif(frames, path, colors=96):
    imgs = [f[0].quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
            for f in frames]
    durs = [f[1] for f in frames]
    imgs[0].save(path, save_all=True, append_images=imgs[1:],
                 duration=durs, loop=0, optimize=True)
    print(f"  {path}  {os.path.getsize(path)//1024} KB  {len(frames)} frames")


# ══════════════════════════════════════════════════════════════════════════════
#  Content
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

# Post text typed in the editor first (like drafting the idea)
POST_TEXT = [
    "// Every AI engineer should learn to write",
    "// exactly one CUDA kernel.",
    "//",
    "// Not because you'll write them at work.",
    "// Because the mental model changes everything.",
    "//",
    "// → you stop thinking 'model is slow'",
    "// → you start seeing memory access patterns",
    "// → ~200 lines. one weekend.",
    "// → you'll never look at PyTorch the same way",
]

# Then CUDA code types in
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
    "    for (int k=0; k<TILE; k++)",
    "      acc += As[threadIdx.y][k]*Bs[k][threadIdx.x];",
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
    "→ because the mental model",
    "   changes everything",
    "→ ~200 lines.  one weekend.",
    "→ you'll never look at PyTorch",
    "   the same way again",
]

END_LINES = [
    "*After you write it,*",
    "*you understand everything.*",
    "──",
    "→ why batch size is the #1 perf knob",
    "→ why FP8 doubles throughput",
    "→ why fused kernels exist",
    "→ how to read a profiler trace",
    "→ why Flash Attention matters",
    "",
    "   Suggested start: GEMM with tiling. ~200 lines.",
]


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
            T, "03_gemm_tiled.cu", FILE_TREE,
            POST_TEXT, CODE, OUTLINE,
            HEADLINE, BULLETS, END_LINES,
        )
        save_gif(frames, f"{OUT}/{out_name}")

    print("\nDone!")
