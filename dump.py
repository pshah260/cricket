import pandas as pd
from sqlalchemy import create_engine

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
engine = create_engine("postgres://postgres:postgres@localhost:5432/cricket")

def get_df():
    query = 'select * from "players21";'
    df = pd.read_sql(query, engine)
    return df

def completedf():
    query = 'select * from "2021";'
    datadf = pd.read_sql(query, engine)
    return datadf

def olddf():
    query = 'select * from "players";'
    datadf = pd.read_sql(query, engine)
    return datadf

    datadf.groupby(["city", "batorder", "battingfirst"])["tp"].mean().unstack(level="battingfirst")

y = datadf.groupby(["fullName"])["tp"].describe()
y = y.fillna(0)
df = pd.merge(df, y, left_on=["Name"], right_on="fullName", how='left')
df.drop(['mean', 'min', '25%', '50%', '75%', 'max'], axis=1, inplace=True)

datadf['ov'] = pd.to_numeric(datadf['ov'])
b = datadf.loc[datadf.ov > 0]
df = df.sort_values(by=['tp'], ascending=False)
a = odf[['Name', 'tp']]
tdf = pd.merge(df, a, left_on='Name', right_on='Name', how='outer')
tdf = tdf.fillna(0)
tdf['dif'] = tdf['tp_y'] - tdf['tp_x']

tdf.loc[tdf.TeamName == 'Mumbai Indians']










import pandas as pd
from sqlalchemy import create_engine
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
engine = create_engine("postgres://postgres:postgres@localhost:5432/cricket")
def get_df():
    query = 'select * from "players21";'
    df = pd.read_sql(query, engine)
    return df

def completedf():
    query = 'select * from "2021";'
    datadf = pd.read_sql(query, engine)
    return datadf

def olddf():
    query = 'select * from "players";'
    datadf = pd.read_sql(query, engine)
    return datadf
df = get_df()
datadf = completedf()
odf = olddf()
y = datadf.groupby(["fullName"])["tp"].describe()
y = y.fillna(0)
df = pd.merge(df, y, left_on=["Name"], right_on="fullName", how='left')
df = df.sort_values(by=['tp'], ascending=False)
a = odf[['Name', 'tp']]
tdf = pd.merge(df, a, left_on='Name', right_on='Name', how='outer')
tdf = tdf.fillna(0)
tdf.drop(['index','mean', 'min', '25%', '50%', '75%', 'max'], axis=1, inplace=True)
tdf['dif'] = tdf['tp_y'] - tdf['tp_x']


a = datadf.groupby(["fullName", "team", "battingfirst"])["tp"].mean().unstack(level="battingfirst")
a = a.reset_index(level=[0,1])
a.loc[a.team == "Sunrisers Hyderabad"]