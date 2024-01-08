from requests import request
import os

from models.belvo_endpoints import BelvoEndpoints

class BelvoManager():
    url_base: str = os.getenv('BELVO_URL_BASE', 'https://sandbox.belvo.com') 
    token: str = os.getenv('BELVO_TOKEN','ZDQ0ZTZkYTQtZDdhOS00OThmLWI3MWMtMzA3YTQ1NDY4NmJjOnlSMWdXMWVvR2N3RXFWeDkqI2FEUjVibVE2RUNXVVo1RmhkMyNtZm9jQWJoMzkjbl9ud2hhdDA2TkBHVlZAI3Y=')
    
    def get_users(self, page:int = 1):
        #Cuentas
        url = f"{self.url_base}/api/owners/?page={page}"
        headers = {
            'Authorization': f'Basic {self.token}'
        }
        response = request("GET", url, headers=headers)
        return response
    
    def get_transactions(self, page:int = 1, user:str = "", session=None):
        # REQUEST INFO
        method = 'GET'
        url = f"{self.url_base}/api/transactions/"
        headers = {
            'Authorization': f'Basic {self.token}'
        }

        params = f"?page={page}&link={user}"
        params_dict = {"page": page, "link": user}
        
        full_url = url + params
        code = 200

        # LOCAL INFO (BD)
        local_results = BelvoEndpoints.find_endpoint_today(session, method, full_url, code)
        
        if local_results:
                response_belvo = local_results.response
                return response_belvo

        else:
            # NOT FIND LOCAL INFO, REQUESTING NEW INFO.
            response_belvo = request(method, full_url, headers=headers)
            response_belvo_json = response_belvo.json()

            # SAVING NEW INFO IN DB
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

            return response_belvo_json

        