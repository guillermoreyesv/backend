import datetime
import jwt, os

SECRET_KEY = os.getenv("SECRET_KEY", "develop")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("EXPIRE", 60)


def encode(payload: dict):
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload['expire'] = str(expire)
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
