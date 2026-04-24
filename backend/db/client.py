from __future__ import annotations
import os
from functools import lru_cache
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

_bearer = HTTPBearer()


@lru_cache(maxsize=1)
def get_supabase() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    return create_client(url, key)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    supabase: Client = Depends(get_supabase),
) -> dict:
    """Verify Supabase JWT and return the user payload."""
    token = credentials.credentials
    try:
        response = supabase.auth.get_user(token)
        if response.user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"id": str(response.user.id), "token": token}
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


def authed_client(user_token: str) -> Client:
    """Return a Supabase client scoped to the user's JWT (respects RLS)."""
    url = os.environ["SUPABASE_URL"]
    anon_key = os.environ.get("SUPABASE_ANON_KEY", os.environ["SUPABASE_SERVICE_ROLE_KEY"])
    client = create_client(url, anon_key)
    client.postgrest.auth(user_token)
    return client
