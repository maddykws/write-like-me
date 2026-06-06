# Post 03 — Day 3

**Topic:** Java  
**GIF style:** Terminal output  
**Attach:** `post_03.gif`

---

"Streams are slower than loops" is the most repeated half-truth in Java.

The truth: streams aren't free, but the difference rarely matters, and readability almost always does.

Where streams genuinely cost you:
- Hot loops running millions of times per second
- Boxing primitives (use IntStream / LongStream)
- Tiny collections where setup overhead dominates

Everywhere else? Write the version your teammate can read at 2am during an incident.

Optimize for the bottleneck you measured, not the one you imagined.

#Java #CleanCode #Performance #SoftwareEngineering #Streams
