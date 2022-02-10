# Extract a users settings in ./config/config.json 
# Variablize every setting for individual use. 

import json

class AppSettings:
    def __init__(self):
        self.appsettings_file = './config/config.json'
        self.appsettings_dict = {}
        self.read_appsettingsjson()

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

if __name__ == '__main__':
    _app = AppSettings()
    settings_dict = _app.read_appsettingsjson()
    print("*** config.json contents ***")
    for k, v in settings_dict.items():
        print(f"{k} : {v}")
