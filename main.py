import pandas as pd
pd.set_option('display.max_columns', None)
from sqlalchemy import create_engine
import time
from selenium import webdriver

if __name__ == '__main__':
    engine = create_engine("postgres://postgres:postgres@localhost:5432/cricket")
    driver = webdriver.Chrome()
    driver.get("https://www.iplt20.com/matches/schedule/men")
    time.sleep(10)

    matches = driver.find_element_by_class_name("js-list")
    match = matches.text.split("\n")
    driver.close()

    for i in range(0, len(match)-1):
        if match[i] == "MATCH CENTRE" and match[i+1] == "v":
            match.insert(i+1, match[i-6])
        else:
            pass
    mlist = []
    for i in range((len(match) + 7) // 7):
        mlist.append(match[i * 7:(i + 1) * 7])

    mlist = mlist[0:60]
    df = pd.DataFrame(mlist, columns=['Date', 'V', 'TeamA', 'TeamB', 'Time', 'Stadium', 'Match'])
    df2 = df.Stadium.str.rsplit(pat=', ', expand=True)
    df = df.drop(['V', 'Match', 'Stadium'], axis=1)
    df["Stadium"] = df2[1]
    df["TeamA"] = df.TeamA.str.title()
    df["TeamB"] = df.TeamB.str.title()
    a = pd.get_dummies(df["TeamA"])
    b = pd.get_dummies(df["TeamB"])
    ab = a.add(b)
    ab = ab.rolling(4).sum()
    ab = ab.shift(periods=-3)
    ab.dropna(inplace=True)
    ab["city"] = df["Stadium"]
    ab = ab.drop(["Tbc"], axis=1)
    ab.to_sql("allteams", engine)
#    print(ab)
#    df.to_sql("schedule", engine)