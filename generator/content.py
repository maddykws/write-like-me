# -*- coding: utf-8 -*-
"""60-day LinkedIn content plan: post copy + GIF storyboards.

Posts 1-15  -> terminal-output style GIFs (start with Java, then Python, then AI/token/GPU).
Posts 16-60 -> Engineering-Manager point-of-view GIFs.
"""

# Each entry:
#   n      : post number (1-60)
#   topic  : short tag used in filename + post header
#   style  : "terminal" or "em"
#   post   : full LinkedIn post text
#   gif    : dict with "title" (window/header text) and "lines"
#            terminal lines: ("prompt"|"output"|"comment", text)
#            em lines:       ("head", text) | ("todo", text) | ("done", text) | ("note", text)

POSTS = [
    # ============================ TERMINAL (1-15) ============================
    dict(n=1, topic="Java", style="terminal",
         post=(
"Most Java latency problems aren't in your code. They're in the JVM you never tuned.\n\n"
"A service I inherited spiked to 400ms p99 every few minutes. The code was fine. The garbage collector wasn't.\n\n"
"What actually moved the needle:\n"
"- Switched to G1GC and set a pause target instead of guessing heap sizes\n"
"- Right-sized the heap to the container, not the host\n"
"- Watched allocation rate, not just heap usage\n\n"
"p99 dropped to 90ms. Zero code changes.\n\n"
"Before you rewrite the service, read the GC logs. The JVM is usually telling you exactly what's wrong.\n\n"
"#Java #JVM #Performance #BackendEngineering #SoftwareEngineering"),
         gif=dict(title="java-gc-tuning", lines=[
            ("comment", "# p99 latency spiking? check the GC, not the code"),
            ("prompt", "java -Xlog:gc* -jar service.jar"),
            ("output", "[gc] Pause Full (Allocation Failure) 412ms"),
            ("output", "[gc] Pause Full (Allocation Failure) 388ms"),
            ("comment", "# switch to G1 + pause target"),
            ("prompt", "java -XX:+UseG1GC -XX:MaxGCPauseMillis=100 -jar service.jar"),
            ("output", "[gc] Pause Young (Normal) 11ms"),
            ("output", "[gc] Pause Young (Normal) 9ms"),
            ("output", "p99: 412ms -> 90ms  | code changes: 0"),
         ])),

    dict(n=2, topic="Java", style="terminal",
         post=(
"Java virtual threads quietly killed one of the oldest excuses in backend engineering.\n\n"
"\"We can't handle that many concurrent requests, threads are too expensive.\"\n\n"
"With Project Loom, a thread is no longer a heavyweight OS resource. You can spin up hundreds of thousands of them and write plain, blocking, readable code.\n\n"
"No reactive spaghetti. No callback hell. Just code that reads top to bottom.\n\n"
"The mental model shift: stop pooling threads like they're scarce. They aren't anymore.\n\n"
"If you wrote off Java as legacy, it's worth a second look.\n\n"
"#Java #Concurrency #ProjectLoom #VirtualThreads #SoftwareEngineering"),
         gif=dict(title="java-virtual-threads", lines=[
            ("comment", "# 100k concurrent tasks, blocking style"),
            ("prompt", "jshell virtual-threads.java"),
            ("output", "try (var ex = Executors.newVirtualThreadPerTaskExecutor()) {"),
            ("output", "    IntStream.range(0, 100_000)"),
            ("output", "        .forEach(i -> ex.submit(this::handle));"),
            ("output", "}"),
            ("comment", "# OS threads used:"),
            ("output", "platform_threads = 12"),
            ("output", "virtual_threads  = 100000   # cost: ~nothing"),
         ])),

    dict(n=3, topic="Java", style="terminal",
         post=(
"\"Streams are slower than loops\" is the most repeated half-truth in Java.\n\n"
"The truth: streams aren't free, but the difference rarely matters, and readability almost always does.\n\n"
"Where streams genuinely cost you:\n"
"- Hot loops running millions of times per second\n"
"- Boxing primitives (use IntStream / LongStream)\n"
"- Tiny collections where setup overhead dominates\n\n"
"Everywhere else? Write the version your teammate can read at 2am during an incident.\n\n"
"Optimize for the bottleneck you measured, not the one you imagined.\n\n"
"#Java #CleanCode #Performance #SoftwareEngineering #Streams"),
         gif=dict(title="java-streams-vs-loops", lines=[
            ("comment", "# microbenchmark: sum 10M ints"),
            ("prompt", "java -jar jmh-bench.jar SumBench"),
            ("output", "forLoop          avgt   2.1 ms/op"),
            ("output", "stream (boxed)   avgt   8.7 ms/op   <- boxing tax"),
            ("output", "IntStream        avgt   2.3 ms/op   <- basically a tie"),
            ("comment", "# readability delta: huge. speed delta: noise"),
            ("output", "verdict: write the one you can debug at 2am"),
         ])),

    dict(n=4, topic="Python", style="terminal",
         post=(
"Python type hints don't slow you down. Skipping them does, three months later.\n\n"
"I used to think types were ceremony for a dynamic language. Then I came back to my own code and couldn't remember what a function actually returned.\n\n"
"What type hints + mypy buy you:\n"
"- Bugs caught before runtime, not in production\n"
"- IDE autocomplete that actually works\n"
"- Documentation that can't go stale\n\n"
"They're not about pleasing the compiler. There isn't one. They're about being kind to future-you.\n\n"
"Add `mypy --strict` to CI and watch your refactors stop being scary.\n\n"
"#Python #TypeHints #mypy #CleanCode #SoftwareEngineering"),
         gif=dict(title="python-type-safety", lines=[
            ("comment", "# looks fine... until it isn't"),
            ("prompt", "python app.py"),
            ("output", "TypeError: can only concatenate str (not \"int\") to str"),
            ("comment", "# add hints, let mypy find it first"),
            ("prompt", "mypy --strict app.py"),
            ("output", "app.py:14: error: Argument 1 has incompatible type \"int\""),
            ("output", "Found 1 error in 1 file (before it shipped)"),
         ])),

    dict(n=5, topic="Python", style="terminal",
         post=(
"The most common Python async bug isn't a race condition. It's accidentally writing synchronous code that looks async.\n\n"
"You sprinkle `async` and `await` everywhere, then call a blocking library inside the event loop and wonder why concurrency disappeared.\n\n"
"Three rules that fix 90% of asyncio pain:\n"
"- One blocking call freezes the entire loop. Push it to a thread.\n"
"- `asyncio.gather` for things that should run together\n"
"- Never `time.sleep` in async code. It's `await asyncio.sleep`.\n\n"
"async isn't magic parallelism. It's cooperative. One greedy task starves the rest.\n\n"
"#Python #asyncio #Concurrency #BackendEngineering #SoftwareEngineering"),
         gif=dict(title="python-asyncio", lines=[
            ("comment", "# 'async' everywhere but still slow?"),
            ("prompt", "python -X importtime bot.py"),
            ("output", "requests.get(url)   # BLOCKS the whole loop"),
            ("comment", "# fix: don't block the loop"),
            ("output", "await asyncio.to_thread(requests.get, url)"),
            ("output", "await asyncio.gather(*tasks)"),
            ("output", "throughput: 1 req/s -> 240 req/s"),
         ])),

    dict(n=6, topic="Python", style="terminal",
         post=(
"A Python for-loop over a million rows isn't slow because Python is slow. It's slow because you're paying the interpreter tax a million times.\n\n"
"Vectorization moves that work down into C.\n\n"
"A data job I rewrote went from 38 seconds to 0.4 seconds. Same laptop. Same logic. No loop.\n\n"
"The shift in thinking:\n"
"- Stop asking \"how do I loop faster\"\n"
"- Start asking \"how do I express this as one operation on the whole array\"\n\n"
"NumPy and pandas reward you for thinking in columns, not rows.\n\n"
"#Python #NumPy #DataEngineering #Performance #Pandas"),
         gif=dict(title="python-vectorization", lines=[
            ("comment", "# loop vs vectorized: same result"),
            ("prompt", "python bench.py"),
            ("output", "for-loop over 1,000,000 rows ... 38.2s"),
            ("comment", "# express it as one array op"),
            ("output", "result = (arr * weights).sum(axis=1)"),
            ("output", "vectorized ........................ 0.41s"),
            ("output", "speedup: ~93x  | loops written: 0"),
         ])),

    dict(n=7, topic="AI", style="terminal",
         post=(
"Most \"the AI hallucinated\" complaints are really \"we gave it no way to know the answer.\"\n\n"
"Retrieval-augmented generation (RAG) fixes that by handing the model the right context at query time instead of hoping it memorized your data.\n\n"
"The pipeline is simpler than the hype suggests:\n"
"- Chunk your documents thoughtfully (this is where most RAG dies)\n"
"- Embed and store them\n"
"- Retrieve the most relevant chunks per question\n"
"- Let the model answer using only that context\n\n"
"Garbage retrieval = garbage answers. Spend your time on chunking and ranking, not the prompt.\n\n"
"#AI #RAG #LLM #MachineLearning #GenAI"),
         gif=dict(title="rag-pipeline", lines=[
            ("comment", "# RAG = give the model the right context"),
            ("prompt", "python rag.py --q \"what's our refund policy?\""),
            ("output", "[embed]    query -> vector"),
            ("output", "[retrieve] top_k=4 chunks (score > 0.82)"),
            ("output", "[augment]  context injected into prompt"),
            ("output", "[generate] answer grounded in 4 sources"),
            ("output", "hallucination risk: down. citations: up."),
         ])),

    dict(n=8, topic="AI", style="terminal",
         post=(
"The order of your prompt changes the answer more than most people realize.\n\n"
"Same instructions, same model. Move the instruction from the bottom to the top and quality jumps.\n\n"
"What consistently works:\n"
"- Put the task and constraints first\n"
"- Give the model a role and a clear output format\n"
"- Place long context before the question, not after\n"
"- Show one example of exactly what 'good' looks like\n\n"
"Prompt engineering isn't tricks. It's removing ambiguity until there's only one reasonable interpretation.\n\n"
"#AI #PromptEngineering #LLM #GenAI #MachineLearning"),
         gif=dict(title="prompt-structure", lines=[
            ("comment", "# same model, different prompt structure"),
            ("prompt", "python eval.py --variant unstructured"),
            ("output", "accuracy: 0.71   format errors: 14%"),
            ("comment", "# role -> task -> context -> format -> example"),
            ("prompt", "python eval.py --variant structured"),
            ("output", "accuracy: 0.93   format errors: 0%"),
            ("output", "delta from reordering words: +22 points"),
         ])),

    dict(n=9, topic="Token Optimization", style="terminal",
         post=(
"Your LLM bill is mostly tokens you didn't need to send.\n\n"
"I audited a production prompt that ran 2M times a month. Half of it was boilerplate the model never used.\n\n"
"Where the waste hides:\n"
"- Re-sending static instructions on every call\n"
"- Dumping whole documents when 3 paragraphs would do\n"
"- Verbose few-shot examples that could be trimmed in half\n"
"- Asking for explanations you immediately throw away\n\n"
"We cut input tokens 60% and quality didn't move. The bill did.\n\n"
"Token optimization is just respecting the model's attention and your budget.\n\n"
"#AI #TokenOptimization #LLM #GenAI #CostOptimization"),
         gif=dict(title="token-audit", lines=[
            ("comment", "# audit a prompt running 2M times/month"),
            ("prompt", "python token_audit.py prod_prompt.txt"),
            ("output", "input tokens/call: 4,120"),
            ("output", "  - static boilerplate: 1,900  (never referenced)"),
            ("output", "  - oversized context:    810  (unused)"),
            ("comment", "# trim + retrieve only what's needed"),
            ("output", "input tokens/call: 1,640   (-60%)"),
            ("output", "quality: unchanged | monthly cost: -60%"),
         ])),

    dict(n=10, topic="Token Optimization", style="terminal",
         post=(
"If you're sending the same system prompt on every API call, you're paying for it every single time. You don't have to.\n\n"
"Prompt caching lets the model reuse the expensive, unchanging part of your prompt, so you only pay full price for the part that actually changes.\n\n"
"Best candidates to cache:\n"
"- Long system instructions\n"
"- Static few-shot examples\n"
"- Large reference documents reused across requests\n\n"
"On a chat app with a heavy system prompt, caching cut our latency and cost on cached tokens dramatically, for what amounted to a config change.\n\n"
"Structure your prompt so the stable stuff comes first. Then cache it.\n\n"
"#AI #TokenOptimization #PromptCaching #LLM #CostOptimization"),
         gif=dict(title="prompt-caching", lines=[
            ("comment", "# stable prefix + changing suffix"),
            ("prompt", "python chat.py --cache on"),
            ("output", "[cache] system prompt (1,800 tok) -> WRITE"),
            ("output", "[cache] system prompt (1,800 tok) -> HIT"),
            ("output", "[cache] system prompt (1,800 tok) -> HIT"),
            ("comment", "# only new tokens billed at full rate"),
            ("output", "cached-token cost: down sharply"),
            ("output", "latency on cache hit: noticeably lower"),
         ])),

    dict(n=11, topic="GPU", style="terminal",
         post=(
"Your GPU is probably idle most of the time you think it's working.\n\n"
"\"CUDA out of memory\" and \"why is my GPU at 20% utilization\" are usually the same bug wearing two hats: bad batching.\n\n"
"What changed everything for me:\n"
"- Watch GPU utilization, not just memory\n"
"- Batch requests so the GPU does real work per kernel launch\n"
"- Stop tiny one-sample inferences that leave the card waiting\n\n"
"A model serving 12 req/s went to 90+ req/s on the same hardware once we batched properly.\n\n"
"The expensive silicon isn't the problem. Feeding it is.\n\n"
"#GPU #CUDA #MachineLearning #MLOps #Performance"),
         gif=dict(title="gpu-batching", lines=[
            ("comment", "# expensive card, barely working"),
            ("prompt", "nvidia-smi --query-gpu=utilization.gpu --format=csv"),
            ("output", "utilization.gpu: 19 %"),
            ("comment", "# batch the requests"),
            ("output", "batch_size: 1 -> 32"),
            ("prompt", "nvidia-smi --query-gpu=utilization.gpu --format=csv"),
            ("output", "utilization.gpu: 94 %"),
            ("output", "throughput: 12 req/s -> 91 req/s"),
         ])),

    dict(n=12, topic="GPU", style="terminal",
         post=(
"Half precision is one of the highest-leverage two-line changes in machine learning.\n\n"
"Mixed precision (FP16/BF16) lets the GPU do more math per second and hold bigger batches, often with no measurable drop in model quality.\n\n"
"What you actually get:\n"
"- Roughly 2x throughput on modern GPUs\n"
"- Larger batch sizes in the same memory\n"
"- Faster training and cheaper inference\n\n"
"The catch is small: watch for numerical stability, and let the framework's autocast handle the casting for you.\n\n"
"Free speed is rare. This is about as close as it gets.\n\n"
"#GPU #DeepLearning #MachineLearning #MixedPrecision #MLOps"),
         gif=dict(title="mixed-precision", lines=[
            ("comment", "# FP32 baseline"),
            ("prompt", "python train.py --precision fp32"),
            ("output", "throughput: 1,020 samples/s   mem: 22.1 GB"),
            ("comment", "# enable autocast (bf16)"),
            ("prompt", "python train.py --precision bf16"),
            ("output", "throughput: 1,980 samples/s   mem: 12.7 GB"),
            ("output", "speed: ~2x  | accuracy delta: negligible"),
         ])),

    dict(n=13, topic="AI Project Management", style="terminal",
         post=(
"The teams shipping reliable AI features have one habit the others skip: they wrote the evals before the feature.\n\n"
"Without evals, \"is the AI good now?\" becomes a vibe check in a meeting. With them, it's a number you can move.\n\n"
"Eval-driven development in practice:\n"
"- Define what 'correct' means as test cases, first\n"
"- Run every prompt and model change against them\n"
"- Track quality like you track latency: as a metric, over time\n"
"- Never ship on a hunch you can't reproduce\n\n"
"You can't manage what you can't measure. With LLMs, that's doubly true.\n\n"
"#AI #AIProjectManagement #LLM #Evals #MachineLearning"),
         gif=dict(title="eval-driven-dev", lines=[
            ("comment", "# 'is the AI good now?' -> make it a number"),
            ("prompt", "python run_evals.py --suite checkout_assistant"),
            ("output", "cases: 240   passed: 188   score: 0.78"),
            ("comment", "# new prompt -> measure, don't guess"),
            ("prompt", "python run_evals.py --suite checkout_assistant"),
            ("output", "cases: 240   passed: 223   score: 0.93"),
            ("output", "ship decision: backed by data, not vibes"),
         ])),

    dict(n=14, topic="AI", style="terminal",
         post=(
"A bigger context window is not a memory upgrade. It's a longer desk, not a better brain.\n\n"
"Just because you can paste 200 pages into the prompt doesn't mean the model uses all of it well. Important details in the middle quietly get less attention.\n\n"
"How to use long context wisely:\n"
"- Put the most important information at the start and end\n"
"- Retrieve and include only what's relevant, not everything\n"
"- Don't confuse 'fits in the window' with 'the model reasoned over it'\n\n"
"More context is a tool, not a strategy. Curation still beats volume.\n\n"
"#AI #LLM #ContextWindow #GenAI #MachineLearning"),
         gif=dict(title="context-window", lines=[
            ("comment", "# fact placed at different positions in 100k ctx"),
            ("prompt", "python needle_test.py --ctx 100000"),
            ("output", "position=start   recall: 0.99"),
            ("output", "position=middle  recall: 0.61   <- attention dip"),
            ("output", "position=end     recall: 0.97"),
            ("comment", "# fits != understood. curate what you send."),
            ("output", "lesson: place key facts at the edges"),
         ])),

    dict(n=15, topic="Python", style="terminal",
         post=(
"If you're building with LLMs and don't have an eval harness, you don't have engineering. You have guessing with extra steps.\n\n"
"The good news: a useful one is ~50 lines of Python.\n\n"
"What a minimal harness needs:\n"
"- A dataset of inputs with expected behavior\n"
"- A function that calls your model\n"
"- A scorer (exact match, regex, or an LLM judge)\n"
"- A number at the end you can compare against last time\n\n"
"Once that number exists, prompt tweaks stop being arguments and start being experiments.\n\n"
"Build the ruler before you start measuring.\n\n"
"#Python #AI #LLM #Evals #MachineLearning"),
         gif=dict(title="eval-harness.py", lines=[
            ("comment", "# a real eval harness in ~50 lines"),
            ("prompt", "python eval_harness.py --dataset golden.jsonl"),
            ("output", "for case in dataset:"),
            ("output", "    out = model(case.input)"),
            ("output", "    score += judge(out, case.expected)"),
            ("output", "----------------------------------------"),
            ("output", "n=120  score=0.88  vs last run 0.84  (+0.04)"),
         ])),

    # ====================== ENGINEERING MANAGER POV (16-60) ======================
    dict(n=16, topic="AI Project Management", style="em",
         post=(
"As an engineering manager, the hardest part of shipping AI isn't the model. It's resetting how the team defines \"done.\"\n\n"
"Traditional features are done when the tests pass. AI features are never quite done, they're tuned. That breaks a lot of planning instincts.\n\n"
"What I changed on my team:\n"
"- We estimate AI work in experiments, not story points\n"
"- \"Done\" means hitting an eval threshold, not closing a ticket\n"
"- We budget time for iteration after launch, not just before\n\n"
"Manage AI features like research with a deadline, not construction with a blueprint.\n\n"
"#EngineeringManagement #AIProjectManagement #AI #Leadership #TechLeadership"),
         gif=dict(title="standup -- defining 'done' for AI",
             lines=[
                ("head", "EM POV: what does 'done' mean for AI work?"),
                ("done", "Tests pass (necessary, not sufficient)"),
                ("done", "Eval score above the agreed threshold"),
                ("done", "Iteration budget reserved post-launch"),
                ("todo", "Stop estimating ML work in story points"),
                ("note", "Manage it like research with a deadline"),
             ])),

    dict(n=17, topic="AI", style="em",
         post=(
"My most useful skill as an engineering manager in the AI era isn't technical. It's protecting the team from hype-driven roadmaps.\n\n"
"Every week brings a new model, a new framework, a new 'this changes everything.' Half of it is real. Half is noise. Telling them apart is the job.\n\n"
"How I filter:\n"
"- Does this solve a problem we actually have?\n"
"- What does it cost in tokens, latency, and complexity?\n"
"- Can we measure if it's better, or are we just chasing shiny?\n\n"
"Adopting everything is the same as adopting nothing. Pick deliberately.\n\n"
"#EngineeringManagement #AI #Leadership #TechLeadership #DecisionMaking"),
         gif=dict(title="roadmap-review -- hype filter",
             lines=[
                ("head", "EM POV: should we adopt this new AI thing?"),
                ("todo", "Does it solve a problem we actually have?"),
                ("todo", "Cost in tokens / latency / complexity?"),
                ("todo", "Can we measure the improvement?"),
                ("note", "3 no's -> it's a demo, not a roadmap item"),
                ("done", "Adopt deliberately, not reflexively"),
             ])),

    dict(n=18, topic="Token Optimization", style="em",
         post=(
"A junior engineer cut our LLM costs more than any architecture decision I made that quarter. As their manager, here's what I learned from it.\n\n"
"They didn't optimize the model. They read the bill, line by line, and asked \"why are we sending this?\"\n\n"
"What it taught me about leading AI teams:\n"
"- Cost is a feature. Make it visible to everyone, not just finance.\n"
"- The person closest to the code often sees the waste first\n"
"- Reward the unglamorous wins, not just the launches\n\n"
"Give engineers visibility into the bill and they'll optimize what you'd never think to ask about.\n\n"
"#EngineeringManagement #TokenOptimization #AI #Leadership #CostOptimization"),
         gif=dict(title="retro -- who owns the LLM bill?",
             lines=[
                ("head", "EM POV: cost is a feature, not finance's job"),
                ("done", "Made token spend visible on the team dashboard"),
                ("done", "Junior eng found 60% waste in one prompt"),
                ("todo", "Add cost-per-request to PR review checklist"),
                ("note", "Reward unglamorous wins, not just launches"),
             ])),

    dict(n=19, topic="AI Project Management", style="em",
         post=(
"The fastest way to derail an AI project is to promise a demo date before you have an eval.\n\n"
"I've watched it happen. The demo looks magical. Then real users arrive, and the team has no way to tell if changes make things better or worse.\n\n"
"As a manager, I now insist on this order:\n"
"- Evals before demos\n"
"- A quality baseline before a launch date\n"
"- A way to measure regressions before we add features\n\n"
"A demo proves it can work once. An eval proves it works repeatedly. Stakeholders need the second one.\n\n"
"#EngineeringManagement #AIProjectManagement #AI #Leadership #Evals"),
         gif=dict(title="planning -- demo vs eval",
             lines=[
                ("head", "EM POV: don't promise a demo before an eval"),
                ("note", "Demo = it worked once"),
                ("note", "Eval = it works repeatedly"),
                ("todo", "Baseline quality before committing a date"),
                ("todo", "Regression suite before adding features"),
                ("done", "Stakeholders get the number, not the magic trick"),
             ])),

    dict(n=20, topic="GPU", style="em",
         post=(
"\"We need more GPUs\" is the most expensive sentence a team can say without checking utilization first.\n\n"
"As an engineering manager, my job when I hear it is to ask one question before signing the bill: how busy are the GPUs we already have?\n\n"
"More often than not:\n"
"- Utilization is sitting at 20-30%\n"
"- The bottleneck is batching or data loading, not compute\n"
"- A week of optimization beats a quarter of procurement\n\n"
"Throwing hardware at a software problem feels fast. It's usually just expensive.\n\n"
"#EngineeringManagement #GPU #MLOps #Leadership #CostOptimization"),
         gif=dict(title="budget-review -- 'we need more GPUs'",
             lines=[
                ("head", "EM POV: before approving more GPUs..."),
                ("todo", "What's current utilization?  (often ~25%)"),
                ("todo", "Is the bottleneck batching or data loading?"),
                ("todo", "Did we profile before we procured?"),
                ("note", "A week of tuning < a quarter of procurement"),
                ("done", "Approve hardware only after the easy wins"),
             ])),

    dict(n=21, topic="Java", style="em",
         post=(
"Leading a team on a 'legacy' Java codebase taught me that legacy is a story we tell, not a fact about the code.\n\n"
"The team had quietly decided the system was old and slow and that was that. Morale followed the story down.\n\n"
"What turned it around:\n"
"- We measured instead of assumed (the JVM was fine, the queries weren't)\n"
"- We upgraded the runtime and got modern language features for free\n"
"- We let people fix things they'd been told not to touch\n\n"
"\"Legacy\" usually means \"nobody's been allowed to care about it.\" Change that and the code changes too.\n\n"
"#EngineeringManagement #Java #Leadership #TechLeadership #TechDebt"),
         gif=dict(title="1:1 -- reframing 'legacy'",
             lines=[
                ("head", "EM POV: 'legacy' is a story, not a fact"),
                ("note", "Team believed the system was just slow"),
                ("done", "Measured: JVM fine, queries weren't"),
                ("done", "Upgraded runtime -> modern features free"),
                ("todo", "Let people fix what they were told to ignore"),
                ("note", "Morale follows ownership"),
             ])),

    dict(n=22, topic="Python", style="em",
         post=(
"I asked my team to add type hints to our Python services and got pushback. Six months later, no one wants to go back.\n\n"
"The objection was familiar: \"Python is dynamic, types are overhead, they slow us down.\"\n\n"
"What actually happened once we adopted them:\n"
"- Onboarding got faster, new folks could read intent from signatures\n"
"- Refactors stopped being terrifying\n"
"- Code review focused on logic, not 'what does this return?'\n\n"
"As a manager, I've learned the best standards feel like overhead for a week and relief forever after.\n\n"
"#EngineeringManagement #Python #Leadership #CleanCode #TechLeadership"),
         gif=dict(title="standards -- adopting type hints",
             lines=[
                ("head", "EM POV: rolling out Python type hints"),
                ("note", "Week 1: 'this is overhead' (it is)"),
                ("done", "Onboarding faster, intent readable"),
                ("done", "Refactors no longer terrifying"),
                ("done", "Reviews focus on logic, not return types"),
                ("note", "Good standards: overhead for a week, relief forever"),
             ])),

    dict(n=23, topic="AI", style="em",
         post=(
"The question I ask before every AI feature my team builds: what happens when it's wrong?\n\n"
"Not if. When. Every model is wrong sometimes. The teams that ship safely are the ones who designed for that day one.\n\n"
"What I push for as a manager:\n"
"- A graceful fallback when confidence is low\n"
"- A human in the loop where the cost of error is high\n"
"- Clear UX that sets expectations instead of overpromising\n\n"
"Great AI products aren't the ones that are never wrong. They're the ones that fail gracefully when they are.\n\n"
"#EngineeringManagement #AI #Leadership #ProductEngineering #TechLeadership"),
         gif=dict(title="design-review -- 'what if it's wrong?'",
             lines=[
                ("head", "EM POV: design for when the model is wrong"),
                ("note", "Not if. When."),
                ("todo", "Graceful fallback on low confidence"),
                ("todo", "Human in the loop for high-cost errors"),
                ("todo", "UX that sets expectations, not hype"),
                ("done", "Ship features that fail gracefully"),
             ])),

    dict(n=24, topic="AI Project Management", style="em",
         post=(
"My team's AI velocity doubled when we stopped treating prompts like config and started treating them like code.\n\n"
"Prompts were living in random strings, edited in production, with no history of what changed or why. Sound familiar?\n\n"
"What we put in place:\n"
"- Prompts in version control, reviewed like any other change\n"
"- Every prompt change runs through evals in CI\n"
"- A changelog so we know which version is live and why\n\n"
"If a prompt can change your product's behavior, it deserves the same rigor as the code around it.\n\n"
"#EngineeringManagement #AIProjectManagement #AI #LLM #TechLeadership"),
         gif=dict(title="process -- prompts as code",
             lines=[
                ("head", "EM POV: treat prompts like code"),
                ("note", "Before: strings edited live, no history"),
                ("done", "Prompts in version control + reviewed"),
                ("done", "Eval gate in CI on every prompt change"),
                ("done", "Changelog: what's live and why"),
                ("note", "It changes behavior -> it deserves rigor"),
             ])),

    dict(n=25, topic="AI", style="em",
         post=(
"The most valuable engineer on an AI team is often the one who's skeptical of AI.\n\n"
"As a manager, I used to worry the skeptics would slow us down. Now I seek them out.\n\n"
"They're the ones who:\n"
"- Ask whether we even need a model for this (sometimes a rule works)\n"
"- Catch the demo that won't survive real users\n"
"- Insist on measuring before we believe\n\n"
"Enthusiasm ships the prototype. Skepticism ships the product. A healthy team needs both, in tension.\n\n"
"#EngineeringManagement #AI #Leadership #TeamBuilding #TechLeadership"),
         gif=dict(title="team -- value of the skeptic",
             lines=[
                ("head", "EM POV: hire the AI skeptic on purpose"),
                ("done", "Asks: do we even need a model here?"),
                ("done", "Catches demos that won't survive users"),
                ("done", "Insists on measuring before believing"),
                ("note", "Enthusiasm ships prototypes"),
                ("note", "Skepticism ships products"),
             ])),

    dict(n=26, topic="Token Optimization", style="em",
         post=(
"I set one rule for my team this year: every LLM feature ships with a cost-per-request number. It changed how we build.\n\n"
"When cost is invisible, engineers optimize for what they can see, latency and accuracy. The bill becomes someone else's surprise.\n\n"
"Making cost a first-class metric did three things:\n"
"- Engineers started trimming prompts without being asked\n"
"- We caught a runaway feature before it hit the invoice\n"
"- 'Is it worth the tokens?' became a normal design question\n\n"
"You get the behavior you measure. Measure cost, and frugality follows.\n\n"
"#EngineeringManagement #TokenOptimization #AI #Leadership #CostOptimization"),
         gif=dict(title="dashboard -- cost per request",
             lines=[
                ("head", "EM POV: make cost-per-request a shipped metric"),
                ("done", "Every LLM feature reports its token cost"),
                ("done", "Engineers trim prompts unprompted"),
                ("done", "Caught a runaway feature pre-invoice"),
                ("note", "'Is it worth the tokens?' = normal question"),
                ("note", "You get the behavior you measure"),
             ])),

    dict(n=27, topic="AI Project Management", style="em",
         post=(
"The hardest estimate I give as an engineering manager: how long will the AI feature take?\n\n"
"With normal features, I can decompose and estimate. With AI, the honest answer is often \"we'll know after the first eval.\"\n\n"
"How I handle it without losing trust:\n"
"- I commit to a spike, not a ship date, up front\n"
"- I give stakeholders ranges with confidence levels, not false precision\n"
"- I update the estimate publicly as we learn\n\n"
"Pretending AI work is predictable is how you burn credibility. Naming the uncertainty is how you keep it.\n\n"
"#EngineeringManagement #AIProjectManagement #AI #Leadership #Estimation"),
         gif=dict(title="planning -- estimating AI work",
             lines=[
                ("head", "EM POV: 'how long will the AI feature take?'"),
                ("note", "Honest answer: known after the first eval"),
                ("done", "Commit to a spike, not a ship date"),
                ("done", "Give ranges + confidence, not false precision"),
                ("done", "Update the estimate publicly as we learn"),
                ("note", "Naming uncertainty protects credibility"),
             ])),

    dict(n=28, topic="GPU", style="em",
         post=(
"I learned to read an nvidia-smi output not because I write the kernels, but because as a manager I sign the cloud bill.\n\n"
"You don't need to be an expert to ask the right questions. You need to know what 'healthy' looks like.\n\n"
"What I keep an eye on:\n"
"- Are the GPUs actually busy, or expensively idle?\n"
"- Is memory the limit, or is the pipeline starving them?\n"
"- Are we paying for top-tier cards to do work a cheaper tier could?\n\n"
"Managers don't need to write the optimization. We need to create the space and incentive for someone to.\n\n"
"#EngineeringManagement #GPU #MLOps #Leadership #CostOptimization"),
         gif=dict(title="cost-review -- reading the GPU bill",
             lines=[
                ("head", "EM POV: you sign the bill, learn to read it"),
                ("todo", "Busy GPUs or expensively idle?"),
                ("todo", "Memory-bound or pipeline-starved?"),
                ("todo", "Right card tier for the actual work?"),
                ("note", "Don't write the fix -> make space for it"),
             ])),

    dict(n=29, topic="AI", style="em",
         post=(
"A demo that wows leadership and a feature that survives production are two completely different artifacts. Confusing them is a management failure, not an engineering one.\n\n"
"The demo runs on three hand-picked inputs. Production runs on the inputs you never imagined.\n\n"
"How I keep the gap honest:\n"
"- I never let a happy-path demo set the launch timeline\n"
"- I ask to see the failure cases, not just the highlight reel\n"
"- I budget the unglamorous 80%: edge cases, guardrails, monitoring\n\n"
"Anyone can demo AI. Shipping it is the job. Protect the time the second one needs.\n\n"
"#EngineeringManagement #AI #Leadership #ProductEngineering #TechLeadership"),
         gif=dict(title="review -- demo vs production",
             lines=[
                ("head", "EM POV: the demo is not the feature"),
                ("note", "Demo: 3 hand-picked inputs"),
                ("note", "Prod: inputs you never imagined"),
                ("todo", "Don't let happy-path set the timeline"),
                ("todo", "Ask to see the failure cases"),
                ("done", "Budget the unglamorous 80%"),
             ])),

    dict(n=30, topic="AI Project Management", style="em",
         post=(
"Halfway through 60 days of posting about engineering leadership, here's the throughline I keep coming back to: AI changes the tools, not the fundamentals.\n\n"
"The teams winning with AI aren't the ones with the fanciest models. They're the ones who kept doing the boring things well:\n"
"- Measuring before believing\n"
"- Making cost and quality visible\n"
"- Designing for failure, not just the happy path\n"
"- Protecting focus from the hype cycle\n\n"
"New technology, same disciplines. The managers who internalize that will outlast every model release.\n\n"
"#EngineeringManagement #AIProjectManagement #AI #Leadership #TechLeadership"),
         gif=dict(title="checkpoint -- day 30 of 60",
             lines=[
                ("head", "EM POV: AI changes tools, not fundamentals"),
                ("done", "Measure before believing"),
                ("done", "Make cost + quality visible"),
                ("done", "Design for failure, not happy path"),
                ("done", "Protect focus from the hype cycle"),
                ("note", "New tech, same disciplines"),
             ])),

    dict(n=31, topic="AI", style="em",
         post=(
"One underrated engineering manager skill in the AI era: knowing when NOT to use AI.\n\n"
"There's enormous pressure to put a model in everything. But a regex, a lookup table, or a simple rule is often faster, cheaper, and more reliable.\n\n"
"My team's checklist before reaching for an LLM:\n"
"- Is the problem actually fuzzy, or just unspecified?\n"
"- Would deterministic logic be more testable here?\n"
"- Are we adding a model to look modern, or to solve something?\n\n"
"The goal was never to use AI. It was to solve the problem. Sometimes those are the same. Often they aren't.\n\n"
"#EngineeringManagement #AI #Leadership #TechLeadership #Pragmatism"),
         gif=dict(title="design -- do we even need AI?",
             lines=[
                ("head", "EM POV: when NOT to use AI"),
                ("todo", "Is it fuzzy, or just unspecified?"),
                ("todo", "Would deterministic logic be more testable?"),
                ("todo", "Modern-looking or problem-solving?"),
                ("note", "Sometimes a regex wins"),
                ("done", "Solve the problem, not the trend"),
             ])),

    dict(n=32, topic="Python", style="em",
         post=(
"The Python code review comment I write most as a manager isn't about bugs. It's \"would the on-call engineer understand this at 3am?\"\n\n"
"Clever code is a tax your team pays later, usually during an incident, usually at the worst time.\n\n"
"What I coach for:\n"
"- Boring, obvious code over impressive one-liners\n"
"- Names that explain intent, not just type\n"
"- Comments for the 'why', when the 'what' isn't enough\n\n"
"I'd rather maintain readable code that's slightly slower than brilliant code no one can touch. The team's velocity lives in readability.\n\n"
"#EngineeringManagement #Python #CleanCode #Leadership #TechLeadership"),
         gif=dict(title="code-review -- the 3am test",
             lines=[
                ("head", "EM POV: would on-call get this at 3am?"),
                ("done", "Boring + obvious > clever one-liner"),
                ("done", "Names explain intent"),
                ("done", "Comment the 'why'"),
                ("note", "Clever code is a tax paid during incidents"),
             ])),

    dict(n=33, topic="Token Optimization", style="em",
         post=(
"A 30% reduction in tokens isn't a cost story to my finance team. It's a latency story to my users. As a manager, I sell it as both.\n\n"
"Fewer tokens in and out usually means a faster response. So token optimization quietly improves the thing users actually feel.\n\n"
"How I frame the work to get it prioritized:\n"
"- To finance: this lowers our cost per user\n"
"- To product: this makes the feature feel faster\n"
"- To engineers: this is a craft problem worth solving\n\n"
"The same work, told three ways, gets buy-in from three audiences. That translation is the manager's job.\n\n"
"#EngineeringManagement #TokenOptimization #AI #Leadership #Communication"),
         gif=dict(title="alignment -- selling token work",
             lines=[
                ("head", "EM POV: one optimization, three pitches"),
                ("done", "Finance: lower cost per user"),
                ("done", "Product: the feature feels faster"),
                ("done", "Engineers: a real craft problem"),
                ("note", "Translation is the manager's job"),
             ])),

    dict(n=34, topic="AI Project Management", style="em",
         post=(
"The riskiest moment in an AI project isn't the launch. It's the silence after, when everyone assumes it's still working.\n\n"
"Models drift. Inputs change. The thing that scored 0.93 at launch can quietly slide without a single code change.\n\n"
"What I require before we call an AI feature 'done':\n"
"- Production monitoring on quality, not just uptime\n"
"- Alerts when key metrics drift past a threshold\n"
"- A scheduled re-eval, not a one-time check\n\n"
"Shipping an AI feature isn't crossing a finish line. It's adopting something that needs ongoing care.\n\n"
"#EngineeringManagement #AIProjectManagement #AI #MLOps #Leadership"),
         gif=dict(title="post-launch -- the silent drift",
             lines=[
                ("head", "EM POV: the risk is the silence after launch"),
                ("note", "0.93 at launch can quietly slide"),
                ("todo", "Monitor quality, not just uptime"),
                ("todo", "Alert on metric drift"),
                ("todo", "Schedule re-evals"),
                ("done", "Shipping = adopting, not finishing"),
             ])),

    dict(n=35, topic="AI", style="em",
         post=(
"Every engineer on my team now uses AI to code. My job shifted from reviewing code to reviewing judgment.\n\n"
"When a model can generate a plausible solution in seconds, the scarce skill is no longer typing. It's knowing whether the solution is right, safe, and worth keeping.\n\n"
"What I coach now:\n"
"- Read AI-generated code as critically as a stranger's PR\n"
"- Understand it before you ship it, you own it either way\n"
"- Use AI to go faster, not to skip thinking\n\n"
"The tool got powerful. That makes human judgment more valuable, not less.\n\n"
"#EngineeringManagement #AI #Leadership #TechLeadership #FutureOfWork"),
         gif=dict(title="coaching -- reviewing judgment",
             lines=[
                ("head", "EM POV: the scarce skill is judgment now"),
                ("done", "Read AI code as critically as a stranger's PR"),
                ("done", "Understand before you ship -> you own it"),
                ("done", "Use AI to go faster, not skip thinking"),
                ("note", "Powerful tools raise the value of judgment"),
             ])),

    dict(n=36, topic="GPU", style="em",
         post=(
"As an engineering manager, I don't optimize GPU kernels. But I do decide whether the team has time to.\n\n"
"Infrastructure efficiency is almost always a prioritization problem disguised as a technical one. The know-how exists. The calendar space doesn't.\n\n"
"What I've learned to do:\n"
"- Treat a week of GPU optimization as an investment with a clear ROI\n"
"- Show the team the cost curve so the 'why' is obvious\n"
"- Defend that week from getting eaten by feature pressure\n\n"
"The deepest technical wins often need a manager to simply make room for them.\n\n"
"#EngineeringManagement #GPU #MLOps #Leadership #CostOptimization"),
         gif=dict(title="prioritization -- making room for tuning",
             lines=[
                ("head", "EM POV: efficiency is a calendar problem"),
                ("note", "The know-how exists; the time doesn't"),
                ("done", "Framed tuning as ROI, not chore"),
                ("done", "Showed the team the cost curve"),
                ("todo", "Defend the week from feature pressure"),
             ])),

    dict(n=37, topic="Java", style="em",
         post=(
"A Java service my team owned hadn't been touched in two years because everyone was afraid of it. Fixing the fear was a leadership task, not a coding one.\n\n"
"The code wasn't the problem. The absence of tests, docs, and anyone who felt safe changing it was.\n\n"
"What we did, in order:\n"
"- Added characterization tests to capture current behavior\n"
"- Paired people on it so knowledge spread\n"
"- Made small, safe changes to rebuild confidence\n\n"
"Fear compounds in codebases just like it does in teams. The fix is the same: make it safe to act.\n\n"
"#EngineeringManagement #Java #Leadership #TechLeadership #TechDebt"),
         gif=dict(title="1:1 -- the service nobody touches",
             lines=[
                ("head", "EM POV: fixing the fear, not just the code"),
                ("note", "Untouched 2 years = a confidence problem"),
                ("done", "Characterization tests pin behavior"),
                ("done", "Paired to spread the knowledge"),
                ("done", "Small safe changes rebuilt confidence"),
                ("note", "Make it safe to act"),
             ])),

    dict(n=38, topic="AI Project Management", style="em",
         post=(
"The best AI roadmap I've run had fewer features on it than the one before. That was the point.\n\n"
"AI work has a long tail: the feature is 'working' at 70%, and the last 30% (edge cases, safety, reliability) takes as long as the first 70.\n\n"
"So I plan differently now:\n"
"- Fewer AI bets, each fully finished\n"
"- Explicit time for the unglamorous last mile\n"
"- The courage to say no to the demo that isn't production-ready\n\n"
"Three shipped, trustworthy AI features beat ten impressive prototypes that erode user trust. Depth over breadth.\n\n"
"#EngineeringManagement #AIProjectManagement #AI #Leadership #Roadmap"),
         gif=dict(title="roadmap -- fewer, finished",
             lines=[
                ("head", "EM POV: fewer AI bets, fully finished"),
                ("note", "70% 'works'; the last 30% is the work"),
                ("done", "Reserve time for the last mile"),
                ("done", "Say no to demos that aren't prod-ready"),
                ("note", "3 trustworthy > 10 prototypes"),
             ])),

    dict(n=39, topic="AI", style="em",
         post=(
"When a model in production makes a bad call, my first question to the team is never 'who prompted it wrong?' It's 'why could it fail silently?'\n\n"
"Blameless is easy to say and hard to do, especially with AI, where it's tempting to blame the model or the person who configured it.\n\n"
"What I steer toward instead:\n"
"- What guardrail was missing that let this reach a user?\n"
"- What signal would have caught it sooner?\n"
"- What do we change in the system, not the person?\n\n"
"AI failures are systems problems. Treating them as individual mistakes just teaches people to hide them.\n\n"
"#EngineeringManagement #AI #Leadership #BlamelessCulture #TechLeadership"),
         gif=dict(title="incident -- blameless with AI",
             lines=[
                ("head", "EM POV: not 'who', but 'why silently?'"),
                ("todo", "What guardrail was missing?"),
                ("todo", "What signal would've caught it sooner?"),
                ("todo", "What changes in the system, not the person?"),
                ("note", "Blame teaches people to hide failures"),
             ])),

    dict(n=40, topic="Token Optimization", style="em",
         post=(
"The cheapest token is the one you never send. I repeat this to my team until it's a reflex.\n\n"
"Before we optimize models, quantize, or chase a cheaper provider, we ask the boring question: do we need this call at all?\n\n"
"Where we find free wins:\n"
"- Cache responses for repeated identical requests\n"
"- Short-circuit with a rule before invoking the model\n"
"- Batch and dedupe instead of one call per item\n\n"
"The most elegant optimization isn't a faster call. It's no call. As a manager, I reward the engineer who deletes the request entirely.\n\n"
"#EngineeringManagement #TokenOptimization #AI #Leadership #CostOptimization"),
         gif=dict(title="design -- the call you don't make",
             lines=[
                ("head", "EM POV: cheapest token = never sent"),
                ("done", "Cache identical requests"),
                ("done", "Rule-based short-circuit before the model"),
                ("done", "Batch + dedupe vs one call per item"),
                ("note", "Reward the engineer who deletes the call"),
             ])),

    dict(n=41, topic="AI Project Management", style="em",
         post=(
"The stakeholder question that used to scare me: \"Can you just make the AI a bit more accurate?\"\n\n"
"It sounds reasonable. It hides a world of tradeoffs. As a manager, my job is to make those tradeoffs visible instead of nodding along.\n\n"
"How I respond now:\n"
"- \"More accurate on which cases? Improving one often costs another.\"\n"
"- \"Here's the cost and latency that accuracy buys.\"\n"
"- \"Here's the eval that tells us if we actually got there.\"\n\n"
"Turning a vague ask into a measurable tradeoff is how AI projects stay sane. Vague goals produce endless work.\n\n"
"#EngineeringManagement #AIProjectManagement #AI #Leadership #Stakeholders"),
         gif=dict(title="stakeholder -- 'just make it more accurate'",
             lines=[
                ("head", "EM POV: turn vague asks into tradeoffs"),
                ("todo", "More accurate on WHICH cases?"),
                ("todo", "What cost + latency does it buy?"),
                ("todo", "Which eval confirms we got there?"),
                ("note", "Vague goals = endless work"),
             ])),

    dict(n=42, topic="AI", style="em",
         post=(
"I stopped asking my team \"is the AI working?\" and started asking \"how would we know if it stopped?\"\n\n"
"The first question gets you a confident yes. The second gets you a real engineering conversation.\n\n"
"It surfaces the things that matter:\n"
"- What's our quality metric, and who watches it?\n"
"- What's the alert when it degrades?\n"
"- How fast could we even notice a regression?\n\n"
"The quality of a team's answers is capped by the quality of the manager's questions. With AI, ask about failure, not success.\n\n"
"#EngineeringManagement #AI #Leadership #MLOps #TechLeadership"),
         gif=dict(title="standup -- a better question",
             lines=[
                ("head", "EM POV: 'how would we know if it stopped?'"),
                ("note", "'Is it working?' -> a confident yes"),
                ("todo", "What's the metric, and who watches it?"),
                ("todo", "What's the degradation alert?"),
                ("todo", "How fast would we notice?"),
                ("note", "Better questions, better answers"),
             ])),

    dict(n=43, topic="Python", style="em",
         post=(
"My team standardized on one Python toolchain and got back a day a week. The tools mattered less than the decision to stop arguing about them.\n\n"
"Formatter, linter, type checker, test runner, every project the same. Boring on purpose.\n\n"
"What standardizing bought us:\n"
"- No more 'works on my machine' style debates\n"
"- New repos start productive on day one\n"
"- Code review is about logic, not whitespace\n\n"
"As a manager, removing a hundred tiny decisions frees the team for the few that actually matter. Consistency is a feature.\n\n"
"#EngineeringManagement #Python #Leadership #DeveloperExperience #TechLeadership"),
         gif=dict(title="tooling -- one toolchain",
             lines=[
                ("head", "EM POV: standardize, stop arguing"),
                ("done", "Same formatter / linter / types everywhere"),
                ("done", "New repos productive on day one"),
                ("done", "Reviews about logic, not whitespace"),
                ("note", "Remove 100 tiny decisions"),
             ])),

    dict(n=44, topic="GPU", style="em",
         post=(
"The most expensive line item my team manages is GPU time, and the biggest savings came from a culture change, not a code change.\n\n"
"We made efficiency visible and celebrated. Suddenly people cared about utilization the way they care about test coverage.\n\n"
"What shifted the culture:\n"
"- A shared dashboard everyone could see\n"
"- Shouting out the person who improved utilization, publicly\n"
"- Treating waste as a bug, not a fact of life\n\n"
"You can mandate a metric, but you can't mandate that people care. As a manager, making them care is the actual work.\n\n"
"#EngineeringManagement #GPU #MLOps #Leadership #EngineeringCulture"),
         gif=dict(title="culture -- making efficiency matter",
             lines=[
                ("head", "EM POV: savings came from culture, not code"),
                ("done", "Shared utilization dashboard"),
                ("done", "Public shout-outs for efficiency wins"),
                ("done", "Waste treated as a bug"),
                ("note", "You can't mandate that people care"),
             ])),

    dict(n=45, topic="AI Project Management", style="em",
         post=(
"I've started running 'pre-mortems' before every major AI feature. We imagine it failed badly, then work backwards. It's the highest-ROI hour we spend.\n\n"
"Instead of asking 'how will this succeed?', we ask 'it's six months later and this blew up, what happened?'\n\n"
"What it surfaces that normal planning misses:\n"
"- The edge case everyone assumed someone else owned\n"
"- The silent failure mode with no alerting\n"
"- The trust we'd lose if the model embarrassed a user\n\n"
"Optimism plans the launch. Pessimism, scheduled deliberately, prevents the disaster. AI needs both.\n\n"
"#EngineeringManagement #AIProjectManagement #AI #Leadership #RiskManagement"),
         gif=dict(title="pre-mortem -- imagine it failed",
             lines=[
                ("head", "EM POV: pre-mortem before AI launches"),
                ("note", "'It's 6 months later and it blew up. Why?'"),
                ("todo", "The edge case nobody owned"),
                ("todo", "The silent failure with no alert"),
                ("todo", "The user trust we'd lose"),
                ("done", "Scheduled pessimism prevents disasters"),
             ])),

    dict(n=46, topic="AI", style="em",
         post=(
"AI didn't make my engineers obsolete. It moved the bottleneck from writing code to deciding what's worth building.\n\n"
"When generating a solution is cheap, the expensive part becomes taste: choosing the right problem, the right scope, the right tradeoffs.\n\n"
"How I'm shifting the team's focus:\n"
"- Less time on implementation, more on problem definition\n"
"- More design review, because mistakes scale faster now\n"
"- Rewarding 'we decided not to build this' as a real outcome\n\n"
"The team that wins isn't the one that codes fastest. It's the one that aims best. Direction beats speed.\n\n"
"#EngineeringManagement #AI #Leadership #TechLeadership #FutureOfWork"),
         gif=dict(title="strategy -- the bottleneck moved",
             lines=[
                ("head", "EM POV: aiming now beats coding fast"),
                ("note", "Generating code is cheap; taste is not"),
                ("done", "More time on problem definition"),
                ("done", "More design review (mistakes scale)"),
                ("done", "'We chose not to build it' = a win"),
             ])),

    dict(n=47, topic="Token Optimization", style="em",
         post=(
"I treat our LLM cost dashboard the same way I treat our error rate: a number that should trend down and never surprise me.\n\n"
"When cost spikes are invisible until the invoice, you're managing blind. We wired token spend into the same observability everything else lives in.\n\n"
"What that gives my team:\n"
"- Cost anomalies caught in hours, not at month-end\n"
"- A clear before/after for every optimization\n"
"- Engineers who can see the impact of their own changes\n\n"
"You can't manage a number you only see once a month. Bring cost into the daily loop and it stops being scary.\n\n"
"#EngineeringManagement #TokenOptimization #AI #MLOps #CostOptimization"),
         gif=dict(title="observability -- cost as a metric",
             lines=[
                ("head", "EM POV: treat cost like error rate"),
                ("done", "Token spend wired into observability"),
                ("done", "Anomalies caught in hours, not month-end"),
                ("done", "Before/after visible per change"),
                ("note", "A monthly number can't be managed"),
             ])),

    dict(n=48, topic="AI Project Management", style="em",
         post=(
"The phrase that quietly kills AI projects: \"we'll figure out evaluation later.\"\n\n"
"Later never comes. The team ships, moves on, and the feature becomes unmaintainable because no one can safely change it.\n\n"
"So I make evaluation a starting condition, not a finishing one:\n"
"- The eval set is part of the design doc, not an afterthought\n"
"- 'How will we measure this?' is a question in kickoff\n"
"- No eval, no go, the same way we treat no tests\n\n"
"Evaluation isn't the boring part you do at the end. It's the foundation that makes everything else iterable.\n\n"
"#EngineeringManagement #AIProjectManagement #AI #Evals #Leadership"),
         gif=dict(title="kickoff -- evals are a precondition",
             lines=[
                ("head", "EM POV: 'evaluate later' = never"),
                ("done", "Eval set lives in the design doc"),
                ("done", "'How do we measure this?' at kickoff"),
                ("todo", "No eval, no go (like no tests)"),
                ("note", "Evals are the foundation, not the finish"),
             ])),

    dict(n=49, topic="Java", style="em",
         post=(
"Half my team writes Java, half writes Python, and the AI services sit in between. Bridging that divide is one of my quieter responsibilities.\n\n"
"The temptation is to let each camp optimize locally and lob artifacts over the wall. That's how integration bugs are born.\n\n"
"What keeps it healthy:\n"
"- Shared contracts (clear API schemas) so neither side guesses\n"
"- Cross-pollination: Java folks review Python PRs and vice versa\n"
"- One definition of 'done' across the whole pipeline\n\n"
"Polyglot teams don't fail on syntax. They fail on the seams between languages. Manage the seams.\n\n"
"#EngineeringManagement #Java #Python #Leadership #TechLeadership"),
         gif=dict(title="integration -- managing the seams",
             lines=[
                ("head", "EM POV: polyglot teams fail at the seams"),
                ("done", "Shared API contracts, no guessing"),
                ("done", "Cross-language PR reviews"),
                ("done", "One 'done' across the pipeline"),
                ("note", "Manage the seams, not the syntax"),
             ])),

    dict(n=50, topic="AI", style="em",
         post=(
"Ten posts from the finish line, the leadership lesson AI has hammered home hardest: speed without direction is just expensive motion.\n\n"
"AI lets teams move faster than ever. That's exactly why direction matters more than ever, fast in the wrong direction is just faster waste.\n\n"
"Where I spend my energy as a manager now:\n"
"- Making sure we're solving a real problem before we accelerate\n"
"- Keeping quality and cost visible so speed doesn't hide rot\n"
"- Protecting the team's focus from every shiny new release\n\n"
"The tools will keep getting faster. Judgment, taste, and direction are the moat. Invest there.\n\n"
"#EngineeringManagement #AI #Leadership #TechLeadership #Strategy"),
         gif=dict(title="checkpoint -- day 50 of 60",
             lines=[
                ("head", "EM POV: speed without direction = waste"),
                ("done", "Solve a real problem before accelerating"),
                ("done", "Keep quality + cost visible"),
                ("done", "Protect focus from the shiny"),
                ("note", "Judgment is the moat"),
             ])),

    dict(n=51, topic="AI Project Management", style="em",
         post=(
"The most valuable artifact my AI team produces isn't the model. It's the eval set. And I manage it like the asset it is.\n\n"
"Models come and go. Providers change. But a well-curated set of test cases that captures what 'good' means? That compounds in value every quarter.\n\n"
"How we treat it as a first-class asset:\n"
"- It's versioned, reviewed, and owned, like production code\n"
"- We add the hard cases we find in production back into it\n"
"- It's the first thing we run when any dependency changes\n\n"
"Your evals outlive your models. Invest in them accordingly. That's where institutional knowledge actually lives.\n\n"
"#EngineeringManagement #AIProjectManagement #AI #Evals #Leadership"),
         gif=dict(title="asset -- the eval set",
             lines=[
                ("head", "EM POV: evals are the asset, not the model"),
                ("done", "Versioned, reviewed, owned"),
                ("done", "Prod failures fed back in"),
                ("done", "First thing run on any change"),
                ("note", "Evals outlive models"),
             ])),

    dict(n=52, topic="GPU", style="em",
         post=(
"\"It's slow, let's scale up\" is a reflex. \"It's slow, let's profile\" is a discipline. As a manager, I'm paid to install the discipline.\n\n"
"Scaling hardware to fix a software bottleneck is the most seductive mistake in ML infrastructure. It works just well enough to hide the real problem.\n\n"
"What I ask before we add capacity:\n"
"- Where is the time actually going? (show me the profile)\n"
"- Is the GPU the bottleneck, or the thing feeding it?\n"
"- What's the cheapest experiment that could disprove our theory?\n\n"
"Capacity buys time. Profiling buys understanding. Only one of them compounds.\n\n"
"#EngineeringManagement #GPU #MLOps #Leadership #Performance"),
         gif=dict(title="decision -- scale vs profile",
             lines=[
                ("head", "EM POV: profile is a discipline, scale is a reflex"),
                ("todo", "Where is the time actually going?"),
                ("todo", "GPU-bound or feeding-bound?"),
                ("todo", "Cheapest experiment to disprove us?"),
                ("note", "Capacity buys time; profiling compounds"),
             ])),

    dict(n=53, topic="Python", style="em",
         post=(
"A senior engineer told me our Python tests were 'slowing the team down.' They were right, and the fix wasn't fewer tests.\n\n"
"A 20-minute test suite that everyone skips locally is worse than no suite, because it gives false confidence and gets ignored.\n\n"
"What we did as a team:\n"
"- Split fast unit tests from slow integration tests\n"
"- Made the fast suite run in under a minute, every commit\n"
"- Pushed the slow stuff to CI where it doesn't block flow\n\n"
"As a manager, when a good practice starts hurting, the answer is usually to fix the practice, not abandon it. Diagnose before you cut.\n\n"
"#EngineeringManagement #Python #Testing #Leadership #DeveloperExperience"),
         gif=dict(title="retro -- tests slowing us down",
             lines=[
                ("head", "EM POV: slow tests get skipped = false confidence"),
                ("done", "Split fast unit vs slow integration"),
                ("done", "Fast suite < 1 min, every commit"),
                ("done", "Slow suite to CI, off the hot path"),
                ("note", "Fix the practice, don't abandon it"),
             ])),

    dict(n=54, topic="AI", style="em",
         post=(
"The hardest conversation I have as an AI team's manager: telling leadership the impressive demo isn't ready to ship.\n\n"
"The pressure is enormous. The demo wowed everyone. Saying 'not yet' feels like sandbagging. But shipping a fragile AI feature erodes trust faster than a delay ever could.\n\n"
"How I hold the line without being the blocker:\n"
"- I show the failure cases, not just my opinion\n"
"- I name exactly what 'ready' requires and how long\n"
"- I offer a smaller, real thing we can ship now\n\n"
"Protecting the user from a half-baked AI feature is protecting the product. That's the job, even when it's unpopular.\n\n"
"#EngineeringManagement #AI #Leadership #TechLeadership #ProductEngineering"),
         gif=dict(title="leadership -- 'the demo isn't ready'",
             lines=[
                ("head", "EM POV: saying 'not yet' to a great demo"),
                ("done", "Show failure cases, not opinions"),
                ("done", "Define what 'ready' needs + timeline"),
                ("done", "Offer a smaller real thing now"),
                ("note", "A fragile launch erodes trust faster than delay"),
             ])),

    dict(n=55, topic="Token Optimization", style="em",
         post=(
"Token optimization taught my team a lesson that goes way beyond AI: constraints make better engineers.\n\n"
"When we set a token budget per feature, the work got more creative, not less. People found smarter prompts, better caching, leaner context, because they had to.\n\n"
"What the constraint produced:\n"
"- Sharper thinking about what information actually matters\n"
"- Reuse and caching that helped latency too\n"
"- Pride in elegant solutions, not just working ones\n\n"
"As a manager, I've stopped seeing budgets as limits on the team. A well-set constraint is a creativity engine.\n\n"
"#EngineeringManagement #TokenOptimization #AI #Leadership #EngineeringCulture"),
         gif=dict(title="budget -- constraints as fuel",
             lines=[
                ("head", "EM POV: constraints make better engineers"),
                ("done", "Token budget per feature"),
                ("done", "Sharper thinking on what matters"),
                ("done", "Caching that helped latency too"),
                ("note", "A good constraint is a creativity engine"),
             ])),

    dict(n=56, topic="AI Project Management", style="em",
         post=(
"I rate AI project health on one signal above all others: how quickly the team can answer 'did that change make it better or worse?'\n\n"
"If the answer takes a week of manual checking, the project is sick, no matter how good the demo looks. If it takes minutes, the project is healthy.\n\n"
"What a fast feedback loop requires:\n"
"- Automated evals anyone can run on demand\n"
"- A baseline that's trusted and up to date\n"
"- A culture where 'show me the numbers' is normal, not confrontational\n\n"
"Iteration speed is the heartbeat of an AI team. Protect it, and almost everything else follows.\n\n"
"#EngineeringManagement #AIProjectManagement #AI #Evals #Leadership"),
         gif=dict(title="health-check -- the feedback loop",
             lines=[
                ("head", "EM POV: how fast can you answer 'better or worse?'"),
                ("note", "A week of manual checking = sick"),
                ("done", "On-demand automated evals"),
                ("done", "A trusted, current baseline"),
                ("done", "'Show me the numbers' is normal"),
             ])),

    dict(n=57, topic="AI", style="em",
         post=(
"The engineers thriving most in the AI era on my team share one trait, and it isn't raw coding speed. It's curiosity about how the tools actually work.\n\n"
"Anyone can prompt a model. The people who pull ahead understand why it behaves the way it does, so they can debug it when it surprises them.\n\n"
"What I try to cultivate:\n"
"- Time to read the docs and papers, not just the API\n"
"- Permission to experiment without a ticket attached\n"
"- A team norm of sharing what we learn, including the failures\n\n"
"In a field this new, the willingness to keep learning beats any current skill. Hire and grow for curiosity.\n\n"
"#EngineeringManagement #AI #Leadership #TeamBuilding #LearningCulture"),
         gif=dict(title="growth -- hire for curiosity",
             lines=[
                ("head", "EM POV: curiosity beats coding speed"),
                ("done", "Time to read docs + papers"),
                ("done", "Permission to experiment, no ticket"),
                ("done", "Share learnings, including failures"),
                ("note", "Willingness to learn > current skill"),
             ])),

    dict(n=58, topic="AI Project Management", style="em",
         post=(
"After managing AI projects for a while, my one-line definition of success has changed. It's not 'the model is accurate.' It's 'the team can improve it safely, forever.'\n\n"
"Accuracy is a snapshot. Maintainability is the movie. The features that last are the ones a new engineer can change next year without fear.\n\n"
"What I optimize the system for:\n"
"- Evals that catch regressions before users do\n"
"- Prompts and configs that live in version control\n"
"- Documentation of why, not just what\n\n"
"Build AI features that your future team can confidently change. That's the difference between an asset and a liability.\n\n"
"#EngineeringManagement #AIProjectManagement #AI #Leadership #TechLeadership"),
         gif=dict(title="definition -- what success means",
             lines=[
                ("head", "EM POV: success = improvable forever"),
                ("note", "Accuracy is a snapshot; maintainability is the movie"),
                ("done", "Regression-catching evals"),
                ("done", "Prompts + configs in version control"),
                ("done", "Document the 'why'"),
             ])),

    dict(n=59, topic="AI", style="em",
         post=(
"The biggest shift in my engineering management over the last few years: I optimize less for output and more for learning velocity.\n\n"
"AI changes so fast that what my team knows today is half-obsolete in a year. A team that learns quickly will out-execute a team that's merely productive.\n\n"
"How I build for it:\n"
"- We run small experiments constantly and share the results\n"
"- We treat 'this didn't work, here's why' as valuable output\n"
"- We make time to absorb what's new instead of just shipping\n\n"
"Productivity is this quarter's results. Learning velocity is every quarter's results. In a fast field, bet on the second.\n\n"
"#EngineeringManagement #AI #Leadership #LearningCulture #TechLeadership"),
         gif=dict(title="strategy -- learning velocity",
             lines=[
                ("head", "EM POV: optimize for learning velocity"),
                ("note", "Today's knowledge is half-obsolete in a year"),
                ("done", "Constant small experiments, shared"),
                ("done", "'Didn't work, here's why' = output"),
                ("done", "Time to absorb the new"),
             ])),

    dict(n=60, topic="AI Project Management", style="em",
         post=(
"Day 60 of 60. Here's everything I believe about engineering leadership in the AI era, compressed into one post.\n\n"
"The tools changed completely. The job barely did.\n\n"
"What still decides whether an AI team wins:\n"
"- Measure before you believe (evals over vibes)\n"
"- Make cost and quality visible to everyone\n"
"- Design for failure, because the model will fail\n"
"- Protect focus from the endless hype cycle\n"
"- Hire for curiosity and judgment, not just speed\n"
"- Build things your future team can safely change\n\n"
"New models will keep arriving. These fundamentals won't expire. Thanks for following along, this is where the real work begins.\n\n"
"#EngineeringManagement #AIProjectManagement #AI #Leadership #TechLeadership"),
         gif=dict(title="day 60/60 -- the whole playbook",
             lines=[
                ("head", "EM POV: tools changed, the job didn't"),
                ("done", "Measure before you believe"),
                ("done", "Make cost + quality visible"),
                ("done", "Design for failure"),
                ("done", "Protect focus from hype"),
                ("done", "Hire for curiosity + judgment"),
                ("done", "Build what your future team can change"),
             ])),
]

assert len(POSTS) == 60, f"expected 60 posts, got {len(POSTS)}"
# 15 terminal, 45 em
_term = sum(1 for p in POSTS if p["style"] == "terminal")
assert _term == 15, f"expected 15 terminal, got {_term}"
