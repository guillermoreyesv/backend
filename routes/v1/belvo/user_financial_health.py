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


@router.get("/user_financial_health")
def user_financial_health(page: Annotated[int, 1], user: Annotated[str, ""], token: Annotated[str, Depends(oauth2_scheme)]):
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
            response_belvo = BelvoManager().get_transactions(page, user, session)
            
            page_transactions = len(response_belvo['results'])

            # Find total pages
            if response_belvo['next']:
                # Normal page
                pages = round( int(response_belvo['count']) / page_transactions )
            else:
                # Last page
                previous = str(response_belvo['previous'])
                index = previous.find('page=')
                pages = previous[index:len(previous)]
                pages = int(pages.replace("page=","")) + 1
            
            inflow = 0
            outflow = 0
            details = {}
            for result in response_belvo['results']:
                title = result['type']
                if title == 'INFLOW':
                    inflow += result['amount']
                elif title == 'OUTFLOW':
                    outflow += result['amount']

                if title in details:
                    details[title].append(result)
                else:
                    details[title] = [result]

            total_details = len(details)
            subtotal = inflow - outflow
            health = True if subtotal > 0 else False
            results = {
                "pages": pages,
                "total_transactions": response_belvo['count'],
                "page_transactions": page_transactions,
                "total_categories": total_details,
                "transactions_info": {
                    "INFLOW": inflow,
                    "OUTFLOW": outflow,
                    "subtotal": subtotal,
                    "Health": health,
                },
                "details": details
            }

            session.commit()
            response = {"message": "ok", "results":results}
            return JSONResponse(status_code=status.HTTP_200_OK, content=response)
        
    except Exception as e:
        print('error:',e)
        response = {"message": "Can't connect to database or start a session"}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response)