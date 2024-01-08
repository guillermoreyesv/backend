from requests import request
import os

from models.belvo_endpoints import BelvoEndpoints

class BelvoManager():
    url_base: str = os.getenv('BELVO_URL_BASE', 'https://sandbox.belvo.com') 
    token: str = os.getenv('BELVO_TOKEN','ZDQ0ZTZkYTQtZDdhOS00OThmLWI3MWMtMzA3YTQ1NDY4NmJjOnlSMWdXMWVvR2N3RXFWeDkqI2FEUjVibVE2RUNXVVo1RmhkMyNtZm9jQWJoMzkjbl9ud2hhdDA2TkBHVlZAI3Y=')
    
    def get_users(self, page:int = 1, session=None):
        #Cuentas
        method = 'GET'
        url = f"{self.url_base}/api/owners/"
        headers = {
            'Authorization': f'Basic {self.token}'
        }

        params = f"?page={page}"
        params_dict = {"page": page}

        code = 200

        return self.cache_manager(session, method, url, params, params_dict, headers, code)
    
    def get_transactions(self, page:int = 1, user:str = "", session=None):
        # REQUEST INFO
        method = 'GET'
        url = f"{self.url_base}/api/transactions/"
        headers = {
            'Authorization': f'Basic {self.token}'
        }

        params = f"?page={page}&link={user}"
        params_dict = {"page": page, "link": user}
        
        code = 200

        return self.cache_manager(session, method, url, params, params_dict, headers, code)

    def cache_manager(self, session, method, url, params, params_dict, headers, code):
        full_url = url + params

         # LOCAL INFO (BD)
        local_results = BelvoEndpoints.find_endpoint_today(session, method, full_url, code)
        
        if local_results:
            #print('cached')
            response_belvo = local_results.response
            return response_belvo

        else:
            # NOT FIND LOCAL INFO, REQUESTING NEW INFO.
            #print('updating', method, full_url, headers)
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