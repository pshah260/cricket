import pandas as pd
pd.set_option('display.max_columns', None)
from sqlalchemy import create_engine
import time
from selenium import webdriver

def squad(team):
    engine = create_engine("postgres://postgres:postgres@localhost:5432/cricket")
    driver = webdriver.Chrome()
    url = "https://www.iplt20.com/teams/" + team.replace(' ', '-').lower()
    driver.get(url)
    time.sleep(5)
    players = driver.find_elements_by_class_name("player-name")
    p = []
    for play in players:
        a = play.text
        p.append(a.replace("\n", " "))
    df = pd.DataFrame(p, columns=["Players"])
    df.to_sql(team.replace(' ', '-').lower(), engine)
    driver.close()

def teams():
    team = ["Chennai Super Kings", "Delhi Capitals", "Kolkata Knight Riders", "Mumbai Indians",
            "Punjab Kings", "Rajasthan Royals", "Royal Challengers Bangalore", "Sunrisers Hyderabad"]
    for t in team:
        squad(t)

def master():
    team = ["Chennai Super Kings", "Delhi Capitals", "Kolkata Knight Riders", "Mumbai Indians",
            "Punjab Kings", "Rajasthan Royals", "Royal Challengers Bangalore", "Sunrisers Hyderabad"]
    abv = ["CSK", "DC", "KKR", "MI", "PBKS", "RR", "RCB", "SRH"]
    res = dict(zip(team, abv))
    print(res)

if __name__ == '__main__':
#    teams()
    master()