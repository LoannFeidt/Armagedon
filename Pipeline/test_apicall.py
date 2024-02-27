import http.client
import os
from dotenv import load_dotenv

if (not load_dotenv()):
    raise DOTENV_NOTFOUND


APIKEY = os.getenv('NBA_API_KEY')

conn = http.client.HTTPSConnection("api-nba-v1.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': APIKEY,
    'X-RapidAPI-Host': "api-nba-v1.p.rapidapi.com"
}

print(headers)
conn.request("GET", "/teams", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
