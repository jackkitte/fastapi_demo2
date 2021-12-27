from app.models.profile import ProfilePublic, ProfileUpdate
from fastapi import APIRouter, Body, Path

router = APIRouter()


@router.get(
    "/{username}/",
    response_model=ProfilePublic,
    name="profiles:get-profile-by-username",
)
async def get_profile_by_username(
    *, username: str = Path(..., min_length=3, regex="^[a-zA-Z0-9_-]+$")
) -> ProfilePublic:
    return None


@router.put("/me/", response_model=ProfilePublic, name="profiles:update-own-profile")
async def update_own_profile(
    profile_update: ProfileUpdate = Body(..., embed=True)
) -> ProfilePublic:
    return None
