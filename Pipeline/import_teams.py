import http.client
import os
from dotenv import load_dotenv
import  json
import psycopg2

if (not load_dotenv()):
    raise DOTENV_NOTFOUND

conn_db = psycopg2.connect(database=os.getenv('DATANAME'),
                        host=os.getenv('HOST'),
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'),
                        port=os.getenv('PORT'))



APIKEY = os.getenv('NBA_API_KEY')

conn_api = http.client.HTTPSConnection("api-nba-v1.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': APIKEY,
    'X-RapidAPI-Host': "api-nba-v1.p.rapidapi.com"
}

conn_api.request("GET", "/teams", headers=headers)

res = conn_api.getresponse()
data = json.loads(res.read().decode("utf-8"))


cur = conn_db.cursor()
count = 0
for row in data['response'] :
    if row['nbaFranchise'] == True:
            cur.execute("INSERT INTO teams (id, name, abrev, logo, conference, division) VALUES (%s, %s, %s, %s, %s, %s);",
                (
                    row['id'],
                    row['name'],
                    row['code'],
                    row['logo'],
                    row['leagues']['standard']['conference'],
                    row['leagues']['standard']['division']
                )
            )
            count += 1

conn_db.commit()
print(f"{count} team(s) added")
cur.close()
conn_db.close()
