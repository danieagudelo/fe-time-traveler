from sqlalchemy.orm import Session
from models.location import Location
from schemas.location import LocationSchema
from fastapi.encoders import jsonable_encoder


def get_all_location(db: Session):
    """
    Get ALl locations
    """
    return db.query(Location).all()


def create_location(db: Session, location_obj: LocationSchema):
    """
    Create locations
    """

    obj_in_data = jsonable_encoder(location_obj)
    location = Location(**obj_in_data)

    db.add(location)
    db.commit()
    db.refresh(location)
    return location
