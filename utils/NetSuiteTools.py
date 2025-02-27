from requests_oauthlib import OAuth1
import requests
import json
class NetSuiteTools:
    def __init__(self):
        self.__consumer_key = "0ccadad2b3f1a0827b095a329868d3d16b36fbfc5acdddbb04ef6dbb5b5b35fd"
        self.__consumer_secret = "d1364aa4a1def3701cb68dde4589c50c7edf46994a62b949e68ff9934a4cb93c"
        self.__token_key = "d98165c84440d6abd0f13a2837a9abefabdd8bbe15b0f1df7bb367854a6c7099"
        self.__token_secret = "412f22a603e41ac2be58b67f7551f0f9534179d42bc285a5a4afb409fa763663"
        self.__realm = "11012044"
        self.__BASE_API_URL = "https://11012044.suitetalk.api.netsuite.com/services/rest/record/v1"
        
    def generate_auth(self):
        return OAuth1(self.__consumer_key, 
                      client_secret=self.__consumer_secret, 
                      resource_owner_key=self.__token_key, 
                      resource_owner_secret=self.__token_secret,
                      signature_method='HMAC-SHA256',
                      realm=self.__realm)
        
    def netsuite_request(self, method, endpoint, data=None):
        url = f"{self.__BASE_API_URL}/{endpoint}"
        auth = self.generate_auth()
        headers = {
            "Content-Type": "application/json",
            "prefer": "transient"
        }
        try:
            response = requests.request(method, url, auth=auth, headers=headers, data=json.dumps(data))
            if response.status_code == 200 or response.status_code == 204:
                location = response.headers.get("Location")
                if location:
                    loc = location.split("/")
                    id_journal = loc[-1]
                    print("Journal || journal creado con id:", id_journal)
                    return {
                        "success": True,
                        "status": response.status_code,
                        "data": f"https://11012044.app.netsuite.com/app/accounting/transactions/journal.nl?id={id_journal}&whence="
                    }
                else:
                    return {
                        "success": True,
                        "status": response.status_code,
                        "data": "No fue posible obtener el ID del Journal, verifica su creación en el siguiente link:\n https://11012044.app.netsuite.com/app/accounting/transactions/transactionlist.nl?Transaction_TYPE=Journal&whence="
                    }
            if response.status_code >= 400:
                return {
                    "success": False,
                    "status": response.status_code,
                    "message": response.text
                }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "status": 500,
                "message": str(e)
            }
        