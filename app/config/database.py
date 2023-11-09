import os

import settings
import sqlalchemy
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def create_session():
    enviroments_vars = settings.Settings()
    connection_name = enviroments_vars.CONNECTION_NAME
    db_socket_dir = enviroments_vars.DB_SOCKET_DIR
    db_name = enviroments_vars.DB_NAME
    username = enviroments_vars.USERNAME
    password = enviroments_vars.PASSWORD
    db_port = enviroments_vars.DB_PORT
    db_host = enviroments_vars.DB_HOST

    if os.getenv("MACHINE") == "DEV":
        engine = create_engine(
            sqlalchemy.engine.url.URL(
                drivername="postgresql+pg8000",
                username=username,
                password=password,
                host=db_host,
                port=db_port,
                database=db_name,
            ),
            poolclass=NullPool,
        )
    else:
        url = sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=username,
            password=password,
            database=db_name,
        )
        url.query["unix_sock"] = "{}/{}/.s.PGSQL.5432".format(
            db_socket_dir, connection_name
        )
        engine = create_engine(url)

    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    return session
