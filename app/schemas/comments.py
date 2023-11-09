from uuid import UUID
from pydantic import BaseModel


class CommentData(BaseModel):
    location_id: int
    user_id: UUID
    username: str
    text: str
    created: str


class ReactComment(BaseModel):
    comment_id: int
    reaction_type: str
    user_id: str
