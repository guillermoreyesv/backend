from requests import request
import os

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
    
    def get_transactions(self, page:int = 1, user:str = "", info:bool = False):
        method = 'GET'
        url = f"{self.url_base}/api/transactions/"
        params = f"?page={page}&link={user}"
        params_dict = {"page": page, "link": user}
        headers = {
            'Authorization': f'Basic {self.token}'
        }

        if info:
            return {"method": method, "url": url,"params":params, "params_dict":params_dict}
        else:
            #Transacciones vinculadas a un usuario
            response = request(method, url+params, headers=headers)
            return response