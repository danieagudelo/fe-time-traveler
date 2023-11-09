import logging
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from config.database import create_session
from schemas.location import LocationSchema
from fastapi.encoders import jsonable_encoder
from repositories.location import create_location, get_all_location


def get_locations():
    try:
        session = create_session()
        location = get_all_location(session)

        encoded_comments = jsonable_encoder(location)
        return JSONResponse(content=encoded_comments, status_code=201)

    except ValueError as ve:
        logging.error(f"Method create_new_user: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Method create_new_user: {e}")
        raise HTTPException(status_code=500, detail="Server error")


def save_location(location_data: LocationSchema):
    try:
        session = create_session()
        location = create_location(session, location_data)

        encoded_comments = jsonable_encoder(location)
        return JSONResponse(content=encoded_comments, status_code=201)

    except ValueError as ve:
        logging.error(f"Method create_new_user: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Method create_new_user: {e}")
        raise HTTPException(status_code=500, detail="Server error")
