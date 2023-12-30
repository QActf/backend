from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app.models import Profile


class ProfileFilter(Filter):
    age__gte: Optional[int] = Field(None)
    age__lte: Optional[int] = Field(None)

    class Constants(Filter.Constants):
        model = Profile
