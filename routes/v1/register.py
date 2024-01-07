from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from models.users import Users
from models.users_roles import UsersRoles
from config.mysql import MySQLDBSingleton
from config import tokens

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/login")
class UserAPI(BaseModel):
    email: EmailStr
    password: str
    name: str
    lastname: str
    role_id: int

@router.post("/register")
def register_new_user(user: UserAPI, token: Annotated[str, Depends(oauth2_scheme)]):
    user_info = {}
    try:
        #Validamos token
        user_info = tokens.decode(token)
    except:
        response = {'message': f'Invalid token'}
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content=response)

    try:
        engine = MySQLDBSingleton().get_database()
        with Session(engine) as session:
            #Validamos permisos
            resultUserRole = UsersRoles.find_user_role(session, user_info['id'], 1)
            if not resultUserRole:
                response = {'message': f'You don\'t have the right role'}
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response)
            
            result = Users.user_exists(session, user.email)
            if result:
                response = {'message': f'user {user.email} already exists'}
                return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content=response)
            
            user.password = hash_password(user.password)
            new_user = Users(
                email= user.email,
                password= user.password,
                name= user.name,
                lastname= user.lastname
            )
            session.add(new_user)
            session.commit()
    except Exception as e:
        print(e)
        response = {"message": "Can't connect to database or start a session"}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response)

    return {"message": "User registered successfully", "user_data": user}

def hash_password(password: str):
    from config.passwords import PasswordManager
    password = PasswordManager().hash_password(password)
    return password