from __future__ import annotations
from supabase import Client


def find_similar_samples(
    supabase: Client,
    user_id: str,
    query_embedding: list[float],
    limit: int = 6,
) -> list[dict]:
    """
    pgvector cosine distance search over writing_samples.
    Returns rows ordered by similarity (most similar first).
    """
    vector_str = "[" + ",".join(str(x) for x in query_embedding) + "]"

    result = (
        supabase.rpc(
            "match_writing_samples",
            {
                "query_embedding": vector_str,
                "match_user_id": user_id,
                "match_count": limit,
            },
        )
        .execute()
    )
    return result.data or []
