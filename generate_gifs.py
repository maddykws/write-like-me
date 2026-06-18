#!/usr/bin/env python3
"""
15 recruiter-targeted LinkedIn posts as animated GIFs.
Same format as reference: split view → full-width code typing → overlay box.
"""

from PIL import Image, ImageDraw, ImageFont
import os, re

OUT = "/home/user/write-like-me/post_assets/v2"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1080
HALF = W // 2

def F(path, size):
    try:    return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

MONO   = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

f_head   = F(SANS_B, 54)
f_bullet = F(MONO,   20)
f_code   = F(MONO,   15)
f_ui     = F(MONO,   11)
f_ui_b   = F(MONO_B, 11)
f_ov_h   = F(MONO_B, 15)
f_ov_b   = F(MONO,   14)

# ── Single Tokyo Night theme (matches reference exactly) ──────────────────────
T = {
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
    "card_bg":     "#0d0e17",
    "card_white":  "#ffffff",
    "card_cyan":   "#2ac3de",
    "card_body":   "#7982a9",
    "card_div":    "#2ac3de",
    "ov_border":   "#2ac3de",
    "ov_bg":       "#1a1b26",
    "ov_head":     "#2ac3de",
    "ov_check":    "#e0af68",
    "ov_cta":      "#e0af68",
    "ov_hash":     "#2ac3de",
}

KW = {"__global__","__shared__","__device__","__syncthreads","float","int","void",
      "auto","for","if","else","elif","return","const","double","char","import",
      "from","def","class","async","await","with","as","True","False","None",
      "and","or","not","in","yield","lambda","try","except","raise","pass",
      "include","define","pragma","unsigned","while","do","struct","typedef",
      "self","cls","super"}

def tok(line, T):
    if re.match(r'\s*(//|#\s*(?!include|define|pragma))', line):
        return [(line, T["comment"])]
    m = re.match(r'(\s*#\s*(?:include|define|pragma)\b)(.*)', line)
    if m:
        rest = m.group(2)
        col2 = T["string"] if ("<" in rest or '"' in rest) else T["number"] if rest.strip().replace('.','',1).isdigit() else T["text"]
        return [(m.group(1), T["keyword"]), (rest, col2)]
    pat = re.compile(
        r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|<[a-zA-Z_./]+>)'
        r'|(\b(?:' + '|'.join(re.escape(k) for k in KW) + r')\b)'
        r'|(\b\d+\.?\d*(?:e[+-]?\d+)?[fFLUlu]?\b)'
        r'|([A-Za-z_]\w*(?=\s*\())'
        r'|([^\w\s])'
        r'|(\w+)|(\s+)'
    )
    out = []
    for mo in pat.finditer(line):
        s,kw,num,fn,pu,_,ws = mo.groups()
        t = mo.group(0)
        if ws:    c=T["text"]
        elif s:   c=T["string"]
        elif kw:  c=T["keyword"]
        elif num: c=T["number"]
        elif fn:  c=T["func"]
        elif pu:  c=T["punct"]
        else:     c=T["text"]
        out.append((t,c))
    return out or [(line, T["text"])]

TITLE_H=38; SB_W=258; TAB_H=30; STAT_H=22; GUT_W=48; OL_H=185; LH=22; SLH=17

def titlebar(draw, width, filename):
    draw.rectangle([0,0,width,TITLE_H], fill=T["titlebar_bg"])
    draw.ellipse([14,12,26,24], fill="#ff5f57")
    draw.ellipse([32,12,44,24], fill="#febc2e")
    draw.ellipse([50,12,62,24], fill="#28c840")
    title = f"{filename} — write-like-me — Cursor"
    tw = draw.textlength(title, font=f_ui)
    draw.text(((width-tw)/2,(TITLE_H-11)/2), title, fill="#808080", font=f_ui)

def sidebar(draw, file_tree, outline, height=H):
    draw.rectangle([0,TITLE_H,SB_W,height-STAT_H], fill=T["sidebar_bg"])
    draw.text((8,TITLE_H+8), "EXPLORER", fill=T["dim"], font=f_ui_b)
    ty = TITLE_H+26
    for ind,name,is_dir,active in file_tree:
        if ty > height-OL_H-STAT_H-2: break
        if active: draw.rectangle([0,ty-1,SB_W,ty+SLH], fill=T["select_bg"])
        col = T["folder"] if is_dir else (T["text"] if active else T["dim"])
        draw.text((6+ind*12, ty), ("▾ " if is_dir else "  ")+name, fill=col, font=f_ui)
        ty += SLH
    OLY = height-OL_H-STAT_H
    draw.rectangle([0,OLY,SB_W,height-STAT_H], fill=T["tabbar_bg"])
    draw.line([0,OLY,SB_W,OLY], fill=T["dim"])
    draw.text((8,OLY+5), "OUTLINE", fill=T["dim"], font=f_ui_b)
    oy = OLY+20
    for ind,label,sec in outline:
        if oy > height-STAT_H-2: break
        draw.text((6+ind*10, oy), label, fill=T["func"] if sec else T["comment"], font=f_ui)
        oy += SLH

def editor_chrome(draw, width, filename):
    EDX=SB_W
    draw.rectangle([EDX,TITLE_H,width,TITLE_H+TAB_H], fill=T["tabbar_bg"])
    te = EDX+min(len(filename)*8+36,220)
    draw.rectangle([EDX,TITLE_H,te,TITLE_H+TAB_H], fill=T["ide_bg"])
    draw.line([te,TITLE_H,te,TITLE_H+TAB_H], fill=T["dim"])
    draw.ellipse([EDX+7,TITLE_H+TAB_H//2-5,EDX+17,TITLE_H+TAB_H//2+5], fill=T["tab_dot"])
    draw.text((EDX+21,TITLE_H+(TAB_H-11)//2), filename, fill=T["text"], font=f_ui)
    draw.rectangle([EDX,TITLE_H+TAB_H,EDX+GUT_W,H-STAT_H], fill=T["gutter_bg"])

def code_area(draw, width, code_lines, cursor_li):
    CODE_X = SB_W+GUT_W
    top = TITLE_H+TAB_H+4
    bot = H-STAT_H-OL_H
    vis = (bot-top)//LH
    start = max(0, cursor_li-vis+3)
    for i,line in enumerate(code_lines[start:start+vis]):
        ali=start+i; cy=top+i*LH
        draw.text((SB_W+2,cy), f"{ali+1:>3}", fill=T["ln_fg"], font=f_ui)
        if ali==cursor_li: draw.rectangle([SB_W+GUT_W,cy-1,width,cy+LH-1], fill=T["select_bg"])
        cx=CODE_X
        for t,c in tok(line,T):
            tw=draw.textlength(t,font=f_code)
            if cx+tw>width-2: break
            draw.text((cx,cy), t, fill=c, font=f_code); cx+=tw
    vi=cursor_li-start
    if 0<=vi<vis and cursor_li<len(code_lines):
        cy=top+vi*LH
        cx=CODE_X+draw.textlength(code_lines[cursor_li],font=f_code)
        draw.rectangle([min(cx,width-4),cy,min(cx+2,width-2),cy+LH-2], fill=T["text"])

def status_bar(draw, width, branch, lang):
    draw.rectangle([0,H-STAT_H,width,H], fill=T["status_bg"])
    draw.text((8,H-STAT_H+4), f"  {branch}  ↑2 ↓0  {lang}  ·  UTF-8  ·  LF  ·  256 cols",
              fill=T["status_fg"], font=f_ui_b)
    draw.text((width-115,H-STAT_H+4), "GPU: H100 · SM96", fill=T["status_fg"], font=f_ui_b)

def split_frame(p):
    img=Image.new("RGB",(W,H),T["ide_bg"]); draw=ImageDraw.Draw(img)
    titlebar(draw, HALF, p["filename"])
    sidebar(draw, p["file_tree"], p["outline"])
    # editor chrome (half-width)
    EDX=SB_W
    draw.rectangle([EDX,TITLE_H,HALF,TITLE_H+TAB_H], fill=T["tabbar_bg"])
    te=EDX+min(len(p["filename"])*8+36,180)
    draw.rectangle([EDX,TITLE_H,te,TITLE_H+TAB_H], fill=T["ide_bg"])
    draw.ellipse([EDX+7,TITLE_H+TAB_H//2-5,EDX+17,TITLE_H+TAB_H//2+5], fill=T["tab_dot"])
    draw.text((EDX+21,TITLE_H+(TAB_H-11)//2), p["filename"], fill=T["text"], font=f_ui)
    draw.rectangle([EDX,TITLE_H+TAB_H,EDX+GUT_W,H-STAT_H], fill=T["gutter_bg"])
    status_bar(draw, HALF, p.get("branch","main"), p.get("lang","Python"))
    # card
    draw.rectangle([HALF,0,W,H], fill=T["card_bg"])
    px=HALF+46; cy=100; lh=68; cx=px
    for text,hi in p["headline"]:
        col=T["card_cyan"] if hi else T["card_white"]
        for word in text.split():
            tw=draw.textlength(word+" ",font=f_head)
            if cx+tw>W-46 and cx>px: cx=px; cy+=lh
            draw.text((cx,cy), word, fill=col, font=f_head); cx+=tw
    cy+=lh+20
    draw.rectangle([px,cy,px+118,cy+4], fill=T["card_div"]); cy+=28
    for b in p["card_bullets"]:
        draw.text((px,cy), b, fill=T["card_body"], font=f_bullet); cy+=36
    return img

def full_frame(p, code_lines, cursor_li):
    img=Image.new("RGB",(W,H),T["ide_bg"]); draw=ImageDraw.Draw(img)
    titlebar(draw, W, p["filename"])
    sidebar(draw, p["file_tree"], p["outline"])
    draw.rectangle([SB_W,TITLE_H,W,H], fill=T["ide_bg"])
    editor_chrome(draw, W, p["filename"])
    code_area(draw, W, code_lines, cursor_li)
    status_bar(draw, W, p.get("branch","main"), p.get("lang","Python"))
    return img

def overlay_frame(base_img, p):
    img=base_img.copy(); draw=ImageDraw.Draw(img)
    top=TITLE_H+TAB_H+4; bot=H-STAT_H-OL_H
    vis=(bot-top)//LH; total=len(p["code"])
    # position box to start partway through — leave first ~half of code visible
    box_start_line = max(12, total-14)
    box_y1 = top + box_start_line*LH - 4
    box_y2 = bot - 4
    box_x1 = SB_W+GUT_W-8; box_x2 = W-8
    draw.rectangle([box_x1,box_y1,box_x2,box_y2], fill=T["ov_bg"])
    draw.rectangle([box_x1,box_y1,box_x2,box_y2], outline=T["ov_border"], width=2)
    tx=box_x1+14; ty=box_y1+12; lh_ov=25
    for text,kind in p["overlay"]:
        if kind is None: ty+=lh_ov//2; continue
        col={"head":T["ov_head"],"check":T["ov_check"],"cta":T["ov_cta"],"hash":T["ov_hash"]}[kind]
        font=f_ov_h if kind=="head" else f_ov_b
        draw.text((tx,ty), text, fill=col, font=font); ty+=lh_ov
    return img

def build_gif(p):
    frames=[]
    sf=split_frame(p)
    for _ in range(8): frames.append((sf,100))   # 0.8s split view
    typed=[]
    for li,line in enumerate(p["code"]):
        typed.append("")
        for ci,ch in enumerate(line):
            typed[-1]+=ch
            if ci%3==0: frames.append((full_frame(p,list(typed),li),30))
        for _ in range(2): frames.append((full_frame(p,list(typed),li),60))
    last=list(typed); ll=len(p["code"])-1
    frames.append((full_frame(p,last,ll),300))
    frames.append((full_frame(p,last,-1),300))
    base=full_frame(p,last,ll); ov=overlay_frame(base,p)
    for _ in range(20): frames.append((ov,100))   # 2s overlay
    return frames

def save(frames, path, colors=96):
    imgs=[f[0].quantize(colors=colors,method=Image.Quantize.MEDIANCUT) for f in frames]
    durs=[f[1] for f in frames]
    imgs[0].save(path,save_all=True,append_images=imgs[1:],duration=durs,loop=0,optimize=True)
    print(f"  {os.path.basename(path)}  {os.path.getsize(path)//1024} KB")

# ══════════════════════════════════════════════════════════════════════════════
#  15 POSTS
# ══════════════════════════════════════════════════════════════════════════════

POSTS = [

# ── 1. CUDA Kernel ────────────────────────────────────────────────────────────
{
"filename":"03_gemm_tiled.cu","branch":"main","lang":"CUDA",
"file_tree":[
    (0,"cuda-kernels-from-scratch",True,False),(1,"src",True,False),
    (2,"01_vector_add.cu",False,False),(2,"02_matmul_naive.cu",False,False),
    (2,"03_gemm_tiled.cu",False,True),(2,"04_softmax.cu",False,False),
    (1,"bench",True,False),(2,"bench.py",False,False),
    (0,"README.md",False,False),(0,"Makefile",False,False),
],
"outline":[(0,"__global__ gemm_tiled",True),(1,"↳ load A tile → smem",False),
           (1,"↳ __syncthreads()",False),(1,"↳ tile-mma accumulate",False),(0,"host_launcher()",True)],
"headline":[("Every AI engineer should learn to write ",False),("exactly one CUDA kernel.",True)],
"card_bullets":["→ not because you'll write them at work",
                "→ because the mental model changes everything",
                "→ ~200 lines.  one weekend.",
                "→ you'll never look at PyTorch the same way"],
"code":[
    "// tiny GEMM with shared-memory tiling — your starter kernel",
    "// goal: 200 lines, weekend project, changes how you think.",
    "","#include <cuda_runtime.h>","",
    "#define BM 128","#define BN 128","#define BK 16","",
    "__global__ void gemm_tiled(const float* A,",
    "                           const float* B,  float* C,",
    "                           int M, int N, int K) {",
    "  __shared__ float As[BM][BK];",
    "  __shared__ float Bs[BK][BN];",
    "  int tx=threadIdx.x, ty=threadIdx.y;",
    "  int row=blockIdx.y*BM+ty, col=blockIdx.x*BN+tx;",
    "  float acc=0.0f;",
    "  for (int t=0; t<K; t+=BK) {",
    "    As[ty][tx]=A[row*K+t+tx];",
    "    Bs[ty][tx]=B[(t+ty)*N+col];",
    "    __syncthreads();",
    "    #pragma unroll",
    "    for (int k=0; k<BK; ++k) acc+=As[ty][k]*Bs[k][tx];",
    "    __syncthreads();",
    "  }","  C[row*N+col]=acc;","}",
],
"overlay":[
    ("AFTER YOU WRITE IT, YOU UNDERSTAND:","head"),("",""),
    ("✓   why batch size is the #1 perf knob","check"),
    ("✓   why FP8 doubles throughput","check"),
    ("✓   why fused kernels exist","check"),
    ("✓   what 'memory access pattern' means","check"),
    ("✓   flash attention papers, actually","check"),("",""),
    ("have you written a CUDA kernel? what did it teach you?","cta"),("",""),
    ("#CUDA  #GPU  #AIInfrastructure  #LearnToCode","hash"),
],
},

# ── 2. LLM Inference Batching ─────────────────────────────────────────────────
{
"filename":"batched_inference.py","branch":"main","lang":"Python",
"file_tree":[
    (0,"llm-inference-engine",True,False),(1,"src",True,False),
    (2,"batched_inference.py",False,True),(2,"kv_cache.py",False,False),
    (2,"continuous_batching.py",False,False),(2,"speculative.py",False,False),
    (1,"bench",True,False),(2,"throughput_bench.py",False,False),
    (0,"README.md",False,False),
],
"outline":[(0,"BatchedEngine",True),(1,"↳ __init__",False),(1,"↳ generate()",False),
           (1,"↳ _pad_batch()",False),(0,"benchmark()",True)],
"headline":[("Batching is the most underrated skill in ",False),("LLM inference.",True)],
"card_bullets":["→ latency ≠ throughput — pick one",
                "→ batch=1 wastes 90% of your GPU",
                "→ continuous batching changed everything",
                "→ this is why vLLM exists"],
"code":[
    "# LLM inference: why batching changes everything",
    "import torch","from transformers import AutoModelForCausalLM, AutoTokenizer","",
    "class BatchedEngine:",
    "    def __init__(self, model_id: str, max_batch: int = 32):",
    "        self.model = AutoModelForCausalLM.from_pretrained(",
    "            model_id, torch_dtype=torch.float16).cuda()",
    "        self.tok   = AutoTokenizer.from_pretrained(model_id)",
    "        self.max_batch = max_batch","",
    "    def generate(self, prompts: list[str]) -> list[str]:",
    "        inputs = self.tok(prompts, return_tensors='pt',",
    "                          padding=True).to('cuda')",
    "        with torch.no_grad():",
    "            out = self.model.generate(**inputs, max_new_tokens=256,",
    "                                     do_sample=False)",
    "        return self.tok.batch_decode(out, skip_special_tokens=True)","",
    "# batch=1  → ~12% GPU util    batch=32 → ~74% GPU util",
    "# same hardware, 6x throughput — just from batching",
],
"overlay":[
    ("AFTER YOU SHIP THIS, YOU REALIZE:","head"),("",""),
    ("✓   latency and throughput are opposites","check"),
    ("✓   batching is the #1 inference lever","check"),
    ("✓   continuous batching > static batching","check"),
    ("✓   KV cache sizing determines your limits","check"),
    ("✓   vLLM/TGI solve this so you don't have to","check"),("",""),
    ("what's your biggest LLM serving bottleneck?","cta"),("",""),
    ("#LLM  #AIInfrastructure  #GPU  #MLOps","hash"),
],
},

# ── 3. RAG Pipeline ───────────────────────────────────────────────────────────
{
"filename":"retrieval.py","branch":"main","lang":"Python",
"file_tree":[
    (0,"production-rag",True,False),(1,"src",True,False),
    (2,"retrieval.py",False,True),(2,"chunker.py",False,False),
    (2,"reranker.py",False,False),(2,"eval.py",False,False),
    (1,"prompts",True,False),(2,"rag_system.txt",False,False),
    (0,"README.md",False,False),
],
"outline":[(0,"HybridRetriever",True),(1,"↳ dense_search()",False),
           (1,"↳ sparse_search()",False),(1,"↳ rerank()",False),(0,"RAGPipeline",True)],
"headline":[("Most RAG pipelines fail at ",False),("retrieval, not generation.",True)],
"card_bullets":["→ retrieval quality > model size",
                "→ chunk strategy matters more than embeddings",
                "→ hybrid search beats dense-only",
                "→ eval without retrieval metrics is blind"],
"code":[
    "# Production RAG: where most teams get it wrong",
    "from langchain.retrievers import EnsembleRetriever",
    "from langchain_community.retrievers import BM25Retriever",
    "from langchain_openai import OpenAIEmbeddings","",
    "class HybridRetriever:",
    "    def __init__(self, docs, k: int = 6):",
    "        dense  = Chroma.from_documents(docs, OpenAIEmbeddings())",
    "        sparse = BM25Retriever.from_documents(docs)",
    "        sparse.k = k",
    "        self.retriever = EnsembleRetriever(",
    "            retrievers=[dense.as_retriever(k=k), sparse],",
    "            weights=[0.6, 0.4]   # tune per domain","        )","",
    "    def get(self, query: str):",
    "        docs = self.retriever.invoke(query)",
    "        # rerank: cross-encoder scores beat cosine sim",
    "        return self._rerank(query, docs)","",
    "# dense alone: 61% recall@5  |  hybrid: 84% recall@5",
],
"overlay":[
    ("WHAT RAG ACTUALLY TAUGHT ME:","head"),("",""),
    ("✓   retrieval quality ≫ generation quality","check"),
    ("✓   chunk size is a hyperparameter — tune it","check"),
    ("✓   hybrid search (BM25 + dense) beats either alone","check"),
    ("✓   reranking adds ~15% recall with zero cost","check"),
    ("✓   eval without retrieval metrics is theatre","check"),("",""),
    ("what's your hardest RAG problem right now?","cta"),("",""),
    ("#RAG  #LLM  #AppliedAI  #AIEngineering","hash"),
],
},

# ── 4. LangGraph Agentic AI ───────────────────────────────────────────────────
{
"filename":"research_agent.py","branch":"main","lang":"Python",
"file_tree":[
    (0,"agentic-workflows",True,False),(1,"agents",True,False),
    (2,"research_agent.py",False,True),(2,"code_agent.py",False,False),
    (2,"orchestrator.py",False,False),(1,"tools",True,False),
    (2,"search.py",False,False),(2,"executor.py",False,False),
    (0,"README.md",False,False),
],
"outline":[(0,"build_graph()",True),(1,"↳ research_node()",False),
           (1,"↳ reflect_node()",False),(1,"↳ write_node()",False),(0,"AgentState",True)],
"headline":[("LangGraph changed how I build ",False),("Agentic AI systems.",True)],
"card_bullets":["→ state machines > prompt chains",
                "→ cycles enable real reflection & retry",
                "→ tool reliability = agent reliability",
                "→ human-in-the-loop is a graph edge"],
"code":[
    "# LangGraph: stateful multi-step AI agents",
    "from langgraph.graph import StateGraph, END",
    "from langchain_core.messages import HumanMessage","",
    "class AgentState(TypedDict):",
    "    messages: list","    research: str","    draft: str","    iterations: int","",
    "def build_graph():",
    "    g = StateGraph(AgentState)",
    "    g.add_node('research',  research_node)",
    "    g.add_node('reflect',   reflect_node)",
    "    g.add_node('write',     write_node)",
    "    g.add_edge('research', 'reflect')",
    "    g.add_conditional_edges('reflect',",
    "        lambda s: 'write' if s['iterations']>2 else 'research')",
    "    g.add_edge('write', END)",
    "    g.set_entry_point('research')",
    "    return g.compile()","",
    "# cycles = agents that actually think before acting",
],
"overlay":[
    ("WHAT AGENTIC AI TAUGHT ME:","head"),("",""),
    ("✓   state machines beat prompt chains","check"),
    ("✓   cycles enable real reflection & retry","check"),
    ("✓   tool reliability = agent reliability","check"),
    ("✓   streaming state makes debugging tractable","check"),
    ("✓   human-in-the-loop is just a conditional edge","check"),("",""),
    ("what's the hardest agent failure mode you've hit?","cta"),("",""),
    ("#AgenticAI  #LangGraph  #LLM  #AIEngineering","hash"),
],
},

# ── 5. Kafka for ML Pipelines ─────────────────────────────────────────────────
{
"filename":"feature_producer.py","branch":"main","lang":"Python",
"file_tree":[
    (0,"streaming-ml-platform",True,False),(1,"producers",True,False),
    (2,"feature_producer.py",False,True),(2,"event_schema.py",False,False),
    (1,"consumers",True,False),(2,"feature_store_sink.py",False,False),
    (2,"model_trigger.py",False,False),(0,"docker-compose.yml",False,False),
    (0,"README.md",False,False),
],
"outline":[(0,"FeatureProducer",True),(1,"↳ __init__()",False),(1,"↳ emit()",False),
           (1,"↳ _serialize()",False),(0,"run_pipeline()",True)],
"headline":[("Real-time AI needs real-time features. ",False),("Kafka is how.",True)],
"card_bullets":["→ batch features = stale predictions",
                "→ streaming cuts feature lag from hours to ms",
                "→ Kafka decouples your ML from your app",
                "→ exactly-once delivery matters in finance/health"],
"code":[
    "# Real-time ML features via Kafka",
    "from confluent_kafka import Producer","import json, time","",
    "class FeatureProducer:",
    "    def __init__(self, brokers: str, topic: str):",
    "        self.producer = Producer({'bootstrap.servers': brokers,",
    "                                  'acks': 'all',",
    "                                  'compression.type': 'lz4'})","        self.topic = topic","",
    "    def emit(self, user_id: str, features: dict) -> None:",
    "        payload = json.dumps({",
    "            'user_id':   user_id,",
    "            'features':  features,",
    "            'timestamp': time.time_ns(),",
    "        }).encode()","        self.producer.produce(self.topic, key=user_id.encode(),",
    "                               value=payload, on_delivery=self._ack)","        self.producer.poll(0)","",
    "# batch pipeline latency: ~4 hours  |  streaming: ~50ms",
],
"overlay":[
    ("AFTER WIRING THIS UP, YOU SEE:","head"),("",""),
    ("✓   ML models need fresh features — batch won't cut it","check"),
    ("✓   streaming cuts prediction latency by 100x","check"),
    ("✓   Kafka decouples ML from application logic","check"),
    ("✓   schema registry saves you from yourself","check"),
    ("✓   exactly-once delivery is non-negotiable in prod","check"),("",""),
    ("what's your real-time feature latency SLA?","cta"),("",""),
    ("#Kafka  #MLOps  #AIInfrastructure  #StreamingAI","hash"),
],
},

# ── 6. AWS AI Factory ─────────────────────────────────────────────────────────
{
"filename":"ai_factory.py","branch":"main","lang":"Python",
"file_tree":[
    (0,"aws-ai-factory",True,False),(1,"pipelines",True,False),
    (2,"ai_factory.py",False,True),(2,"bedrock_chain.py",False,False),
    (2,"sagemaker_endpoint.py",False,False),(1,"infra",True,False),
    (2,"cdk_stack.py",False,False),(2,"iam_roles.py",False,False),
    (0,"README.md",False,False),
],
"outline":[(0,"AIFactory",True),(1,"↳ ingest()",False),(1,"↳ enrich()",False),
           (1,"↳ serve()",False),(0,"BedrockChain",True)],
"headline":[("An AI Factory isn't a model. ",False),("It's an operating system.",True)],
"card_bullets":["→ model is 10% — pipeline is 90%",
                "→ data flywheel beats model upgrades",
                "→ AWS Bedrock + SageMaker = production AI",
                "→ governance from day 1, not day 100"],
"code":[
    "# AWS AI Factory: beyond the model",
    "import boto3","from dataclasses import dataclass","",
    "@dataclass","class AIFactory:",
    "    region: str = 'us-east-1'","",
    "    def __post_init__(self):",
    "        self.bedrock  = boto3.client('bedrock-runtime', region_name=self.region)",
    "        self.s3       = boto3.client('s3')",
    "        self.sm       = boto3.client('sagemaker')","",
    "    def invoke(self, prompt: str, model='amazon.nova-pro-v1:0') -> str:",
    "        resp = self.bedrock.invoke_model(",
    "            modelId=model,",
    "            body=json.dumps({'messages':[{'role':'user','content':prompt}]}),",
    "            contentType='application/json'","        )",
    "        return json.loads(resp['body'].read())['output']['message']['content'][0]['text']","",
    "# model is a commodity — the factory around it is the moat",
],
"overlay":[
    ("BUILDING AI FACTORIES TAUGHT ME:","head"),("",""),
    ("✓   the model is 10% of the problem","check"),
    ("✓   data pipelines are the real competitive moat","check"),
    ("✓   AWS Bedrock makes enterprise AI tractable","check"),
    ("✓   governance baked in beats retrofitted","check"),
    ("✓   the factory compounds — models don't","check"),("",""),
    ("what does your AI factory look like?","cta"),("",""),
    ("#AWS  #AIFactory  #AppliedAI  #AIInfrastructure","hash"),
],
},

# ── 7. PyTorch Distributed Training ──────────────────────────────────────────
{
"filename":"ddp_trainer.py","branch":"main","lang":"Python",
"file_tree":[
    (0,"distributed-training",True,False),(1,"src",True,False),
    (2,"ddp_trainer.py",False,True),(2,"fsdp_trainer.py",False,False),
    (2,"gradient_checkpointing.py",False,False),(1,"configs",True,False),
    (2,"8gpu_config.yaml",False,False),(0,"Makefile",False,False),
    (0,"README.md",False,False),
],
"outline":[(0,"DDPTrainer",True),(1,"↳ setup()",False),(1,"↳ train_epoch()",False),
           (1,"↳ _sync_gradients()",False),(0,"main()",True)],
"headline":[("Distributed training will surprise you. ",False),("Not in a good way.",True)],
"card_bullets":["→ communication overhead kills linear scaling",
                "→ gradient sync is usually your bottleneck",
                "→ FSDP > DDP once model > 7B params",
                "→ mixed precision is table stakes"],
"code":[
    "# PyTorch DDP: what nobody tells you",
    "import torch","import torch.distributed as dist",
    "from torch.nn.parallel import DistributedDataParallel as DDP","",
    "def setup(rank: int, world_size: int):",
    "    dist.init_process_group('nccl', rank=rank, world_size=world_size)","",
    "class DDPTrainer:",
    "    def __init__(self, model, rank, world_size):",
    "        setup(rank, world_size)",
    "        self.model = DDP(model.cuda(rank), device_ids=[rank],",
    "                         gradient_as_bucket_view=True)  # 20% speedup","",
    "    def train_step(self, batch):",
    "        with torch.autocast('cuda', dtype=torch.bfloat16):  # BF16",
    "            loss = self.model(**batch).loss",
    "        loss.backward()   # DDP all-reduces grads automatically","",
    "# 8 GPUs, ideal: 8x speedup  |  real: ~5.8x (comm overhead)",
    "# gradient bucketing + overlap = your path to 7x",
],
"overlay":[
    ("DISTRIBUTED TRAINING REVEALS:","head"),("",""),
    ("✓   8 GPUs ≠ 8x speedup (expect ~73%)","check"),
    ("✓   NCCL all-reduce is your hidden bottleneck","check"),
    ("✓   gradient bucketing recovers 15-20%","check"),
    ("✓   FSDP beats DDP beyond 7B parameters","check"),
    ("✓   BF16 + grad checkpointing = train 70B on 8x A100","check"),("",""),
    ("what's your scaling efficiency on multi-GPU?","cta"),("",""),
    ("#PyTorch  #DistributedTraining  #GPU  #LLM","hash"),
],
},

# ── 8. NVIDIA Nemotron ────────────────────────────────────────────────────────
{
"filename":"nemotron_finetune.py","branch":"main","lang":"Python",
"file_tree":[
    (0,"nemotron-experiments",True,False),(1,"src",True,False),
    (2,"nemotron_finetune.py",False,True),(2,"data_prep.py",False,False),
    (2,"reward_model.py",False,False),(1,"configs",True,False),
    (2,"lora_config.yaml",False,False),(2,"rlhf_config.yaml",False,False),
    (0,"README.md",False,False),
],
"outline":[(0,"NemotronTrainer",True),(1,"↳ load_model()",False),(1,"↳ apply_lora()",False),
           (1,"↳ train()",False),(0,"evaluate()",True)],
"headline":[("NVIDIA Nemotron changed what I thought was ",False),("possible with fine-tuning.",True)],
"card_bullets":["→ domain data > model size every time",
                "→ LoRA fine-tuning in hours, not weeks",
                "→ Nemotron-3 8B beats GPT-3.5 on code",
                "→ RLHF alignment is craft, not science"],
"code":[
    "# NVIDIA Nemotron fine-tuning with LoRA",
    "from nemo.collections.llm import LoRAConfig, FineTuningConfig",
    "from peft import get_peft_model, LoraConfig, TaskType","",
    "def load_nemotron(model_path: str):",
    "    model = AutoModelForCausalLM.from_pretrained(",
    "        model_path,  # nvidia/nemotron-3-8b-base",
    "        torch_dtype=torch.bfloat16,",
    "        attn_implementation='flash_attention_2')","    return model","",
    "def apply_lora(model, r: int = 16, alpha: int = 32):",
    "    cfg = LoraConfig(task_type=TaskType.CAUSAL_LM,",
    "                     r=r, lora_alpha=alpha,",
    "                     target_modules=['q_proj','v_proj'],",
    "                     lora_dropout=0.05)","    return get_peft_model(model, cfg)","",
    "# 8B Nemotron + LoRA: fine-tune in 4h on 1x A100",
    "# domain-tuned 8B > vanilla 70B on your task",
],
"overlay":[
    ("FINE-TUNING NEMOTRON SHOWED ME:","head"),("",""),
    ("✓   domain data beats model scale","check"),
    ("✓   LoRA makes single-GPU fine-tuning real","check"),
    ("✓   Flash Attention 2 is non-optional at 8B+","check"),
    ("✓   RLHF alignment is still craft, not recipe","check"),
    ("✓   Nemotron-3 8B > GPT-3.5 on domain tasks","check"),("",""),
    ("what domain have you fine-tuned on?","cta"),("",""),
    ("#NVIDIA  #Nemotron  #LLM  #FineTuning  #GenAI","hash"),
],
},

# ── 9. GPU Memory Bandwidth ───────────────────────────────────────────────────
{
"filename":"memory_bench.cu","branch":"main","lang":"CUDA",
"file_tree":[
    (0,"gpu-perf-lab",True,False),(1,"src",True,False),
    (2,"memory_bench.cu",False,True),(2,"compute_bench.cu",False,False),
    (2,"roofline.py",False,False),(1,"results",True,False),
    (2,"a100_roofline.png",False,False),(0,"Makefile",False,False),
    (0,"README.md",False,False),
],
"outline":[(0,"bandwidth_test()",True),(1,"↳ coalesced read",False),
           (1,"↳ strided read",False),(1,"↳ random read",False),(0,"roofline_plot()",True)],
"headline":[("Your GPU isn't compute-bound. ",False),("It's memory-bound.",True)],
"card_bullets":["→ A100 peak: 312 TFLOPS — BW: 2 TB/s",
                "→ most ops live well below the roofline",
                "→ memory coalescing is free performance",
                "→ cache beats compute optimisation every time"],
"code":[
    "// Memory bandwidth: the real GPU bottleneck",
    "#include <cuda_runtime.h>","",
    "__global__ void coalesced_read(float* in, float* out, int N) {",
    "    int i = blockIdx.x * blockDim.x + threadIdx.x;",
    "    if (i < N) out[i] = in[i];   // ← coalesced: 1 transaction",
    "}","",
    "__global__ void strided_read(float* in, float* out, int N, int stride) {",
    "    int i = (blockIdx.x * blockDim.x + threadIdx.x) * stride;",
    "    if (i < N) out[i/stride] = in[i];  // ← strided: N transactions",
    "}","",
    "// benchmark result on A100:",
    "// coalesced:  1,935 GB/s  (96% of peak)",
    "// stride=2:   1,021 GB/s  (50% of peak)",
    "// stride=32:    64 GB/s   ( 3% of peak  ← THIS is your bottleneck)",
    "//",
    "// fix your access pattern before tuning anything else.",
],
"overlay":[
    ("MEMORY BANDWIDTH TAUGHT ME:","head"),("",""),
    ("✓   FLOPS are free — data movement is expensive","check"),
    ("✓   strided access kills performance (3% of peak)","check"),
    ("✓   L2 cache hit rate is your perf leading indicator","check"),
    ("✓   roofline model tells you where you actually are","check"),
    ("✓   Nsight Compute shows the truth in 30 seconds","check"),("",""),
    ("what's your L2 cache hit rate in production?","cta"),("",""),
    ("#GPU  #CUDA  #HPC  #AIInfrastructure  #Performance","hash"),
],
},

# ── 10. Flash Attention ───────────────────────────────────────────────────────
{
"filename":"flash_attn_fwd.cu","branch":"main","lang":"CUDA",
"file_tree":[
    (0,"attention-kernels",True,False),(1,"src",True,False),
    (2,"flash_attn_fwd.cu",False,True),(2,"naive_attn.cu",False,False),
    (2,"flash_attn_bwd.cu",False,False),(1,"bench",True,False),
    (2,"attn_bench.py",False,False),(0,"Makefile",False,False),
    (0,"README.md",False,False),
],
"outline":[(0,"flash_fwd_kernel()",True),(1,"↳ load Q block",False),
           (1,"↳ online softmax",False),(1,"↳ accumulate O",False),(0,"host_flash_fwd()",True)],
"headline":[("Flash Attention is the best algorithm ",False),("most engineers never read.",True)],
"card_bullets":["→ O(N) HBM reads instead of O(N²)",
                "→ tiling + online softmax = same result",
                "→ -88% memory bandwidth vs naive",
                "→ reading the paper changes your intuition"],
"code":[
    "// Flash Attention: O(N) HBM reads, not O(N²)",
    "#define BLK 64","",
    "__global__ void flash_fwd(",
    "    const float* Q, const float* K, const float* V,",
    "    float* O, int N, int d, float scale) {",
    "  __shared__ float Qs[BLK][64], Ks[BLK][64], Vs[BLK][64];",
    "  float m=-1e9f, l=0.f, acc[64]={};",
    "  // load Q block once — never materialise N×N matrix",
    "  load_tile(Q, Qs, blockIdx.x, N, d);",
    "  for (int j=0; j<N/BLK; j++) {",
    "    load_tile(K, Ks, j, N, d);",
    "    load_tile(V, Vs, j, N, d);",
    "    // online softmax: update m and l incrementally",
    "    online_softmax(Qs, Ks, Vs, acc, m, l, scale, d);",
    "    __syncthreads();",
    "  }","  write_output(O, acc, l, blockIdx.x, N, d);","}","",
    "// HBM reads: naive O(N²) → flash O(N)  (-88% bandwidth)",
],
"overlay":[
    ("FLASH ATTENTION CHANGED HOW I THINK:","head"),("",""),
    ("✓   O(N) vs O(N²) HBM reads — the key insight","check"),
    ("✓   tiling + online softmax = same numerics","check"),
    ("✓   -88% memory bandwidth over naive attention","check"),
    ("✓   SM utilisation: 31% naive → 84% flash","check"),
    ("✓   reading the paper ≠ understanding the kernel","check"),("",""),
    ("have you read the FlashAttention paper end-to-end?","cta"),("",""),
    ("#CUDA  #FlashAttention  #LLM  #Transformer  #GPU","hash"),
],
},

# ── 11. Multi-Agent Systems ───────────────────────────────────────────────────
{
"filename":"orchestrator.py","branch":"main","lang":"Python",
"file_tree":[
    (0,"multi-agent-system",True,False),(1,"agents",True,False),
    (2,"orchestrator.py",False,True),(2,"planner_agent.py",False,False),
    (2,"executor_agent.py",False,False),(2,"critic_agent.py",False,False),
    (1,"tools",True,False),(2,"code_runner.py",False,False),
    (0,"README.md",False,False),
],
"outline":[(0,"Orchestrator",True),(1,"↳ route()",False),(1,"↳ plan()",False),
           (1,"↳ execute()",False),(1,"↳ critique()",False)],
"headline":[("Multi-agent AI systems break in ways ",False),("single agents don't.",True)],
"card_bullets":["→ reliability compounds across agents",
                "→ one bad tool = broken entire workflow",
                "→ async execution needs explicit state",
                "→ critique agents cut errors by 40%"],
"code":[
    "# Multi-agent orchestration: where complexity hides",
    "from langgraph.graph import StateGraph",
    "from typing import Literal","",
    "class Orchestrator:",
    "    def __init__(self, llm, tools: dict):",
    "        self.llm   = llm","        self.tools = tools","        self.graph = self._build()","",
    "    def route(self, state) -> Literal['plan','execute','critique','end']:",
    "        if state['errors'] > 2: return 'end'   # circuit breaker",
    "        if not state['plan']:   return 'plan'",
    "        if not state['result']: return 'execute'",
    "        return 'critique' if state['iterations'] < 3 else 'end'","",
    "    def critique(self, state):",
    "        # critic agent: independent LLM call to verify output",
    "        verdict = self.llm.invoke(CRITIQUE_PROMPT.format(**state))",
    "        return {'verified': verdict.score > 0.8,",
    "                'feedback': verdict.reasoning}","",
    "# without critique: 61% task success  |  with: 84%",
],
"overlay":[
    ("MULTI-AGENT SYSTEMS REVEALED:","head"),("",""),
    ("✓   reliability compounds — one bad tool = broken chain","check"),
    ("✓   circuit breakers are non-optional in production","check"),
    ("✓   critic agents add 23% success rate for free","check"),
    ("✓   async execution needs explicit shared state","check"),
    ("✓   LangGraph makes these patterns tractable","check"),("",""),
    ("what's your hardest multi-agent failure mode?","cta"),("",""),
    ("#AgenticAI  #LangGraph  #LLM  #AIEngineering","hash"),
],
},

# ── 12. Production AI Mistakes ────────────────────────────────────────────────
{
"filename":"serving.py","branch":"main","lang":"Python",
"file_tree":[
    (0,"production-ai",True,False),(1,"src",True,False),
    (2,"serving.py",False,True),(2,"monitor.py",False,False),
    (2,"guardrails.py",False,False),(1,"infra",True,False),
    (2,"k8s_deploy.yaml",False,False),(2,"autoscale.yaml",False,False),
    (0,"README.md",False,False),
],
"outline":[(0,"AIServer",True),(1,"↳ predict()",False),(1,"↳ _validate()",False),
           (1,"↳ _monitor()",False),(0,"HealthCheck",True)],
"headline":[("3 mistakes every team makes ",False),("deploying AI to production.",True)],
"card_bullets":["→ mistake 1: demo accuracy ≠ prod accuracy",
                "→ mistake 2: no latency SLA before launch",
                "→ mistake 3: monitoring as an afterthought",
                "→ all 3 are fixable — before you ship"],
"code":[
    "# Production AI: the 3 mistakes in code",
    "from fastapi import FastAPI","import time, prometheus_client as prom","",
    "LATENCY  = prom.Histogram('ai_latency_seconds', 'Predict latency')",
    "ACCURACY = prom.Gauge('ai_accuracy_7d', 'Rolling 7-day accuracy')","",
    "class AIServer:",
    "    async def predict(self, request):",
    "        # mistake 1: no input validation → garbage in, garbage out",
    "        payload = self._validate(request)   # schema + range checks","",
    "        # mistake 2: no latency budget → silent SLA breaches",
    "        with LATENCY.time():",
    "            result = await self.model.apredict(payload)","",
    "        # mistake 3: no monitoring → blind in production",
    "        self._emit_metrics(payload, result)","        return result","",
    "# with monitoring: MTTR 4h → 23 min",
    "# with validation: prod accuracy gap 18% → 4%",
],
"overlay":[
    ("PRODUCTION AI TAUGHT ME:","head"),("",""),
    ("✓   demo accuracy ≠ production accuracy (usually -18%)","check"),
    ("✓   set your latency SLA before you write a line","check"),
    ("✓   monitoring is the feature — not an afterthought","check"),
    ("✓   input validation cuts accuracy gap by 4x","check"),
    ("✓   MTTR drops from 4h to 23min with good observability","check"),("",""),
    ("which mistake cost your team the most?","cta"),("",""),
    ("#AppliedAI  #MLOps  #AIEngineering  #ProductionAI","hash"),
],
},

# ── 13. AI Infrastructure ─────────────────────────────────────────────────────
{
"filename":"gpu_cluster.py","branch":"main","lang":"Python",
"file_tree":[
    (0,"ai-infrastructure",True,False),(1,"compute",True,False),
    (2,"gpu_cluster.py",False,True),(2,"spot_manager.py",False,False),
    (2,"autoscaler.py",False,False),(1,"storage",True,False),
    (2,"s3_fsx_bridge.py",False,False),(0,"cdk_app.py",False,False),
    (0,"README.md",False,False),
],
"outline":[(0,"GPUCluster",True),(1,"↳ provision()",False),(1,"↳ schedule_job()",False),
           (1,"↳ spot_fallback()",False),(0,"CostOptimizer",True)],
"headline":[("AI Infrastructure is the competitive moat. ",False),("Not the model.",True)],
"card_bullets":["→ 70% of AI cost is idle compute",
                "→ spot + on-demand hybrid cuts cost 60%",
                "→ data pipeline speed > model accuracy",
                "→ the infra compounds — models commoditise"],
"code":[
    "# AI Infrastructure: the real competitive moat",
    "import boto3","from dataclasses import dataclass, field","",
    "@dataclass","class GPUCluster:",
    "    instance_type: str = 'p4d.24xlarge'   # 8x A100",
    "    max_nodes:     int = 16",
    "    spot_ratio:    float = 0.7  # 70% spot = 60% cost reduction","",
    "    def schedule_job(self, job_config: dict) -> str:",
    "        # prefer spot; fall back to on-demand automatically",
    "        try:",
    "            return self._launch_spot(job_config)",
    "        except SpotCapacityError:",
    "            return self._launch_ondemand(job_config)","",
    "    def utilisation(self) -> float:",
    "        metrics = self.cw.get_metric_data(...)",
    "        return metrics['gpu_util_avg']   # target: >80%","",
    "# idle GPU = burning money.  target: 80%+ utilisation",
],
"overlay":[
    ("AI INFRA REVEALED:","head"),("",""),
    ("✓   70% of AI spend is idle compute — fix scheduling","check"),
    ("✓   spot + on-demand hybrid cuts GPU cost 60%","check"),
    ("✓   data pipeline throughput > model accuracy","check"),
    ("✓   80%+ GPU utilisation is the operating target","check"),
    ("✓   infra compounds over time — models commoditise","check"),("",""),
    ("what's your GPU utilisation in production?","cta"),("",""),
    ("#AIInfrastructure  #AWS  #GPU  #HPC  #CloudAI","hash"),
],
},

# ── 14. Forward Deployed AI ───────────────────────────────────────────────────
{
"filename":"integration.py","branch":"main","lang":"Python",
"file_tree":[
    (0,"forward-deployed-ai",True,False),(1,"connectors",True,False),
    (2,"integration.py",False,True),(2,"workflow_mapper.py",False,False),
    (2,"data_adapter.py",False,False),(1,"evals",True,False),
    (2,"customer_eval.py",False,False),(2,"ab_test.py",False,False),
    (0,"README.md",False,False),
],
"outline":[(0,"CustomerIntegration",True),(1,"↳ discover_workflow()",False),
           (1,"↳ adapt_data()",False),(1,"↳ deploy()",False),(0,"eval_loop()",True)],
"headline":[("Forward Deployed AI engineering is ",False),("the hardest job in tech.",True)],
"card_bullets":["→ the best AI solves a workflow, not a benchmark",
                "→ customer data is always messier than the demo",
                "→ integration is 80% of the work",
                "→ trust is built in iteration 3, not iteration 1"],
"code":[
    "# Forward Deployed AI: what the job actually looks like",
    "from typing import Any","",
    "class CustomerIntegration:",
    "    \"\"\"90% of forward-deployed work is right here.\"\"\"","",
    "    def discover_workflow(self, customer_id: str) -> dict:",
    "        # step 1: map their actual workflow, not the demo one",
    "        raw = self.crm.get_processes(customer_id)",
    "        return self._extract_ai_opportunities(raw)","",
    "    def adapt_data(self, raw_data: Any) -> dict:",
    "        # customer data is ALWAYS messier than you expect",
    "        return {",
    "            'cleaned':   self._clean(raw_data),",
    "            'validated': self._validate(raw_data),",
    "            'enriched':  self._enrich(raw_data),",
    "        }","",
    "    def eval_loop(self, outputs, ground_truth):",
    "        # trust is built here — in iterations 3, 5, 10",
    "        return {'accuracy': ..., 'latency': ..., 'cost': ...}","",
    "# demo: 2 days  |  production for a real customer: 8 weeks",
],
"overlay":[
    ("FORWARD DEPLOYED TAUGHT ME:","head"),("",""),
    ("✓   the best AI solves a workflow, not a benchmark","check"),
    ("✓   customer data is always messier than the demo","check"),
    ("✓   trust is earned in iteration 3, not 1","check"),
    ("✓   integration is 80% of the actual work","check"),
    ("✓   the gap from demo to prod is where engineers live","check"),("",""),
    ("what's the biggest gap you've seen: demo → production?","cta"),("",""),
    ("#ForwardDeployed  #AppliedAI  #AIEngineering  #LLM","hash"),
],
},

# ── 15. AI Patent / Invention ─────────────────────────────────────────────────
{
"filename":"invention_log.py","branch":"main","lang":"Python",
"file_tree":[
    (0,"ai-patent-research",True,False),(1,"experiments",True,False),
    (2,"invention_log.py",False,True),(2,"prior_art.py",False,False),
    (2,"claim_drafter.py",False,False),(1,"notebooks",True,False),
    (2,"novelty_analysis.ipynb",False,False),(0,"README.md",False,False),
    (0,"disclosure.md",False,False),
],
"outline":[(0,"InventionLog",True),(1,"↳ capture()",False),(1,"↳ prior_art_search()",False),
           (1,"↳ draft_claims()",False),(0,"NoveltyScorer",True)],
"headline":[("The AI engineers who will matter most ",False),("are the ones who invent.",True)],
"card_bullets":["→ patents = moat that doesn't depreciate",
                "→ most novel AI work goes undocumented",
                "→ invention starts with 'why doesn't this exist?'",
                "→ filed ≠ granted — but filed matters"],
"code":[
    "# AI Patent workflow: capturing invention as it happens",
    "from datetime import datetime","import hashlib","",
    "class InventionLog:",
    "    \"\"\"Log novel AI methods before the moment passes.\"\"\"","",
    "    def capture(self, title: str, problem: str,",
    "                solution: str, results: dict) -> str:",
    "        disclosure = {",
    "            'title':     title,",
    "            'problem':   problem,   # prior art gap",
    "            'solution':  solution,  # novel method",
    "            'evidence':  results,   # quantitative delta",
    "            'timestamp': datetime.utcnow().isoformat(),",
    "        }","        uid = hashlib.sha256(str(disclosure).encode()).hexdigest()[:8]",
    "        self._save(uid, disclosure)","        return uid","",
    "    def prior_art_search(self, query: str) -> list:",
    "        # USPTO + arXiv + semantic scholar — all three",
    "        return self.searcher.search(query, sources=['uspto','arxiv'])","",
    "# every novel result deserves a disclosure. most don't get one.",
],
"overlay":[
    ("BEING AN AI PATENT INVENTOR TAUGHT ME:","head"),("",""),
    ("✓   most novel work goes undocumented — don't let yours","check"),
    ("✓   invention starts with: why doesn't this exist?","check"),
    ("✓   prior art search is 80% of the work","check"),
    ("✓   a patent is a 20-year technical moat","check"),
    ("✓   filed ≠ granted — but filed changes how you think","check"),("",""),
    ("have you ever filed a patent? what was the insight?","cta"),("",""),
    ("#AIPatent  #Innovation  #AIResearch  #AIEngineering","hash"),
],
},

]  # end POSTS

# ══════════════════════════════════════════════════════════════════════════════
#  Generator
# ══════════════════════════════════════════════════════════════════════════════

def build_gif(p):
    frames = []
    sf = split_frame(p)
    for _ in range(8): frames.append((sf, 100))   # 0.8s split view

    typed = []
    for li, line in enumerate(p["code"]):
        typed.append("")
        for ci, ch in enumerate(line):
            typed[-1] += ch
            if ci % 3 == 0:
                frames.append((full_frame(p, list(typed), li), 30))
        for _ in range(2):
            frames.append((full_frame(p, list(typed), li), 60))

    last = list(typed); ll = len(p["code"]) - 1
    frames.append((full_frame(p, last, ll), 300))
    frames.append((full_frame(p, last, -1), 300))

    base = full_frame(p, last, ll)
    ov   = overlay_frame(base, p)
    for _ in range(20): frames.append((ov, 100))   # 2s overlay
    return frames

def save(frames, path, colors=96):
    imgs = [f[0].quantize(colors=colors, method=Image.Quantize.MEDIANCUT) for f in frames]
    durs = [f[1] for f in frames]
    imgs[0].save(path, save_all=True, append_images=imgs[1:], duration=durs, loop=0, optimize=True)
    print(f"  {os.path.basename(path)}  {os.path.getsize(path)//1024} KB")

def split_frame(p):
    img  = Image.new("RGB", (W, H), T["ide_bg"]); draw = ImageDraw.Draw(img)
    titlebar(draw, HALF, p["filename"])
    sidebar(draw, p["file_tree"], p["outline"])
    EDX = SB_W
    draw.rectangle([EDX,TITLE_H,HALF,TITLE_H+TAB_H], fill=T["tabbar_bg"])
    te = EDX+min(len(p["filename"])*8+36,180)
    draw.rectangle([EDX,TITLE_H,te,TITLE_H+TAB_H], fill=T["ide_bg"])
    draw.ellipse([EDX+7,TITLE_H+TAB_H//2-5,EDX+17,TITLE_H+TAB_H//2+5], fill=T["tab_dot"])
    draw.text((EDX+21,TITLE_H+(TAB_H-11)//2), p["filename"], fill=T["text"], font=f_ui)
    draw.rectangle([EDX,TITLE_H+TAB_H,EDX+GUT_W,H-STAT_H], fill=T["gutter_bg"])
    status_bar(draw, HALF, p.get("branch","main"), p.get("lang","Python"))
    draw.rectangle([HALF,0,W,H], fill=T["card_bg"])
    px=HALF+46; cy=100; lh=68; cx=px
    for text,hi in p["headline"]:
        col = T["card_cyan"] if hi else T["card_white"]
        for word in text.split():
            tw=draw.textlength(word+" ",font=f_head)
            if cx+tw>W-46 and cx>px: cx=px; cy+=lh
            draw.text((cx,cy), word, fill=col, font=f_head); cx+=tw
    cy+=lh+20
    draw.rectangle([px,cy,px+118,cy+4], fill=T["card_div"]); cy+=28
    for b in p["card_bullets"]:
        draw.text((px,cy), b, fill=T["card_body"], font=f_bullet); cy+=36
    return img

def full_frame(p, code_lines, cursor_li):
    img  = Image.new("RGB", (W, H), T["ide_bg"]); draw = ImageDraw.Draw(img)
    titlebar(draw, W, p["filename"])
    sidebar(draw, p["file_tree"], p["outline"])
    draw.rectangle([SB_W,TITLE_H,W,H], fill=T["ide_bg"])
    EDX=SB_W
    draw.rectangle([EDX,TITLE_H,W,TITLE_H+TAB_H], fill=T["tabbar_bg"])
    te=EDX+min(len(p["filename"])*8+36,220)
    draw.rectangle([EDX,TITLE_H,te,TITLE_H+TAB_H], fill=T["ide_bg"])
    draw.line([te,TITLE_H,te,TITLE_H+TAB_H], fill=T["dim"])
    draw.ellipse([EDX+7,TITLE_H+TAB_H//2-5,EDX+17,TITLE_H+TAB_H//2+5], fill=T["tab_dot"])
    draw.text((EDX+21,TITLE_H+(TAB_H-11)//2), p["filename"], fill=T["text"], font=f_ui)
    draw.rectangle([EDX,TITLE_H+TAB_H,EDX+GUT_W,H-STAT_H], fill=T["gutter_bg"])
    code_area(draw, W, code_lines, cursor_li)
    status_bar(draw, W, p.get("branch","main"), p.get("lang","Python"))
    return img

def overlay_frame(base_img, p):
    img=base_img.copy(); draw=ImageDraw.Draw(img)
    top=TITLE_H+TAB_H+4; bot=H-STAT_H-OL_H
    total=len(p["code"])
    box_start=max(10, total-14)
    box_y1=top+box_start*LH-4; box_y2=bot-4
    box_x1=SB_W+GUT_W-8; box_x2=W-8
    draw.rectangle([box_x1,box_y1,box_x2,box_y2], fill=T["ov_bg"])
    draw.rectangle([box_x1,box_y1,box_x2,box_y2], outline=T["ov_border"], width=2)
    tx=box_x1+14; ty=box_y1+12; lh_ov=25
    for text,kind in p["overlay"]:
        if kind in (None,""): ty+=lh_ov//2; continue
        col={"head":T["ov_head"],"check":T["ov_check"],"cta":T["ov_cta"],"hash":T["ov_hash"]}[kind]
        font=f_ov_h if kind=="head" else f_ov_b
        draw.text((tx,ty), text, fill=col, font=font); ty+=lh_ov
    return img

if __name__ == "__main__":
    for i, p in enumerate(POSTS, 1):
        name = f"post{i:02d}.gif"
        print(f"\n[{i:02d}/15] {p['filename']}")
        frames = build_gif(p)
        save(frames, f"{OUT}/{name}")
    print(f"\nDone! {len(POSTS)} GIFs in {OUT}")
