from __future__ import annotations
import re
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag

# Download required NLTK data on first import
for _pkg in ("punkt", "averaged_perceptron_tagger", "punkt_tab", "averaged_perceptron_tagger_eng"):
    try:
        nltk.data.find(f"tokenizers/{_pkg}" if "punkt" in _pkg else f"taggers/{_pkg}")
    except LookupError:
        nltk.download(_pkg, quiet=True)


def avg_sentence_length(text: str) -> float:
    sentences = sent_tokenize(text)
    if not sentences:
        return 0.0
    lengths = [len(word_tokenize(s)) for s in sentences]
    return sum(lengths) / len(lengths)


def mattr_ttr(text: str, window: int = 50) -> float:
    """Moving Average Type-Token Ratio with a 50-token window."""
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalpha()]
    if len(tokens) < window:
        return len(set(tokens)) / max(len(tokens), 1)
    ratios = [
        len(set(tokens[i : i + window])) / window
        for i in range(len(tokens) - window + 1)
    ]
    return sum(ratios) / len(ratios)


def formality_score(text: str) -> float:
    """
    Heylighen & Dewaele F-measure.
    F = (noun + adj + prep + article freq - pronoun - verb - adverb - interj + 100) / 2
    Returns 0.0 (casual) to 1.0 (formal).
    """
    tokens = word_tokenize(text)
    if not tokens:
        return 0.5
    tagged = pos_tag(tokens)
    tag_counts: Counter = Counter()
    for _, tag in tagged:
        tag_counts[tag] += 1

    total = len(tagged)

    def freq(*tags: str) -> float:
        return sum(tag_counts.get(t, 0) for t in tags) / total * 100

    formal = freq("NN", "NNS", "NNP", "NNPS") + freq("JJ", "JJR", "JJS") + freq("IN") + freq("DT")
    informal = freq("PRP", "PRP$", "WP", "WP$") + freq("VB", "VBD", "VBG", "VBN", "VBP", "VBZ") + freq("RB", "RBR", "RBS") + freq("UH")

    raw = (formal - informal + 100) / 2
    return max(0.0, min(1.0, raw / 100))


def punct_signature(text: str) -> dict[str, float]:
    """Per-1000-character frequencies of distinctive punctuation."""
    n = max(len(text), 1)
    scale = 1000 / n
    return {
        "em_dash": (text.count("—") + text.count("--")) * scale,
        "ellipsis": (text.count("…") + text.count("...")) * scale,
        "semicolon": text.count(";") * scale,
        "colon": text.count(":") * scale,
        "parens": (text.count("(") + text.count(")")) * scale / 2,
    }


def compute_metrics(text: str) -> dict:
    return {
        "avg_sentence_length": avg_sentence_length(text),
        "type_token_ratio": mattr_ttr(text),
        "formality_score": formality_score(text),
        "punct_signature": punct_signature(text),
    }
