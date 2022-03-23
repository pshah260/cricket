import pandas as pd
from sqlalchemy import create_engine

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
engine = create_engine("postgres://postgres:postgres@localhost:5432/cricket")

def get_schedule():
    query = 'select * from "allteams";'
    df = pd.read_sql(query, engine)
    return df

def get_players():
    query = 'select * from "players";'
    df = pd.read_sql(query, engine)
    return df

def get_data():
    query = 'select * from "2021";'
    df = pd.read_sql(query, engine)
    return df

if __name__ == '__main__':
