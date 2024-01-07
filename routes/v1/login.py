from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models.users import Users
from config.mysql import MySQLDBSingleton
from config.passwords import PasswordManager
from config import tokens

router = APIRouter()

@router.post("/login")
def login(user: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        engine = MySQLDBSingleton().get_database()
        with Session(engine) as session:
            result = Users.user_exists(session, user.username)
            if not result:
                response = {'message': f'user {user.username} not found'}
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)
            
            verify = PasswordManager().verify_password(plain_password=user.password, hashed_password=result.password)
            if not verify:
                response = {'message':f"User {str(login.username)} not found"}
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)
            
            payload = {
                "id": str(result.id)
            }
            session.commit()

            token = tokens.encode(payload)
            response = {"access_token": token, "token_type": "bearer"}
            return JSONResponse(status_code=status.HTTP_200_OK, content=response)
            
    except Exception as e:
        print(e)
        response = {"message": "Can't connect to database or start a session"}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response)