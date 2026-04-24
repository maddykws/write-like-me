from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from db.client import get_current_user, get_supabase
from models.schemas import FeedbackRequest, FeedbackResponse
from services.embedding import embed
from services.profile_builder import recompute_profile

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackResponse)
async def submit_feedback(
    body: FeedbackRequest,
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase),
):
    # Verify the rewrite belongs to this user
    rewrite_resp = (
        supabase.table("rewrites")
        .select("id, rewritten_text, user_id")
        .eq("id", str(body.rewrite_id))
        .eq("user_id", user["id"])
        .single()
        .execute()
    )
    if not rewrite_resp.data:
        raise HTTPException(status_code=404, detail="Rewrite not found")

    rewrite = rewrite_resp.data

    # Insert feedback
    fb_row = {
        "rewrite_id": str(body.rewrite_id),
        "user_id": user["id"],
        "action": body.action,
    }
    if body.action == "edited" and body.edited_text:
        fb_row["edited_text"] = body.edited_text

    fb_result = supabase.table("feedback").insert(fb_row).execute()
    if not fb_result.data:
        raise HTTPException(status_code=500, detail="Failed to save feedback")

    feedback_id = fb_result.data[0]["id"]

    # Update rewrite status
    supabase.table("rewrites").update({"status": body.action}).eq("id", str(body.rewrite_id)).execute()

    # Feedback loop: accepted or edited → add as new writing sample
    sample_added = False
    if body.action in ("accepted", "edited"):
        text_to_add = body.edited_text if (body.action == "edited" and body.edited_text) else rewrite["rewritten_text"]
        vector = embed(text_to_add)
        sample_row = {
            "user_id": user["id"],
            "content": text_to_add,
            "char_count": len(text_to_add),
            "embedding": "[" + ",".join(str(x) for x in vector) + "]",
        }
        supabase.table("writing_samples").insert(sample_row).execute()
        sample_added = True

        # Recompute profile metrics (no LLM summary regeneration — no API key here)
        try:
            recompute_profile(supabase, user["id"])
        except Exception:
            pass

    return FeedbackResponse(
        feedback_id=feedback_id,
        action=body.action,
        sample_added=sample_added,
    )
