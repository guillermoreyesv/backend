from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from models.user import User
from config.mysql import MySQLDBSingleton
from config.passwords import PasswordManager

router = APIRouter()
class UserAPI(BaseModel):
    email: EmailStr
    password: str

@router.post("/")
def login(user: UserAPI):
    try:
        engine = MySQLDBSingleton().get_database()
        with Session(engine) as session:
            result = User.user_exists(session, user.email)
            if not result:
                response = {'message': f'user {user.email} not found'}
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)
            
            verify = PasswordManager().verify_password(plain_password=user.password, hashed_password=result.password)
            if not verify:
                response = {'message':f"User {str(login.email)} not found"}
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)
            
            payload = {
                "id": str(result.id)
            }

            return JSONResponse(status_code=status.HTTP_200_OK, content=payload)
            
    except Exception as e:
        print(e)
        response = {"message": "Can't connect to database or start a session"}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response)