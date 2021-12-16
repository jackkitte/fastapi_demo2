from app.db.repositories.base import BaseRepository
from app.models.user import UserCreate, UserInDB


class UsersRepository(BaseRepository):
    async def register_new_user(self, *, new_user: UserCreate) -> UserInDB:
        return None
