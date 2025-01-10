import json
import urllib.request
from PIL import Image

# Opening JSON file
with open('ads.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)


ads = json_object["ad_creatives"]

for i in range(len(ads)):
    print(ads[i])
    if ads[i]["format"] == "text":
        try:
            print(ads[i]["image"])
        except:
            pass


