import logging
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import Union, Dict, Any

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.session import make_transient
from models.comment import Comment, CommentReaction
from schemas.comments import CommentData, ReactComment


def get_all_comments_by_local_id(db: Session, location_id: int):
    """
    Get All Comments by Local ID
    """
    return db.query(Comment).filter(Comment.location_id == location_id).order_by(desc(Comment.created)).all()


def create_comment(db: Session, comment: CommentData):
    """
    Create Comment
    """
    obj_in_data = jsonable_encoder(comment)
    comment = Comment(**obj_in_data)

    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_all_comments_by_id(db: Session, comment_id: int):
    """
    Get Comments by ID
    """
    return db.query(Comment).filter(Comment.id == comment_id).first()


def get_react_comment(db: Session, user_id: str, comment_id: int):
    """
    React to comment
    """
    return (
        db.query(CommentReaction)
        .filter(
            CommentReaction.user_id == user_id, CommentReaction.comment_id == comment_id
        )
        .first()
    )


def create_reaction(db: Session, react: ReactComment):
    """
    Create Reaction
    """
    obj_in_data = jsonable_encoder(react)
    react = CommentReaction(**obj_in_data)

    db.add(react)
    db.commit()
    db.refresh(react)
    return react


def update_react(db: Session, comment_id: int, user_id: str, obj_reaction: CommentReaction):
    """
    Update Reaction
    """
    try:
        db_react = db.query(CommentReaction).filter(
            CommentReaction.user_id == user_id, CommentReaction.comment_id == comment_id
        ).first()

        if not db_react:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "Reaction does not exist"},
            )

        obj_react_data = obj_reaction.__dict__

        db.expunge(db_react)
        make_transient(db_react)

        for field, value in obj_react_data.items():
            setattr(db_react, field, value)

        db_react = db.merge(db_react)

        db.commit()
        db.refresh(db_react)
        return db_react
    except Exception as ex:
        db.rollback()
        logging.error(f"function: update_react => {ex}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": str(ex) + " function: update_react"},
        )
    finally:
        db.close()


def update_react_comment(db: Session, comment_id: int, obj_comment: Comment):
    """
    Update Comment Reaction in Comment table
    """
    try:
        db_comment = db.query(Comment).filter(Comment.id == comment_id).first()

        if not db_comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "update_react_comment"},
            )

        obj_comment_data = obj_comment.__dict__

        for field, value in obj_comment_data.items():
            setattr(db_comment, field, value)

        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    except Exception as ex:
        db.rollback()
        logging.error(f"function: update_react_comment => {ex}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": str(ex) + " function: update_react_comment"},
        )

    finally:
        db.close()
