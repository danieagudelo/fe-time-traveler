from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = {"extend_existing": True, "schema": "sh_users"}

    id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    location_id = Column(Integer)
    user_id = Column(String)
    username = Column(String)
    text = Column(String)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    created = Column(String)


class CommentReaction(Base):
    __tablename__ = "comment_reactions"
    __table_args__ = {"extend_existing": True, "schema": "sh_users"}

    id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    comment_id = Column(Integer)
    user_id = Column(String, index=True)
    reaction_type = Column(String)
