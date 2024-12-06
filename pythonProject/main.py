from serpapi import GoogleSearch

params = {
  "engine": "google_ads_transparency_center",
  "advertiser_id": "AR17828074650563772417",
  "region": "2840",
  "api_key": "051df811addc5cfd8771b4ec5f2eaea057115f51fcadb086a0a7b2ebc35b2e88"
}

search = GoogleSearch(params)
results = search.get_dict()
ad_creatives = results["ad_creatives"]
print(results)
print(ad_creatives)