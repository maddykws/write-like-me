from __future__ import annotations
from fastapi import APIRouter
from models.schemas import ValidateKeyRequest, ValidateKeyResponse
from services.llm import validate_key

router = APIRouter(prefix="/settings", tags=["settings"])


@router.post("/validate-key", response_model=ValidateKeyResponse)
async def validate_api_key(body: ValidateKeyRequest):
    valid, message = await validate_key(body.provider, body.api_key)
    return ValidateKeyResponse(valid=valid, message=message)
