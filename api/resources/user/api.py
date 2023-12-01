from api.app import session
from api.resources.user.model import User


def get(user, token_info):
    q: User = session.query(User).filter(User.id == user).one_or_none()
    print(q.email)
    return q.dump()
