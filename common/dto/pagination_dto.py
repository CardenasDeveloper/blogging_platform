from pydantic import BaseModel, Field

class PaginationDto(BaseModel):
    limit: int = Field(default=10, gt=0)
    page: int = Field(default=1, gt=0)