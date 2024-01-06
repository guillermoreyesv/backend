from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from models.user import User
from config.mysql import MySQLDBSingleton

router = APIRouter()
class UserAPI(BaseModel):
    email: EmailStr
    password: str
    name: str
    lastname: str

@router.post("/")
def register_new_user(user: UserAPI):
    try:
        engine = MySQLDBSingleton().get_database()
        with Session(engine) as session:
            result = User.user_exists(session, user.email)
            if result:
                response = {'message': f'user {user.email} already exists'}
                return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content=response)
            
            user.password = hash_password(user.password)
            new_user = User(
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