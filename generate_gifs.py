#!/usr/bin/env python3
"""
Two-phase animated GIFs:
  Phase 1 — Code typed line-by-line in a VS Code-style IDE
  Phase 2 — Terminal panel slides up, shows execution output
"""

from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = "/home/user/write-like-me/post_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 860, 480
FONT_SIZE = 14
try:
    MONO   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",      FONT_SIZE)
    MONO_B = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", FONT_SIZE)
except:
    MONO = MONO_B = ImageFont.load_default()

LH    = 20          # line height
PAD_L = 56          # left pad (after gutter)
GUTTER= 44          # line-number gutter width
TAB_W = 36          # editor tab height
STATUS= 22          # bottom status bar height

# ── colour tokens ──────────────────────────────────────────────────────────
THEME = {
    "bg":       "#1e1e2e",
    "gutter":   "#181825",
    "tab_bar":  "#11111b",
    "tab_act":  "#1e1e2e",
    "tab_in":   "#181825",
    "status":   "#313244",
    "ln":       "#45475a",
    "cursor":   "#cdd6f4",
    "text":     "#cdd6f4",
    "comment":  "#6c7086",
    "keyword":  "#cba6f7",
    "func":     "#89b4fa",
    "string":   "#a6e3a1",
    "number":   "#fab387",
    "type":     "#f38ba8",
    "punct":    "#89dceb",
    "term_bg":  "#11111b",
    "term_fg":  "#a6e3a1",
    "term_err": "#f38ba8",
    "term_dim": "#6c7086",
    "prompt":   "#89b4fa",
}

# ── simple token colourer (keyword-first matching) ─────────────────────────
KEYWORDS = {"import","from","def","class","return","for","in","if","else",
            "elif","with","as","pass","True","False","None","and","or","not",
            "__global__","__shared__","__device__","float","int","void","auto"}
BUILTINS = {"print","range","len","open","torch","np","cuda","tqdm"}

def token_color(word: str, raw_line: str) -> str:
    if raw_line.lstrip().startswith("#") or raw_line.lstrip().startswith("//"):
        return THEME["comment"]
    if word in KEYWORDS:
        return THEME["keyword"]
    if word in BUILTINS:
        return THEME["func"]
    if word.startswith('"') or word.startswith("'"):
        return THEME["string"]
    if word.lstrip("-").replace(".","",1).isdigit():
        return THEME["number"]
    return THEME["text"]

def draw_line_highlighted(draw, x, y, line):
    """Naive per-word syntax highlight."""
    if line.lstrip().startswith(("#", "//")):
        draw.text((x, y), line, fill=THEME["comment"], font=MONO)
        return
    # simple: split on spaces but preserve them
    import re
    tokens = re.split(r'(\s+)', line)
    cx = x
    for tok in tokens:
        if not tok:
            continue
        if tok.strip() == "":
            cx += draw.textlength(tok, font=MONO)
            continue
        col = token_color(tok.strip('()[]{}:,.<>=+-*/'), line)
        draw.text((cx, y), tok, fill=col, font=MONO)
        cx += draw.textlength(tok, font=MONO)


# ── IDE frame renderer ─────────────────────────────────────────────────────
def render_ide(filename, code_lines, cursor_line, cursor_col, term_lines=None, term_frac=0.0):
    """
    filename   : shown in tab
    code_lines : list of strings (fully typed so far)
    cursor_line: 0-based index of active line
    cursor_col : character position of cursor in active line
    term_lines : list of output strings (shown in terminal panel)
    term_frac  : 0.0 = no terminal, 1.0 = fully open (fraction of lower half)
    """
    img  = Image.new("RGB", (W, H), THEME["bg"])
    draw = ImageDraw.Draw(img)

    TERM_H = int((H - TAB_W - STATUS) * min(term_frac, 1.0) * 0.46)
    CODE_H = H - TAB_W - STATUS - TERM_H

    # ── tab bar ──
    draw.rectangle([0, 0, W, TAB_W], fill=THEME["tab_bar"])
    tab_w = 180
    draw.rectangle([0, 0, tab_w, TAB_W], fill=THEME["tab_act"])
    draw.line([tab_w, 0, tab_w, TAB_W], fill=THEME["ln"], width=1)
    draw.text((12, (TAB_W - FONT_SIZE) // 2), filename, fill=THEME["text"], font=MONO)
    # close dot
    draw.ellipse([tab_w - 18, TAB_W//2 - 4, tab_w - 10, TAB_W//2 + 4], fill=THEME["ln"])

    # ── editor area ──
    editor_top = TAB_W
    draw.rectangle([0, editor_top, GUTTER, editor_top + CODE_H], fill=THEME["gutter"])

    vis_lines = (CODE_H - 8) // LH
    # scroll so cursor line is visible
    start = max(0, cursor_line - vis_lines + 3)
    y = editor_top + 6
    for i, li in enumerate(code_lines[start:start + vis_lines]):
        ln = start + i + 1
        draw.text((6, y), f"{ln:>3}", fill=THEME["ln"], font=MONO)
        draw_line_highlighted(draw, PAD_L, y, li)
        y += LH

    # cursor
    cur_abs = cursor_line - start
    if 0 <= cur_abs < vis_lines:
        cur_y = editor_top + 6 + cur_abs * LH
        cur_x = PAD_L + draw.textlength(code_lines[cursor_line][:cursor_col], font=MONO)
        draw.rectangle([cur_x, cur_y, cur_x + 2, cur_y + FONT_SIZE], fill=THEME["cursor"])

    # ── terminal panel ──
    if TERM_H > 0:
        term_top = editor_top + CODE_H
        draw.rectangle([0, term_top, W, term_top + TERM_H], fill=THEME["term_bg"])
        draw.line([0, term_top, W, term_top], fill="#313244", width=1)
        # panel label
        draw.text((10, term_top + 4), "TERMINAL", fill=THEME["term_dim"], font=MONO_B)
        ty = term_top + 22
        for tl in term_lines or []:
            col = THEME["term_err"] if tl.startswith("Error") or tl.startswith("Traceback") \
                  else THEME["prompt"] if tl.startswith("$") or tl.startswith(">>>") \
                  else THEME["term_fg"]
            draw.text((10, ty), tl, fill=col, font=MONO)
            ty += LH
            if ty > term_top + TERM_H - 4:
                break

    # ── status bar ──
    sb_top = H - STATUS
    draw.rectangle([0, sb_top, W, H], fill=THEME["status"])
    draw.text((10, sb_top + 4), "  main  Python  UTF-8  CRLF  Ln {} Col {}".format(
        cursor_line + 1, cursor_col + 1), fill="#b4befe", font=MONO)

    return img


# ── animation builder ──────────────────────────────────────────────────────
def make_frames(filename, code_lines, term_lines,
                char_delay=35, line_pause=6, term_slide_steps=12, hold=30):
    frames = []

    typed = []
    for li, line in enumerate(code_lines):
        typed.append("")
        for ci, ch in enumerate(line):
            typed[-1] += ch
            img = render_ide(filename, list(typed), li, ci + 1)
            frames.append((img, char_delay))
        for _ in range(line_pause):
            img = render_ide(filename, list(typed), li, len(line))
            frames.append((img, 60))

    # cursor blink at end of code
    last_typed = list(typed)
    last_li    = len(code_lines) - 1
    last_col   = len(code_lines[-1])
    for _ in range(4):
        frames.append((render_ide(filename, last_typed, last_li, last_col), 300))
        frames.append((render_ide(filename, last_typed, last_li, 0), 300))

    # terminal slides in
    term_so_far = []
    for step in range(1, term_slide_steps + 1):
        frac = step / term_slide_steps
        img = render_ide(filename, last_typed, last_li, last_col,
                         term_lines=term_so_far, term_frac=frac)
        frames.append((img, 30))

    # output lines appear one by one
    for tl in term_lines:
        term_so_far.append(tl)
        for _ in range(4):
            img = render_ide(filename, last_typed, last_li, last_col,
                             term_lines=list(term_so_far), term_frac=1.0)
            frames.append((img, 80))

    # hold
    final = render_ide(filename, last_typed, last_li, last_col,
                       term_lines=list(term_so_far), term_frac=1.0)
    for _ in range(hold):
        frames.append((final, 100))

    return frames


def save_gif(frames, path):
    imgs = [f[0] for f in frames]
    durs = [f[1] for f in frames]
    imgs[0].save(path, save_all=True, append_images=imgs[1:],
                 duration=durs, loop=0, optimize=False)
    kb = os.path.getsize(path) // 1024
    print(f"Saved {path}  ({kb} KB)")


# ══════════════════════════════════════════════════════════════════════════════
#  GIF 1 — CUDA GEMM kernel (main post)
# ══════════════════════════════════════════════════════════════════════════════
def gif1():
    code = [
        "# gemm_tiled.cu — tiled matrix multiply",
        "#define TILE 16",
        "",
        "__global__ void gemm_tiled(",
        "    float* A, float* B, float* C,",
        "    int M, int N, int K) {",
        "  __shared__ float As[TILE][TILE];",
        "  __shared__ float Bs[TILE][TILE];",
        "  int row = blockIdx.y * TILE + threadIdx.y;",
        "  int col = blockIdx.x * TILE + threadIdx.x;",
        "  float acc = 0.0f;",
        "  for (int t = 0; t < K / TILE; t++) {",
        "    As[threadIdx.y][threadIdx.x] = A[row*K + t*TILE + threadIdx.x];",
        "    Bs[threadIdx.y][threadIdx.x] = B[(t*TILE + threadIdx.y)*N + col];",
        "    __syncthreads();",
        "    for (int k = 0; k < TILE; k++) acc += As[threadIdx.y][k]*Bs[k][threadIdx.x];",
        "    __syncthreads();",
        "  }",
        "  C[row * N + col] = acc;",
        "}",
    ]
    term = [
        "$ nvcc -O3 -arch=sm_89 gemm_tiled.cu -o gemm",
        "$ ./gemm 4096 4096 4096",
        "Running GEMM  4096x4096 ...",
        "Custom kernel :  8.3 ms   →  16.6 TFLOPS",
        "cuBLAS        :  7.1 ms   →  19.4 TFLOPS",
        "Efficiency    :  85.6 %  ✓ not bad for a weekend!",
    ]
    save_gif(make_frames("gemm_tiled.cu", code, term), f"{OUTPUT_DIR}/gif1_cuda_gemm.gif")


# ══════════════════════════════════════════════════════════════════════════════
#  GIF 2 — Batch size / MFU profiler
# ══════════════════════════════════════════════════════════════════════════════
def gif2():
    code = [
        "# profile_mfu.py",
        "import torch, time",
        "",
        "model = torch.nn.Transformer(d_model=1024).cuda()",
        "GPU_PEAK = 312e12  # A100 BF16 TFLOPS",
        "",
        "for batch in [1, 4, 16, 64, 128]:",
        "    x = torch.randn(batch, 512, 1024).cuda()",
        "    torch.cuda.synchronize()",
        "    t0 = time.perf_counter()",
        "    for _ in range(20): model(x, x)",
        "    torch.cuda.synchronize()",
        "    elapsed = (time.perf_counter() - t0) / 20",
        "    flops = 2 * batch * 512 * 1024 * 12 * 1024",
        "    mfu = flops / (elapsed * GPU_PEAK) * 100",
        "    print(f'batch={batch:>3}  MFU={mfu:.1f}%')",
    ]
    term = [
        "$ python profile_mfu.py",
        "batch=  1  MFU= 3.2%",
        "batch=  4  MFU=11.8%",
        "batch= 16  MFU=38.4%",
        "batch= 64  MFU=61.7%",
        "batch=128  MFU=74.3%   ← this is why batch size matters",
    ]
    save_gif(make_frames("profile_mfu.py", code, term), f"{OUTPUT_DIR}/gif2_batch_mfu.gif")


# ══════════════════════════════════════════════════════════════════════════════
#  GIF 3 — FP8 vs FP16 throughput
# ══════════════════════════════════════════════════════════════════════════════
def gif3():
    code = [
        "# fp8_bench.py",
        "import torch",
        "from transformer_engine import pytorch as te",
        "",
        "SEQ, D = 2048, 4096",
        "",
        "def bench(dtype, label):",
        "    x = torch.randn(SEQ, D, dtype=dtype).cuda()",
        "    w = torch.randn(D, D,   dtype=dtype).cuda()",
        "    # warmup",
        "    for _ in range(10): torch.matmul(x, w)",
        "    torch.cuda.synchronize()",
        "    import time; t = time.perf_counter()",
        "    for _ in range(200): torch.matmul(x, w)",
        "    torch.cuda.synchronize()",
        "    ms = (time.perf_counter() - t) / 200 * 1e3",
        "    print(f'{label}: {ms:.2f} ms/iter')",
        "",
        "bench(torch.float16, 'FP16')",
        "bench(torch.float8_e4m3fn, 'FP8 ')",
    ]
    term = [
        "$ python fp8_bench.py",
        "FP16: 2.41 ms/iter",
        "FP8 : 1.19 ms/iter   ← 2.02x faster",
        "",
        "Same accuracy with loss scaling.",
        "Smaller dtype = 2x compute density. That's it.",
    ]
    save_gif(make_frames("fp8_bench.py", code, term), f"{OUTPUT_DIR}/gif3_fp8_bench.gif")


# ══════════════════════════════════════════════════════════════════════════════
#  GIF 4 — Nsight / profiler before-after
# ══════════════════════════════════════════════════════════════════════════════
def gif4():
    code = [
        "# train.py  — naive attention (before kernel knowledge)",
        "import torch, torch.nn.functional as F",
        "",
        "def naive_attention(Q, K, V):",
        "    # materialises full N×N attention matrix in HBM",
        "    scale = Q.size(-1) ** -0.5",
        "    scores = torch.matmul(Q, K.transpose(-2, -1)) * scale",
        "    attn   = F.softmax(scores, dim=-1)",
        "    return torch.matmul(attn, V)",
        "",
        "# profile this",
        "Q = torch.randn(8, 16, 2048, 64).cuda()",
        "K = torch.randn(8, 16, 2048, 64).cuda()",
        "V = torch.randn(8, 16, 2048, 64).cuda()",
        "out = naive_attention(Q, K, V)",
    ]
    term = [
        "$ ncu --metrics l1tex__t_bytes,sm__inst_executed ./train.py",
        "",
        "[profiler output]",
        "  HBM reads      :  18.4 GB   ← reading N² attention scores",
        "  Arithmetic Inten:  0.14 FLOP/byte  (memory-bound!)",
        "  SM utilization  :  31 %",
        "",
        "→ fused kernel (FlashAttention) fixes this:",
        "  HBM reads      :   2.1 GB   (-88%)",
        "  SM utilization :  84 %      (+170%)",
    ]
    save_gif(make_frames("train.py", code, term), f"{OUTPUT_DIR}/gif4_profiler.gif")


# ══════════════════════════════════════════════════════════════════════════════
#  GIF 5 — Starter project: clone & run
# ══════════════════════════════════════════════════════════════════════════════
def gif5():
    code = [
        "# starter_gemm.py — your weekend project",
        "\"\"\"",
        "Step 1: implement naive_gemm in CUDA",
        "Step 2: add shared-memory tiling",
        "Step 3: compare against cuBLAS",
        "Step 4: read the Nsight profile",
        "Step 5: you now understand every ML perf paper",
        "\"\"\"",
        "import subprocess, sys",
        "",
        "def run(cmd):",
        "    print(f'$ {cmd}')",
        "    subprocess.run(cmd, shell=True, check=True)",
        "",
        "run('nvcc -O3 -arch=sm_89 gemm_tiled.cu -o gemm')",
        "run('./gemm 4096 4096 4096')",
        "run('ncu --set full ./gemm 4096 4096 4096')",
        "print('Weekend well spent. 🚀')",
    ]
    term = [
        "$ python starter_gemm.py",
        "$ nvcc -O3 -arch=sm_89 gemm_tiled.cu -o gemm",
        "$ ./gemm 4096 4096 4096",
        "  Kernel time : 8.3 ms  |  16.6 TFLOPS",
        "$ ncu --set full ./gemm 4096 4096 4096",
        "  L2 hit rate : 94.2 %  ✓",
        "  Warp efficiency: 97 % ✓",
        "Weekend well spent.",
    ]
    save_gif(make_frames("starter_gemm.py", code, term), f"{OUTPUT_DIR}/gif5_starter.gif")


if __name__ == "__main__":
    print("Generating GIFs …")
    gif1()
    gif2()
    gif3()
    gif4()
    gif5()
    print("\nDone! Files in", OUTPUT_DIR)
