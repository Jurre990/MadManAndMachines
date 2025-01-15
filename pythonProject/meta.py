import requests
from classmeta import MetaAds

keyword = "trump"
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
    "access_token": "EAAZAWL2N19L0BO9QEhoXr63TutGakM8qwQv1K1ygfDxEFHdpBQclqxMO53KRhCluZAhnbtRRYNzGEExAY7VRNxdFL97tNpGtlTPFDFiYTBLCM5D4T6XPRPKzwm0WaclaoLuw7gH52LnEqr8Lkqy0Tbn6qv9DiD70FZALFfMMUexZAYdCay15gZCficdxTvzN7hc1yZBdHpklqCbyaRkArOW1ZBggqZAxvYnAJvmNJUBW4qZCUzQBU2xZAfGbTmc05mZAbtCaXXX6UnKuUEZBGNdjfuwZD",

}
a = MetaAds(params)
print(a.get_ads())