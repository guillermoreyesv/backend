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

def decode(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    expire_str = payload.get('expire')
    
    if expire_str:
        expire = datetime.datetime.strptime(expire_str, '%Y-%m-%d %H:%M:%S.%f')
        
        if expire <= datetime.datetime.utcnow():
            raise jwt.ExpiredSignatureError('El token ha expirado')
    return payload