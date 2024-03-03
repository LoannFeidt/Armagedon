
from airflow.hooks.postgres_hook import PostgresHook
from airflow import DAG
from airflow.operators.bash import BashOperator
import datetime
import pendulum
from airflow.operators.python import (
    ExternalPythonOperator,
    PythonOperator,
    PythonVirtualenvOperator,
    is_venv_installed,
)
from airflow.models import Variable
import requests
import  json
import http.client
from airflow.models.taskinstance import TaskInstance

def set_games_finish(game_id, cur):
    cur.execute(f"""UPDATE games
        SET status = 3
        WHERE id={game_id};""")
    return

def set_games_KO(game_id, cur):
    cur.execute(f"""UPDATE games
        SET times_import_failed = times_import_failed + 1
    WHERE id={game_id};""")

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


with DAG(
  dag_id ="import_missing_stats",
  schedule="@weekly",
  start_date=pendulum.datetime(2024, 2, 20, tz="UTC"),
  catchup=True,
  tags=["armagedon","weekly","postgres"],
  default_args={"retries": 1 },
)as dag:
    def test_db_connection():
        postgres_hook = PostgresHook(postgres_conn_id='armagedon_db')

        conn  = postgres_hook.get_conn()
        conn.close()

    def import_missed_games(**context):
        ti: TaskInstance = context["task_instance"]
        max_retry = Variable.get('max_retry')

        postgres_hook = PostgresHook(postgres_conn_id='armagedon_db')
        conn  = postgres_hook.get_conn()

        cur = conn.cursor()
        cur.execute(f"""SELECT id, home_team, away_team, status
            FROM public.games
            WHERE status = 4 AND times_import_failed < {max_retry}
            """)
        print(f"""SELECT id, home_team, away_team, status
            FROM public.games
            WHERE status = 4 AND times_import_failed < {max_retry}
            """)
        values = cur.fetchall()
        ti.xcom_push(key="list_games",value= values)

    def import_missed_stats(**context):
        max_retry = Variable.get('max_retry')
        ti: TaskInstance = context["task_instance"]

        postgres_hook = PostgresHook(postgres_conn_id='armagedon_db')
        conn  = postgres_hook.get_conn()

        cur = conn.cursor()
        cur.execute(f"""SELECT game_id, team_id
            FROM stats
            INNER JOIN public.games ON game_id = games.id
            WHERE status = 4 AND times_import_failed < {max_retry}
            """)

        values = cur.fetchall()
        ti.xcom_push(key="list_stats",value= values)

    def push_missed_stats(**context):
        ti: TaskInstance = context["task_instance"]
        postgres_hook = PostgresHook(postgres_conn_id='armagedon_db')
        conn  = postgres_hook.get_conn()
        cur = conn.cursor()
        APIKEY = Variable.get('NBA_API_KEY')
        conn_api = http.client.HTTPSConnection("api-nba-v1.p.rapidapi.com")
        headers = {
            'X-RapidAPI-Key': APIKEY,
            'X-RapidAPI-Host': "api-nba-v1.p.rapidapi.com"
        }

        count_add = 0
        count_missing = 0
        list_stats = ti.xcom_pull(key="list_stats", task_ids="import_missed_stats")
        list_games = ti.xcom_pull(key="list_games", task_ids="import_missed_games")
        if not list_stats:
            list_stats =[(None, None, None)]
        if not list_games:
            list_games =[]
        for game in list_games:
            game_id, home_team, away_team, status = game
            print(game_id)
            if (game_id, home_team, ) in list_stats and (game_id, away_team, ) in list_stats:
                continue
            conn_api.request("GET", f"/games/statistics?id={game_id}", headers=headers)
            res = conn_api.getresponse()

            data = json.loads(res.read().decode("utf-8"))['response']
            if isinstance(data,bool) or len(data) != 2:
                set_games_KO(game_id, cur)
                count_missing += 1
                continue
            if not (game_id, home_team, ) in list_stats:
                team_index = 0 if data[0]['team']['id'] == home_team else 1
                add_games_stats(game_id, home_team, data[team_index]['statistics'][0], cur)
                count_add +=1

            if not (game_id, away_team, ) in list_stats:
                team_index = 0 if data[0]['team']['id'] == away_team else 1
                add_games_stats(game_id, away_team, data[team_index]['statistics'][0], cur)
                count_add += 1
            set_games_finish(game_id, cur)

        conn.commit()
        print(f"{count_add} stat(s) added")
        print(f"{count_missing} stat(s) missing   ")
        cur.close()
        conn.close()
    test_db_connection = PythonOperator(
        task_id='test_db_connection',
        python_callable=test_db_connection,
        dag=dag,
    )
    import_missed_games = PythonOperator(
        task_id='import_missed_games',
        python_callable=import_missed_games,
        dag=dag,
    )
    import_missed_stats = PythonOperator(
        task_id='import_missed__stats',
        python_callable=import_missed_stats,
        dag=dag,
    )
    push_missed_stats = PythonOperator(
        task_id='push_missed_stats',
        python_callable=push_missed_stats,
        dag=dag,
    )
    test_db_connection >> [import_missed_games, import_missed_stats] >> push_missed_stats
