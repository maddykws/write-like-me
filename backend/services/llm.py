from __future__ import annotations
import os
from typing import Literal

ProviderType = Literal["claude", "openai"]


def rewrite_text(
    original: str,
    system_prompt: str,
    few_shot_examples: list[str],
    provider: ProviderType,
    api_key: str,
    model: str | None,
    temperature: float = 0.7,
    max_tokens: int = 4096,
) -> str:
    user_message = _build_user_message(original, few_shot_examples)
    if provider == "claude":
        return _call_claude(system_prompt, user_message, api_key, model, temperature, max_tokens)
    else:
        return _call_openai(system_prompt, user_message, api_key, model, temperature, max_tokens)


def generate_summary_prompt(metrics_description: str, provider: ProviderType, api_key: str) -> str:
    """Generate a cached NL style description for use in the system prompt."""
    system = (
        "You are a writing style analyst. Given style metrics, produce a concise 2-3 sentence "
        "description of the writer's voice that an LLM can use as a style guide. "
        "Be specific and concrete about sentence rhythm, tone, vocabulary richness, and punctuation habits."
    )
    user = f"Style metrics:\n{metrics_description}\n\nDescribe this writer's voice:"

    if provider == "claude":
        model = os.environ.get("DEFAULT_CLAUDE_MODEL", "claude-haiku-4-5")
        # Use the cheapest model for summary generation
        if "opus" in (model or ""):
            model = "claude-haiku-4-5"
        return _call_claude(system, user, api_key, model, temperature=0.3, max_tokens=300)
    else:
        model = "gpt-4o-mini"
        return _call_openai(system, user, api_key, model, temperature=0.3, max_tokens=300)


async def validate_key(provider: ProviderType, api_key: str) -> tuple[bool, str]:
    """Cheaply test whether an API key is valid."""
    try:
        if provider == "claude":
            _call_claude("You are a test.", "Say: OK", api_key, "claude-haiku-4-5", 0.0, 5)
        else:
            _call_openai("You are a test.", "Say: OK", api_key, "gpt-4o-mini", 0.0, 5)
        return True, "Key is valid"
    except Exception as e:
        msg = str(e)
        if "401" in msg or "authentication" in msg.lower() or "api key" in msg.lower():
            return False, "Invalid API key"
        return False, f"Validation error: {msg}"


def _build_user_message(original: str, examples: list[str]) -> str:
    parts = []
    if examples:
        parts.append("Here are examples of my writing style:")
        for i, ex in enumerate(examples, 1):
            parts.append(f"\n--- Example {i} ---\n{ex.strip()}")
        parts.append("\n")
    parts.append(f"Now rewrite the following text in my voice. Preserve all facts and meaning exactly:\n\n{original}")
    return "\n".join(parts)


def _call_claude(
    system: str,
    user: str,
    api_key: str,
    model: str | None,
    temperature: float,
    max_tokens: int,
) -> str:
    from anthropic import Anthropic
    client = Anthropic(api_key=api_key)
    resolved_model = model or os.environ.get("DEFAULT_CLAUDE_MODEL", "claude-opus-4-5")
    response = client.messages.create(
        model=resolved_model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text


def _call_openai(
    system: str,
    user: str,
    api_key: str,
    model: str | None,
    temperature: float,
    max_tokens: int,
) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    resolved_model = model or os.environ.get("DEFAULT_OPENAI_MODEL", "gpt-4o")
    response = client.chat.completions.create(
        model=resolved_model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return response.choices[0].message.content or ""
