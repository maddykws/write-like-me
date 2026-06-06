# -*- coding: utf-8 -*-
"""Render 60 animated GIFs (terminal-style + EM-POV) and write matching post copy.

Outputs:
  output/gifs/post_NN.gif   animated GIF for each post
  output/posts/post_NN.md   LinkedIn copy for each post
  output/posts/post_NN.txt  plain-text copy (easy paste)
  60-day-linkedin-content.zip   everything, named by post number
"""
import os
import zipfile
import textwrap
from PIL import Image, ImageDraw, ImageFont

from content import POSTS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "output")
GIFS = os.path.join(OUT, "gifs")
POSTS_DIR = os.path.join(OUT, "posts")
for d in (GIFS, POSTS_DIR):
    os.makedirs(d, exist_ok=True)

# ---- canvas / fonts ----
W, H = 880, 480
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
F = ImageFont.truetype(MONO, 21)
FB = ImageFont.truetype(MONO_B, 21)
FT = ImageFont.truetype(MONO_B, 18)   # title bar
LINE_H = 30
PAD_X = 28
BODY_TOP = 88

# ---- terminal theme (dark, green prompt) ----
T = dict(
    bg="#0d1117", bar="#161b22", title="#8b949e",
    prompt="#7ee787", out="#c9d1d9", comment="#6e7681",
    dot1="#ff5f56", dot2="#ffbd2e", dot3="#27c93f",
    accent="#58a6ff", cursor="#7ee787",
)
# ---- EM theme (deep slate, amber/cyan accents) ----
E = dict(
    bg="#0b1220", bar="#13203a", title="#9fb3d1",
    head="#ffd479", done="#5ad19a", todo="#7fb2ff", note="#c4b5fd",
    box="#3b4a66", check="#5ad19a", dot1="#ff5f56", dot2="#ffbd2e", dot3="#27c93f",
    cursor="#ffd479",
)


def _bg(theme, title_text):
    img = Image.new("RGB", (W, H), theme["bg"])
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 56], fill=theme["bar"])
    for i, c in enumerate(("dot1", "dot2", "dot3")):
        d.ellipse([24 + i * 26, 22, 38 + i * 26, 36], fill=theme[c])
    tw = d.textlength(title_text, font=FT)
    d.text(((W - tw) / 2, 19), title_text, font=FT, fill=theme["title"])
    return img


def _save(frames, durations, path):
    frames[0].save(
        path, save_all=True, append_images=frames[1:],
        duration=durations, loop=0, optimize=True, disposal=2,
    )


# ============================ TERMINAL RENDERER ============================
def render_terminal(post):
    g = post["gif"]
    lines = g["lines"]  # list of (kind, text)
    color = {"prompt": T["prompt"], "output": T["out"], "comment": T["comment"]}

    # precompute display text per line ("$ " prefix for prompts)
    disp = []
    for kind, text in lines:
        disp.append((kind, ("$ " + text) if kind == "prompt" else text))

    frames, durs = [], []

    def base_with(n_complete, partial=None):
        """draw first n_complete lines fully, plus optional partial (kind,text,chars)."""
        img = _bg(T, g["title"])
        d = ImageDraw.Draw(img)
        y = BODY_TOP
        for i in range(n_complete):
            kind, text = disp[i]
            d.text((PAD_X, y), text, font=F, fill=color[kind])
            y += LINE_H
        if partial is not None:
            kind, text, ch = partial
            shown = text[:ch]
            d.text((PAD_X, y), shown, font=F, fill=color[kind])
            cx = PAD_X + d.textlength(shown, font=F)
            d.rectangle([cx + 1, y + 3, cx + 12, y + 24], fill=T["cursor"])
        return img

    # typewriter: reveal each line a few chars per frame
    for i, (kind, text) in enumerate(disp):
        step = 4 if kind != "comment" else 6
        for ch in range(0, len(text) + 1, step):
            frames.append(base_with(i, (kind, text, ch)))
            durs.append(18)
        # settle the completed line briefly
        frames.append(base_with(i + 1))
        durs.append(90 if kind == "prompt" else 60)

    # blinking cursor hold at the end
    full = base_with(len(disp))
    d = ImageDraw.Draw(full)
    cy = BODY_TOP + len(disp) * LINE_H
    for blink in range(4):
        f = full.copy()
        if blink % 2 == 0:
            dd = ImageDraw.Draw(f)
            dd.rectangle([PAD_X + 1, cy + 3, PAD_X + 12, cy + 24], fill=T["cursor"])
        frames.append(f)
        durs.append(420)
    return frames, durs


# ============================ EM-POV RENDERER ============================
def render_em(post):
    g = post["gif"]
    lines = g["lines"]  # list of (kind, text)

    frames, durs = [], []

    def draw_line(d, x, y, kind, text, checked=False):
        if kind == "head":
            d.text((x, y), text, font=FB, fill=E["head"])
        elif kind == "note":
            d.text((x, y), "› " + text, font=F, fill=E["note"])
        else:  # todo / done -> checkbox
            bx0, by0 = x, y + 3
            d.rectangle([bx0, by0, bx0 + 20, by0 + 20], outline=E["box"], width=2)
            if checked:
                # checkmark
                d.line([bx0 + 4, by0 + 11, bx0 + 9, by0 + 16], fill=E["check"], width=3)
                d.line([bx0 + 9, by0 + 16, bx0 + 17, by0 + 4], fill=E["check"], width=3)
            col = E["done"] if (kind == "done" or checked) else E["todo"]
            d.text((x + 34, y), text, font=F, fill=col)

    def frame(reveal, checks):
        """reveal = number of lines shown; checks = set of indices drawn checked."""
        img = _bg(E, g["title"])
        d = ImageDraw.Draw(img)
        y = BODY_TOP
        for i in range(reveal):
            kind, text = lines[i]
            chk = (i in checks) or (kind == "done" and i in checks)
            draw_line(d, PAD_X, y, kind, text, checked=(i in checks))
            y += LINE_H + (6 if kind == "head" else 4)
        return img

    # 1) reveal lines one by one
    revealed_checks = set()
    for i in range(len(lines)):
        frames.append(frame(i + 1, revealed_checks))
        durs.append(360)

    # 2) tick the checkboxes (done first, then todo) one at a time
    order = [i for i, (k, _) in enumerate(lines) if k in ("todo", "done")]
    for idx in order:
        revealed_checks.add(idx)
        frames.append(frame(len(lines), revealed_checks))
        durs.append(300)

    # 3) hold the completed card
    final = frame(len(lines), revealed_checks)
    frames.append(final)
    durs.append(1500)
    return frames, durs


# ============================ POST COPY ============================
def write_post(post):
    n = post["n"]
    tag = f"post_{n:02d}"
    day = n
    md = []
    md.append(f"# Post {n:02d} — Day {day}")
    md.append("")
    md.append(f"**Topic:** {post['topic']}  ")
    md.append(f"**GIF style:** {'Terminal output' if post['style']=='terminal' else 'Engineering Manager POV'}  ")
    md.append(f"**Attach:** `{tag}.gif`")
    md.append("")
    md.append("---")
    md.append("")
    md.append(post["post"])
    md.append("")
    with open(os.path.join(POSTS_DIR, f"{tag}.md"), "w") as f:
        f.write("\n".join(md))
    with open(os.path.join(POSTS_DIR, f"{tag}.txt"), "w") as f:
        f.write(post["post"] + "\n")


# ============================ DRIVER ============================
def main():
    index = ["# 60-Day LinkedIn Content Plan",
             "",
             "1 post/day. Attach the matching GIF (same post number).",
             "",
             "| # | Day | Topic | GIF style | Files |",
             "|---|-----|-------|-----------|-------|"]
    for post in POSTS:
        n = post["n"]
        tag = f"post_{n:02d}"
        if post["style"] == "terminal":
            frames, durs = render_terminal(post)
            style_label = "Terminal output"
        else:
            frames, durs = render_em(post)
            style_label = "Engineering Manager POV"
        _save(frames, durs, os.path.join(GIFS, f"{tag}.gif"))
        write_post(post)
        index.append(f"| {n} | {n} | {post['topic']} | {style_label} | {tag}.gif / {tag}.md |")
        print(f"  built {tag}  [{style_label:>24}]  frames={len(frames)}")

    with open(os.path.join(OUT, "INDEX.md"), "w") as f:
        f.write("\n".join(index) + "\n")

    # ---- zip everything, named by post number ----
    zip_path = os.path.join(ROOT, "60-day-linkedin-content.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(OUT, "INDEX.md"), "INDEX.md")
        for post in POSTS:
            tag = f"post_{post['n']:02d}"
            z.write(os.path.join(GIFS, f"{tag}.gif"), f"gifs/{tag}.gif")
            z.write(os.path.join(POSTS_DIR, f"{tag}.md"), f"posts/{tag}.md")
            z.write(os.path.join(POSTS_DIR, f"{tag}.txt"), f"posts/{tag}.txt")
    print(f"\nZIP: {zip_path}  ({os.path.getsize(zip_path)/1024:.0f} KB)")


if __name__ == "__main__":
    main()
