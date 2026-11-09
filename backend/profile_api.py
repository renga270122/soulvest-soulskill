"""Authenticated profile endpoints for the SoulSkill career workspace."""
from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from .auth import AuthContext, get_auth_context

router = APIRouter(prefix="/api/v1", tags=["account", "profile"])


class ProfileUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str | None = Field(default=None, max_length=160)
    career_stage: Literal["fresher", "career_restart", "career_growth", "exploring"] | None = None
    current_title: str | None = Field(default=None, max_length=160)
    headline: str | None = Field(default=None, max_length=240)
    summary: str | None = Field(default=None, max_length=4000)
    years_experience: float | None = Field(default=None, ge=0, le=60)
    target_roles: list[str] | None = Field(default=None, max_length=20)
    target_locations: list[str] | None = Field(default=None, max_length=20)
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    locale: str | None = Field(default=None, max_length=20)
    timezone: str | None = Field(default=None, max_length=64)


@router.get("/me")
def get_me(context: AuthContext = Depends(get_auth_context)):
    user = context.user
    return {
        "user_id": context.user_id,
        "email": context.email,
        "created_at": getattr(user, "created_at", None),
    }


@router.get("/profile")
def get_profile(context: AuthContext = Depends(get_auth_context)):
    response = (
        context.supabase.table("candidate_profiles")
        .select("*")
        .eq("user_id", context.user_id)
        .maybe_single()
        .execute()
    )
    return {"profile": response.data}


@router.patch("/profile")
def update_profile(
    update: ProfileUpdate,
    context: AuthContext = Depends(get_auth_context),
):
    changes = update.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="Provide at least one profile field to update.")

    # Identity is always derived from the verified token, never from request JSON.
    payload = {"user_id": context.user_id, **changes}
    response = (
        context.supabase.table("candidate_profiles")
        .upsert(payload, on_conflict="user_id")
        .execute()
    )
    rows = response.data or []
    profile = rows[0] if isinstance(rows, list) and rows else rows
    return {"profile": profile}
