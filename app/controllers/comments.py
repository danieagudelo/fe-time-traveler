from fastapi import APIRouter, Query, status
from schemas.comments import CommentData, ReactComment
from services.comments import (
    save_comments,
    get_comment_by_location_id,
    react_to_comment,
)


router = APIRouter(
    tags=["Locations"],
    responses={201: {"description": "OK"}},
)


@router.get(
    "/comments",
    description="Get All comments by location id",
    status_code=status.HTTP_200_OK,
)
def get_comments(location_id: int = Query(..., description="Location ID")):
    return get_comment_by_location_id(location_id)


@router.post(
    "/comments",
    description="Create comment",
    status_code=status.HTTP_200_OK,
)
async def create_comment(comment: CommentData):
    return save_comments(comment)


@router.post(
    "/comments/react",
    description="React to comment",
    status_code=status.HTTP_200_OK
)
async def react_comment(react: ReactComment):
    return react_to_comment(react)
