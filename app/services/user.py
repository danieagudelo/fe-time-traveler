import logging
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from config.database import create_session
from services.passwords import hash_password
from services.passwords import verify_password
from repositories.user import create_user, get_user, get_user_login
from services.session_token import generate_session_token
from schemas.user_signup import LoginUserData, UserDataSerialized, CreateUserData


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logging.StreamHandler()],
)


def create_new_user(user: CreateUserData):
    try:
        session = create_session()
        user_data = get_user(session, user.email)

        if user_data:
            return JSONResponse(
                content={"message": "User already exists", "token": None},
                status_code=409,
            )
        new_user = UserDataSerialized(
            name=user.name, email=user.email, password=hash_password(user.password)
        )
        user = create_user(session, new_user)
        token = generate_session_token(str(user.user_id), user.name)

        return JSONResponse(
            content={"message": "Register success", "token": token}, status_code=201
        )
    except ValueError as ve:
        logging.error(f"Method create_new_user: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Method create_new_user: {e}")
        raise HTTPException(status_code=500, detail="Server error")


def login_user(user: LoginUserData):
    try:
        session = create_session()
        user_data = get_user_login(session, user.email)

        if user_data is None:
            return JSONResponse(content={"message": "User not found"}, status_code=404)

        if verify_password(user.password, user_data.password):
            token = generate_session_token(str(user_data.user_id), user_data.name)
            return JSONResponse(
                content={"message": "Login success", "token": token}, status_code=201
            )
        else:
            return JSONResponse(
                content={"message": "Not authorize", "token": None}, status_code=401
            )
    except ValueError as ve:
        logging.error(f"Method create_new_user: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Method create_new_user: {e}")
        raise HTTPException(status_code=500, detail="Server error")
