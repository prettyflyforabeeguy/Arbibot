# Retrieve the credentials and needed URIs from the creds.json

from datetime import datetime, timezone
import hashlib
import hmac
import time
import json
import api_client as _api

class Creds:
    def __init__(self):
        self.creds_file = "./config/creds.json"
        self.creds_dict = {}
        self.read_credsjson()
        self.headers = {}
        self.header2 = {}

    def read_credsjson(self):
        try:
            with open(self.creds_file) as data_file:
                creds = json.load(data_file)
                self.creds_dict = creds
        except Exception as e:
            print(f"There was an error reading credentials from: {self.creds_file}")

    def get_key(self) -> str:
        return self.creds_dict["Cpatexapi_key"]

    def get_secret(self) -> str:
        return self.creds_dict["Cpatexapi_secret"]
    
    def get_endpoint(self) -> str:
        return self.creds_dict["Cpatexendpoint"]

    def get_cmckey(self) -> str:
        return self.creds_dict["CMCKey"]

    def get_timestamp(self) -> str:
        apiTimeStamp = str(int(time.time() * 1000))
        return apiTimeStamp

    def build_authentication(self, method, uri, api_key, api_secret, query1, query2) -> str:
        self.headers= {}
        #cpatex_timezone = pytz.timezone("America/Argentina/ComodRivadavia")
        #apiTimeStamp = str(int(datetime.datetime.now(cpatex_timezone).timestamp() * 1000)) #Create the timestamp ourselves
        apiTimeStamp = _api.APIClient().timestamp("GET") * 1000 #Get the timestamp directly from cpatex.

        if uri == "/api/v2/orders":
            preSign = method + "|" + uri + "|" + "access_key=" + api_key + query1 + "&tonce=" + str(apiTimeStamp) + query2
            #print(f"PreSIGN: {preSign}")

        else:
            preSign = method + "|" + uri + "|" + "access_key=" + api_key + query1 + "&tonce=" + str(apiTimeStamp)

        api_signature = hmac.new(api_secret, preSign.encode(), hashlib.sha256).hexdigest()
        # It appears that C-PateX doesn't require headers currently?
        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded'
            }

        self.headers = headers
        return api_signature, str(apiTimeStamp)


if __name__ == '__main__':
    app = Creds()
    #_api = APIClient()
    #apikey = Creds().get_key()
    #apisecret = Creds().get_secret()
    #apisecret = bytes(apisecret, encoding='utf-8')
    #endpoint = Creds().get_endpoint()

