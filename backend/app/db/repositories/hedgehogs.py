from typing import List, Optional

from app.db.repositories.base import BaseRepository
from app.models.hedgehog import HedgehogCreate, HedgehogInDB, HedgehogUpdate
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

CREATE_HEDGEHOG_QUERY = """
    INSERT INTO hedgehogs (name, description, age, color_type)
    VALUES (:name, :description, :age, :color_type)
    RETURNING id, name, description, age, color_type;
"""
GET_HEDGEHOG_BY_ID_QUERY = """
    SELECT id, name, description, age, color_type
    FROM hedgehogs
    WHERE id = :id;
"""
GET_ALL_HEDGEHOGS_QUERY = """
    SELECT id, name, description, age, color_type
    FROM hedgehogs;
"""
UPDATE_HEDGEHOG_BY_ID_QUERY = """
    UPDATE hedgehogs
    SET name            = :name,
        description     = :description,
        age             = :age,
        color_type      = :color_type
    WHERE id = :id
    RETURNING id, name, description, age, color_type;
"""
DELETE_HEDGEHOG_BY_ID_QUERY = """
    DELETE FROM hedgehogs
    WHERE id = :id
    RETURNING id;
"""


class HedgehogsRepository(BaseRepository):
    async def create_hedgehog(self, *, new_hedgehog: HedgehogCreate) -> HedgehogInDB:
        query_values = new_hedgehog.dict()
        hedgehog = await self.db.fetch_one(
            query=CREATE_HEDGEHOG_QUERY, values=query_values
        )

        return HedgehogInDB(**hedgehog)

    async def get_hedgehog_by_id(self, *, id: int) -> Optional[HedgehogInDB]:
        hedgehog = await self.db.fetch_one(
            query=GET_HEDGEHOG_BY_ID_QUERY,
            values={"id": id},
        )
        if not hedgehog:
            return None
        return HedgehogInDB(**hedgehog)

    async def get_all_hedgehogs(self) -> List[HedgehogInDB]:
        hedgehog_records = await self.db.fetch_all(query=GET_ALL_HEDGEHOGS_QUERY)
        return [HedgehogInDB(**item) for item in hedgehog_records]

    async def update_hedgehog(
        self, *, id: int, hedgehog_update: HedgehogUpdate
    ) -> Optional[HedgehogInDB]:
        hedgehog = await self.get_hedgehog_by_id(id=id)
        if not hedgehog:
            return None
        hedgehog_update_params = hedgehog.copy(
            update=hedgehog_update.dict(exclude_unset=True)
        )
        if hedgehog_update_params.color_type is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid color type. Cannot be None.",
            )
        try:
            update_hedgehog = await self.db.fetch_one(
                query=UPDATE_HEDGEHOG_BY_ID_QUERY, values=hedgehog_update_params.dict()
            )
            return HedgehogInDB(**update_hedgehog)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Invalid update params."
            )

    async def delete_hedgehog_by_id(self, *, id: int) -> Optional[int]:
        hedgehog = await self.get_hedgehog_by_id(id=id)
        if not hedgehog:
            return None
        deleted_id = await self.db.execute(
            query=DELETE_HEDGEHOG_BY_ID_QUERY, values={"id": id}
        )
        return deleted_id
