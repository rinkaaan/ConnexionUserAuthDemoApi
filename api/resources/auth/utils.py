import os

from connexion.exceptions import Unauthorized
from jose import jwt

from requests_oauthlib import OAuth2Session

scope = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]
oauth = OAuth2Session(os.getenv("GOOGLE_OAUTH_CLIENT_ID"), scope=scope, redirect_uri=os.getenv("GOOGLE_OAUTH_REDIRECT_URI"))


def decode_token(token):
    try:
        return jwt.decode(token, os.getenv("JWT_SECRET"))
    except Exception:
        raise Unauthorized
