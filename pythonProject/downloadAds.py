from serpapi import GoogleSearch
import json

params = {
  "engine": "google_ads_transparency_center",
  "advertiser_id": "AR03681116757440856065",
  "region": "2840",
  "political_ads": "true",
  "start_date": "20240901",
  "end_date": "20240909",
  "api_key": "051df811addc5cfd8771b4ec5f2eaea057115f51fcadb086a0a7b2ebc35b2e88"
}

search = GoogleSearch(params)
results = search.get_dict()
#ad_creatives = results["ad_creatives"]
print(results)
#print(ad_creatives)

with open("ads.json", "w") as outfile:
  json.dump(results, outfile)