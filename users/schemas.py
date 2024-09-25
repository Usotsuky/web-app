from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from annotated_types import MinLen, MaxLen


class CreateUser(BaseModel):
    # username: str = Field(..., min_length=1, max_length=15) validation and metadata
    username: Annotated[str, MinLen(3), MaxLen(15)]
    email: EmailStr
