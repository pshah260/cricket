import pandas as pd
from sqlalchemy import create_engine
import time
import json
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import sys
from datetime import datetime
from datetime import date

pd.set_option('display.max_columns', None)

def apis():
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=caps)
    api = []
    for i in range(1,61):
        driver.get("https://www.iplt20.com/match/2020/" + str(i).zfill(2) + "?tab=scorecard")
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
    api = apis()
    ipl = ["Chennai Super Kings", "Delhi Capitals", "Kolkata Knight Riders", "Mumbai Indians",
            "Punjab Kings", "Rajasthan Royals", "Royal Challengers Bangalore", "Sunrisers Hyderabad"]
    for a in api:
        r = requests.get(a).json()
        teams = []
        for i in range(2):
            teams.append(r["matchInfo"]["teams"][i]["team"]["fullName"])
        wn = r['matchInfo']['matchStatus']['outcome'])
        if wn == 'A':
            winner = teams[0]
        else:
            winner = teams[1]


#        teams = []
#        for i in range(2):
#            teams.append(r["matchInfo"]["teams"][i]["team"]["fullName"])
#        battorder = r['matchInfo']['battingOrder']
#        if battorder[0] == 1:
#            teams.reverse()
#        for team in teams:
#            j = {}