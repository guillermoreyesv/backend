from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response as Resp
from pydantic import BaseModel

router = APIRouter()
class User(BaseModel):
    email: str
    password: str
    name: str
    lastname: str

@router.post("/")
def register_new_user(user: User):
    user_data = user.model_dump()
    user_data = validate(user_data)
    return {"message": "User registered successfully", "user_data": user_data}

def validate(user = {}):
    return user