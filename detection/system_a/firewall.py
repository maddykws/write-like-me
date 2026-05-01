"""
System A: Static Pre-Execution Firewall
========================================
Based on:
  - arXiv:2506.08837 "Design Patterns for Securing LLM Agents" (Minimizer/Sanitizer)
  - arXiv:2511.15759 "Securing AI Agents Against Prompt Injection" (embedding anomaly)

Two components:
  1. ToolInputFirewall  — checks tool call ARGUMENTS before execution
  2. ToolOutputSanitizer — checks tool RESPONSES before feeding back to the agent

Decision logic per text chunk:
  - Regex hit at 'critical' → block immediately
  - Regex hit at 'high' → block
  - Regex hit at 'medium' → flag, continue (log only)
  - Embedding cosine similarity > threshold for any attack category → block

Usage:
    fw = Firewall(openai_api_key="sk-...")
    block_reason = fw.check_input("send_email", {"to": "attacker@evil.com", "body": "..."})
    clean_output = fw.sanitize_output("read_email", {}, raw_tool_response)
"""

from __future__ import annotations
import re
import numpy as np
from typing import Any
from .signatures import REGEX_PATTERNS, EMBEDDING_TEMPLATES

BLOCK_SEVERITIES = {"critical", "high"}
EMBEDDING_BLOCK_THRESHOLD = 0.72   # cosine similarity above this → block
EMBEDDING_WARN_THRESHOLD  = 0.55   # above this → log warning only


class Firewall:
    def __init__(self, openai_api_key: str | None = None, use_local_embeddings: bool = True):
        """
        use_local_embeddings=True  → sentence-transformers (free, offline)
        use_local_embeddings=False → OpenAI text-embedding-3-small (more accurate, costs tokens)
        """
        self.openai_api_key = openai_api_key
        self.use_local = use_local_embeddings
        self._model = None
        self._template_embeddings: dict[str, np.ndarray] | None = None

    # ── Public API ───────────────────────────────────────────────────────────

    def check_input(self, tool_name: str, args: dict[str, Any]) -> str | None:
        """
        Called BEFORE a tool executes.
        Returns a block reason string if the call should be blocked, else None.
        """
        text = _args_to_text(args)
        return self._scan(text, context=f"tool_input:{tool_name}")

    def sanitize_output(self, tool_name: str, args: dict[str, Any], raw_output: str) -> str:
        """
        Called AFTER a tool executes, BEFORE the output is fed back to the agent.
        Returns sanitized output (injected instructions stripped or replaced).
        """
        block_reason = self._scan(raw_output, context=f"tool_output:{tool_name}")
        if block_reason:
            # Strip the injected portion rather than blocking the whole response.
            # Heuristic: content after the last "clean" paragraph boundary.
            clean = _strip_injection(raw_output)
            return f"{clean}\n[Sanitizer: {block_reason} — injected content removed]"
        return raw_output

    # ── Internal ─────────────────────────────────────────────────────────────

    def _scan(self, text: str, context: str) -> str | None:
        # Layer 1: regex (fast path)
        for pattern, severity, description in REGEX_PATTERNS:
            if pattern.search(text):
                if severity in BLOCK_SEVERITIES:
                    return f"[SystemA] {severity.upper()} regex match: {description} ({context})"

        # Layer 2: embedding similarity
        try:
            result = self._embedding_scan(text)
            if result:
                return f"[SystemA] Embedding anomaly ({result[0]}, score={result[1]:.3f}) ({context})"
        except Exception:
            pass  # embedding unavailable → fall through

        return None

    def _embedding_scan(self, text: str) -> tuple[str, float] | None:
        """Returns (category, score) if above block threshold, else None."""
        text_emb = self._embed([text])[0]
        templates = self._get_template_embeddings()

        for category, templ_emb in templates.items():
            sim = float(np.dot(text_emb, templ_emb) / (np.linalg.norm(text_emb) * np.linalg.norm(templ_emb) + 1e-9))
            if sim >= EMBEDDING_BLOCK_THRESHOLD:
                return category, sim

        return None

    def _embed(self, texts: list[str]) -> list[np.ndarray]:
        if self.use_local:
            return self._embed_local(texts)
        return self._embed_openai(texts)

    def _embed_local(self, texts: list[str]) -> list[np.ndarray]:
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
        vecs = self._model.encode(texts, normalize_embeddings=True)
        return [np.array(v) for v in vecs]

    def _embed_openai(self, texts: list[str]) -> list[np.ndarray]:
        from openai import OpenAI
        client = OpenAI(api_key=self.openai_api_key)
        resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
        return [np.array(d.embedding) for d in resp.data]

    def _get_template_embeddings(self) -> dict[str, np.ndarray]:
        if self._template_embeddings is None:
            self._template_embeddings = {}
            for category, sentences in EMBEDDING_TEMPLATES.items():
                vecs = self._embed(sentences)
                # Average the template embeddings into one representative vector
                avg = np.mean(np.stack(vecs), axis=0)
                avg = avg / (np.linalg.norm(avg) + 1e-9)
                self._template_embeddings[category] = avg
        return self._template_embeddings


# ── Helpers ──────────────────────────────────────────────────────────────────

def _args_to_text(args: dict[str, Any]) -> str:
    return " ".join(str(v) for v in args.values())


def _strip_injection(text: str) -> str:
    """
    Heuristic: split on double-newline, drop any paragraph that hits a
    critical/high regex pattern. Keeps legitimate content intact.
    """
    paragraphs = re.split(r"\n{2,}", text)
    clean = []
    for para in paragraphs:
        hit = False
        for pattern, severity, _ in REGEX_PATTERNS:
            if severity in BLOCK_SEVERITIES and pattern.search(para):
                hit = True
                break
        if not hit:
            clean.append(para)
    return "\n\n".join(clean)


def make_hooks(firewall: Firewall):
    """
    Returns (pre_call_hook, post_call_hook) callables for AgentHarness.
    """
    def pre_call(tool_name: str, args: dict) -> str | None:
        return firewall.check_input(tool_name, args)

    def post_call(tool_name: str, args: dict, result: str) -> str:
        return firewall.sanitize_output(tool_name, args, result)

    return pre_call, post_call
