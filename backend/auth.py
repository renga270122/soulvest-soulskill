"""Supabase Auth integration for request-scoped, RLS-aware API access."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import Client, create_client

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class AuthContext:
    user_id: str
    email: str | None
    user: Any
    supabase: Client


def get_auth_context(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> AuthContext:
    """Validate the Supabase access token and bind it to a fresh RLS-scoped client."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sign in to continue.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    project_url = os.getenv("SUPABASE_URL", "").strip()
    publishable_key = (
        os.getenv("SUPABASE_PUBLISHABLE_KEY", "").strip()
        or os.getenv("SUPABASE_ANON_KEY", "").strip()
    )
    if not project_url or not publishable_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Account services are not configured yet.",
        )

    try:
        client = create_client(project_url, publishable_key)
        response = client.auth.get_user(credentials.credentials)
        user = getattr(response, "user", None)
        if user is None or not getattr(user, "id", None):
            raise ValueError("Supabase did not return an authenticated user.")
        # A new client per request prevents one user's JWT from leaking into another request.
        client.postgrest.auth(credentials.credentials)
        return AuthContext(
            user_id=str(user.id),
            email=getattr(user, "email", None),
            user=user,
            supabase=client,
        )
    except HTTPException:
        raise
    except Exception as exc:
        # Do not log or return the token, provider response, or exception contents.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your session is invalid or expired. Please sign in again.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
