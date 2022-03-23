import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
import re
import requests
import sys
from datetime import datetime
from datetime import date
import numpy as np

pd.set_option('display.max_columns', None)

if __name__ == '__main__':
    engine = create_engine("postgres://postgres:postgres@localhost:5432/cricket")
    query = 'select * from "full";'
    df = pd.read_sql(query, engine)
    df = df.drop(["index", "mod.bowlerId", "mod.additionalPlayerIds"], axis=1)
    df["battingfirst"] = df["battingfirst"].astype(int)
    df["rightArmedBowl"] = df["rightArmedBowl"].astype(int)
    df["rightHandedBat"] = df["rightHandedBat"].astype(int)
    df["bowlingfirst"] = df["bowlingfirst"].astype(int)
    df['batorder'] = df['batorder'].replace(0, np.nan)
    df['bowlingStyle'] = df['bowlingStyle'].replace(0, np.nan)
    df['mod.dismissedMethod_x'] = df['mod.dismissedMethod_x'].replace(0, np.nan)



'''
    X = df
    y = X.pop("tp")

    X_train, X_test, y_train, y_test = train_test_split(X, y)



#    df = df.drop(["r_x", "b", "sr", "4s", "6s", "mod.dismissedBp.over", "mod.bowlerId",
#                  "mod.additionalPlayerIds", "mod.dismissedMethod_x", "rp", "sp", "btp", "ov",
#                  "w",  "d", "maid", "e", "wd", "nb", "ep", "wp", "bep", "sum", "bop",
#                  "fp"], axis=1)
    print(df)
'''


ndf = df[["mod.bowlerId"]]

mdf = pd.merge(ndf, df, how="left", left_on="mod.bowlerId", right_on="playerId")

y = mdf.groupby(["city", "bowlingStyle"])["index"].nunique()
