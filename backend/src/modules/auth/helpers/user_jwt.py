import os
import uuid
from datetime import datetime, timedelta

from jose import jwt


def create_user_jwt(user_id: str, data: dict, secret: str) -> str:
    return jwt.encode({
        'iss': 'fai',
        'sub': user_id,
        'aud': 'fai',
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'iat': datetime.utcnow(),
        'jti': str(uuid.uuid4()),
        'data': data,
    }, secret, algorithm='HS256')


def verify_user_jwt(jwt_token: str, secret: str) -> dict:
    return jwt.decode(
        jwt_token,
        secret,
        algorithms=['HS256'],
        issuer='fai',
        audience='fai',
    )
