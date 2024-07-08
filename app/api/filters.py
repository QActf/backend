from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app.models import Profile


class ProfileFilter(Filter):
    first_name__ilike: Optional[str] = Field(None)
    last_name__ilike: Optional[str] = Field(None)

    class Constants(Filter.Constants):
        model = Profile
        search_model_fields = ['first_name', 'last_name']
