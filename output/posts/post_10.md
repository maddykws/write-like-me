# Post 10 — Day 10

**Topic:** Token Optimization  
**GIF style:** Terminal output  
**Attach:** `post_10.gif`

---

If you're sending the same system prompt on every API call, you're paying for it every single time. You don't have to.

Prompt caching lets the model reuse the expensive, unchanging part of your prompt, so you only pay full price for the part that actually changes.

Best candidates to cache:
- Long system instructions
- Static few-shot examples
- Large reference documents reused across requests

On a chat app with a heavy system prompt, caching cut our latency and cost on cached tokens dramatically, for what amounted to a config change.

Structure your prompt so the stable stuff comes first. Then cache it.

#AI #TokenOptimization #PromptCaching #LLM #CostOptimization
