from datetime import datetime
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

### START TRANSFERMARKT

def get_ids(league, season):
    base_url = 'https://www.transfermarkt.com/{}/startseite/wettbewerb/ES1/plus/?saison_id={}'.format(league, season)
    url = base_url
    res = requests.get(url)
    res = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    soup = BeautifulSoup(res.content, "html.parser")
    data = soup.find_all("td", {"class": "zentriert no-border-rechts"})
    id = []
    ids = []

    for team in range(len(data)):

        for i in data[team].findChildren():
            if i.name == 'img':
                id.append(i.attrs['alt'])
            if i.name == 'a':
                id.append(i.attrs['href'].split('/')[4])
                id.append(i.attrs['href'].split('/')[1])
            
        ids.append(id)
        id = []

    teams_ids = pd.DataFrame(ids).drop_duplicates().rename(columns={0: 'id', 1: 'href-team', 2: 'team'})  
    
    return teams_ids

def get_value_positions(league, season):

    all_data = pd.DataFrame()
    teams_ids = get_ids(league, season)

    for info in teams_ids.itertuples():
        href_team = info[2]
        id = info[1]
        base_url = 'https://www.transfermarkt.com/{}/kader/verein/{}/plus/0/galerie/0?saison_id={}'.format(href_team, id, season)
        url = base_url
        res = requests.get(url)
        res = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        soup = BeautifulSoup(res.content, "html.parser")
        data = soup.find_all("div", {"class": "box"})

        temp = []
        all = []

        parent = data[1].find_all('tr', recursive=True)
        for number in range(len(parent)):
            for child in parent[number].findChildren():
                temp.append(child.get_text())

            if '\xa0' in temp:
                temp.remove('\xa0')
            all.append(temp)
            temp = []

        data = pd.DataFrame(all)
        data.columns = data.iloc[0]
        data = data.iloc[1:].reset_index(drop=True)
        data['team'] = info[3]

        all_data = all_data.append(data)
        all_data['season'] = season

    return all_data

def get_headers(url):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.content, "html.parser")
    return soup

def market_value(league, season):
    all_data = pd.DataFrame()
    teams_ids = get_ids(league, season)

    #yw1
    #   https://www.transfermarkt.co.uk/sevilla-fc/kader/verein/368/saison_id/2021/plus/1

    test_team = 'sevilla-fc'
    test_id = '368'
    test_year = '2021'
    base_url = 'https://www.transfermarkt.co.uk/{}/kader/verein/{}/saison_id/{}/plus/1'.format(test_team, test_id, test_year)

    soup = get_headers(base_url)
    data = soup.find_all("div", {"id": "yw1"})

    number_lst = []
    for temp_list in data:
        for number in temp_list.find_all('div', {'class': 'rn_nummer'}):
            number_lst.append(number.text)

    name_lst = []
    for temp_list in data:
        for name in temp_list.find_all('td', {'class': 'hauptlink'}):
            for link in name.find_all('a'):
                name_lst.append(link.text.strip())
        

    position_lst = []
    for position in soup.select('td.posrela tr:nth-child(2) td'):
        position_lst.append(position.text.strip())

    bday_lst = []
    for bday in soup.select('tbody tr td:nth-child(3)'):
        bday_temp = bday.text.strip()[:-4]
        if bday_temp == '':
            pass
        else:
            bday_temp = datetime.strptime(bday_temp, '%b %d, %Y').strftime('%Y/%m/%d')
            bday_lst.append(bday_temp)

    height_lst = []
    for height in soup.select('tbody tr td:nth-child(5)'):
        height_lst.append(float(height.text.replace(' m', '').replace(',', '.')))

    leading_foot_lst = []
    for leading_foot in soup.select('tbody tr td:nth-child(6)'):
        leading_foot_lst.append(leading_foot.text.strip())

    joined_lst = []
    for joined in soup.select('tbody tr td:nth-child(7)'):
        joined_temp = joined.text.strip()
        if joined_temp == '-':
            pass
        else:
            joined_temp = datetime.strptime(joined_temp, '%b %d, %Y').strftime('%Y/%m/%d')
            joined_lst.append(joined_temp)

    end_contract_lst = []
    for end_contract in soup.select('tbody tr td:nth-child(9)'):
        end_contract_temp = end_contract.text.strip()
        if end_contract_temp == '-':
            pass
        else:
            end_contract_temp = datetime.strptime(end_contract_temp, '%b %d, %Y').strftime('%Y/%m/%d')
            end_contract_lst.append(end_contract_temp)

    value_lst = []
    char_cons = []
    char_cons_value = ''
    for value in soup.select('tbody tr td:nth-child(10)'):
        value_temp = value.text
        for s in list(value_temp):
            if s.isdigit():
                char_cons.append(s)

            elif s == '.':
                char_cons.append(s)

        for i in char_cons:
            char_cons_value = char_cons_value + i

        if char_cons_value[-1] == '.':
            char_cons_value = char_cons_value[:-1]
            char_cons_value = '0.' + char_cons_value

        char_cons_value = float(char_cons_value)
        value_lst.append(char_cons_value)

        char_cons_value = ''
        char_cons = []

    dict = {'number': number_lst, 'name': name_lst, 'position': position_lst, 'born': bday_lst, 'height': height_lst, 'leading_foot': leading_foot_lst, 'joined': joined_lst, 'end_contract': end_contract_lst, 'market_value': value_lst} 
    market_value_df = pd.DataFrame(list(dict.values()), index=dict.keys()).T

    return market_value_df

### END TRANSFERMARKT