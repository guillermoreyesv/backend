from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session

from models.users_roles import UsersRoles
from config.mysql import MySQLDBSingleton
from config import tokens
from config.belvo import BelvoManager

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/login")


@router.get("/user_list")
def user_list(page: Annotated[int, 1], token: Annotated[str, Depends(oauth2_scheme)]):
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
            
            #CONSUMO BELVO
            response_belvo = BelvoManager().get_users(page)
            session.commit()
            response = {"message": "ok", "results":response_belvo}
            return JSONResponse(status_code=status.HTTP_200_OK, content=response)
        
    except Exception as e:
        print(e)
        response = {"message": "Can't connect to database or start a session"}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response)