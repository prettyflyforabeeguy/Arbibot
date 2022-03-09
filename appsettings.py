# Extract a users settings in ./config/config.json 
# Variablize every setting for individual use. 

import json

class AppSettings:
    def __init__(self):
        self.appsettings_file = './config/config.json'
        self.appsettings_dict = {}
        self.read_appsettingsjson()

         #self.crexPairs = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "CrexTradePairs")
        #self.xeggexPairs = _appsettings.AppSettings().appsetting_vsearch(self.appsettings_dict, "XeggexTradePairs")
        #self.pairsList = []

    def read_appsettingsjson(self):
        try:
            with open(self.appsettings_file) as data_file:
                appsettings = json.load(data_file)
                self.appsettings_dict = appsettings
                return self.appsettings_dict
        except Exception as e:
            print(f"There was an error reading appsettings from: {self.appsettings_file}") 
            print(e)

    def appsetting_vsearch(self, dict, key):
        for k, v in dict.items():
            if k == key:
                return v
        else:
            return None    

    def get_unique_trade_pairs(self):
        appsettings_dict = self.read_appsettingsjson()
        coin = self.appsetting_vsearch(appsettings_dict, "Coin")
        cpatexEnabled = self.appsetting_vsearch(appsettings_dict, "CpatexEnabled")
        cpatexPairs = self.appsetting_vsearch(appsettings_dict, "CpatexTradePairs")
        crex24Enabled = self.appsetting_vsearch(appsettings_dict, "Crex24Enabled")
        crexPairs = self.appsetting_vsearch(appsettings_dict, "CrexTradePairs")
        xeggexEnabled = self.appsetting_vsearch(appsettings_dict, "XeggexEnabled")
        xeggexPairs = self.appsetting_vsearch(appsettings_dict, "XeggexTradePairs")
        pairsList = []

        if cpatexEnabled == True:
            for each_pair in cpatexPairs:
                clenght = len(coin)
                c = each_pair[clenght:]
                c = c.upper()
                pairsList.append(c)

        if crex24Enabled == True:
            for each_pair in crexPairs:
                clenght = len(coin) + 1
                c = each_pair[clenght:]
                c = c.upper()
                pairsList.append(c)
        
        if xeggexEnabled == True:
            for each_pair in xeggexPairs:
                clenght = len(coin) + 1
                c = each_pair[clenght:]
                c = c.upper()
                pairsList.append(c)   

        unique_pairs = list(set(pairsList)) 
        return unique_pairs


if __name__ == '__main__':
    _app = AppSettings()
    settings_dict = _app.read_appsettingsjson()
    print("*** config.json contents ***")
    for k, v in settings_dict.items():
        print(f"{k} : {v}")

    unique_pairs = _app.get_unique_trade_pairs()
    print(f"Unique trade pairs: {unique_pairs}")