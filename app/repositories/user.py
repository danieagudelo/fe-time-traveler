from models.user import User
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from schemas.user_signup import UserDataSerialized, UserSocialMediaSerialized


def create_user(db: Session, user: UserDataSerialized):
    """
    Create User
    """
    obj_in_data = jsonable_encoder(user)
    user = User(**obj_in_data)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_social_media_user(db: Session, user: UserSocialMediaSerialized):
    """
    Create Social Media User
    """
    obj_in_data = jsonable_encoder(user)
    user = User(**obj_in_data)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, email: str):
    """
    Get user by Email from user table
    """
    return db.query(User).filter(User.email == email).first()


def get_user_login(db: Session, email: str):
    """
    Get user by Email from user table
    """
    return (
        db.query(User).filter(User.email == email, User.social_media == False).first()
    )


def get_user_social_media(db: Session, email: str):
    """
    Get user by Email from social media users
    """
    return db.query(User).filter(User.email == email).first()
