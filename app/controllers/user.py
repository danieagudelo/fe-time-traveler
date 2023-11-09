from settings import Settings
from starlette.requests import Request
from schemas.user_signup import LoginUserData, CreateUserData
from fastapi import APIRouter, status, HTTPException
from services.user import create_new_user, login_user
from services.social_media_login import google_login, facebook_login


settings = Settings()


router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={201: {"description": "OK"}},
)


@router.get(
    "/auth/google",
    description="Validate Google session",
    status_code=status.HTTP_200_OK,
)
def verify_login(request: Request, token):
    return google_login(token)


@router.post(
    "/auth/facebook",
    description="Validate Facebook session",
    status_code=status.HTTP_200_OK,
)
def verify_login(response: dict):
    return facebook_login(response["response"])


@router.post(
    "/auth/signup",
    description="SignUp new user",
    status_code=status.HTTP_200_OK,
)
def signup(data: CreateUserData):
    return create_new_user(data)


@router.post(
    "/auth/login",
    description="Login user",
    status_code=status.HTTP_200_OK,
)
def login(data: LoginUserData):
    return login_user(data)
