from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
from db.client import get_current_user, get_supabase, authed_client
from models.schemas import SampleBatch, SampleResponse
from services.embedding import embed
from services.profile_builder import recompute_profile

router = APIRouter(prefix="/samples", tags=["samples"])


@router.post("", response_model=list[SampleResponse], status_code=status.HTTP_201_CREATED)
async def create_samples(
    body: SampleBatch,
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    rows = []
    for s in body.samples:
        vector = embed(s.content)
        row = {
            "user_id": user["id"],
            "content": s.content,
            "char_count": len(s.content),
            "embedding": "[" + ",".join(str(x) for x in vector) + "]",
        }
        rows.append(row)

    result = supabase.table("writing_samples").insert(rows).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to insert samples")

    # Trigger profile recompute (fire-and-forget style — no API key needed for metrics)
    try:
        recompute_profile(supabase, user["id"])
    except Exception:
        pass

    return [
        SampleResponse(
            id=r["id"],
            content=r["content"],
            char_count=r["char_count"],
            created_at=r["created_at"],
        )
        for r in result.data
    ]


@router.get("", response_model=list[SampleResponse])
async def list_samples(
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    result = (
        supabase.table("writing_samples")
        .select("id, content, char_count, created_at")
        .eq("user_id", user["id"])
        .order("created_at", desc=True)
        .execute()
    )
    return [
        SampleResponse(
            id=r["id"],
            content=r["content"],
            char_count=r["char_count"],
            created_at=r["created_at"],
        )
        for r in (result.data or [])
    ]


@router.delete("/{sample_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sample(
    sample_id: UUID,
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    result = (
        supabase.table("writing_samples")
        .delete()
        .eq("id", str(sample_id))
        .eq("user_id", user["id"])
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Sample not found")

    try:
        recompute_profile(supabase, user["id"])
    except Exception:
        pass
