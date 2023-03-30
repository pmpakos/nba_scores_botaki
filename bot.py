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
# import bitly_api
import requests
import json
import time
import sys

# https://www.makeuseof.com/python-bitly-url-shortener-create/
def url_shortener(url):
    endpoint = 'https://api-ssl.bitly.com/v4/shorten' 
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN_BITLY}',
        'Content-Type': 'application/json',
    }

    max_retries = 3
    retry_count = 0
    while retry_count < max_retries:
        data = {'long_url': url}
        response = requests.post(endpoint, headers=headers, data=json.dumps(data)) 
        if response.status_code == 200:
            shortened_url = json.loads(response.content)['link']
            # print(f'Shortened URL: {shortened_url}')
            return shortened_url
            break
        else:
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(5)
    else:
        print('URL shortening was not successful.')

def find_between(s,first,last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ''


def create_tweet(result):
    #####################################################################
    match = result.find('ul',attrs={'class':'ScoreboardScoreCell__Competitors'})

    home_team = match.find('li',attrs={'class':'ScoreboardScoreCell__Item--home'})
    away_team = match.find('li',attrs={'class':'ScoreboardScoreCell__Item--away'})

    home_team_name = find_between(str(home_team.find('div',attrs={'class':'ScoreCell__TeamName--shortDisplayName'})),"db\">","</div>")
    away_team_name = find_between(str(away_team.find('div',attrs={'class':'ScoreCell__TeamName--shortDisplayName'})),"db\">","</div>")
    
    home_score = find_between(str(home_team.find('div',attrs={'class':'ScoreCell_Score--scoreboard'})),"pl2\">","</div>")
    away_score = find_between(str(away_team.find('div',attrs={'class':'ScoreCell_Score--scoreboard'})),"pl2\">","</div>")
    
    score = ' '.join((fullnames_dict[away_team_name],'('+handles_dict[away_team_name]+')',away_score,'-', fullnames_dict[home_team_name],'('+handles_dict[home_team_name]+')' ,home_score))
    hashtags = ' '.join((hashtags_dict[away_team_name],hashtags_dict[home_team_name]))
    hashtags2 = ' '.join(('#NBA', '#NBATwitter'))
    #####################################################################v
    links = result.find('div',attrs={'class':'Scoreboard__Callouts flex items-center mv4 flex-column'}).find_all('a')

    gameId = find_between(str(links[0]),'/gameId/',"\"")
    
    base_url = 'http://www.espn.com'
    recap = base_url + '/nba/recap?gameId=' + gameId
    boxscore = base_url + '/nba/boxscore/_/gameId/' + gameId
    play_by_play = base_url + '/nba/playbyplay/_/gameId/' + gameId
    gamecast = base_url + '/nba/game/_/gameId/' + gameId

    # base_bitly = 'es.pn/'
    # recap = 'Recap\t\t : ' + base_bitly + bitly.shorten(recap)['hash']
    # boxscore = 'Boxscore\t : ' + base_bitly + bitly.shorten(boxscore)['hash']
    # play_by_play = 'Play-By-Play\t : ' + base_bitly + bitly.shorten(play_by_play)['hash']
    # gamecast = base_bitly + bitly.shorten(gamecast)['hash']
    recap = 'Recap\t\t : ' + url_shortener(recap)
    boxscore = 'Boxscore\t : ' + url_shortener(boxscore)
    play_by_play = 'Play-By-Play\t : ' + url_shortener(play_by_play)
    gamecast = url_shortener(gamecast)
    urls=''.join((recap, '\n', boxscore, '\n', play_by_play,'\n', hashtags, '\n', hashtags2, '\n', gamecast))

    tweet = ''.join((score,'\n',urls))
    return tweet    
    

if __name__ == '__main__':
    # CONSUMER_KEY = '***'
    # CONSUMER_SECRET = '***'
    # ACCESS_TOKEN = '***'
    # ACCESS_TOKEN_SECRET = '***'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    # ACCESS_TOKEN_BITLY = '***'
    # bitly = bitly_api.Connection(access_token=ACCESS_TOKEN_BITLY)

    CHROME_PATH = '/usr/bin/google-chrome'
    CHROMEDRIVER_PATH = '/mnt/various/BOTS/nba_scores_botaki/chromedriver'
    WINDOW_SIZE = '1920,1080'

    chrome_options = webdriver.chrome.options.Options()  
    chrome_options.add_argument('--headless')  
    chrome_options.add_argument('--window-size=%s' % WINDOW_SIZE)
    chrome_options.binary_location = CHROME_PATH


    date = str(datetime.date.today()-datetime.timedelta(1)).split('-')
    latest_tweet_date = str(api.user_timeline(id = api.me().id, count = 1)[0].created_at)[0:10]
    todays_date = str(datetime.date.today())[0:10]
    if(latest_tweet_date == todays_date):
        print('Already tweeted for today, tomorrow again!')
        exit()

    urlpage = 'https://www.espn.com/nba/scoreboard/_/date/'+date[0]+date[1]+date[2]

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    driver.get(urlpage)
    res = driver.execute_script('return document.documentElement.outerHTML')
    driver.quit()

    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(res,'lxml')

    # find results within table
    table = soup.find('section',attrs={'class':'Card gameModules'})
    results = table.find_all('section',attrs={'class':'Scoreboard bg-clr-white flex flex-auto justify-between'})

    print(len(results),'NBA Games on ',date[1],'-',date[2],'-',date[0],'\n')
    for result in results:
        reso1 = create_tweet(result)
        print(reso1,'\n')
        api.update_status(reso1)
        time.sleep(10)
