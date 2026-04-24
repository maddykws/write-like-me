from __future__ import annotations
import os
from supabase import Client
from services.style_metrics import compute_metrics
from services.llm import generate_summary_prompt, ProviderType


def recompute_profile(
    supabase: Client,
    user_id: str,
    provider: ProviderType = "claude",
    api_key: str | None = None,
) -> dict:
    """
    Fetch all writing samples for the user, aggregate style metrics
    (weighted by char_count), regenerate summary_prompt, upsert voice_profiles.
    """
    samples_resp = (
        supabase.table("writing_samples")
        .select("content, char_count")
        .eq("user_id", user_id)
        .execute()
    )
    samples = samples_resp.data or []

    if not samples:
        return {}

    total_chars = sum(s.get("char_count") or len(s["content"]) for s in samples)
    sample_count = len(samples)

    # Weighted aggregation
    agg = {
        "avg_sentence_length": 0.0,
        "formality_score": 0.0,
        "type_token_ratio": 0.0,
        "punct_signature": {"em_dash": 0.0, "ellipsis": 0.0, "semicolon": 0.0, "colon": 0.0, "parens": 0.0},
    }

    for sample in samples:
        weight = (sample.get("char_count") or len(sample["content"])) / max(total_chars, 1)
        metrics = compute_metrics(sample["content"])
        agg["avg_sentence_length"] += metrics["avg_sentence_length"] * weight
        agg["formality_score"] += metrics["formality_score"] * weight
        agg["type_token_ratio"] += metrics["type_token_ratio"] * weight
        for k in agg["punct_signature"]:
            agg["punct_signature"][k] += metrics["punct_signature"][k] * weight

    # Only regenerate summary_prompt when we have a key and meaningful samples
    summary_prompt = None
    if api_key:
        metrics_desc = _build_metrics_description(agg, sample_count)
        try:
            summary_prompt = generate_summary_prompt(metrics_desc, provider, api_key)
        except Exception:
            pass  # non-fatal: rewrite will work without cached summary

    profile_data = {
        "user_id": user_id,
        "sample_count": sample_count,
        "avg_sentence_length": agg["avg_sentence_length"],
        "formality_score": agg["formality_score"],
        "type_token_ratio": agg["type_token_ratio"],
        "punct_signature": agg["punct_signature"],
        "updated_at": "now()",
    }
    if summary_prompt:
        profile_data["summary_prompt"] = summary_prompt

    supabase.table("voice_profiles").upsert(profile_data, on_conflict="user_id").execute()
    return profile_data


def _build_metrics_description(agg: dict, sample_count: int) -> str:
    ps = agg["punct_signature"]
    formality_label = "formal" if agg["formality_score"] > 0.6 else ("casual" if agg["formality_score"] < 0.4 else "neutral")
    return (
        f"Samples: {sample_count}\n"
        f"Avg sentence length: {agg['avg_sentence_length']:.1f} words\n"
        f"Formality: {agg['formality_score']:.2f} ({formality_label})\n"
        f"Vocabulary richness (MATTR): {agg['type_token_ratio']:.3f}\n"
        f"Punctuation per 1000 chars — em-dash: {ps['em_dash']:.1f}, "
        f"ellipsis: {ps['ellipsis']:.1f}, semicolon: {ps['semicolon']:.1f}, "
        f"colon: {ps['colon']:.1f}, parens: {ps['parens']:.1f}"
    )
