import requests
from classmeta import MetaAds

keyword = "voter fraud"
end_date = ""
start_date = ""
media_type = "IMAGE"

params = {
    "ad_reached_countries" : "US",
    "ad_delivery_date_max": end_date,
    "ad_delivery_date_min": start_date,
    #"estimated_audience_size_min": 5000,
    "languages" : "en",
    "search_terms" : keyword,
    "media_type" : media_type,
    "ad_type ": "POLITICAL_AND_ISSUE_ADS",
    'unmask_removed_content' : "true",
    "access_token": "EAAZAWL2N19L0BO0z6rgYjCcCgENol9olalM280qwzvoKAYgbPWK20oVp7OfmEUvxGNiGt3kViy00zzZBbzpkxEHWclWuIPDxZAacZBdNFmfO4hqDeW5NmRiZA6aJs8kpfBFzuOTzZCQ8sUn8zM210MVSWnbWIZA1qTLZAG65PwQhNz0Lj5GZCoDiueZBbS0g2ILG8IEwXIhyc0NGzI1OsbOVx3GMI74uQlzumZB33755xZB7qaZARfHMWZCVMYZAtFl18U2ZCi5Nf0rarrzZAogZDZD",

}
a = MetaAds(params)
print(a.get_ads())