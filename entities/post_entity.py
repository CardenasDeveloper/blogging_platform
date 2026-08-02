from sqlmodel import SQLModel, Field

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
