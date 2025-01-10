import requests

url = 'https://graph.facebook.com/v21.0/ads_archive'

params = {
    "ad_reached_countries" : "US",
    "search_terms" : "trump",
    "ad_type ": "POLITICAL_AND_ISSUE_ADS",
    "access_token": "EAAZAWL2N19L0BOZBV8vAbxIdyVyMmfp2np0JZAREMEEHKf5hEwjIHZAMqmagJCJS2nksBCgAtZA74EEB7fUvivhOBTA9ITgpZCNubkRXNNXumSuijwho7hdLAGiGBZCtHBMXPULbApQjLgdKDJSoZAbQGalgg4ZBV0UvbitJskQO80wMz6zAZCKCq39RJWSVZC59PKzUUPqHrRhD3KsBvd55YROgAEz3PbDBCOqe5SwKnOd9oZCSvRsph65a9TfzBgMQjRJQ0OWZAuNAl41ZAc0ct3Ll8ZD"
}

response = requests.get(url, params=params)

print(response.text)