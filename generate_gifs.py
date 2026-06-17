#!/usr/bin/env python3
"""Generate terminal-style animated GIFs for social media posts."""

from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = "/home/user/write-like-me/post_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 800, 420
FONT_SIZE = 15
try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", FONT_SIZE)
    FONT_BOLD = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", FONT_SIZE)
except:
    FONT = ImageFont.load_default()
    FONT_BOLD = FONT

LINE_H = 20
PAD = 20


def char_frames(bg, fg, lines, title="terminal", blink_cursor=True, extra_static=15):
    """Return a list of PIL frames typing out `lines` char by char."""
    frames = []
    typed = []  # list of (line_idx, char_idx_end)

    # flatten to list of (line, chars_revealed)
    full_text = []
    for line in lines:
        full_text.append(line)

    def render(revealed_lines, show_cursor):
        img = Image.new("RGB", (W, H), bg)
        draw = ImageDraw.Draw(img)
        # title bar
        draw.rectangle([0, 0, W, 28], fill="#2d2d2d" if bg != "#0d1117" else "#161b22")
        draw.ellipse([10, 8, 22, 20], fill="#ff5f56")
        draw.ellipse([26, 8, 38, 20], fill="#ffbd2e")
        draw.ellipse([42, 8, 54, 20], fill="#27c93f")
        draw.text((W // 2 - 40, 7), title, fill="#888", font=FONT)
        y = 38
        for i, rline in enumerate(revealed_lines):
            draw.text((PAD, y), rline, fill=fg, font=FONT)
            y += LINE_H
        if show_cursor and revealed_lines:
            last = revealed_lines[-1]
            cx = PAD + draw.textlength(last, font=FONT)
            cy = 38 + (len(revealed_lines) - 1) * LINE_H
            draw.rectangle([cx + 1, cy, cx + 9, cy + FONT_SIZE], fill=fg)
        return img

    # build char-by-char frames
    current = []
    for line in full_text:
        current.append("")
        for ch in line:
            current[-1] += ch
            frames.append((render(list(current), True), 40))
        # pause at end of line
        for _ in range(3):
            frames.append((render(list(current), True), 80))

    # blink cursor at end
    last_state = list(current)
    for _ in range(6):
        frames.append((render(last_state, True), 300))
        frames.append((render(last_state, False), 300))

    # hold last frame
    for _ in range(extra_static):
        frames.append((render(last_state, False), 100))

    return frames


def save_gif(frames, path):
    images = [f[0] for f in frames]
    durations = [f[1] for f in frames]
    images[0].save(
        path,
        save_all=True,
        append_images=images[1:],
        duration=durations,
        loop=0,
        optimize=False,
    )
    print(f"Saved {path}")


# ── GIF 1: Classic green-on-black terminal — CUDA kernel snippet ──
def gif1():
    bg = "#0a0a0a"
    fg = "#00ff41"
    lines = [
        "$ nvcc -O3 gemm_tiled.cu -o gemm",
        "",
        "// CUDA GEMM with shared memory tiling",
        "__global__ void gemm_tiled(",
        "    float* A, float* B, float* C,",
        "    int M, int N, int K) {",
        "  __shared__ float As[TILE][TILE];",
        "  __shared__ float Bs[TILE][TILE];",
        "  // load tile → compute → accumulate",
        "  ...",
        "}",
        "",
        "✓ Compiled. Weekend well spent.",
    ]
    frames = char_frames(bg, fg, lines, title="bash — cuda_kernel", extra_static=20)
    save_gif(frames, f"{OUTPUT_DIR}/gif1_green_terminal.gif")


# ── GIF 2: Dark VS-Code-style editor — batch size insight ──
def gif2():
    bg = "#1e1e1e"
    fg = "#d4d4d4"

    def render_vscode(revealed, show_cursor):
        img = Image.new("RGB", (W, H), bg)
        draw = ImageDraw.Draw(img)
        # top bar
        draw.rectangle([0, 0, W, 28], fill="#323232")
        draw.text((W // 2 - 60, 7), "insight.py — write-like-me", fill="#ccc", font=FONT)
        # line numbers gutter
        draw.rectangle([0, 28, 44, H], fill="#252526")
        y = 38
        keyword_color = "#569cd6"
        string_color = "#ce9178"
        comment_color = "#6a9955"
        colors = {
            "import": keyword_color, "def": keyword_color,
            "return": keyword_color, "#": comment_color,
        }
        for i, line in enumerate(revealed, 1):
            draw.text((6, y), f"{i:>2}", fill="#555", font=FONT)
            # simple keyword highlight on first word
            first = line.lstrip().split(" ")[0] if line.strip() else ""
            col = colors.get(first, fg)
            if line.lstrip().startswith("#"):
                col = comment_color
            elif '"""' in line or "'''" in line:
                col = string_color
            draw.text((50, y), line, fill=col, font=FONT)
            y += LINE_H
        if show_cursor and revealed:
            last = revealed[-1]
            cx = 50 + draw.textlength(last, font=FONT)
            cy = 38 + (len(revealed) - 1) * LINE_H
            draw.rectangle([cx + 1, cy, cx + 2, cy + FONT_SIZE], fill="#aeafad")
        return img

    lines = [
        "# Why batch size matters in GPU compute",
        "",
        "import torch",
        "",
        "def utilization(batch: int, seq: int) -> float:",
        '    """Larger batches → better memory coalescing."""',
        "    tokens = batch * seq",
        "    flops = 2 * tokens * D_MODEL * N_LAYERS",
        "    return flops / GPU_PEAK_FLOPS",
        "",
        "# batch=1  → ~12% MFU",
        "# batch=32 → ~68% MFU   ← this is why",
    ]
    frames = []
    current = []
    for line in lines:
        current.append("")
        for ch in line:
            current[-1] += ch
            frames.append((render_vscode(list(current), True), 40))
        for _ in range(3):
            frames.append((render_vscode(list(current), True), 80))
    last_state = list(current)
    for _ in range(6):
        frames.append((render_vscode(last_state, True), 300))
        frames.append((render_vscode(last_state, False), 300))
    for _ in range(20):
        frames.append((render_vscode(last_state, False), 100))

    save_gif(frames, f"{OUTPUT_DIR}/gif2_vscode_dark.gif")


# ── GIF 3: Matrix rain + code reveal — FP8 / precision ──
def gif3():
    import random, math
    random.seed(42)
    bg = "#000000"
    fg_bright = "#00ff41"
    fg_dim = "#003d0f"
    COLS = W // 10
    drops = [random.randint(-H // LINE_H, 0) for _ in range(COLS)]
    chars_pool = list("01アイウエオカキクABCDEF[]{}()=>+-*/0123456789")

    code_lines = [
        "__global__ void fp8_matmul(",
        "    __nv_fp8_e4m3* A,",
        "    __nv_fp8_e4m3* B,",
        "    float*         C) {",
        "  // 2x throughput vs FP16",
        "  // same accuracy with loss scaling",
        "}",
    ]
    total_rain = 30
    reveal_start = 18
    total_frames = total_rain + len(code_lines) * 5 + 20

    frames = []
    for f in range(total_frames):
        img = Image.new("RGB", (W, H), bg)
        draw = ImageDraw.Draw(img)

        # matrix rain
        if f < total_rain + 5:
            for col_i, drop in enumerate(drops):
                x = col_i * 10
                for row in range(max(0, drop - 8), min(H // LINE_H, drop + 1)):
                    ch = random.choice(chars_pool)
                    color = fg_bright if row == drop else fg_dim
                    draw.text((x, row * LINE_H), ch, fill=color, font=FONT)
            # advance drops
            for i in range(COLS):
                drops[i] += 1
                if drops[i] > H // LINE_H + 8:
                    drops[i] = random.randint(-20, -1)

        # fade in code overlay
        if f >= reveal_start:
            rel = f - reveal_start
            lines_shown = min(rel // 5 + 1, len(code_lines))
            overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            od = ImageDraw.Draw(overlay)
            od.rectangle([60, H // 2 - 90, W - 60, H // 2 + 90], fill=(0, 20, 0, 200))
            img = img.convert("RGBA")
            img = Image.alpha_composite(img, overlay).convert("RGB")
            draw = ImageDraw.Draw(img)
            for li in range(lines_shown):
                draw.text((80, H // 2 - 80 + li * LINE_H), code_lines[li], fill=fg_bright, font=FONT)

        frames.append((img, 60))

    # hold
    for _ in range(20):
        frames.append((frames[-1][0], 100))

    save_gif(frames, f"{OUTPUT_DIR}/gif3_matrix_rain.gif")


# ── GIF 4: Split-pane terminal — before/after mental model ──
def gif4():
    bg = "#0f111a"
    left_fg = "#ff6b6b"   # "before" — red/confused
    right_fg = "#69ff47"  # "after"  — green/clear
    divider = W // 2

    before_lines = [
        "# Before CUDA",
        "$ python train.py",
        "... epoch 1 slow ...",
        "... epoch 2 slow ...",
        "?? why is GPU at 34%",
        "?? model is just slow",
        ">> buy bigger GPU??",
    ]
    after_lines = [
        "# After CUDA kernel",
        "$ ncu profile train.py",
        "→ memory bandwidth: 38%",
        "→ bad access pattern!",
        "→ fuse ops + tile data",
        "✓ GPU util: 91%",
        "✓ 2.6x faster, same hw",
    ]

    def render_split(bl, al, cursor_side, show_cursor):
        img = Image.new("RGB", (W, H), bg)
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, W, 28], fill="#1a1d27")
        draw.text((divider // 2 - 30, 7), "BEFORE", fill=left_fg, font=FONT_BOLD)
        draw.text((divider + divider // 2 - 25, 7), "AFTER", fill=right_fg, font=FONT_BOLD)
        draw.line([divider, 0, divider, H], fill="#333", width=2)
        y = 38
        for i, line in enumerate(bl):
            draw.text((PAD, y + i * LINE_H), line, fill=left_fg, font=FONT)
        for i, line in enumerate(al):
            draw.text((divider + PAD, y + i * LINE_H), line, fill=right_fg, font=FONT)
        if show_cursor:
            if cursor_side == "left" and bl:
                last = bl[-1]
                cx = PAD + draw.textlength(last, font=FONT)
                cy = 38 + (len(bl) - 1) * LINE_H
                draw.rectangle([cx + 1, cy, cx + 9, cy + FONT_SIZE], fill=left_fg)
            elif cursor_side == "right" and al:
                last = al[-1]
                cx = divider + PAD + draw.textlength(last, font=FONT)
                cy = 38 + (len(al) - 1) * LINE_H
                draw.rectangle([cx + 1, cy, cx + 9, cy + FONT_SIZE], fill=right_fg)
        return img

    frames = []
    bl, al = [], []
    # type left side
    for line in before_lines:
        bl.append("")
        for ch in line:
            bl[-1] += ch
            frames.append((render_split(list(bl), list(al), "left", True), 45))
        for _ in range(4):
            frames.append((render_split(list(bl), list(al), "left", True), 80))
    # type right side
    for line in after_lines:
        al.append("")
        for ch in line:
            al[-1] += ch
            frames.append((render_split(list(bl), list(al), "right", True), 45))
        for _ in range(4):
            frames.append((render_split(list(bl), list(al), "right", True), 80))
    # blink
    last_bl, last_al = list(bl), list(al)
    for _ in range(5):
        frames.append((render_split(last_bl, last_al, "right", True), 350))
        frames.append((render_split(last_bl, last_al, "right", False), 350))
    for _ in range(25):
        frames.append((render_split(last_bl, last_al, "right", False), 100))

    save_gif(frames, f"{OUTPUT_DIR}/gif4_split_pane.gif")


# ── GIF 5: Retro amber terminal — call to action ──
def gif5():
    bg = "#1a0d00"
    fg = "#ffb347"
    lines = [
        "$ echo 'Have you written a CUDA kernel?'",
        "",
        "> GEMM with tiling: weekend project",
        "> ~200 lines of CUDA",
        "> teaches you more than 10 ML papers",
        "",
        "$ git clone cuda-gemm-starter",
        "Cloning into 'cuda-gemm-starter'...",
        "remote: objects: 42, done.",
        "",
        "# Drop your kernel story below ↓",
    ]
    frames = char_frames(bg, fg, lines, title="amber — share your kernel", extra_static=25)
    save_gif(frames, f"{OUTPUT_DIR}/gif5_amber_terminal.gif")


if __name__ == "__main__":
    print("Generating GIFs...")
    gif1()
    gif2()
    gif3()
    gif4()
    gif5()
    print("Done! All GIFs saved to", OUTPUT_DIR)
