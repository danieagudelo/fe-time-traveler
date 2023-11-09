from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, Integer

Base = declarative_base()


class Location(Base):
    __tablename__ = "location"
    __table_args__ = {"extend_existing": True, "schema": "sh_users"}

    id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    lat = Column(String)
    lng = Column(String)
    title = Column(String)
    text = Column(String)
    images = Column(ARRAY(String))
    created = Column(
        TIMESTAMP(timezone=False), nullable=False, default=datetime.utcnow()
    )
    updated = Column(
        TIMESTAMP(timezone=False), nullable=False, default=datetime.utcnow()
    )
