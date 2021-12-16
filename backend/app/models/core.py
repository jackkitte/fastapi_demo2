from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel, validator

JST = ZoneInfo("Asia/Tokyo")


class CoreModel(BaseModel):
    pass


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now(JST)


class IDModelMixin(BaseModel):
    id: int
