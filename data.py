import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
pd.set_option('mode.chained_assignment',None)

##################################################
####################          ####################
#################### GET DATA ####################
####################          ####################
##################################################

def leagues_available():
    leagues = {'Spanish La Liga': 'laliga',
                'English Premier League': 'epl',
                'French Ligue1': 'ligue1',
                'German Bundesliga': 'bundesliga',
                'Italian Serie A': 'seriea'}

    leagues = pd.Series(leagues, name='leagues_available')
    return leagues

def get_teams_names(season, league):

    if league == 'laliga':
        base_url = 'https://understat.com/league/La_liga/'

    elif league == 'epl':
        base_url = 'https://understat.com/league/EPL/'

    elif league == 'ligue1':
        base_url = 'https://understat.com/league/Ligue_1/'

    elif league == 'bundesliga':
        base_url = 'https://understat.com/league/Bundesliga/'

    elif league == 'seriea':
        base_url = 'https://understat.com/league/Serie_A/'

    season = str(season)
    match = season
    url = base_url + match
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    scripts = soup.find_all('script')

    match_id = scripts[2].string
    
    ind_start = match_id.index("('")+2
    ind_end = match_id.index("')")

    json_teams_data = match_id[ind_start:ind_end]
    json_teams_data = json_teams_data.encode('utf8').decode('unicode_escape')

    teams_data = json.loads(json_teams_data)

    teams = pd.DataFrame(teams_data)

    teams = teams.T['title'].tolist()

    return teams

def get_match_info(team, season):
    base_url = 'https://understat.com/team/'+team+'/'
    match = str(season)
    url = base_url + match
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    scripts = soup.find_all('script')

    match_id = scripts[1].string
    
    ind_start = match_id.index("('")+2
    ind_end = match_id.index("')")

    json_matchid_data = match_id[ind_start:ind_end]
    json_matchid_data = json_matchid_data.encode('utf8').decode('unicode_escape')

    matchid_data = json.loads(json_matchid_data)

    matchid = pd.DataFrame(matchid_data)

    matchid = matchid[matchid['isResult'] == True]

    return matchid

def get_match_data(matchid, side):
    base_url = 'https://understat.com/match/'
    match = str(matchid)
    url = base_url + match
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    scripts = soup.find_all('script')
    shots = scripts[1].string
    ind_start = shots.index("('")+2
    ind_end = shots.index("')")

    json_shots_data = shots[ind_start:ind_end]
    json_shots_data = json_shots_data.encode('utf8').decode('unicode_escape')

    shots_data = json.loads(json_shots_data)

    home_shots = pd.DataFrame(shots_data[side])

    return home_shots

def match_stats(season, league):
    season = str(season)
    teams = get_teams_names(season, league)
    all_data = pd.DataFrame()
    single_data = pd.DataFrame()

    for team in teams:
        match_ids = get_match_info(team, season)['id']
        side = get_match_info(team, season)['side']

        for info in zip(match_ids, side):
            temp = get_match_data(info[0], info[1])
            temp['key'] = team
            single_data = single_data.append(temp)

    for team in teams:
        all_data_temp = single_data[single_data.key == team]
        all_data_temp['matchday'] = all_data_temp.date.apply(lambda x: x.split()[0])
        all_data_temp['matchday'] = all_data_temp['matchday'].astype('category')
        all_data_temp['matchday'] = all_data_temp['matchday'].cat.codes
        all_data_temp['matchday'] = all_data_temp['matchday'] + 1
        all_data = all_data.append(all_data_temp)

    all_data['X'] = all_data['X'].astype('float')
    all_data['Y'] = all_data['Y'].astype('float')
    all_data['X'] = all_data['X'].apply(lambda x:x*100)
    all_data['Y'] = all_data['Y'].apply(lambda x:x*100)

    return all_data

def players_stats(season, league):

    season = str(season)
    all_player_info = pd.DataFrame()
    teams = get_teams_names(season, league)

    for team in teams:
        base_url = 'https://understat.com/team/'+team+'/'
        match = season
        url = base_url + match
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "html.parser")
        scripts = soup.find_all('script')

        players_info = scripts[3].string
        
        ind_start = players_info.index("('")+2
        ind_end = players_info.index("')")

        json_player_data = players_info[ind_start:ind_end]
        json_player_data = json_player_data.encode('utf8').decode('unicode_escape')

        player_data = json.loads(json_player_data)
        player_info = pd.DataFrame(player_data)

        player_info['id'] = player_info['id'].astype('int')
        player_info['games'] = player_info['games'].astype('int')
        player_info['time'] = player_info['time'].astype('int')
        player_info['goals'] = player_info['goals'].astype('int')
        player_info['xG'] = player_info['xG'].astype('float')
        player_info['assists'] = player_info['assists'].astype('int')
        player_info['xA'] = player_info['xA'].astype('float')
        player_info['shots'] = player_info['shots'].astype('int')
        player_info['key_passes'] = player_info['key_passes'].astype('int')
        player_info['yellow_cards'] = player_info['yellow_cards'].astype('int')
        player_info['red_cards'] = player_info['red_cards'].astype('int')
        player_info['npg'] = player_info['npg'].astype('int')
        player_info['npxG'] = player_info['npxG'].astype('float')
        player_info['xGChain'] = player_info['xGChain'].astype('float')
        player_info['xGBuildup'] = player_info['xGBuildup'].astype('float')

        all_player_info = all_player_info.append(player_info)

    return all_player_info