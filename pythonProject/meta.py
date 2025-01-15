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
    "access_token": "EAAZAWL2N19L0BOyqR8ZBXmwl4OtrdNgqumqrSXZCJDJ6iuyAsHXzNlb4V1YrUrTsrDKOSPDe10pRdZC5tmGQ3ZB1EX2nJzZBEDGeZAGx3v73np36yxqBKlBJZALc5Up3Mtidd3Tq4W2lDWhHE4cE69moTRqMlPEb50fXFZB3nV4CNqxz3mZBZAh7euOHwIV1PsSq81WLqdaAQSP7P8juGZBGZC72vZBhAzTt5egbLjuO2t8yciHtFrf1GgOsF6XoXtuUQk2M6PE9ju4SxJlZC8g6y7nhxWt",

}
a = MetaAds(params)
print(a.get_ads())