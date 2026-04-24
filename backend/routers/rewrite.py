from __future__ import annotations
import os
from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from db.client import get_current_user, get_supabase
from models.schemas import RewriteRequest, RewriteResponse
from services.embedding import embed, cosine_similarity
from services.retrieval import find_similar_samples
from services.llm import rewrite_text

router = APIRouter(prefix="/rewrite", tags=["rewrite"])

CONTENT_PRESERVATION_THRESHOLD = 0.92
STYLE_SYSTEM_TEMPLATE = """\
You are a writing style transfer assistant. Your task is to rewrite text in the user's personal voice.

{summary_section}

Rules:
- Preserve ALL facts, names, numbers, and meaning exactly
- Only change sentence structure, word choice, tone, and rhythm
- Match the user's typical sentence length and formality level
- Mirror their punctuation habits (use of dashes, semicolons, etc.)
- Do NOT add information that wasn't in the original
- Return ONLY the rewritten text, nothing else
"""


@router.post("", response_model=RewriteResponse)
async def rewrite(
    body: RewriteRequest,
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    # Step 1: Embed input
    input_embedding = embed(body.text)

    # Step 2: Retrieve similar samples
    similar = find_similar_samples(supabase, user["id"], input_embedding, limit=6)
    few_shot_texts = [s["content"] for s in similar]
    few_shot_ids = [s["id"] for s in similar]

    if not few_shot_texts:
        raise HTTPException(
            status_code=400,
            detail="No writing samples found. Please add at least 5 writing samples first."
        )

    # Step 3: Load cached summary_prompt
    profile_resp = (
        supabase.table("voice_profiles")
        .select("summary_prompt")
        .eq("user_id", user["id"])
        .single()
        .execute()
    )
    summary = profile_resp.data.get("summary_prompt") if profile_resp.data else None
    summary_section = f"The user's writing style:\n{summary}" if summary else ""

    system_prompt = STYLE_SYSTEM_TEMPLATE.format(summary_section=summary_section).strip()

    # Step 4 & 5: Build prompt and call LLM
    model = body.model or (
        os.environ.get("DEFAULT_CLAUDE_MODEL", "claude-opus-4-5")
        if body.provider == "claude"
        else os.environ.get("DEFAULT_OPENAI_MODEL", "gpt-4o")
    )
    max_tokens = min(len(body.text.split()) * 3 * 2, 4096)  # rough word estimate * tokens/word * 2x

    rewritten = rewrite_text(
        original=body.text,
        system_prompt=system_prompt,
        few_shot_examples=few_shot_texts,
        provider=body.provider,
        api_key=body.api_key,
        model=model,
        max_tokens=max_tokens,
    )

    # Step 6: Content preservation check
    output_embedding = embed(rewritten)
    similarity = cosine_similarity(input_embedding, output_embedding)

    if similarity < CONTENT_PRESERVATION_THRESHOLD:
        # Retry once with stricter prompt
        strict_system = system_prompt + "\n\nCRITICAL: The previous rewrite drifted from the original meaning. Keep the same information — only change style."
        rewritten = rewrite_text(
            original=body.text,
            system_prompt=strict_system,
            few_shot_examples=few_shot_texts,
            provider=body.provider,
            api_key=body.api_key,
            model=model,
            max_tokens=max_tokens,
        )

    # Step 7: Persist
    row = {
        "user_id": user["id"],
        "original_text": body.text,
        "rewritten_text": rewritten,
        "provider": body.provider,
        "model": model,
        "few_shot_ids": few_shot_ids,
        "status": "pending",
    }
    result = supabase.table("rewrites").insert(row).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to persist rewrite")

    inserted = result.data[0]
    return RewriteResponse(
        rewrite_id=inserted["id"],
        original_text=body.text,
        rewritten_text=rewritten,
        provider=body.provider,
        model=model,
    )
