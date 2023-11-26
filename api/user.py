from app import session
from models.index import User


def get(user, token_info):
    q: User = session.query(User).filter(User.id == user).one_or_none()
    print(q.email)
    return q.dump()
