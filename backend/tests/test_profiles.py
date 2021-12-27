import pytest
from app.db.repositories.profiles import ProfilesRepository
from app.models.profile import ProfileInDB, ProfilePublic
from app.models.user import UserInDB, UserPublic
from databases import Database
from fastapi import FastAPI, status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestProfilesRoutes:
    async def test_routes_exist(
        self, app: FastAPI, client: AsyncClient, test_user: UserInDB
    ) -> None:
        res = await client.get(
            app.url_path_for(
                "profiles:get-profile-by-username", username=test_user.username
            )
        )
        assert res.status_code != status.HTTP_404_NOT_FOUND

        res = await client.put(
            app.url_path_for("profiles:update-own-profile"), json={"profile_update": {}}
        )
        assert res.status_code != status.HTTP_404_NOT_FOUND


class TestProfileCreate:
    async def test_profile_created_for_new_users(
        self, app: FastAPI, client: AsyncClient, db: Database
    ) -> None:
        profiles_repo = ProfilesRepository(db)
        new_user = {
            "email": "nmomos@mail.com",
            "username": "nmomoishedgehog",
            "password": "nmomosissocute",
        }
        res = await client.post(
            app.url_path_for("users:register-new-user"), json={"new_user": new_user}
        )
        assert res.status_code == status.HTTP_201_CREATED
        created_user = UserPublic(**res.json())
        user_profile = await profiles_repo.get_profile_by_user_id(
            user_id=created_user.id
        )
        assert user_profile is not None
        assert isinstance(user_profile, ProfileInDB)
