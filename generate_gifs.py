"""Generate 30 LinkedIn GIFs, one per day of the campaign."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = "/home/user/write-like-me/gifs"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 900, 500
BG = (15, 23, 42)
PANEL = (30, 41, 59)
ACCENT = (56, 189, 248)
ACCENT2 = (167, 139, 250)
ACCENT3 = (52, 211, 153)
ACCENT4 = (251, 146, 60)
ACCENT5 = (244, 114, 182)
WHITE = (248, 250, 252)
MUTED = (148, 163, 184)
CHIP_BG = (51, 65, 85)
CHIP_TEXT = (226, 232, 240)
GREEN = (34, 197, 94)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

f_day    = ImageFont.truetype(BOLD, 14)
f_name   = ImageFont.truetype(BOLD, 34)
f_title  = ImageFont.truetype(BOLD, 40)
f_title_lg = ImageFont.truetype(BOLD, 48)
f_sub    = ImageFont.truetype(REG, 20)
f_cat    = ImageFont.truetype(BOLD, 22)
f_chip   = ImageFont.truetype(REG, 18)
f_meta   = ImageFont.truetype(BOLD, 14)
f_small  = ImageFont.truetype(REG, 15)
f_quote  = ImageFont.truetype(BOLD, 30)
f_quote_sm = ImageFont.truetype(BOLD, 24)
f_bullet = ImageFont.truetype(REG, 22)

FRAMES_PER = 8
HOLD_RATIO = 0.6

def alpha_for(phase):
    edge = (1.0 - HOLD_RATIO) / 2
    if phase < edge:
        return phase / edge
    if phase > 1 - edge:
        return (1.0 - phase) / edge
    return 1.0

def fade(base, fg, a):
    return tuple(int(base[i] + (fg[i] - base[i]) * a) for i in range(3))

def wrap_text(d, text, font, max_w):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        bbox = d.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] > max_w and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines

def draw_chip(d, x, y, text, font, bg=CHIP_BG, fg=CHIP_TEXT, pad_x=12, pad_y=6, radius=14):
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    w, h = tw + 2 * pad_x, th + 2 * pad_y
    d.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=bg)
    d.text((x + pad_x - bbox[0], y + pad_y - bbox[1]), text, font=font, fill=fg)
    return w, h

def draw_grid(d):
    for x in range(0, W, 40):
        for y in range(0, H, 40):
            d.ellipse([x-1, y-1, x+1, y+1], fill=PANEL)

def draw_header(d, day, accent=ACCENT):
    # accent bar top-left
    d.rounded_rectangle([30, 38, 90, 50], radius=6, fill=accent)
    # name top-right
    bbox = d.textbbox((0, 0), "Shravan N", font=f_meta)
    tw = bbox[2] - bbox[0]
    d.text((W - 30 - tw, 38), "Shravan N", font=f_meta, fill=WHITE)
    # subtle separator
    d.rectangle([30, 75, W - 30, 77], fill=(51, 65, 85))

def draw_footer(d, status_text="Open to Work  -  New Grad December 2026"):
    d.rectangle([30, H - 60, W - 30, H - 58], fill=(51, 65, 85))
    d.ellipse([30, H - 38, 44, H - 24], fill=GREEN)
    d.text((52, H - 38), status_text, font=f_small, fill=MUTED)

# ---------- Template A: Announcement (cycling roles) ----------
def template_announcement(day, title, subtitle, roles, accent=ACCENT):
    roles_count = len(roles)
    frames = []
    for ri in range(roles_count):
        for fi in range(FRAMES_PER):
            phase = fi / (FRAMES_PER - 1)
            a = alpha_for(phase)
            img = Image.new("RGB", (W, H), BG)
            d = ImageDraw.Draw(img)
            draw_grid(d)
            draw_header(d, day, accent)

            # big title
            d.text((50, 100), title, font=f_title_lg, fill=WHITE)
            # subtitle
            d.text((50, 165), subtitle, font=f_sub, fill=MUTED)

            # cycling role line
            d.text((50, 230), "Open to:", font=f_meta, fill=MUTED)
            color = fade(BG, accent, a)
            d.text((50, 255), roles[ri], font=f_title, fill=color)

            # dots
            dot_y = 330
            spacing = 24
            for i in range(roles_count):
                cx = 50 + i * spacing
                if i == ri:
                    d.ellipse([cx-6, dot_y-6, cx+6, dot_y+6], fill=accent)
                else:
                    d.ellipse([cx-3, dot_y-3, cx+3, dot_y+3], fill=(71, 85, 105))

            # location strip
            d.text((50, 380), "United States  -  Remote / Hybrid / Onsite  -  Open to relocation",
                   font=f_small, fill=MUTED)
            d.text((50, 405), "Available December 2026  -  6 months hands-on experience",
                   font=f_small, fill=MUTED)

            draw_footer(d)
            frames.append(img)
    return frames

# ---------- Template B: Skill deep-dive (chips by category) ----------
def template_skill(day, title, subtitle, categories, accent=ACCENT):
    frames = []
    for ci in range(len(categories)):
        for fi in range(FRAMES_PER):
            phase = fi / (FRAMES_PER - 1)
            a = alpha_for(phase)
            img = Image.new("RGB", (W, H), BG)
            d = ImageDraw.Draw(img)
            draw_grid(d)
            draw_header(d, day, accent)

            d.text((50, 100), title, font=f_title_lg, fill=WHITE)
            d.text((50, 165), subtitle, font=f_sub, fill=MUTED)

            cat_name, items = categories[ci]
            color = fade(BG, accent, a)
            d.text((50, 220), cat_name.upper(), font=f_meta, fill=MUTED)
            d.text((50, 245), cat_name, font=f_cat, fill=color)

            # chips
            x, y = 50, 290
            line_h = 0
            max_x = W - 50
            chip_bg = fade(BG, CHIP_BG, a)
            chip_fg = fade(PANEL, CHIP_TEXT, a)
            for item in items:
                bbox = d.textbbox((0, 0), item, font=f_chip)
                tw = bbox[2] - bbox[0]
                chip_w = tw + 24
                if x + chip_w > max_x:
                    x = 50
                    y += line_h + 10
                w, h = draw_chip(d, x, y, item, f_chip, bg=chip_bg, fg=chip_fg)
                x += w + 10
                line_h = max(line_h, h)

            # progress dots
            dot_y = H - 90
            for i in range(len(categories)):
                cx = 50 + i * 22
                if i == ci:
                    d.ellipse([cx-6, dot_y-6, cx+6, dot_y+6], fill=accent)
                else:
                    d.ellipse([cx-3, dot_y-3, cx+3, dot_y+3], fill=(71, 85, 105))

            draw_footer(d)
            frames.append(img)
    return frames

# ---------- Template C: Quote / reflection ----------
def template_quote(day, headline, quotes, accent=ACCENT):
    frames = []
    for qi in range(len(quotes)):
        for fi in range(FRAMES_PER):
            phase = fi / (FRAMES_PER - 1)
            a = alpha_for(phase)
            img = Image.new("RGB", (W, H), BG)
            d = ImageDraw.Draw(img)
            draw_grid(d)
            draw_header(d, day, accent)

            d.text((50, 100), headline, font=f_title, fill=WHITE)
            d.rectangle([50, 155, 130, 157], fill=accent)

            quote = quotes[qi]
            lines = wrap_text(d, quote, f_quote, W - 100)
            y = 200
            color = fade(BG, WHITE, a)
            for line in lines:
                d.text((50, y), line, font=f_quote, fill=color)
                y += 40

            # attribution
            d.text((50, H - 90), "Shravan N  -  CS  -  Class of 2026",
                   font=f_small, fill=MUTED)

            draw_footer(d)
            frames.append(img)
    return frames

# ---------- Template D: Project showcase ----------
def template_project(day, project_name, blurb, tech, outcomes, accent=ACCENT):
    frames = []
    panels = ["stack", "outcomes"]
    for pi in range(len(panels)):
        for fi in range(FRAMES_PER):
            phase = fi / (FRAMES_PER - 1)
            a = alpha_for(phase)
            img = Image.new("RGB", (W, H), BG)
            d = ImageDraw.Draw(img)
            draw_grid(d)
            draw_header(d, day, accent)

            d.text((50, 100), "PROJECT", font=f_meta, fill=MUTED)
            d.text((50, 120), project_name, font=f_title, fill=WHITE)
            lines = wrap_text(d, blurb, f_sub, W - 100)
            y = 180
            for line in lines[:2]:
                d.text((50, y), line, font=f_sub, fill=MUTED)
                y += 28

            if panels[pi] == "stack":
                d.text((50, 250), "TECH STACK", font=f_meta, fill=MUTED)
                x, y = 50, 280
                line_h = 0
                chip_bg = fade(BG, CHIP_BG, a)
                chip_fg = fade(PANEL, CHIP_TEXT, a)
                for item in tech:
                    bbox = d.textbbox((0, 0), item, font=f_chip)
                    tw = bbox[2] - bbox[0]
                    if x + tw + 24 > W - 50:
                        x = 50
                        y += line_h + 10
                    w, h = draw_chip(d, x, y, item, f_chip, bg=chip_bg, fg=chip_fg)
                    x += w + 10
                    line_h = max(line_h, h)
            else:
                d.text((50, 250), "OUTCOMES", font=f_meta, fill=MUTED)
                y = 280
                for o in outcomes:
                    color = fade(BG, accent, a)
                    d.rectangle([50, y + 8, 62, y + 20], fill=color)
                    text_color = fade(BG, WHITE, a)
                    d.text((75, y), o, font=f_bullet, fill=text_color)
                    y += 36

            # panel dots
            dot_y = H - 90
            for i in range(len(panels)):
                cx = 50 + i * 22
                if i == pi:
                    d.ellipse([cx-6, dot_y-6, cx+6, dot_y+6], fill=accent)
                else:
                    d.ellipse([cx-3, dot_y-3, cx+3, dot_y+3], fill=(71, 85, 105))

            draw_footer(d)
            frames.append(img)
    return frames

# ---------- Template E: Bullet pitch ----------
def template_pitch(day, headline, bullets, accent=ACCENT):
    frames = []
    # animate bullets appearing one by one then holding
    total_phases = len(bullets) + 1
    for ph in range(total_phases):
        for fi in range(FRAMES_PER):
            phase = fi / (FRAMES_PER - 1)
            img = Image.new("RGB", (W, H), BG)
            d = ImageDraw.Draw(img)
            draw_grid(d)
            draw_header(d, day, accent)

            d.text((50, 100), headline, font=f_title, fill=WHITE)
            d.rectangle([50, 155, 100, 157], fill=accent)

            y = 200
            for i, b in enumerate(bullets):
                if i < ph:
                    a = 1.0
                elif i == ph:
                    a = alpha_for(phase)
                else:
                    a = 0.0
                color = fade(BG, WHITE, a)
                dot_color = fade(BG, accent, a)
                d.ellipse([50, y + 10, 64, y + 24], fill=dot_color)
                d.text((80, y), b, font=f_bullet, fill=color)
                y += 40

            draw_footer(d)
            frames.append(img)
    return frames

# ===========================================================
# Per-day configurations
# ===========================================================

DAYS = []

# Day 1 — Announcement
DAYS.append(dict(
    day=1, template="announcement", accent=ACCENT,
    title="Open to Work",
    subtitle="Software Engineer  -  New Grad 2026",
    roles=["Software Engineer", "Full Stack Developer", "AI / ML Engineer",
           "LLM Engineer", "Backend Engineer", "Cloud Engineer"],
))

# Day 2 — Why I chose SWE (quote)
DAYS.append(dict(
    day=2, template="quote", accent=ACCENT3,
    headline="Why I chose engineering",
    quotes=[
        "Two years ago I couldn't write a for-loop without Googling it.",
        "My first project was a coin-flip simulator. Four hours to write.",
        "Somewhere in there, building stopped feeling like assignments.",
        "Six months in: full-stack apps, AWS deployments, LLM applications.",
    ],
))

# Day 3 — What's on my laptop (skill)
DAYS.append(dict(
    day=3, template="skill", accent=ACCENT2,
    title="On my laptop right now",
    subtitle="The actual tools I use to ship every day",
    categories=[
        ("Editor",   ["VS Code", "Pylance", "ESLint", "Prettier", "GitHub Copilot"]),
        ("Languages",["Python", "TypeScript", "JavaScript", "SQL", "Bash"]),
        ("Backend",  ["FastAPI", "uvicorn", "SQLAlchemy", "Pydantic", "PostgreSQL"]),
        ("Frontend", ["React", "Vite", "Tailwind", "React Query", "TypeScript"]),
        ("AI / LLM", ["OpenAI SDK", "LangChain", "Chroma", "Anthropic Claude"]),
        ("Cloud",    ["AWS Lambda", "S3", "API Gateway", "CloudWatch", "Docker"]),
    ],
))

# Day 4 — Full-stack project
DAYS.append(dict(
    day=4, template="project", accent=ACCENT,
    project_name="Full-Stack Web Application",
    blurb="React + FastAPI + PostgreSQL deployed to AWS ECS",
    tech=["React", "TypeScript", "Tailwind", "FastAPI", "SQLAlchemy",
          "PostgreSQL", "Alembic", "Docker", "AWS ECS", "CloudFront", "S3", "GitHub Actions"],
    outcomes=["End-to-end React + FastAPI + Postgres + AWS",
              "JWT auth with OAuth 2.0 social login",
              "CI/CD via GitHub Actions, zero-downtime deploy",
              "Live URL + GitHub repo in profile"],
))

# Day 5 — RAG LLM project
DAYS.append(dict(
    day=5, template="project", accent=ACCENT2,
    project_name="RAG LLM Chatbot",
    blurb="Course catalog Q&A with semantic search and GPT-4o",
    tech=["Python", "LangChain", "OpenAI GPT-4o", "text-embedding-3-small",
          "ChromaDB", "FastAPI", "React", "Server-Sent Events"],
    outcomes=["Semantic chunking with 50-token overlap",
              "Top-k retrieval with cosine similarity",
              "Streaming responses via Server-Sent Events",
              "Local cache cut p50 latency by 60%"],
))

# Day 6 — 5 lessons (pitch)
DAYS.append(dict(
    day=6, template="pitch", accent=ACCENT4,
    headline="5 lessons from 6 months of building",
    bullets=["Ship the ugly version first",
             "Read the docs before the Stack Overflow answer",
             "Logs beat the debugger most of the time",
             "Cloud is just somebody else's Linux box",
             "Reviewing PRs teaches more than writing them"],
))

# Day 7 — Week 1 recap (announcement)
DAYS.append(dict(
    day=7, template="announcement", accent=ACCENT,
    title="Week 1 recap",
    subtitle="One week in. Here's what I'm working with.",
    roles=["Python", "React.js", "AI / ML", "LLMs", "AWS Cloud", "Open to Work"],
))

# Day 8 — Python deep-dive
DAYS.append(dict(
    day=8, template="skill", accent=(255, 214, 10),
    title="Python, day to day",
    subtitle="Not just a scripting language",
    categories=[
        ("Web APIs",    ["FastAPI", "Flask", "Django", "uvicorn", "Pydantic"]),
        ("Async",       ["asyncio", "httpx", "asyncpg", "aiohttp"]),
        ("Data",        ["Pandas", "NumPy", "Polars", "SQLAlchemy"]),
        ("Testing",     ["PyTest", "pytest-asyncio", "coverage", "mypy"]),
        ("LLM",         ["OpenAI", "Anthropic", "LangChain", "LlamaIndex"]),
    ],
))

# Day 9 — React deep-dive
DAYS.append(dict(
    day=9, template="skill", accent=(97, 218, 251),
    title="React, the way I write it",
    subtitle="Hooks, TypeScript, performance",
    categories=[
        ("Hooks",       ["useState", "useEffect", "useMemo", "useCallback", "useRef"]),
        ("State",       ["Context", "useReducer", "Redux Toolkit", "React Query"]),
        ("Performance", ["React.memo", "code splitting", "React.lazy", "Suspense"]),
        ("Type-safety", ["TypeScript", "strict mode", "discriminated unions"]),
        ("Tooling",     ["Vite", "Vitest", "Playwright", "ESLint", "Tailwind"]),
    ],
))

# Day 10 — AWS in production
DAYS.append(dict(
    day=10, template="skill", accent=ACCENT4,
    title="AWS, in production",
    subtitle="What I actually deploy on",
    categories=[
        ("Compute",      ["EC2", "Lambda", "ECS Fargate", "AWS Batch"]),
        ("Storage",      ["S3", "EFS", "DynamoDB", "RDS PostgreSQL"]),
        ("Edge",         ["CloudFront", "Route 53", "ACM", "WAF"]),
        ("Integration",  ["API Gateway", "EventBridge", "SQS", "SNS"]),
        ("Ops",          ["CloudWatch", "IAM", "Secrets Manager", "Parameter Store"]),
    ],
))

# Day 11 — How RAG works (pitch)
DAYS.append(dict(
    day=11, template="pitch", accent=ACCENT2,
    headline="RAG is three steps",
    bullets=["1. Embed — split + vectorize your corpus",
             "2. Retrieve — top-k similarity search at query time",
             "3. Generate — pass context + question to the LLM",
             "Everything else is engineering on top of these three"],
))

# Day 12 — System design (pitch)
DAYS.append(dict(
    day=12, template="pitch", accent=ACCENT3,
    headline="System design ideas that clicked",
    bullets=["Load balancing is not just round-robin",
             "Caching is a 3-sided tradeoff",
             "Queues turn hard problems into easier ones",
             "Databases scale by giving things up",
             "CAP theorem is a lens, not a rule"],
))

# Day 13 — DSA (pitch)
DAYS.append(dict(
    day=13, template="pitch", accent=ACCENT5,
    headline="200 LeetCode problems in: what changed",
    bullets=["Solve by pattern, not by problem",
             "30-minute time-box, then read the editorial",
             "Re-solve from memory, don't re-read",
             "Always write the brute force first",
             "Test edge cases before you submit"],
))

# Day 14 — DB decision (skill)
DAYS.append(dict(
    day=14, template="skill", accent=ACCENT,
    title="SQL vs NoSQL",
    subtitle="How I actually decide",
    categories=[
        ("PostgreSQL", ["ACID", "JOINs", "JSONB", "full-text search", "pgvector"]),
        ("MongoDB",    ["documents", "flexible schema", "horizontal writes"]),
        ("Redis",      ["cache", "rate limit", "queue", "pub/sub", "sessions"]),
        ("DynamoDB",   ["AWS-native", "single-digit ms", "predictable access"]),
    ],
))

# Day 15 — Building in public (project)
DAYS.append(dict(
    day=15, template="project", accent=ACCENT2,
    project_name="Paper Summarizer (in progress)",
    blurb="CLI tool: arXiv URL in, structured Markdown out",
    tech=["Python", "Anthropic Claude", "pypdf", "Pydantic",
          "Streamlit", "SQLite"],
    outcomes=["PDF text extraction working on 30+ page papers",
              "Claude streaming + structured JSON output",
              "TL;DR + 3 contributions + 5 follow-up questions",
              "Batch ingestion + Obsidian export coming next"],
))

# Day 16 — debugging story (quote)
DAYS.append(dict(
    day=16, template="quote", accent=ACCENT4,
    headline="The 4-hour bug",
    quotes=[
        "Spent 4 hours debugging.",
        "Turned out to be one missing 'await'.",
        "Python returned a coroutine. FastAPI tried to serialize it.",
        "The bug is almost always in your code, not the library's.",
    ],
))

# Day 17 — LangChain LCEL (pitch)
DAYS.append(dict(
    day=17, template="pitch", accent=ACCENT2,
    headline="LCEL: how chains compose now",
    bullets=["chain = prompt | llm | parser",
             "Streaming for free on every Runnable",
             "Batching for free with .batch([inputs])",
             "Async for free with .ainvoke()",
             "LangSmith traces every step automatically"],
))

# Day 18 — first deploy crashed (quote)
DAYS.append(dict(
    day=18, template="quote", accent=ACCENT4,
    headline="My first deploy crashed",
    quotes=[
        "Deploy succeeded. Every request returned 502.",
        "The zip was 280MB. Lambda's limit is 250MB.",
        "CloudWatch had the answer. API Gateway didn't.",
        "Read the limits page before you deploy.",
    ],
))

# Day 19 — AWS for $0 (pitch)
DAYS.append(dict(
    day=19, template="pitch", accent=ACCENT4,
    headline="A Python API for $0 / month",
    bullets=["API Gateway HTTP API — 1M req free",
             "Lambda — 1M invocations free forever",
             "DynamoDB on-demand — 25GB free forever",
             "S3 + CloudFront — pennies for static assets",
             "Total: ~$0.50/month with a custom domain"],
))

# Day 20 — first OSS PR (quote)
DAYS.append(dict(
    day=20, template="quote", accent=ACCENT3,
    headline="My first merged PR",
    quotes=[
        "Found an example in a README that didn't run.",
        "Fixed it. Added the missing import. Ran the test.",
        "Merged in two hours. Conversation was kind.",
        "The bar to start contributing is much lower than I thought.",
    ],
))

# Day 21 — Vector DB comparison (skill)
DAYS.append(dict(
    day=21, template="skill", accent=ACCENT2,
    title="Vector DBs, compared",
    subtitle="What I'd pick for which job",
    categories=[
        ("Pinecone",  ["managed", "production", "zero ops", "$ from day 1"]),
        ("FAISS",     ["fastest single-node", "free", "no service", "no metadata"]),
        ("ChromaDB",  ["self-host", "persistent", "metadata filters", "Python-first"]),
        ("pgvector",  ["already in Postgres", "transactional", "simple ops"]),
        ("Qdrant",    ["Rust-fast", "rich filtering", "great single-node"]),
    ],
))

# Day 22 — Why hire a new grad (pitch)
DAYS.append(dict(
    day=22, template="pitch", accent=ACCENT5,
    headline="Why hire a new grad",
    bullets=["~50% cost of a senior engineer",
             "Velocity converges by month 6",
             "Trained in your codebase, your culture",
             "Curiosity and unglamorous-task tolerance",
             "Two years in, they're your new senior"],
))

# Day 23 — what I want (quote)
DAYS.append(dict(
    day=23, template="quote", accent=ACCENT,
    headline="What I want in my first role",
    quotes=[
        "A team that ships every week, not 'when it's perfect.'",
        "Structured mentorship. Not 'ask if you have questions.'",
        "A modern stack — Python, TS, React, AWS, real CI/CD.",
        "Becoming a strong mid-level engineer in 12-18 months.",
    ],
))

# Day 24 — Interview prep (skill)
DAYS.append(dict(
    day=24, template="skill", accent=ACCENT3,
    title="Interview prep checkpoint",
    subtitle="Honest about where I am",
    categories=[
        ("Strong",     ["Behavioral (STAR)", "Arrays / strings", "Hashmaps", "Two pointers"]),
        ("Solid",      ["BFS / DFS", "Sliding window", "Heap top-K", "Backtracking"]),
        ("Improving",  ["DP on subsequences", "Graph algorithms", "System design (mid)"]),
        ("Working on", ["Raft / consensus", "B-trees / LSM internals"]),
    ],
))

# Day 25 — Favorite project (project)
DAYS.append(dict(
    day=25, template="project", accent=ACCENT2,
    project_name="Course Recommendation Chatbot",
    blurb="The one project I'd show a hiring manager first",
    tech=["React", "FastAPI", "PostgreSQL", "pgvector",
          "OpenAI GPT-4o", "AWS ECS Fargate", "CloudFront", "Docker"],
    outcomes=["RAG with pgvector — no separate vector DB",
              "Sub-2-second p50 query latency",
              "Streaming responses with Server-Sent Events",
              "Deployed on AWS ECS behind CloudFront"],
))

# Day 26 — Why AI/ML (quote)
DAYS.append(dict(
    day=26, template="quote", accent=ACCENT2,
    headline="Why AI / ML",
    quotes=[
        "I came to AI through frustration.",
        "Spent days hand-crafting an NL-to-SQL parser.",
        "Tried an LLM. Wrote a 200-token prompt. It worked.",
        "That afternoon changed my career path.",
    ],
))

# Day 27 — Day 90 (pitch)
DAYS.append(dict(
    day=27, template="pitch", accent=ACCENT,
    headline="What day 90 looks like with me",
    bullets=["Month 1: read the code, ship 5-10 small PRs",
             "Month 2: own one feature end-to-end",
             "Month 3: own a cross-team feature",
             "Quarter 2: mentor the next new grad's first PR"],
))

# Day 28 — Recruiter pitch (announcement)
DAYS.append(dict(
    day=28, template="announcement", accent=ACCENT,
    title="For recruiters",
    subtitle="Saving you a scroll",
    roles=["Software Engineer", "Full Stack Developer", "AI / ML Engineer",
           "LLM Engineer", "Backend Engineer", "Cloud Engineer",
           "Junior Software Engineer", "Associate Software Engineer"],
))

# Day 29 — Gratitude (quote)
DAYS.append(dict(
    day=29, template="quote", accent=ACCENT3,
    headline="30 days in. Thank you.",
    quotes=[
        "I started this campaign uncomfortable with posting publicly.",
        "Recruiters DM'd. Engineers gave feedback. Friends reposted.",
        "Daily posting is compounding interest, slowly.",
        "One more post tomorrow.",
    ],
))

# Day 30 — Final ask (announcement)
DAYS.append(dict(
    day=30, template="announcement", accent=ACCENT,
    title="Still open to work",
    subtitle="Day 30. Same message. December 2026 start.",
    roles=["Software Engineer", "Full Stack Developer", "AI / ML Engineer",
           "LLM Engineer", "Backend Engineer", "Cloud Engineer"],
))

# ============ Generate ============
def render(cfg):
    t = cfg["template"]
    day = cfg["day"]
    accent = cfg.get("accent", ACCENT)
    if t == "announcement":
        frames = template_announcement(day, cfg["title"], cfg["subtitle"], cfg["roles"], accent)
    elif t == "skill":
        frames = template_skill(day, cfg["title"], cfg["subtitle"], cfg["categories"], accent)
    elif t == "quote":
        frames = template_quote(day, cfg["headline"], cfg["quotes"], accent)
    elif t == "project":
        frames = template_project(day, cfg["project_name"], cfg["blurb"],
                                  cfg["tech"], cfg["outcomes"], accent)
    elif t == "pitch":
        frames = template_pitch(day, cfg["headline"], cfg["bullets"], accent)
    else:
        raise ValueError(t)

    out = os.path.join(OUT_DIR, f"day_{day:02d}.gif")
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=130,
        loop=0,
        optimize=True,
        disposal=2,
    )
    return out, len(frames)

if __name__ == "__main__":
    for cfg in DAYS:
        path, n = render(cfg)
        size = os.path.getsize(path) // 1024
        print(f"day {cfg['day']:02d}  {cfg['template']:13s}  {n} frames  {size} KB  {path}")
    print("done.")
