import logging
import settings
from fastapi import HTTPException
from google.oauth2 import id_token
from config.database import create_session
from google.auth.transport import requests
from fastapi.responses import JSONResponse
from repositories.user import get_user_social_media
from repositories.user import create_social_media_user
from schemas.user_signup import UserSocialMediaSerialized
from services.session_token import generate_session_token


setting = settings.Settings()


def google_login(token: str):
    try:
        user_google = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            setting.GOOGLE_SECRET,
        )

        session = create_session()
        user_data = get_user_social_media(session, user_google["email"])

        name = (
            capitalize_first_letter(user_google["given_name"])
            + " "
            + capitalize_first_letter(user_google["family_name"])
        )

        if user_data is None:
            user_data = UserSocialMediaSerialized(
                name=name,
                email=user_google["email"],
                social_media=True,
                social_media_name="Google",
            )
            user_data = create_social_media_user(session, user_data)

        token = generate_session_token(str(user_data.user_id), name)

        return JSONResponse(
            content={"message": "Login success", "token": token}, status_code=201
        )

    except ValueError as ve:
        logging.error(f"Method create_new_user: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Method create_new_user: {e}")
        raise HTTPException(status_code=500, detail="Server error")


def facebook_login(data: dict):
    try:
        session = create_session()
        user_data = get_user_social_media(session, data["email"])

        if user_data is None:
            user_data = UserSocialMediaSerialized(
                name=data["name"],
                email=data["email"],
                social_media=True,
                social_media_name="Facebook",
            )
            user_data = create_social_media_user(session, user_data)

        token = generate_session_token(str(user_data.user_id), data["name"])
        return JSONResponse(
            content={"message": "Login success", "token": token}, status_code=201
        )

    except ValueError as ve:
        logging.error(f"Method create_new_user: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Method create_new_user: {e}")
        raise HTTPException(status_code=500, detail="Server error")


def capitalize_first_letter(word):
    return word.capitalize()
