
from airflow.hooks.postgres_hook import PostgresHook
from airflow import DAG
from airflow.operators.bash import BashOperator
import datetime
import pendulum
from airflow.macros import ds_add
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

with DAG(
  dag_id ="import_next_week_games",
  schedule="0 0 * * 5",
  start_date=pendulum.datetime(2024, 2, 20, tz="UTC"),
  catchup=True,
  tags=["armagedon","daily","postgres"],
  default_args={"retries": 1 },
)as dag:
    def test_db_connection():
        postgres_hook = PostgresHook(postgres_conn_id='armagedon_db')
        conn  = postgres_hook.get_conn()
        conn.close()

    def import_games(**context):
        postgres_hook = PostgresHook(postgres_conn_id='armagedon_db')
        conn_db  = postgres_hook.get_conn()
        cur = conn_db.cursor()

        APIKEY = Variable.get('NBA_API_KEY')
        date_start = context['ds']


        conn_api = http.client.HTTPSConnection("api-nba-v1.p.rapidapi.com")

        headers = {
            'X-RapidAPI-Key': APIKEY,
            'X-RapidAPI-Host': "api-nba-v1.p.rapidapi.com"
        }
        cur.execute("SELECT id from teams;")
        list_id_teams = cur.fetchall()

        cur = conn_db.cursor()
        for i in range (0,7):

            date = ds_add(date_start,i)
            print(f"******** {date} ********")
            cur.execute(f"SELECT id from games WHERE date = '{date}' ;")
            list_id_games = cur.fetchall()

            conn_api.request("GET", f"/games?date={date}", headers=headers)
            res = conn_api.getresponse()
            data = json.loads(res.read().decode("utf-8"))

            count = 0
            for row in data['response'] :
                team_vis_id = row['teams']['visitors']['id']
                team_hom_id = row['teams']['home']['id']
                game_id = row['id']
                if ((team_vis_id,) in list_id_teams) and ((team_hom_id,) in list_id_teams) and not ((game_id,) in list_id_games):
                    cur.execute("INSERT INTO games (id, date, home_team, away_team, status, season, times_import_failed) VALUES (%s, %s, %s, %s, %s, %s, %s);",
                            (
                                game_id,
                                row['date']['start'],
                                team_hom_id,
                                team_vis_id,
                                row['status']['short'],
                                row['season'],
                                0
                            )
                        )
                    count += 1

            conn_db.commit()
            print(f"{count} match(s) added for the {date}")
        cur.close()
        conn_db.close()
    test_db_connection = PythonOperator(
        task_id='test_db_connection',
        python_callable=test_db_connection,
        dag=dag,
    )
    import_games = PythonOperator(
        task_id='import_games',
        python_callable=import_games,
        dag=dag,
    )
    test_db_connection >> import_games
