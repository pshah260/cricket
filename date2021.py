import pandas as pd
from sqlalchemy import create_engine
import json

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

engine = create_engine("postgres://postgres:postgres@localhost:5432/cricket")

f = open("day1.json")
a = json.load(f)

def get_players():
    query = 'select * from "players";'
    df = pd.read_sql(query, engine)
    return df


df = pd.json_normalize(a["Data"]["Value"]["PlayerStats"], max_level=2)
df = df[["plyrnm", "tmnm", "isuncap", "isfp", "value", "isinjd", "ovrpoint", "pstats"]]
c = pd.DataFrame(df["pstats"].to_list())
for i in c.columns:
    d = pd.DataFrame(c[i].to_list())
    d = d[['gdpoint']]
    d = d.rename(columns={'gdpoint': str(i)})
    d = d.replace("-", 0)
    d = d.apply(pd.to_numeric)
    df = pd.merge(df, d, how='outer', left_on=None, right_on=None, left_index=True, right_index=True)

df = df.drop(["pstats"], axis=1)
df = df.loc[:, (df != 0).any(axis=0)]


a = get_players()

abc = pd.merge(df, a.drop("index", axis=1), how='inner', left_on='plyrnm', right_on='Name')
abc = abc.T.drop_duplicates().T

df.to_sql("2021points", engine)