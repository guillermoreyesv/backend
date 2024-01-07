from requests import request
import os

class BelvoManager():
    url_base: str = os.getenv('BELVO_URL_BASE', 'https://sandbox.belvo.com') 
    token: str = os.getenv('BELVO_TOKEN','ZDQ0ZTZkYTQtZDdhOS00OThmLWI3MWMtMzA3YTQ1NDY4NmJjOnlSMWdXMWVvR2N3RXFWeDkqI2FEUjVibVE2RUNXVVo1RmhkMyNtZm9jQWJoMzkjbl9ud2hhdDA2TkBHVlZAI3Y=')
    
    def get_users(self, page:int = 1):
        url = f"{self.url_base}/api/owners/?page={page}"
        headers = {
            'Authorization': f'Basic {self.token}'
        }
        response = request("GET", url, headers=headers)
        return response.json()