import http.client
import os
from dotenv import load_dotenv
import  json
import psycopg2
import sys



if (not load_dotenv()):
    raise DOTENV_NOTFOUND

season = sys.argv[1]
if not int(season) :
    season = "2023"


conn_db = psycopg2.connect(database=os.getenv('DATANAME'),
                        host=os.getenv('HOST'),
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'),
                        port=os.getenv('PORT'))

if (not load_dotenv()):
    raise DOTENV_NOTFOUND

APIKEY = os.getenv('NBA_API_KEY')

conn_api = http.client.HTTPSConnection("api-nba-v1.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': APIKEY,
    'X-RapidAPI-Host': "api-nba-v1.p.rapidapi.com"
}

print(headers)
conn_api.request("GET", f"/games?season={season}", headers=headers)

res = conn_api.getresponse()
data = json.loads(res.read().decode("utf-8"))

cur = conn_db.cursor()


cur.execute("SELECT id from teams")
list_id_teams = cur.fetchall()
cur.execute("SELECT id from matchs")
list_id_games = cur.fetchall()

count = 0
for row in data['response'] :
    team_vis_id = row['teams']['visitors']['id']
    team_hom_id = row['teams']['home']['id']
    game_id = row['id']
    if ((team_vis_id,) in list_id_teams) and ((team_hom_id,) in list_id_teams) and not ((game_id,) in list_id_games):
        cur.execute("INSERT INTO matchs (id, date, home_team, away_team, status) VALUES (%s, %s, %s, %s, %s)",
                (
                    game_id,
                    row['date']['start'],
                    team_hom_id,
                    team_vis_id,
                    row['status']['short']
                )
            )
        count += 1


conn_db.commit()
print(f"{count} match(s) added for the season {season}")
cur.close()
conn_db.close()
