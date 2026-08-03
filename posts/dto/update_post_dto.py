from pydantic import BaseModel, Field

class UpdatePostDto(BaseModel):
    title: str | None = Field(default=None)
    content: str | None = Field(default=None)
    category: str | None = Field(default=None)