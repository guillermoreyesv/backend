from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response as Resp
from pydantic import BaseModel, EmailStr, Field
from models.user import User
from config.mysql import MySQLDBSingleton
from sqlalchemy.orm import Session

router = APIRouter()
class UserAPI(BaseModel):
    email: EmailStr
    password: str
    name: str
    lastname: str

@router.post("/")
def register_new_user(user: UserAPI):
    #user_data = user.model_dump()
    try:
        engine = MySQLDBSingleton().get_database()
        with Session(engine) as session:
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
        response = {"message": "Can't connect to database or start a session"}
        print(e)
        #return JSONResponse(status_codem=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response)

    return {"message": "User registered successfully", "user_data": user}

def hash_password(password: str):
    from config.passwords import PasswordManager
    password_manager = PasswordManager()
    password = password_manager.hash_password(password)
    return password

def validate(user = {}):
    
    return user