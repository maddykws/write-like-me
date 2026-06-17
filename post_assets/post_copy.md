# CUDA Kernel Post — 5 Variations

---

## Post 1 — Main Hook Post
**GIF:** `gif1_green_terminal.gif` — Classic green-on-black terminal compiling a CUDA GEMM kernel

---

Every AI engineer should learn to write exactly one CUDA kernel.

Not because you'll write them at work. You probably won't.

Because the mental model changes everything:

→ You stop thinking "model is slow" and start thinking
 "this operation has bad memory access patterns"
→ You stop seeing GPUs as black boxes and start seeing them
 as streaming processors
→ You understand why batch size matters, why FP8 helps, why
 fused kernels exist
→ You can read flash attention papers and actually understand
 them
→ You can debug performance issues 10x faster

Suggested starter kernel: GEMM with tiling.
~200 lines of CUDA, takes a weekend.
You'll never look at PyTorch the same way.

Have you written a CUDA kernel? What did it teach you?

---

## Post 2 — The Batch Size Insight
**GIF:** `gif2_vscode_dark.gif` — VS Code dark editor revealing a Python insight on GPU utilization

---

"Why is my GPU only at 34%?"

Most people blame the model.
The real answer is almost always memory access patterns.

Here's what changes after you write a CUDA kernel:

batch=1  → 12% MFU
batch=32 → 68% MFU

That's not magic. It's memory coalescing.
Bigger batches → threads access contiguous memory → 5x throughput.

The mental model: your GPU isn't a faster CPU.
It's 10,000 threads that all need to eat from the same buffet line.
Feed them in sync or starve them.

This is why batch size is the first knob to tune before anything else.

---

## Post 3 — Why FP8 Exists
**GIF:** `gif3_matrix_rain.gif` — Matrix rain revealing a CUDA FP8 kernel in the center

---

FP8 training gives you ~2x throughput over FP16.

That sounds like a hardware trick. It's actually a math insight.

After writing one CUDA kernel, you understand:
→ Precision determines how many values fit in a register
→ Smaller values = more threads computing in parallel
→ FP8 halves the bits → doubles the compute density

The "loss scaling" people warn you about? That's just keeping
gradients in a representable range. Dead simple once you see it.

Papers describe FP8 as "numerically challenging."
Engineers who've written kernels call it "a load instruction change."

The difference is the mental model.

---

## Post 4 — Before vs After Mental Model
**GIF:** `gif4_split_pane.gif` — Split-pane terminal: confused "before" (red) vs. sharp "after" (green)

---

The before/after of writing a CUDA kernel:

BEFORE:
- "The model is just slow"
- "I need a bigger GPU"
- GPU sitting at 34% utilization
- Changing hyperparameters at random

AFTER:
- Read the profiler first, always
- Identify the bottleneck in 10 minutes
- Fused ops, tiled memory, coalesced access
- 2.6x faster on the same hardware

I'm not saying CUDA knowledge makes you a kernel engineer.
I'm saying it makes you a better ML engineer.
Because you stop guessing and start seeing.

The ~200 lines of a tiled GEMM kernel will reframe every
performance conversation you ever have.

---

## Post 5 — Call to Action / Community
**GIF:** `gif5_amber_terminal.gif` — Retro amber terminal inviting people to share their kernel story

---

Hot take: every ML engineer should spend one weekend writing a CUDA kernel before touching a profiler.

Not to ship it. To understand what the profiler is actually telling you.

The starter project I'd recommend:
→ GEMM with shared memory tiling
→ ~200 lines of real CUDA C
→ Compare your output to cuBLAS
→ Read the Nsight profile and understand every line

Resources that actually helped me:
→ CUDA Programming Guide (Chapter 5 — memory model)
→ Simon Boehm's "How to Optimize a CUDA Matmul"
→ Tri Dao's Flash Attention repo — read the CUDA, not just the paper

Have you written a CUDA kernel? What clicked for you when you did?
Drop your experience below — or the kernel that broke your brain first.
