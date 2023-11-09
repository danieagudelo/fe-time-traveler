from pydantic import BaseModel


class CreateUserData(BaseModel):
    name: str
    email: str
    password: str


class LoginUserData(BaseModel):
    email: str
    password: str


class UserDataSerialized(BaseModel):
    name: str
    email: str
    password: bytes


class UserSocialMediaSerialized(BaseModel):
    name: str
    email: str
    social_media: bool
    social_media_name: str
