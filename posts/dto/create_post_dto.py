from pydantic import BaseModel
class CreatePostDto(BaseModel):
    model_config = {'extra': 'forbid'}
    title: str
    content: str
    category: str