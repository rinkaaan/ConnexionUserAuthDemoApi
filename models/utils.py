from sqlalchemy import URL, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.index import Base


def deserialize_body(model, body, fields=None):
    fields = fields or model.editable_fields
    body = {k: v for k, v in body.items() if k in fields}
    return model(**body)


def init_db(db_type, host):
    """
    :param db_type: sqlite, postgres
    :param host: localhost, hetzner
    :return: db session
    """
    if host == "localhost":
        host = "127.0.0.1"

    if db_type == "sqlite":
        url = URL.create(
            drivername="sqlite",
            database="demo.db"
        )
    elif db_type == "postgres":
        url = URL.create(
            drivername="postgresql+psycopg",
            username="yourUser",
            password="changeit",
            host=host,
            port=5432,
            database="postgres"
        )
    else:
        raise ValueError(f"db_type must be one of 'sqlite' or 'postgres', not {db_type}")

    engine = create_engine(url)
    session = scoped_session(
        sessionmaker(autoflush=False, bind=engine)
    )
    Base.query = session.query_property()
    Base.metadata.create_all(bind=engine)
    return session
