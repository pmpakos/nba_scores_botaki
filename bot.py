from secrets import *

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


fullnames_dict={}
fullnames_dict['Boston'] = 'Boston Celtics'
fullnames_dict['Atlanta'] = 'Atlanta Hawks'
fullnames_dict['Minnesota'] = 'Minnesota Timberwolves'
fullnames_dict['Brooklyn'] = 'Brooklyn Nets'
fullnames_dict['Miami'] = 'Miami Heat'
fullnames_dict['Chicago'] = 'Chicago Bulls'
fullnames_dict['Orlando'] = 'Orlando Magic'
fullnames_dict['Denver'] = 'Denver Nuggets'
fullnames_dict['Houston'] = 'Houston Rockets'
fullnames_dict['Detroit'] =  'Detroit Pistons'
fullnames_dict['Portland'] =  'Portland Trailblazers'
fullnames_dict['Golden State'] =  'Golden State Warriors'
fullnames_dict['San Antonio'] =  'San Antonio Spurs'
fullnames_dict['Indiana'] =  'Indiana Pacers'
fullnames_dict['Memphis'] =  'Memphis Grizzlies'
fullnames_dict['LA Clippers'] =  'Los Angeles Clippers'
fullnames_dict['Utah'] =  'Utah Jazz'
fullnames_dict['LA Lakers'] = 'Los Angeles Lakers' 
fullnames_dict['Phoenix'] =  'Phoenix Suns'
fullnames_dict['Milwaukee'] =  'Milwaukee Bucks'
fullnames_dict['New Orleans'] =  'New Orleans Pelicans'
fullnames_dict['New York'] =  'New York Knicks'
fullnames_dict['Charlotte'] =  'Charlotte Hornets '
fullnames_dict['Oklahoma City'] =  'Oklahoma City Thunder'
fullnames_dict['Cleveland'] =  'Cleveland Cavaliers'
fullnames_dict['Philadelphia'] =  'Philadelphia 76ers'
fullnames_dict['Washington'] =  'Washington Wizards'
fullnames_dict['Toronto'] =  'Toronto Raptors'
fullnames_dict['Sacramento'] =  'Sacramento Kings'
fullnames_dict['Dallas'] =  'Dallas Mavericks'

handles_dict={}
handles_dict['Boston'] = '@celtics'
handles_dict['Atlanta'] = '@ATLHawks'
handles_dict['Minnesota'] = '@Timberwolves'
handles_dict['Brooklyn'] = '@BrooklynNets'
handles_dict['Miami'] = '@MiamiHEAT'
handles_dict['Chicago'] = '@chicagobulls'
handles_dict['Orlando'] = '@OrlandoMagic'
handles_dict['Denver'] = '@nuggets'
handles_dict['Houston'] = '@HoustonRockets'
handles_dict['Detroit'] =  '@DetroitPistons'
handles_dict['Portland'] =  '@trailblazers'
handles_dict['Golden State'] =  '@warriors'
handles_dict['San Antonio'] =  '@spurs'
handles_dict['Indiana'] =  '@Pacers'
handles_dict['Memphis'] =  '@memgrizz'
handles_dict['LA Clippers'] =  '@LAClippers'
handles_dict['Utah'] =  '@utahjazz'
handles_dict['LA Lakers'] = '@Lakers' 
handles_dict['Phoenix'] =  '@Suns'
handles_dict['Milwaukee'] =  '@Bucks'
handles_dict['New Orleans'] =  '@PelicansNBA'
handles_dict['New York'] =  '@nyknicks'
handles_dict['Charlotte'] =  '@hornets'
handles_dict['Oklahoma City'] =  '@okcthunder'
handles_dict['Cleveland'] =  '@cavs'
handles_dict['Philadelphia'] =  '@sixers'
handles_dict['Washington'] =  '@WashWizards'
handles_dict['Toronto'] =  '@Raptors'
handles_dict['Sacramento'] =  '@SacramentoKings'
handles_dict['Dallas'] =  '@dallasmavs'


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
    
