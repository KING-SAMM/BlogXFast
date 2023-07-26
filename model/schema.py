from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    body: str
    author: str
    category_id: int
