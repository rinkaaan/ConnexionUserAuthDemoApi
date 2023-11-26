import os
import uuid
import datetime

from jose import jwt
from sqlalchemy import Column, DateTime, UUID, ColumnElement, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseExtended:
    def dump(self):
        columns = [c.name for c in self.__table__.columns]
        return {k: v for k, v in vars(self).items() if k in columns}


class User(Base, BaseExtended):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    created_at: ColumnElement = Column(DateTime(), index=True)
    email = Column(Text())
    name = Column(Text())
    picture = Column(Text())
    given_name = Column(Text())
    family_name = Column(Text())
    locale = Column(Text())

    editable_fields = []
    google_fields = ["email", "name", "picture", "given_name", "family_name", "locale"]

    def generate_token(self):
        timestamp = datetime.now(datetime.UTC).timestamp()
        payload = {
            "iss": "com.nguylinc",
            "iat": int(timestamp),
            "sub": str(self.id),
        }

        return jwt.encode(payload, os.getenv("JWT_SECRET"))
