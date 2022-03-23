import pandas as pd
from sqlalchemy import create_engine
import time
import json
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from datetime import datetime
from datetime import date
import numpy as np

pd.set_option('display.max_columns', None)


def calculate_age(born):
    born = datetime.strptime(born, "%Y-%m-%d").date()
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def e(x):
    if float(x["r"]) >= 30 and float(x["r"]) < 50:
        return 4
    elif float(x["r"]) >= 50 and float(x["r"]) < 100:
        return 8
    elif float(x["r"]) >= 100:
        return 16
    else:
        return 0

def f(x):
    if float(x["b"]) > 9 and float(x["sr"]) < 50:
        return -6
    elif float(x["b"]) > 9 and float(x["sr"]) >= 50 and float(x["sr"]) < 60:
        return -4
    elif float(x["b"]) > 9 and float(x["sr"]) >= 60 and float(x["sr"]) <= 70:
        return -2
    elif float(x["b"]) > 9 and float(x["sr"]) >= 130 and float(x["sr"]) <= 150:
        return 2
    elif float(x["b"]) > 9 and float(x["sr"]) > 150 and float(x["sr"]) < 170:
        return 4
    elif float(x["b"]) > 9 and float(x["sr"]) > 170:
        return 6
    else:
        return 0

def g(x):
    if float(x["e"]) > 12 and float(x["ov"]) >= 2:
        return -6
    elif float(x["e"]) > 11 and float(x["e"]) <= 12 and float(x["ov"]) >= 2:
        return -4
    elif float(x["e"]) >= 10 and float(x["e"]) <= 11 and float(x["ov"]) >= 2:
        return -2
    elif float(x["e"]) >= 6 and float(x["e"]) < 7 and float(x["ov"]) >= 2:
        return 2
    elif float(x["e"]) >= 5 and float(x["e"]) <  6 and float(x["ov"]) >= 2:
        return 4
    elif float(x["e"]) < 5 and float(x["ov"]) >= 2:
        return 6
    else:
        return 0

def h(x):
    if float(x["w"]) == 3:
        return 4
    elif float(x["w"]) == 4:
        return 8
    elif float(x["w"]) >= 5:
        return 16
    else:
        return 0

def i(x):
    if x["mod.dismissedMethod"] == "b" or x["mod.dismissedMethod"] == "lbw":
        return 8
    else:
        return 0

def     apis():
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=caps)
    api = []
    for i in range(30, 59):
        driver.get("https://www.iplt20.com/match/2021" + "/" + str(i).zfill(2) + "?tab=scorecard")
        time.sleep(2)
        log = driver.get_log('performance')
        pattern = r'https\:\/\/cricketapi\.platform\.iplt20\.com\/\/fixtures\/\d\d\d\d\d\/scoring'
        urls = []
        for entry in log:
            message = json.loads(entry['message'])
            if message['message']['method'] == 'Network.requestWillBeSent':
                if re.search(pattern, message['message']['params']['request']['url']):
                    urls.append(message['message']['params']['request']['url'])
        api.append(urls[0])
    driver.close()
    return api


if __name__ == '__main__':
    engine = create_engine("postgres://postgres:postgres@localhost:5432/cricket")
    urls = apis()

    df = pd.DataFrame()

    for urlz in urls:
        print(urlz)
        r = requests.get(url=urlz)
        j = r.json()

        teamA = pd.DataFrame.from_dict(j["matchInfo"]["teams"][0]["players"])
        teamA['age'] = teamA['dateOfBirth'].apply(calculate_age)
        teamA = teamA.drop(["shortName", "dateOfBirth"], axis=1)
        teamA["teamid"] = [j["matchInfo"]["teams"][0]["team"]["id"]] * len(teamA)
        teamA["team"] = [j["matchInfo"]["teams"][0]["team"]["fullName"]] * len(teamA)


        teamB = pd.DataFrame.from_dict(j["matchInfo"]["teams"][1]["players"])
        teamB['age'] = teamB['dateOfBirth'].apply(calculate_age)
        teamB = teamB.drop(["shortName", "dateOfBirth"], axis=1)
        teamB["teamid"] = [j["matchInfo"]["teams"][1]["team"]["id"]] * len(teamB)
        teamB["team"] = [j["matchInfo"]["teams"][1]["team"]["fullName"]] * len(teamB)

        teamA["oppteam"] = j["matchInfo"]["teams"][1]["team"]["fullName"]
        teamB["oppteam"] = j["matchInfo"]["teams"][0]["team"]["fullName"]

        if j["matchInfo"]["battingOrder"][0] == 0:
            teamA['battingfirst'] = True
            teamA['bowlingfirst'] = False
            teamB['battingfirst'] = False
            teamB['bowlingfirst'] = True
            teamA["tscore"] = j["innings"][0]["scorecard"]["runs"]
            teamB["tscore"] = j["innings"][1]["scorecard"]["runs"]
            teamA["twkts"] = j["innings"][0]["scorecard"]["wkts"]
            teamB["twkts"] = j["innings"][1]["scorecard"]["wkts"]
        else:
            teamA['battingfirst'] = False
            teamA['bowlingfirst'] = True
            teamB['battingfirst'] = True
            teamB['bowlingfirst'] = False
            teamA["tscore"] = j["innings"][1]["scorecard"]["runs"]
            teamB["tscore"] = j["innings"][0    ]["scorecard"]["runs"]
            teamA["twkts"] = j["innings"][1]["scorecard"]["wkts"]
            teamB["twkts"] = j["innings"][0]["scorecard"]["wkts"]

        teamAB = pd.concat([teamA, teamB], ignore_index=True)
        teamAB = teamAB.rename(columns={"id": "playerId"})

        sc1 = pd.json_normalize(j["innings"][0]["scorecard"]["battingStats"], max_level=2)
        try:
            sc1.update(sc1['mod.additionalPlayerIds'].str[0])
        except:
            sc1['mod.additionalPlayerIds'] = np.nan
        sc2 = pd.json_normalize(j["innings"][1]["scorecard"]["battingStats"], max_level=2)
        try:
            sc2.update(sc2['mod.additionalPlayerIds'].str[0])
        except:
            sc2['mod.additionalPlayerIds'] = np.nan
        sc3 = pd.json_normalize(j["innings"][0]["scorecard"]["bowlingStats"], max_level=2)
        sc4 = pd.json_normalize(j["innings"][1]["scorecard"]["bowlingStats"], max_level=2)
        sc1['rp'] = sc1.apply(e, axis=1)
        sc2['rp'] = sc1.apply(e, axis=1)
        sc1["sp"] = sc1.apply(f, axis=1)
        sc2["sp"] = sc2.apply(f, axis=1)
        sc3["ep"] = sc3.apply(g, axis=1)
        sc4["ep"] = sc4.apply(g, axis=1)
        sc3["wp"] = sc3.apply(h, axis=1)
        sc4["wp"] = sc4.apply(h, axis=1)

        try:
            sc5 = sc1[["mod.bowlerId", "mod.dismissedMethod"]]
        except:
            sc5 = pd.DataFrame(columns=["mod.bowlerId", "mod.dismissedMethod"])
        try:
            sc6 = sc2[["mod.bowlerId", "mod.dismissedMethod"]]
        except:
            sc6 = pd.DataFrame(columns=["mod.bowlerId", "mod.dismissedMethod"])
        sc5 = sc5.rename(columns={"mod.bowlerId": "playerId"})
        sc6 = sc6.rename(columns={"mod.bowlerId": "playerId"})
        try:
            sc5["bep"] = sc1.apply(i, axis=1)
        except:
            sc5["bep"] = 0
        try:
            sc6["bep"] = sc2.apply(i, axis=1)
        except:
            sc6["bep"] = 0
        sc5["sum"] = sc5.groupby(['playerId'])['bep'].transform('sum')
        sc6["sum"] = sc6.groupby(['playerId'])['bep'].transform('sum')
        sc5 = sc5.dropna()
        sc6 = sc6.dropna()
        sc5 = sc5.drop_duplicates(subset=['playerId'])
        sc6 = sc6.drop_duplicates(subset=['playerId'])

        sc3 = pd.merge(sc3, sc5, how="outer", on=["playerId"])
        sc4 = pd.merge(sc4, sc6, how="outer", on=["playerId"])
        sc3 = sc3.fillna(0)
        sc4 = sc4.fillna(0)

        sc1['btp'] = sc1['r'] + sc1['4s'] + 2 * sc1['6s'] + sc1['rp'] + sc1['sp']
        sc2['btp'] = sc2['r'] + sc2['4s'] + 2 * sc2['6s'] + sc2['rp'] + sc2['sp']
        sc3['bop'] = 25*sc3['w'] + 12 * sc3['maid'] + sc3['ep'] + sc3['wp'] + sc3['sum']
        sc4['bop'] = 25*sc4['w'] + 12 * sc4['maid'] + sc4['ep'] + sc4['wp'] + sc4['sum']
        sc1["batorder"] = sc1.index + 1
        sc2["batorder"] = sc2.index + 1
        s1 = pd.concat([sc1, sc2])
        s2 = pd.concat([sc3, sc4])
        s3 = pd.merge(s1, s2, how="outer", on=["playerId"])
        c = pd.DataFrame(s3["mod.additionalPlayerIds"].value_counts())
        c["playerId"] = c.index
        c = c.rename(columns={"mod.additionalPlayerIds": "fp"})
        c["fp"] = c["fp"] * 8
        s4 = pd.merge(s3, c, how="outer", on="playerId")
        s4 = s4.fillna(0)
        s4["tp"] = s4["btp"] + s4["bop"] + s4["fp"]
        s5 = pd.merge(teamAB, s4, how="outer", on=["playerId"])
        s5["city"] = j["matchInfo"]["venue"]["city"]
        s5 = s5.fillna(0)
        s5 = s5.drop(["mod.text"], axis=1)
        df = pd.concat([s5,df], ignore_index=True)
        df = df.drop(["teamid", "mod.dismissedBp.innings", "mod.dismissedBp.ball", "mod.countingBp.innings", "mod.countingBp.over", "mod.countingBp.ball",
                 "mod.isOut", "r_y", "mod.dismissedMethod_y", "bep"], axis=1)
    df.to_sql("2021new", engine)