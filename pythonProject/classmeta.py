import requests
import csv
import pandas as pd
import json

class MetaAds():
    def __init__(self,params):
        self.params = params
        self.url = 'https://graph.facebook.com/v21.0/ads_archive'
    def get_ads(self):
        response = requests.get(self.url, params=self.params)
        response = response.json()
        with open("adsmeta.json", "w") as outfile:
            json.dump(response, outfile)
        return response
