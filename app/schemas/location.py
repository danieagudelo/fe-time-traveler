from typing import List
from pydantic import BaseModel


class LocationSchema(BaseModel):
    lat: str
    lng: str
    title: str
    text: str
    images: List[str]
