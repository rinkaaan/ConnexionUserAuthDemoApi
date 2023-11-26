import os
from datetime import datetime

from connexion.exceptions import Unauthorized
from jose import jwt
from requests_oauthlib import OAuth2Session

from app import session
from models.index import User
from models.utils import deserialize_body

scope = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]
google = OAuth2Session(os.getenv("CLIENT_ID"), scope=scope, redirect_uri=os.getenv("REDIRECT_URI"))


def verify(body):
    body = body.decode('utf-8')
    try:
        id_token = google.fetch_token(os.getenv("TOKEN_URL"), client_secret=os.getenv("CLIENT_SECRET"), code=body)['id_token']
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


def decode_token(token):
    try:
        return jwt.decode(token, os.getenv("JWT_SECRET"))
    except Exception:
        raise Unauthorized
