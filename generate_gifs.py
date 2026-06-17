#!/usr/bin/env python3
"""
Split-layout GIFs matching the Cursor IDE + post-text card style.

Left half  : Cursor/VS Code IDE  (sidebar + file tree + editor + outline + status bar)
Right half : Styled post card     (large bold headline, cyan highlight, monospace bullets)

Canvas: 1080×1080 (square, social-ready)
"""

from PIL import Image, ImageDraw, ImageFont
import os, textwrap

OUT = "/home/user/write-like-me/post_assets"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1080
HALF = W // 2          # 540

# ── fonts ────────────────────────────────────────────────────────────────────
def load(path, size, fallback=None):
    try:
        return ImageFont.truetype(path, size)
    except:
        return fallback or ImageFont.load_default()

MONO_PATH  = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B_PATH= "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANS_PATH  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B_PATH= "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

F_CODE   = load(MONO_PATH,   13)
F_CODE_B = load(MONO_B_PATH, 13)
F_UI     = load(MONO_PATH,   11)
F_UI_B   = load(MONO_B_PATH, 11)
F_HEAD   = load(SANS_B_PATH, 52)
F_HEAD2  = load(SANS_B_PATH, 44)
F_BULLET = load(MONO_PATH,   22)
F_LABEL  = load(MONO_B_PATH, 16)

# ── colour palette (Cursor dark) ──────────────────────────────────────────────
C = {
    "bg":       "#1a1b26",   # editor bg
    "sidebar":  "#16161e",   # sidebar / panel bg
    "tab_bar":  "#13131a",   # tab strip
    "tab_act":  "#1a1b26",   # active tab bg
    "status":   "#7aa2f7",   # status bar (blue)
    "status_bg":"#1a1b26",
    "ln":       "#3b4261",   # line numbers
    "select":   "#283457",   # active file highlight
    "text":     "#c0caf5",   # default text
    "comment":  "#565f89",
    "keyword":  "#bb9af7",
    "func":     "#7dcfff",
    "string":   "#9ece6a",
    "number":   "#ff9e64",
    "type":     "#f7768e",
    "punct":    "#89ddff",
    "dim":      "#3b4261",
    "cyan":     "#2ac3de",
    "yellow":   "#e0af68",
    "outline_h":"#bb9af7",
    # right card
    "card_bg":  "#0d0e14",
    "card_text":"#c0caf5",
    "card_hi":  "#2ac3de",   # cyan highlight
    "card_dim": "#565f89",
    "divider":  "#2ac3de",
}

LH_CODE = 19   # code line height
LH_UI   = 16   # sidebar line height

KEYWORDS = {"__global__","__shared__","__device__","__syncthreads","float","int",
            "void","auto","for","if","else","return","import","from","def","class",
            "with","as","True","False","None","and","or","not","in"}

# ── syntax highlight for one line ─────────────────────────────────────────────
import re
def hl_tokens(line):
    """Return list of (text, color) for a code line."""
    if re.match(r'\s*(#|//)', line):
        return [(line, C["comment"])]
    tokens = []
    i = 0
    pattern = re.compile(
        r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'   # strings
        r'|(\b(?:' + '|'.join(re.escape(k) for k in KEYWORDS) + r')\b)'
        r'|(\b\d+\.?\d*\b)'                            # numbers
        r'|([A-Za-z_]\w*(?=\s*\())'                   # function calls
        r'|([^\w\s])'                                  # punctuation
        r'|(\w+)'                                      # identifiers
        r'|(\s+)'                                      # whitespace
    )
    for m in pattern.finditer(line):
        s, kw, num, fn, pu, ident, ws = m.groups()
        txt = m.group(0)
        if ws:   col = C["text"]
        elif s:  col = C["string"]
        elif kw: col = C["keyword"]
        elif num:col = C["number"]
        elif fn: col = C["func"]
        elif pu: col = C["punct"]
        else:    col = C["text"]
        tokens.append((txt, col))
    return tokens if tokens else [(line, C["text"])]


# ── draw the LEFT IDE panel ───────────────────────────────────────────────────
SIDEBAR_W  = 200
TAB_H      = 32
STATUS_H   = 24
OUTLINE_H  = 180

def draw_ide(draw, img,
             filename, project_name,
             file_tree,        # list of (indent, name, is_folder, is_active)
             code_lines,       # list of strings typed so far
             cursor_li,        # active line index (0-based)
             outline_items,    # list of (indent, label, is_section)
             branch="main", lang="CUDA", cols=256):
    """Draw the full Cursor IDE onto the left half of `draw`."""
    x0, y0, x1, y1 = 0, 0, HALF, H

    # ── background ──
    draw.rectangle([x0, y0, x1, y1], fill=C["sidebar"])

    # ── activity bar (thin strip on far left) ──
    AB = 36
    draw.rectangle([x0, y0, x0+AB, y1], fill=C["tab_bar"])
    for ay in [60, 120, 180, 240]:
        draw.rectangle([x0+8, y0+ay, x0+AB-8, y0+ay+24], fill=C["dim"], outline=None)

    # ── sidebar (file explorer) ──
    SB_X = x0 + AB
    SB_W = SIDEBAR_W
    draw.rectangle([SB_X, y0, SB_X+SB_W, y1], fill=C["sidebar"])
    draw.text((SB_X+10, y0+12), "EXPLORER", fill=C["comment"], font=F_UI_B)
    ty = y0 + 32
    for indent, name, is_folder, is_active in file_tree:
        fx = SB_X + 8 + indent * 12
        if is_active:
            draw.rectangle([SB_X, ty-1, SB_X+SB_W, ty+LH_UI], fill=C["select"])
        icon = "▾ " if is_folder else "  "
        col  = C["text"] if is_active else (C["yellow"] if is_folder else C["dim"])
        draw.text((fx, ty), icon + name, fill=col, font=F_UI)
        ty += LH_UI + 1
        if ty > y1 - OUTLINE_H - STATUS_H - 40:
            break

    # outline panel
    OL_Y = y1 - OUTLINE_H - STATUS_H
    draw.rectangle([SB_X, OL_Y, SB_X+SB_W, y1-STATUS_H], fill=C["tab_bar"])
    draw.text((SB_X+10, OL_Y+6), "OUTLINE", fill=C["comment"], font=F_UI_B)
    oy = OL_Y + 22
    for indent, label, is_sec in outline_items:
        ox = SB_X + 8 + indent * 10
        col = C["outline_h"] if is_sec else C["dim"]
        draw.text((ox, oy), label, fill=col, font=F_UI)
        oy += LH_UI
        if oy > y1 - STATUS_H - 4:
            break

    # ── editor area ──
    ED_X = SB_X + SB_W
    ED_W = x1 - ED_X
    GUTTER = 38
    CODE_X = ED_X + GUTTER

    draw.rectangle([ED_X, y0, x1, y1], fill=C["bg"])

    # tab bar
    draw.rectangle([ED_X, y0, x1, y0+TAB_H], fill=C["tab_bar"])
    tab_w = min(len(filename)*9 + 30, 200)
    draw.rectangle([ED_X, y0, ED_X+tab_w, y0+TAB_H], fill=C["tab_act"])
    draw.line([ED_X+tab_w, y0, ED_X+tab_w, y0+TAB_H], fill=C["dim"], width=1)
    dot_col = C["type"] if cursor_li >= 0 else C["comment"]
    draw.ellipse([ED_X+8, y0+11, ED_X+18, y0+21], fill=dot_col)
    draw.text((ED_X+22, y0+8), filename, fill=C["text"], font=F_UI)

    # gutter
    draw.rectangle([ED_X, y0+TAB_H, ED_X+GUTTER, y1-STATUS_H], fill=C["sidebar"])

    # code lines
    vis = (H - y0 - TAB_H - STATUS_H - 8) // LH_CODE
    start = max(0, cursor_li - vis + 4)
    cy_base = y0 + TAB_H + 6
    for i, line in enumerate(code_lines[start:start+vis]):
        ln = start + i + 1
        cy = cy_base + i * LH_CODE
        draw.text((ED_X+4, cy), f"{ln:>3}", fill=C["ln"], font=F_UI)
        # highlight current line
        if start + i == cursor_li:
            draw.rectangle([ED_X+GUTTER, cy-1, x1, cy+LH_CODE-1], fill="#1e2030")
        # syntax highlight
        cx = CODE_X
        for tok, col in hl_tokens(line):
            draw.text((cx, cy), tok, fill=col, font=F_CODE)
            cx += draw.textlength(tok, font=F_CODE)
        if cx > x1 - 4:
            break

    # cursor bar
    if 0 <= cursor_li - start < vis:
        ci = cursor_li - start
        cur_line = code_lines[cursor_li] if cursor_li < len(code_lines) else ""
        cur_x = CODE_X + draw.textlength(cur_line, font=F_CODE)
        cur_y = cy_base + ci * LH_CODE
        draw.rectangle([cur_x, cur_y, cur_x+2, cur_y+LH_CODE-2], fill=C["text"])

    # status bar
    sb_y = y1 - STATUS_H
    draw.rectangle([x0, sb_y, x1, y1], fill=C["status"])
    draw.text((AB+10, sb_y+5), f"  {branch}  ↑2 ↓0  {lang}  ·  UTF-8  ·  LF  ·  {cols} cols",
              fill="#1a1b26", font=F_UI_B)
    draw.text((x1-80, sb_y+5), "GPU: H100", fill="#1a1b26", font=F_UI_B)


# ── draw the RIGHT post card ──────────────────────────────────────────────────
def draw_card(draw, headline_parts, bullets, accent=C["card_hi"]):
    """
    headline_parts : list of (text, is_highlight)
    bullets        : list of strings (use '→ ' prefix)
    """
    x0, y0, x1, y1 = HALF, 0, W, H
    draw.rectangle([x0, y0, x1, y1], fill=C["card_bg"])

    # padding
    px = x0 + 48
    py = y0 + 120

    # headline — word-wrap into ~18 chars per line, colour per part
    # render each part sequentially, wrapping at x1-48
    LINE_MAX = x1 - 48
    cx, cy = px, py
    line_h_head = 64

    def render_head_word(word, hi):
        nonlocal cx, cy
        col  = accent if hi else "#ffffff"
        font = F_HEAD
        tw = draw.textlength(word + " ", font=font)
        if cx + tw > LINE_MAX and cx > px:
            cx  = px
            cy += line_h_head
        draw.text((cx, cy), word, fill=col, font=font)
        cx += draw.textlength(word + " ", font=font)

    for text, hi in headline_parts:
        for word in text.split():
            render_head_word(word, hi)

    cy += line_h_head + 20

    # divider
    draw.rectangle([px, cy, px+120, cy+4], fill=accent)
    cy += 30

    # bullets
    for b in bullets:
        # wrap long lines
        wrapped = textwrap.wrap(b, width=28)
        for wi, wline in enumerate(wrapped):
            draw.text((px, cy), wline, fill=C["card_text"] if wi==0 else C["card_text"],
                      font=F_BULLET)
            cy += 34
        cy += 4


# ── frame builder ─────────────────────────────────────────────────────────────
def make_frames(ide_args_static, code_lines, term_output_ignored,
                headline_parts, bullets):
    """Animate code typing on left; right card is static throughout."""
    frames = []
    filename     = ide_args_static["filename"]
    project      = ide_args_static["project"]
    file_tree    = ide_args_static["file_tree"]
    outline      = ide_args_static["outline"]
    branch       = ide_args_static.get("branch", "main")
    lang         = ide_args_static.get("lang", "CUDA")

    typed = []

    def make_frame(typed_lines, cursor_li):
        img  = Image.new("RGB", (W, H), C["card_bg"])
        draw = ImageDraw.Draw(img)
        draw_ide(draw, img, filename, project, file_tree,
                 typed_lines, cursor_li, outline, branch, lang)
        draw_card(draw, headline_parts, bullets)
        return img

    # type code line by line
    for li, line in enumerate(code_lines):
        typed.append("")
        for ci, ch in enumerate(line):
            typed[-1] += ch
            if ci % 2 == 0:          # emit every 2nd char to cut frame count
                frames.append((make_frame(list(typed), li), 50))
        # end-of-line pause
        for _ in range(3):
            frames.append((make_frame(list(typed), li), 80))

    # cursor blink at end
    last = list(typed)
    last_li = len(code_lines) - 1
    for _ in range(5):
        frames.append((make_frame(last, last_li), 350))
        img2 = Image.new("RGB", (W, H), C["card_bg"])
        d2   = ImageDraw.Draw(img2)
        draw_ide(d2, img2, filename, project, file_tree,
                 last, -1, outline, branch, lang)
        draw_card(d2, headline_parts, bullets)
        frames.append((img2, 350))

    # hold
    final = make_frame(last, last_li)
    for _ in range(30):
        frames.append((final, 100))

    return frames


def save_gif(frames, path, colors=80):
    imgs = [f[0] for f in frames]
    durs = [f[1] for f in frames]
    # quantize
    qimgs = []
    for im in imgs:
        qimgs.append(im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT))
    qimgs[0].save(path, save_all=True, append_images=qimgs[1:],
                  duration=durs, loop=0, optimize=True)
    print(f"Saved {path}  ({os.path.getsize(path)//1024} KB, {len(frames)} frames)")


# ══════════════════════════════════════════════════════════════════════════════
#  POST 1 — GEMM tiled kernel  (main hook post)
# ══════════════════════════════════════════════════════════════════════════════
def post1():
    ide = dict(
        filename="03_gemm_tiled.cu",
        project="cuda-kernels-from-scratch",
        branch="main", lang="CUDA", cols=256,
        file_tree=[
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
        ],
        outline=[
            (0, "__global__ gemm_tiled", True),
            (1, "↳ load A tile → smem",  False),
            (1, "↳ load B tile → smem",  False),
            (1, "↳ __syncthreads()",     False),
            (1, "↳ tile-mma accumulate", False),
            (1, "↳ __syncthreads()",     False),
            (0, "host_launcher()",       True),
        ],
    )
    code = [
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
        "      acc += As[threadIdx.y][k]",
        "           * Bs[k][threadIdx.x];",
        "    __syncthreads();",
        "  }",
        "  C[row*N + col] = acc;",
        "}",
    ]
    hl = [
        ("Every AI engineer should learn to write ", False),
        ("exactly one CUDA kernel.", True),
    ]
    bullets = [
        "→ not because you'll write them at work",
        "→ because the mental model",
        "   changes everything",
        "→ ~200 lines.  one weekend.",
        "→ you'll never look at PyTorch",
        "   the same way again",
    ]
    frames = make_frames(ide, code, [], hl, bullets)
    save_gif(frames, f"{OUT}/post1.gif")


# ══════════════════════════════════════════════════════════════════════════════
#  POST 2 — Batch size / MFU
# ══════════════════════════════════════════════════════════════════════════════
def post2():
    ide = dict(
        filename="profile_mfu.py",
        project="gpu-profiling-toolkit",
        branch="main", lang="Python", cols=200,
        file_tree=[
            (0, "gpu-profiling-toolkit",  True,  False),
            (1, "src",                    True,  False),
            (2, "profile_mfu.py",         False, True ),
            (2, "memory_bandwidth.py",    False, False),
            (2, "kernel_occupancy.py",    False, False),
            (1, "results",                True,  False),
            (2, "mfu_vs_batch.csv",       False, False),
            (2, "mfu_vs_batch.png",       False, False),
            (0, "README.md",              False, False),
        ],
        outline=[
            (0, "bench(model, batch)", True),
            (1, "↳ warmup loop",       False),
            (1, "↳ timed loop",        False),
            (1, "↳ compute MFU",       False),
            (0, "main()",              True),
            (1, "↳ for batch in ...",  False),
        ],
    )
    code = [
        "import torch, time",
        "",
        "GPU_PEAK = 312e12  # A100 BF16",
        "",
        "def bench(model, batch):",
        "    x = torch.randn(batch, 512, 1024).cuda()",
        "    torch.cuda.synchronize()",
        "    t0 = time.perf_counter()",
        "    for _ in range(20): model(x, x)",
        "    torch.cuda.synchronize()",
        "    elapsed = (time.perf_counter() - t0) / 20",
        "    flops = 2 * batch * 512 * 1024 * 12 * 1024",
        "    mfu = flops / (elapsed * GPU_PEAK) * 100",
        "    print(f'batch={batch:>3}  MFU={mfu:.1f}%')",
        "",
        "model = torch.nn.Transformer(d_model=1024).cuda()",
        "for b in [1, 4, 16, 64, 128]:",
        "    bench(model, b)",
    ]
    hl = [
        ("Why is your GPU stuck at ", False),
        ("34%?", True),
        (" It's not the model.", False),
    ]
    bullets = [
        "→ it's memory access patterns",
        "→ batch=1   →  3% MFU",
        "→ batch=128 → 74% MFU",
        "→ same hardware, same model",
        "→ this is why batch size is",
        "   the first knob to tune",
    ]
    frames = make_frames(ide, code, [], hl, bullets)
    save_gif(frames, f"{OUT}/post2.gif")


# ══════════════════════════════════════════════════════════════════════════════
#  POST 3 — FP8 vs FP16
# ══════════════════════════════════════════════════════════════════════════════
def post3():
    ide = dict(
        filename="fp8_bench.py",
        project="precision-experiments",
        branch="main", lang="Python", cols=180,
        file_tree=[
            (0, "precision-experiments",  True,  False),
            (1, "src",                    True,  False),
            (2, "fp8_bench.py",           False, True ),
            (2, "fp16_baseline.py",       False, False),
            (2, "loss_scaling.py",        False, False),
            (1, "notebooks",              True,  False),
            (2, "fp8_analysis.ipynb",     False, False),
            (0, "requirements.txt",       False, False),
        ],
        outline=[
            (0, "bench(dtype, label)", True),
            (1, "↳ warmup",            False),
            (1, "↳ timed matmul",      False),
            (1, "↳ print ms/iter",     False),
            (0, "main",                True),
            (1, "↳ bench FP16",        False),
            (1, "↳ bench FP8",         False),
        ],
    )
    code = [
        "import torch, time",
        "",
        "SEQ, D = 2048, 4096",
        "",
        "def bench(dtype, label):",
        "    x = torch.randn(SEQ, D, dtype=dtype).cuda()",
        "    w = torch.randn(D, D,   dtype=dtype).cuda()",
        "    for _ in range(10): torch.matmul(x, w)  # warmup",
        "    torch.cuda.synchronize()",
        "    t = time.perf_counter()",
        "    for _ in range(200): torch.matmul(x, w)",
        "    torch.cuda.synchronize()",
        "    ms = (time.perf_counter()-t)/200*1e3",
        "    print(f'{label}: {ms:.2f} ms/iter')",
        "",
        "bench(torch.float16,       'FP16')",
        "bench(torch.float8_e4m3fn, 'FP8 ')",
    ]
    hl = [
        ("FP8 gives you ", False),
        ("2× throughput.", True),
        (" Here's why it works.", False),
    ]
    bullets = [
        "→ smaller dtype = more values",
        "   fit in a register",
        "→ FP16: 2.41 ms/iter",
        "→ FP8 : 1.19 ms/iter  (2×)",
        "→ same accuracy w/ loss scaling",
        "→ it's a load instruction change",
    ]
    frames = make_frames(ide, code, [], hl, bullets)
    save_gif(frames, f"{OUT}/post3.gif")


# ══════════════════════════════════════════════════════════════════════════════
#  POST 4 — Profiler / FlashAttention insight
# ══════════════════════════════════════════════════════════════════════════════
def post4():
    ide = dict(
        filename="05_flash_attention.cu",
        project="cuda-kernels-from-scratch",
        branch="main", lang="CUDA", cols=256,
        file_tree=[
            (0, "cuda-kernels-from-scratch", True,  False),
            (1, "src",                       True,  False),
            (2, "01_vector_add.cu",          False, False),
            (2, "02_matmul_naive.cu",        False, False),
            (2, "03_gemm_tiled.cu",          False, False),
            (2, "04_softmax.cu",             False, False),
            (2, "05_flash_attention.cu",     False, True ),
            (1, "bench",                     True,  False),
            (2, "bench.py",                  False, False),
            (0, "Makefile",                  False, False),
        ],
        outline=[
            (0, "__global__ flash_fwd",   True),
            (1, "↳ load Q block → smem",  False),
            (1, "↳ for K,V blocks ...",   False),
            (1, "↳ online softmax",       False),
            (1, "↳ accumulate output",    False),
            (0, "host_launcher()",        True),
        ],
    )
    code = [
        "// Flash Attention — O(N) HBM reads instead of O(N²)",
        "#define BLK 64",
        "",
        "__global__ void flash_fwd(",
        "    float* Q, float* K, float* V,",
        "    float* O, int N, int d) {",
        "  __shared__ float Qs[BLK][64];",
        "  __shared__ float Ks[BLK][64];",
        "  __shared__ float Vs[BLK][64];",
        "  float m = -1e9f, l = 0.f;",
        "  float acc[64] = {0};",
        "  // iterate K,V blocks — never store N×N",
        "  for (int j = 0; j < N/BLK; j++) {",
        "    load_tile(K, Ks, j, N, d);",
        "    load_tile(V, Vs, j, N, d);",
        "    online_softmax_update(Qs, Ks, Vs,",
        "                         acc, m, l, d);",
        "    __syncthreads();",
        "  }",
        "  write_output(O, acc, l);",
        "}",
    ]
    hl = [
        ("Read the ", False),
        ("FlashAttention paper", True),
        (" and actually understand it.", False),
    ]
    bullets = [
        "→ naive attn: O(N²) HBM reads",
        "→ flash attn: O(N)  HBM reads",
        "→ -88% memory bandwidth",
        "→ SM util: 31% → 84%",
        "→ you only see this after",
        "   writing a kernel yourself",
    ]
    frames = make_frames(ide, code, [], hl, bullets)
    save_gif(frames, f"{OUT}/post4.gif")


# ══════════════════════════════════════════════════════════════════════════════
#  POST 5 — Starter project call to action
# ══════════════════════════════════════════════════════════════════════════════
def post5():
    ide = dict(
        filename="why_kernels_matter.md",
        project="cuda-kernels-from-scratch",
        branch="main", lang="Markdown", cols=180,
        file_tree=[
            (0, "cuda-kernels-from-scratch", True,  False),
            (1, "src",                       True,  False),
            (2, "01_vector_add.cu",          False, False),
            (2, "02_matmul_naive.cu",        False, False),
            (2, "03_gemm_tiled.cu",          False, False),
            (2, "04_softmax.cu",             False, False),
            (2, "05_flash_attention.cu",     False, False),
            (1, "notes",                     True,  False),
            (2, "why_kernels_matter.md",     False, True ),
            (0, "README.md",                 False, False),
        ],
        outline=[
            (0, "# The Weekend Kernel",      True),
            (1, "## What to build",          False),
            (1, "## What you'll learn",      False),
            (1, "## Resources",              False),
        ],
    )
    code = [
        "# The Weekend Kernel",
        "",
        "## What to build",
        "GEMM with shared-memory tiling (~200 lines).",
        "",
        "## What you'll learn",
        "- Why memory access patterns matter more",
        "  than model size",
        "- Why batch size is the first perf knob",
        "- Why FP8 is a load instruction change",
        "- Why fused kernels exist",
        "- How to read a profiler trace",
        "",
        "## Resources",
        "- CUDA Programming Guide ch.5 (memory model)",
        "- Simon Boehm — How to Optimize a CUDA Matmul",
        "- Tri Dao — FlashAttention repo (read the CUDA)",
        "",
        "Have you written a CUDA kernel?",
        "Drop your story below. ↓",
    ]
    hl = [
        ("Have you written a ", False),
        ("CUDA kernel?", True),
        (" What did it teach you?", False),
    ]
    bullets = [
        "→ starter: GEMM with tiling",
        "→ ~200 lines of real CUDA C",
        "→ compare against cuBLAS",
        "→ read the Nsight profile",
        "→ drop your story below ↓",
    ]
    frames = make_frames(ide, code, [], hl, bullets)
    save_gif(frames, f"{OUT}/post5.gif")


if __name__ == "__main__":
    print("Generating GIFs …")
    post1()
    post2()
    post3()
    post4()
    post5()
    print("\nDone!")
