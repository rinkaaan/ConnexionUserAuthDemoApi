import os
from datetime import datetime

from connexion.exceptions import Unauthorized
from jose import jwt

from api.app import session
from api.resources.auth.utils import oauth
from api.resources.user.model import User
from nguylinc_python_utils.sqlalchemy import deserialize_body


def verify(body):
    body = body.decode('utf-8')
    try:
        id_token = oauth.fetch_token(os.getenv("GOOGLE_OAUTH_TOKEN_URL"), client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"), code=body)['id_token']
        id_token = jwt.decode(id_token, key=None, options={
            "verify_signature": False,
            "verify_aud": False,
            "verify_at_hash": False,
        })
    except Exception:
        raise Unauthorized

    user = session.query(User).filter(User.email == id_token["email"]).one_or_none()

    if not user:
        user = deserialize_body(User, id_token, fields=User.google_fields)
        user.created_at = datetime.now()
        session.add(user)
    else:
        new_user = deserialize_body(User, id_token, fields=User.google_fields)
        session.query(User).filter(User.id == user.id).update(new_user.dump())

    session.commit()
    token = user.generate_token()

    return token
