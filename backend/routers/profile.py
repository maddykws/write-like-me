from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from db.client import get_current_user, get_supabase
from models.schemas import VoiceProfileResponse, PunctSignature
from services.profile_builder import recompute_profile

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=VoiceProfileResponse)
async def get_profile(
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    result = (
        supabase.table("voice_profiles")
        .select("*")
        .eq("user_id", user["id"])
        .single()
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="No voice profile yet. Upload writing samples first.")

    data = result.data
    ps = data.get("punct_signature")

    return VoiceProfileResponse(
        sample_count=data.get("sample_count") or 0,
        avg_sentence_length=data.get("avg_sentence_length"),
        formality_score=data.get("formality_score"),
        type_token_ratio=data.get("type_token_ratio"),
        punct_signature=PunctSignature(**ps) if ps else None,
        preferred_connectives=data.get("preferred_connectives"),
        summary_prompt=data.get("summary_prompt"),
        updated_at=data.get("updated_at"),
    )


@router.post("/recompute", response_model=VoiceProfileResponse)
async def force_recompute(
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    data = recompute_profile(supabase, user["id"])
    if not data:
        raise HTTPException(status_code=400, detail="No writing samples found to build profile from.")

    ps = data.get("punct_signature")
    return VoiceProfileResponse(
        sample_count=data.get("sample_count") or 0,
        avg_sentence_length=data.get("avg_sentence_length"),
        formality_score=data.get("formality_score"),
        type_token_ratio=data.get("type_token_ratio"),
        punct_signature=PunctSignature(**ps) if ps else None,
        preferred_connectives=data.get("preferred_connectives"),
        summary_prompt=data.get("summary_prompt"),
        updated_at=None,
    )
