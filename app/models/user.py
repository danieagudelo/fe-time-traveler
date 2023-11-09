import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, TIMESTAMP, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True, "schema": "sh_users"}

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(LargeBinary)
    social_media = Column(Boolean, default=False)
    social_media_name = Column(String)
    created = Column(
        TIMESTAMP(timezone=False), nullable=False, default=datetime.utcnow()
    )
    updated = Column(
        TIMESTAMP(timezone=False), nullable=False, default=datetime.utcnow()
    )
    token = Column(String, unique=True, index=True)
