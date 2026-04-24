from __future__ import annotations
from typing import Literal, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


# ── Samples ─────────────────────────────────────────────────────────────────

class SampleCreate(BaseModel):
    content: str = Field(..., min_length=50, max_length=10000)


class SampleBatch(BaseModel):
    samples: list[SampleCreate] = Field(..., min_length=1, max_length=20)


class SampleResponse(BaseModel):
    id: UUID
    content: str
    char_count: int
    created_at: datetime


# ── Voice Profile ────────────────────────────────────────────────────────────

class PunctSignature(BaseModel):
    em_dash: float = 0.0
    ellipsis: float = 0.0
    semicolon: float = 0.0
    colon: float = 0.0
    parens: float = 0.0


class VoiceProfileResponse(BaseModel):
    sample_count: int
    avg_sentence_length: Optional[float]
    formality_score: Optional[float]
    type_token_ratio: Optional[float]
    punct_signature: Optional[PunctSignature]
    preferred_connectives: Optional[list[str]]
    summary_prompt: Optional[str]
    updated_at: Optional[datetime]


# ── Rewrite ──────────────────────────────────────────────────────────────────

class RewriteRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=8000)
    provider: Literal["claude", "openai"] = "claude"
    api_key: str = Field(..., min_length=10)
    model: Optional[str] = None


class RewriteResponse(BaseModel):
    rewrite_id: UUID
    original_text: str
    rewritten_text: str
    provider: str
    model: str


# ── Feedback ─────────────────────────────────────────────────────────────────

class FeedbackRequest(BaseModel):
    rewrite_id: UUID
    action: Literal["accepted", "edited", "rejected"]
    edited_text: Optional[str] = None


class FeedbackResponse(BaseModel):
    feedback_id: UUID
    action: str
    sample_added: bool


# ── Settings ─────────────────────────────────────────────────────────────────

class ValidateKeyRequest(BaseModel):
    provider: Literal["claude", "openai"]
    api_key: str


class ValidateKeyResponse(BaseModel):
    valid: bool
    message: str
