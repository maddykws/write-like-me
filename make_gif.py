"""
Generate a LinkedIn-ready animated GIF cycling through the
'7 things full-stack engineers don't know about GPU infra' post.

Output: gpu_infra_7_truths.gif (1080x1080, ~21s loop)
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ---------- design tokens ----------
W, H = 1080, 1080
BG = (10, 14, 26)           # near-black navy
PANEL = (18, 24, 42)        # card bg
ACCENT = (0, 230, 180)      # neon teal — GPU/tech feel
ACCENT_DIM = (0, 140, 110)
TEXT = (235, 240, 248)
TEXT_DIM = (150, 165, 185)
NUM_BG = (0, 230, 180)
NUM_FG = (10, 14, 26)
HASHTAG = (110, 200, 255)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

f_title = ImageFont.truetype(FONT_BOLD, 56)
f_title_sub = ImageFont.truetype(FONT_REG, 30)
f_num = ImageFont.truetype(FONT_MONO, 110)
f_headline = ImageFont.truetype(FONT_BOLD, 56)
f_body = ImageFont.truetype(FONT_REG, 36)
f_footer = ImageFont.truetype(FONT_BOLD, 26)
f_hash = ImageFont.truetype(FONT_REG, 24)

# ---------- content ----------
truths = [
    {
        "headline": "A GPU isn't a CPU\nwith more cores.",
        "body": "It's a streaming processor that\nhates branch logic. Your Python\nlist comprehension will embarrass you.",
    },
    {
        "headline": "CUDA OOM errors lie.",
        "body": "The number reported is rarely\nthe number that matters.\nFragmentation is the real killer.",
    },
    {
        "headline": "NCCL hangs aren't\nnetwork issues.",
        "body": "Usually one process died silently\nand 7 others are waiting for it\nforever.",
    },
    {
        "headline": "100% util on nvidia-smi\nmeans almost nothing.",
        "body": "SM occupancy is what you\nactually want.",
    },
    {
        "headline": "Multi-tenant GPUs\nare brutal.",
        "body": "There's no equivalent of cgroups\nfor VRAM. Scheduling fairness\nis still an open problem.",
    },
    {
        "headline": "The slowest GPU\nsets the pace.",
        "body": "Heterogeneous fleets break\ncollectives. Homogeneity isn't\noptional in distributed training.",
    },
    {
        "headline": "Storage will bottleneck\nbefore FLOPS will.",
        "body": "Plan your parallel filesystem\nbefore you plan your model.",
    },
]

# ---------- helpers ----------
def rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius,
                           fill=fill, outline=outline, width=width)

def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_centered_block(draw, text, font, y, color, line_spacing=10):
    lines = text.split("\n")
    total_h = 0
    sizes = []
    for ln in lines:
        w, h = text_size(draw, ln, font)
        sizes.append((w, h))
        total_h += h + line_spacing
    total_h -= line_spacing
    cur_y = y
    for ln, (w, h) in zip(lines, sizes):
        draw.text(((W - w) / 2, cur_y), ln, font=font, fill=color)
        cur_y += h + line_spacing
    return cur_y

# ---------- frame builders ----------
def build_intro_frame():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # accent bar top
    d.rectangle([0, 0, W, 8], fill=ACCENT)

    # eyebrow
    eyebrow = "FOR FULL-STACK ENGINEERS"
    w, _ = text_size(d, eyebrow, f_footer)
    d.text(((W - w) / 2, 220), eyebrow, font=f_footer, fill=ACCENT)

    # title
    title_main = "7 things you don't know"
    title_sub = "about GPU infra"
    title_low = "(until it breaks at 2 AM)"

    w, _ = text_size(d, title_main, f_title)
    d.text(((W - w) / 2, 290), title_main, font=f_title, fill=TEXT)
    w, _ = text_size(d, title_sub, f_title)
    d.text(((W - w) / 2, 365), title_sub, font=f_title, fill=TEXT)

    w, _ = text_size(d, title_low, f_title_sub)
    d.text(((W - w) / 2, 460), title_low, font=f_title_sub, fill=TEXT_DIM)

    # divider
    d.rectangle([W/2 - 60, 540, W/2 + 60, 544], fill=ACCENT)

    # subtle CTA
    cta = "Swipe through ↓"
    w, _ = text_size(d, cta, f_body)
    d.text(((W - w) / 2, 600), cta, font=f_body, fill=TEXT_DIM)

    # footer brand
    foot = "MADHAV V  ·  AI INFRASTRUCTURE"
    w, _ = text_size(d, foot, f_footer)
    d.text(((W - w) / 2, H - 80), foot, font=f_footer, fill=ACCENT_DIM)
    return img

def build_truth_frame(idx, item):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # accent bar top
    d.rectangle([0, 0, W, 8], fill=ACCENT)

    # counter top-right
    counter = f"{idx}/7"
    w, _ = text_size(d, counter, f_footer)
    d.text((W - w - 60, 40), counter, font=f_footer, fill=TEXT_DIM)

    # eyebrow
    eyebrow = "GPU INFRA TRUTH"
    d.text((60, 40), eyebrow, font=f_footer, fill=ACCENT)

    # big number badge
    badge_size = 160
    bx, by = 60, 140
    rounded_rect(d, (bx, by, bx + badge_size, by + badge_size), 28, fill=ACCENT)
    num_str = str(idx)
    nw, nh = text_size(d, num_str, f_num)
    d.text((bx + (badge_size - nw) / 2 - 4,
            by + (badge_size - nh) / 2 - 18),
           num_str, font=f_num, fill=NUM_FG)

    # headline (left aligned, beside/below badge)
    head_y = by + badge_size + 50
    for i, ln in enumerate(item["headline"].split("\n")):
        d.text((60, head_y + i * 70), ln, font=f_headline, fill=TEXT)

    # divider
    div_y = head_y + len(item["headline"].split("\n")) * 70 + 30
    d.rectangle([60, div_y, 160, div_y + 4], fill=ACCENT)

    # body
    body_y = div_y + 40
    for i, ln in enumerate(item["body"].split("\n")):
        d.text((60, body_y + i * 50), ln, font=f_body, fill=TEXT_DIM)

    # footer
    foot = "MADHAV V  ·  AI INFRASTRUCTURE  ·  GPU/HPC"
    d.text((60, H - 70), foot, font=f_footer, fill=ACCENT_DIM)

    # tag strip bottom-right
    tag = "#AIInfrastructure"
    w, _ = text_size(d, tag, f_hash)
    d.text((W - w - 60, H - 68), tag, font=f_hash, fill=HASHTAG)
    return img

def build_outro_frame():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 8], fill=ACCENT)

    eyebrow = "I'VE BROKEN ALL OF THESE."
    w, _ = text_size(d, eyebrow, f_footer)
    d.text(((W - w) / 2, 260), eyebrow, font=f_footer, fill=ACCENT)

    line1 = "8+ yrs full-stack."
    line2 = "2+ yrs AI platform."
    line3 = "Mostly on purpose."

    w, _ = text_size(d, line1, f_title)
    d.text(((W - w) / 2, 330), line1, font=f_title, fill=TEXT)
    w, _ = text_size(d, line2, f_title)
    d.text(((W - w) / 2, 410), line2, font=f_title, fill=TEXT)
    w, _ = text_size(d, line3, f_title)
    d.text(((W - w) / 2, 510), line3, font=f_title, fill=ACCENT)

    d.rectangle([W/2 - 60, 620, W/2 + 60, 624], fill=ACCENT)

    q = "Which one bit you first?"
    w, _ = text_size(d, q, f_body)
    d.text(((W - w) / 2, 680), q, font=f_body, fill=TEXT_DIM)

    tags = "#AIInfrastructure  #GPU  #HPC  #FullStack  #MLOps"
    w, _ = text_size(d, tags, f_hash)
    d.text(((W - w) / 2, H - 130), tags, font=f_hash, fill=HASHTAG)

    foot = "MADHAV V  ·  AI INFRASTRUCTURE"
    w, _ = text_size(d, foot, f_footer)
    d.text(((W - w) / 2, H - 80), foot, font=f_footer, fill=ACCENT_DIM)
    return img

# ---------- assemble ----------
frames = []
durations = []

# intro
frames.append(build_intro_frame())
durations.append(2500)  # 2.5s

# 7 truths
for i, item in enumerate(truths, start=1):
    frames.append(build_truth_frame(i, item))
    durations.append(2800)  # 2.8s each

# outro
frames.append(build_outro_frame())
durations.append(3500)  # 3.5s

out = Path("/home/user/write-like-me/gpu_infra_7_truths.gif")
frames[0].save(
    out,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    optimize=True,
    disposal=2,
)

print(f"wrote {out}  ({out.stat().st_size/1024:.0f} KB, {len(frames)} frames)")
