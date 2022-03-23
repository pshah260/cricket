import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import numpy as np
from itertools import combinations
import sys
import pytz

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
engine = create_engine("postgres://postgres:postgres@localhost:5432/cricket")


def get_df():
    engine = create_engine("postgres://postgres:postgres@localhost:5432/cricket")
    query = 'select * from "full";'
    df = pd.read_sql(query, engine)
    return df

def tprint(team):
    df = m2()
    tp = df[df['Team']== team ]
    print tp

def rprint(role):
    df = m2()
    rp = df[df['Role']== role]
    print rp

def pp(price):
    df = m2()
    ppr = df[df['Price']<=price]
    print ppr

def entire():
    df = m2()
#    df = df.sort_values(by=['CPPM'], ascending=False)
    df = df.reset_index()
    print df

def ranks():
    df = m2()
    df = df.sort_values(by=['CPPM'], ascending=False)
    df = df.reset_index()
    EST = pytz.timezone('America/New_York')
    df["Date"] = datetime.now(EST).date()
    dfd = df.pivot(index="Date", columns="PLAYER")["index"]
    dfp = df.pivot(index="Date", columns="PLAYER")["CPPM"]
    engine = create_engine('postgresql://ai:ai@localhost:5432/ipl')
    dfd.to_sql('daterank', engine, if_exists = 'append')
    dfp.to_sql('pointrank', engine, if_exists = 'append')


def t3(team, role, price):
    df = m2()
    t3 = df[(df['Team'] == team) & (df['Price'] <= float(price)) & (df['Role'] == role)]
    print t3

def rp(role, price):
    df = m2()
    rp = df[(df['Price'] <= float(price)) & (df['Role']== role)]
    print rp

def tp(team, price):
    df = m2()
    tp = df[(df['Team'] == team) & (df['Price'] <= float(price))]
    print tp

def tr(team, role):
    df = m2()
    tr = df[(df['Team'] == team) & (df['Role']== role)]
    print tr

def xtp(t1, t2):
    df = m2()
    df = df[(df['Team'] == t1) | (df['Team']== t2)]
#    df = df.sort_values(by=['CPPM'], ascending=False)
    print df

def wtp(t1, t2, t3, t4):
    df = m2()
    df = df[(df['Team'] == t1) | (df['Team']== t2) | (df['Team'] == t3) | (df['Team']== t4)]
#    df = df.sort_values(by=['CPPM'], ascending=False)
    print df

def main():
    parser = argparse.ArgumentParser(description="Script creates tables for return")
    parser.add_argument('--team', help='Team - CSK, DC, KXI, KKR, MI, RR, RCB, SRH')
    parser.add_argument('--role', help='Role - B=Batsman, A=Allrounder, W=WicketKeeper, P=Bowler')
    parser.add_argument('--price', type=float, help='Under and equal to price needed')
    parser.add_argument('--t1', help='Team - CSK, DC, KXI, KKR, MI, RR, RCB, SRH')
    parser.add_argument('--t2', help='Team - CSK, DC, KXI, KKR, MI, RR, RCB, SRH')
    parser.add_argument('--game', type=float, help='Game number')
    parser.add_argument('--rank', help='Rank')
    parser.add_argument('--we', help='Weekend')


    team = parser.parse_args().team
    role = parser.parse_args().role
    price = parser.parse_args().price
    t1 = parser.parse_args().t1
    t2 = parser.parse_args().t2
    game = parser.parse_args().game
    rank = parser.parse_args().rank
    we = parser.parse_args().we

    if t1 and t2:
        xtp(t1,t2)
        sys.exit(1)
    elif game and we:
        result = gamet(game)
        wtp(result[0], result[1], result[2], result[3])
        sys.exit(1)
    elif game:
        result = gamet(game)
        xtp(result[0], result[1])
        sys.exit(1)
    else:
        pass

    if team and price and role:
        t3(team, role, price)
        sys.exit(1)
    elif team and role:
        tr(team, role)
        sys.exit(1)
    elif role and price:
        rp(role, price)
        sys.exit(1)
    elif team and price:
        tp(team, price)
        sys.exit(1)
    elif team:
        tprint(team)
    elif role:
        rprint(role)
    elif price:
        pp(price)
    elif rank:
        ranks()
    else:
        entire()

if __name__ == '__main__':
    df = pd.read_csv("p.csv")
    datadf = get_df()
    datadf.replace("KL Rahul", "Lokesh Rahul", inplace=True)
    y = datadf.groupby(["fullName"])["tp"].describe()
    y = y.fillna(0)
    df = pd.merge(df, y, left_on=["Name"], right_on="fullName", how='left')
    df.to_sql("players", engine)

