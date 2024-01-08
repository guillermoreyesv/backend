from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session

from models.users_roles import UsersRoles
from models.belvo_endpoints import BelvoEndpoints

from config.mysql import MySQLDBSingleton
from config import tokens
from config.belvo import BelvoManager


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/login")


@router.get("/user_transactions")
def user_transactions(page: Annotated[int, 1], user: Annotated[str, ""], token: Annotated[str, Depends(oauth2_scheme)]):
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
            # BUSCAMOS EN LA BD:
            response_belvo = BelvoManager().get_transactions(page, user, True)
            method = response_belvo['method']
            params = response_belvo['params']
            params_dict = response_belvo['params_dict']
            url = response_belvo['url']
            full_url = url + params
            code = '200'
            local_results = BelvoEndpoints.find_endpoint_today(session, method, full_url, code)

            if local_results:
                response_belvo = local_results.response
            else:
                # SI NO ESTA EN LA BD, OBTENEMOS Y ACTUALIZAMOS.
                response_belvo = BelvoManager().get_transactions(page, user, False)
                response_belvo_json = response_belvo.json()

                # UPDATE DB
                new_belvo_endpoint = BelvoEndpoints(
                    type = method,
                    url = url,
                    params = params_dict,
                    code = response_belvo.status_code,
                    full_url = full_url,
                    response = response_belvo_json
                )
                session.add(new_belvo_endpoint)
                session.commit()
                response_belvo = response_belvo_json

            session.commit()
            response = {"message": "ok", "results":response_belvo}
            return JSONResponse(status_code=status.HTTP_200_OK, content=response)
        
    except Exception as e:
        print(e)
        response = {"message": "Can't connect to database or start a session"}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response)