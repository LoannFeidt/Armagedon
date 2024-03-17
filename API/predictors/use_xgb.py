import pandas as pd
from sqlalchemy import create_engine
from xgboost import XGBClassifier
import sys


xg2 = XGBClassifier()
xg2.load_model('./predictors/XGBmodel_name.json')

def streak(df_):
    df_ = df_.sort_values(by='date',ascending=False)
    val = 0 
    for _, row in df_.iterrows():
        if val == 0:
            result = row['win'] 
        if row['win'] != result:
            return val
        val += 1 if result else -1
    return val

def create_stats(df_):
    df_ = df_.sort_values(by='date')
    df_ = df_.drop(columns=["fastBreakPoints","pointsInPaint","biggestLead","secondChancePoints","pointsOffTurnovers","longestRun"])
    df_['home_team'] = df_['team_id']==df_['home_team']
    df_['win'] = df_['plusMinus']> 0 
    df_['win_home'] = df_['home_team'] & df_['win']
    df_['win_away'] = (-df_['home_team']) & df_['win']
    df_['nb_games'] = df_["game_id"].count()

    for col in df_.drop(columns=["game_id","team_id","date",'nb_games']).columns:
        df_[f'{col}_cumul'] = df_[col].sum()
        df_[f'{col}_avg'] = df_[f'{col}_cumul'] /df_['nb_games']
    df_['win_home_avg'] = df_['win_home_cumul'] /df_['home_team_cumul']
    df_['win_away_avg'] = df_['win_away_cumul'] /(df_['nb_games']-df_['home_team_cumul'])
    df_['last_10_games_wins'] = df_.rolling(window=10, min_periods=1, on="date")['win'].sum().reset_index(drop=False)['win']
    result = df_.iloc[-1:].reset_index(drop=False)
    result['serie'] = streak(df_)
    result = result.drop(columns=result.columns[1:27])
    result = result.loc[:,~result.columns.str.endswith('cumul')]
    result['index']=1
    return result

if __name__ == '__main__':
    home_team = sys.argv[1]
    away_team = sys.argv[2]
    
    engine = create_engine("postgresql://postgres:postgres@127.0.0.1:5432/armagedon")
    
    query_home = f"""
        SELECT stats.*, games.home_team, games.date
        FROM stats
        LEFT JOIN games ON game_id = id
        WHERE season = (SELECT MAX(season) FROM games)
        AND team_id={home_team};
        """.replace('\n', ' ')
    query_away = f"""
        SELECT stats.*, games.home_team, games.date
        FROM stats
        LEFT JOIN games ON game_id = id
        WHERE season = (SELECT MAX(season) FROM games)
        AND team_id={away_team};
        """.replace('\n', ' ')
    data_home = pd.read_sql(query_home, engine)
    result_h  = create_stats(data_home)
    data_away  = pd.read_sql(query_away, engine)
    resutl_a  = create_stats(data_away)
    X = pd.merge(result_h,resutl_a, how='inner', on='index', suffixes=('_home','_away')).drop(columns='index')
    y = xg2.predict_proba(X)
    print(round(y[0][1],5), end="")
