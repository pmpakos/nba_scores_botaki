from secrets import *
from data import *
import tweepy
import datetime
from bs4 import BeautifulSoup
import urllib.request
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


def find_between(s,first,last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def create_tweet(result):
    #####################################################################v
    match = result.find('table',attrs={'class':'teams'})        
    home_team = match.find_all('tr')[1]
    away_team = match.find_all('tr')[0]
    
    home_team_name = find_between(str(home_team.find_all('td')[0].find('a')),".html\">","</a>")
    away_team_name = find_between(str(away_team.find_all('td')[0].find('a')),".html\">","</a>")
    
    home_score = find_between(str(home_team.find_all('td')[1]),"right\">","</td>")
    away_score = find_between(str(away_team.find_all('td')[1] ),"right\">","</td>")
    
    score = " ".join((fullnames_dict[away_team_name],"("+handles_dict[away_team_name]+")",away_score,'-', fullnames_dict[home_team_name],"("+handles_dict[home_team_name]+")" ,home_score))
    #####################################################################v
    links = result.find('p',attrs={'class':'links'}).find_all('a')
    base_url = "https://www.basketball-reference.com"
    boxscore1 = base_url+find_between(str(links[0]),"\"","\"")    
    play_by_play = base_url+find_between(str(links[1]),"\"","\"")    
    shot_chart = base_url+find_between(str(links[2]),"\"","\"")

    base_bitly = "bit.ly/"
    boxscore = "Boxscore\t : " + base_bitly + bitly.shorten(boxscore1)['hash']
    play_by_play = "Play-By-Play\t : " + base_bitly + bitly.shorten(play_by_play)['hash']
    shot_chart = "Shot Chart\t : " + base_bitly + bitly.shorten(shot_chart)['hash']
    boxscore2 = base_bitly + bitly.shorten(boxscore1)['hash']
    urls="".join((boxscore, "\n", play_by_play,"\n",shot_chart, "\n", boxscore2))

    tweet = "".join((score,"\n",urls))
    return tweet
        
    
    
date = str(datetime.date.today()-datetime.timedelta(1)).split('-')
urlpage = 'https://www.basketball-reference.com/boxscores/?month='+date[1]+'&day='+date[2]+'&year='+date[0]

# query the website and return the html to the variable 'page'
page = urllib.request.urlopen(urlpage)
# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

# find results within table
table = soup.find('div', attrs={'class': 'game_summaries'})
results = table.find_all('div')

print(len(results),'NBA Games on ',date[1],'-',date[2],'-',date[0],'\n')

for result in results:
    reso1 = create_tweet(result)
    print(reso1)
    api.update_status(reso1)
    time.sleep(10)
    
