import http.client
import os
from dotenv import load_dotenv
import  json
import psycopg2
from tqdm import tqdm


def set_games_KO(game_id, cur):
    cur.execute(f"""UPDATE games
        SET status = 4
    WHERE id={game_id};""")
    print('game cleanse')

def add_games_stats(game_id, team_id, stats, cur):
    cur.execute("""INSERT INTO stats (
      game_id,
      team_id,
      "fastBreakPoints",
      "pointsInPaint",
      "biggestLead",
      "secondChancePoints",
      "pointsOffTurnovers",
      "longestRun",
      points,
      fgm,
      fga,
      fgp,
      ftm,
      fta,
      ftp,
      tpm,
      tpa,
      tpp,
      "offReb",
      "defReb",
      "totReb",
      assists,
      "pFouls",
      steals,
      turnovers,
      blocks,
      "plusMinus")
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
            (
              game_id,
              team_id,
              stats['fastBreakPoints'],
              stats['pointsInPaint'],
              stats['biggestLead'],
              stats['secondChancePoints'],
              stats['pointsOffTurnovers'],
              stats['longestRun'],
              stats['points'],
              stats['fgm'],
              stats['fga'],
              stats['fgp'],
              stats['ftm'],
              stats['fta'],
              stats['ftp'],
              stats['tpm'],
              stats['tpa'],
              stats['tpp'],
              stats['offReb'],
              stats['defReb'],
              stats['totReb'],
              stats['assists'],
              stats['pFouls'],
              stats['steals'],
              stats['turnovers'],
              stats['blocks'],
              stats['plusMinus'],)
        )

def get_games(cur):
    cur.execute("SELECT id, home_team, away_team, status from games;")
    return cur.fetchall()

def get_stats(cur):
    cur.execute("SELECT game_id, team_id from stats;")
    return cur.fetchall()


if __name__ == "__main__":
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

    cur = conn_db.cursor()

    list_games = get_games(cur)
    list_stats = get_stats(cur)

    count = 0

    for game in tqdm(list_games):
    # for game in list_games:
        game_id, home_team, away_team, status = game
        if status != 3:
            continue
        if (game_id, home_team, ) in list_stats and (game_id, away_team, ) in list_stats:
            continue
        conn_api.request("GET", f"/games/statistics?id={game_id}", headers=headers)
        res = conn_api.getresponse()
        if res.status != 200:
            print(res.status, res.reason)
            break
        data = json.loads(res.read().decode("utf-8"))['response']
        if isinstance(data,bool) or len(data) != 2:
            print(f" [ERROR]: GAME_ID: {game_id} invalid data format: \n {data}")
            set_games_KO(game_id, cur)
            continue
        if not (game_id, home_team, ) in list_stats:
            team_index = 0 if data[0]['team']['id'] == home_team else 1
            add_games_stats(game_id, home_team, data[team_index]['statistics'][0], cur)
            count +=1

        if not (game_id, away_team, ) in list_stats:
            team_index = 0 if data[0]['team']['id'] == away_team else 1
            add_games_stats(game_id, away_team, data[team_index]['statistics'][0], cur)
            count += 1




    conn_db.commit()
    print(f"{count} stats(s) added")
    cur.close()
    conn_db.close()
