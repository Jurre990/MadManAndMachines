import requests

url = 'https://graph.facebook.com/v21.0/ads_archive'

params = {
    "ad_reached_countries": "all",
    "access_token": "EAAZAWL2N19L0BOxi40HzBNwKZC2ii5eT7hcZCo952P9eLRwJ2ALaC88TWM3Hfb0cZAcYHEKwSE7oek8QFUup6nMQ9b5v9tNrPUTJgqkgZCD3FvS60rwUrdsVh8v6pQe8UsUPCZAyA9rCBE977urcsYush6Ugslv4ROXb516XCD3FDoCW2MKz86njhKhsiQrZCodPgAbcRY1Ih577NuGUmlRksSQOKGxXth0lEFkqpqoBAZDZD"
}

response = requests.get(url, params=params)

print(response.text)