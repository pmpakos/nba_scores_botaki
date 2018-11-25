from secrets import *

import tweepy
import datetime
from bs4 import BeautifulSoup
import urllib.request
import time

# CONSUMER_KEY = '***'
# CONSUMER_SECRET = '***'
# ACCESS_TOKEN = '***'
# ACCESS_TOKEN_SECRET = '***'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


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
    match = result.find('table',attrs={'class':'teams'})        
    home_team = match.find_all('tr')[1]
    away_team = match.find_all('tr')[0]
    
    home_team_name = find_between(str(home_team.find_all('td')[0].find('a')),".html\">","</a>")
    away_team_name = find_between(str(away_team.find_all('td')[0].find('a')),".html\">","</a>")
    
    home_score = find_between(str(home_team.find_all('td')[1]),"right\">","</td>")
    away_score = find_between(str(away_team.find_all('td')[1] ),"right\">","</td>")
    return " ".join((away_team_name,"("+handles_dict[away_team_name]+")",away_score,'-', home_team_name,"("+handles_dict[home_team_name]+")" ,home_score))
        
    
#     details = result.find_all('table')[1]
#     quarters_scores = details.find_all('td',attrs={"class":"center"})
    
#     q1_0 = find_between(str(quarters_scores[0]),"center\">","</td>")
#     q2_0 = find_between(str(quarters_scores[1]),"center\">","</td>")
#     q3_0 = find_between(str(quarters_scores[2]),"center\">","</td>")
#     q4_0 = find_between(str(quarters_scores[3]),"center\">","</td>")

#     q1_1 = find_between(str(quarters_scores[4]),"center\">","</td>")
#     q2_1 = find_between(str(quarters_scores[5]),"center\">","</td>")
#     q3_1 = find_between(str(quarters_scores[6]),"center\">","</td>")
#     q4_1 = find_between(str(quarters_scores[7]),"center\">","</td>")
    
#     pts_leader = 
#     trb_leader = 
#     print()
#     print("{:15} {:3} {:3} {:3} {:3} | {:4}".format('','1','2','3','4','Final'))
#     print('-'*40)
#     print("{:15} {:3} {:3} {:3} {:3} | {:4}".format(away_team_name,q1_0,q2_0,q3_0,q4_0,away_score))
#     print("{:15} {:3} {:3} {:3} {:3} | {:4}".format(home_team_name,q1_1,q2_1,q3_1,q4_1,home_score))
#     print()
    
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
    time.sleep(30)
    api.update_status(reso1)
