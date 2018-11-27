from secrets import *
from data import *

import tweepy
import datetime
from bs4 import BeautifulSoup
import urllib.request
import requests
from selenium import webdriver
import os
import time
import bitly_api

# CONSUMER_KEY = '***'
# CONSUMER_SECRET = '***'
# ACCESS_TOKEN = '***'
# ACCESS_TOKEN_SECRET = '***'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# ACCESS_TOKEN_BITLY = '***'
bitly = bitly_api.Connection(access_token=ACCESS_TOKEN_BITLY)


CHROME_PATH = '/usr/bin/google-chrome'
CHROMEDRIVER_PATH = os.path.join(os.getcwd(), 'chromedriver')
WINDOW_SIZE = "1920,1080"

chrome_options = webdriver.chrome.options.Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH

def find_between(s,first,last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def create_tweet(result):
    #####################################################################v
    match = result.find('tbody',attrs={'id':'teams'})        

    home_team = match.find('tr',attrs={'class':'home'})
    away_team = match.find('tr',attrs={'class':'away'})

    home_team_name = find_between(str(home_team.find('span',attrs={'class':'sb-team-short'})),"short\">","</span>")
    away_team_name = find_between(str(away_team.find('span',attrs={'class':'sb-team-short'})),"short\">","</span>")
    
    home_score = find_between(str(home_team.find('td',attrs={'class':'total'})),"<span>","</span>")
    away_score = find_between(str(away_team.find('td',attrs={'class':'total'})),"<span>","</span>")
    
    score = " ".join((fullnames_dict[away_team_name],"("+handles_dict[away_team_name]+")",away_score,'-', fullnames_dict[home_team_name],"("+handles_dict[home_team_name]+")" ,home_score))    
    #####################################################################v
    links = result.find('section',attrs={'class':'sb-actions'}).find_all('a')
    gameId = find_between(str(links[0]),"gameId=","\"")
    
    base_url = "http://www.espn.com"
    recap = base_url + "/nba/recap?gameId=" + gameId
    boxscore = base_url + "/nba/boxscore?gameId=" + gameId
    play_by_play = base_url + "/nba/playbyplay?gameId=" + gameId
    gamecast = base_url + "/nba/game?gameId=" + gameId

    recap = base_url + "/nba/recap?gameId=" + gameId
    boxscore = base_url + "/nba/boxscore?gameId=" + gameId
    playbyplay = base_url + "/nba/playbyplay?gameId=" + gameId
    gamecast = base_url + "/nba/game?gameId=" + gameId

    base_bitly = "bit.ly/"
    recap = "Recap\t\t : " + base_bitly + bitly.shorten(recap)['hash']
    boxscore = "Boxscore\t : " + base_bitly + bitly.shorten(boxscore)['hash']
    play_by_play = "Play-By-Play\t : " + base_bitly + bitly.shorten(play_by_play)['hash']
    gamecast = base_bitly + bitly.shorten(gamecast)['hash']
    urls="".join((recap, "\n", boxscore, "\n", play_by_play,"\n",gamecast))

    tweet = "".join((score,"\n",urls))
    return tweet

        
    
    
date = str(datetime.date.today()-datetime.timedelta(1)).split('-')
urlpage = 'http://www.espn.com/nba/scoreboard/_/date/'+date[0]+date[1]+date[2]

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
driver.get(urlpage)
res = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()

# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(res,'lxml')

# find results within table
table = soup.find('div',attrs={'id':'events'})
results = table.find_all('article',attrs={'class':'scoreboard'})

print(len(results),'NBA Games on ',date[1],'-',date[2],'-',date[0],'\n')
for result in results:
    reso1 = create_tweet(result)
    print(reso1,'\n')
    api.update_status(reso1)
    time.sleep(10)
    
