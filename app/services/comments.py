import logging
from fastapi import HTTPException
from schemas.comments import CommentData, ReactComment
from fastapi.responses import JSONResponse
from config.database import create_session
from fastapi.encoders import jsonable_encoder
from repositories.comments import (
    create_comment,
    get_all_comments_by_local_id,
    get_react_comment,
    update_react_comment,
    get_all_comments_by_id,
    update_react,
    create_reaction,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logging.StreamHandler()],
)


def get_comment_by_location_id(location_id: int):
    try:
        session = create_session()
        comments = get_all_comments_by_local_id(session, location_id)
        encoded_comments = jsonable_encoder(comments)
        return JSONResponse(content=encoded_comments, status_code=201)
    except ValueError as ve:
        logging.error(f"Method create_new_user: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Method get_comment_by_location_id: {e}")
        raise HTTPException(status_code=500, detail="Server error")


def save_comments(comment: CommentData):
    try:
        session = create_session()
        comment = create_comment(session, comment)
        encoded_comments = jsonable_encoder(comment)
        return JSONResponse(content=encoded_comments, status_code=201)
    except ValueError as ve:
        logging.error(f"Method create_new_user: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Method save_comments: {e}")
        raise HTTPException(status_code=500, detail="Server error")


def react_to_comment(react: ReactComment):
    try:
        session = create_session()
        react_data = get_react_comment(session, react.user_id, react.comment_id)
        comment_data = get_all_comments_by_id(session, react.comment_id)

        if react_data is not None:
            if react.reaction_type != react_data.reaction_type:
                if react.reaction_type == "like":
                    comment_data.likes += 1
                    comment_data.dislikes -= 1
                elif react.reaction_type == "dislike":
                    comment_data.likes -= 1
                    comment_data.dislikes += 1

                comment = update_react_comment(session, react.comment_id, comment_data)

                react_data.reaction_type = react.reaction_type
                react = update_react(
                    session, react.comment_id, react.user_id, react_data
                )

                encoded_comments = jsonable_encoder(comment)
                return JSONResponse(content=encoded_comments, status_code=201)
            else:
                encoded_comments = jsonable_encoder(comment_data)
                return JSONResponse(content=encoded_comments, status_code=201)

        else:
            react = create_reaction(session, react)
            if react.reaction_type == "like":
                comment_data.likes += 1
            elif react.reaction_type == "dislike":
                comment_data.dislikes += 1

            comment = update_react_comment(session, react.comment_id, comment_data)

            encoded_comments = jsonable_encoder(comment)
            return JSONResponse(content=encoded_comments, status_code=201)

    except ValueError as ve:
        logging.error(f"Method react_to_comment: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Method react_to_comment: {e}")
        raise HTTPException(status_code=500, detail="Server error")
