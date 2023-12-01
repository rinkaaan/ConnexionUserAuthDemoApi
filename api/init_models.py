from sqlalchemy.orm import declarative_base

Base = declarative_base()

from api.resources.user.model import User
