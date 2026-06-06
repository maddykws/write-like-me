# Post 11 — Day 11

**Topic:** GPU  
**GIF style:** Terminal output  
**Attach:** `post_11.gif`

---

Your GPU is probably idle most of the time you think it's working.

"CUDA out of memory" and "why is my GPU at 20% utilization" are usually the same bug wearing two hats: bad batching.

What changed everything for me:
- Watch GPU utilization, not just memory
- Batch requests so the GPU does real work per kernel launch
- Stop tiny one-sample inferences that leave the card waiting

A model serving 12 req/s went to 90+ req/s on the same hardware once we batched properly.

The expensive silicon isn't the problem. Feeding it is.

#GPU #CUDA #MachineLearning #MLOps #Performance
