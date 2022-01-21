import pandas as pd
pd.set_option('mode.chained_assignment',None)

###################################################
####################           ####################
#################### ANALYTICS ####################
####################           ####################
###################################################

def open_season_data(year, league):
    data = pd.read_csv('data/{}/{}_season_{}.csv'.format(league, league, year), parse_dates=['date'], index_col='date').drop(columns=['Unnamed: 0'])
    return data

def open_squads_data(year, league):
    data = pd.read_csv('data/{}/squads_info_{}.csv'.format(league, year)).drop(columns=['Unnamed: 0'])
    return data

def open_value_squad_position_data(year, league):
    data = pd.read_csv('data/{}/value_squad_position_{}.csv'.format(league, year)).drop(columns=['Unnamed: 0'])
    return data

###################################################

def goals_scored_avg_time(team, year, league, home=False, away=False, all=False):

    data = open_season_data(year, league)

    if home == True:
        result = data[(data.h_team == team) & (data.result == 'Goal') & (data.key == team)]
        result['match'] = result['h_team'] + " - " + result['a_team']
        result = result.groupby(
            [result[(result.h_team == team) & (result.result == 'Goal') & (result.key == team)].index,
            result.match,
            result.matchday]
        ).minute.mean()
        return result

    if away == True:
        result = data[(data.a_team == team) & (data.result == 'Goal') & (data.key == team)]
        result['match'] = result['h_team'] + " - " + result['a_team']
        result = result.groupby(
            [result[(result.a_team == team) & (result.result == 'Goal') & (result.key == team)].index,
            result.match,
            result.matchday]
        ).minute.mean()
        return result

    if all == True:
        result_home = data[(data.h_team == team) & (data.result == 'Goal') & (data.key == team)]
        result_home['match'] = result_home['h_team'] + " - " + result_home['a_team']
        result_home = result_home.groupby(
            [result_home[(result_home.h_team == team) & (result_home.result == 'Goal') & (result_home.key == team)].index,
            result_home.match,
            result_home.matchday]
        ).minute.mean()

        result_away = data[(data.a_team == team) & (data.result == 'Goal') & (data.key == team)]
        result_away['match'] = result_away['h_team'] + " - " + result_away['a_team']
        result_away = result_away.groupby(
            [result_away[(result_away.a_team == team) & (result_away.result == 'Goal') & (result_away.key == team)].index,
            result_away.match,
            result_away.matchday]
        ).minute.mean()

        result_all = result_home.append(result_away)#.sort_index(ascending=True)
        result_all = pd.DataFrame(result_all).reset_index()

        return result_all

def goals_scored(team, year, league, home=False, away=False, all=False):

    data = open_season_data(year, league)

    if home == True:
        result = data[(data.h_team == team) & (data.result == 'Goal') & (data.key == team)]
        result['match'] = result['h_team'] + " - " + result['a_team']
        result = result.groupby(
            [result[(result.h_team == team) & (result.result == 'Goal') & (result.key == team)].index,
            result.match,
            result.matchday]
        ).h_goals.mean()
        return result

    if away == True:
        result = data[(data.a_team == team) & (data.result == 'Goal') & (data.key == team)]
        result['match'] = result['h_team'] + " - " + result['a_team']
        result = result.groupby(
            [result[(result.a_team == team) & (result.result == 'Goal') & (result.key == team)].index,
            result.match,
            result.matchday]
        ).h_goals.mean()
        return result

    if all == True:
        result_home = data[(data.h_team == team) & (data.result == 'Goal') & (data.key == team)]
        result_home['match'] = result_home['h_team'] + " - " + result_home['a_team']
        result_home = result_home.groupby(
            [result_home[(result_home.h_team == team) & (result_home.result == 'Goal') & (result_home.key == team)].index,
            result_home.match,
            result_home.matchday]
        ).h_goals.mean()

        result_away = data[(data.a_team == team) & (data.result == 'Goal') & (data.key == team)]
        result_away['match'] = result_away['h_team'] + " - " + result_away['a_team']
        result_away = result_away.groupby(
            [result_away[(result_away.a_team == team) & (result_away.result == 'Goal') & (result_away.key == team)].index,
            result_away.match,
            result_away.matchday]
        ).h_goals.mean()

        result_all = result_home.append(result_away).sort_index(ascending=True)
        result_all = pd.DataFrame(result_all).reset_index()

        return result_all

def goals_conceded_avg_time(team, year, league, home=False, away=False, all=False):

    data = open_season_data(year, league)

    if home == True:
        result = data[(data.h_team == team) & (data.result == 'Goal') & (data.key != team)]
        result['match'] = result['h_team'] + " - " + result['a_team']
        result = result.groupby(
            [result[(result.h_team == team) & (result.result == 'Goal') & (result.key != team)].index,
            result.match,
            result.matchday]
        ).minute.mean()
        return result

    if away == True:
        result = data[(data.a_team == team) & (data.result == 'Goal') & (data.key != team)]
        result['match'] = result['h_team'] + " - " + result['a_team']
        result = result.groupby(
            [result[(result.a_team == team) & (result.result == 'Goal') & (result.key != team)].index,
            result.match,
            result.matchday]
        ).minute.mean()
        return result

    if all == True:
        result_home = data[(data.h_team == team) & (data.result == 'Goal') & (data.key != team)]
        result_home['match'] = result_home['h_team'] + " - " + result_home['a_team']
        result_home = result_home.groupby(
            [result_home[(result_home.h_team == team) & (result_home.result == 'Goal') & (result_home.key != team)].index,
            result_home.match,
            result_home.matchday]
        ).minute.mean()

        result_away = data[(data.a_team == team) & (data.result == 'Goal') & (data.key != team)]
        result_away['match'] = result_away['h_team'] + " - " + result_away['a_team']
        result_away = result_away.groupby(
            [result_away[(result_away.a_team == team) & (result_away.result == 'Goal') & (result_away.key != team)].index,
            result_away.match,
            result_away.matchday]
        ).minute.mean()

        result_all = result_home.append(result_away)#.sort_index(ascending=True)
        result_all = pd.DataFrame(result_all).reset_index()

        return result_all

def goals_conceded(team, year, league, home=False, away=False, all=False):

    data = open_season_data(year, league)

    if home == True:

        result = data[(data.h_team == team) & (data.result == 'Goal') & (data.key != team)]
        result['match'] = result['h_team'] + " - " + result['a_team']
        result = result.groupby(
            [data[(data.h_team == team) & (data.result == 'Goal') & (data.key != team)].index,
            result.match,
            result.matchday]
        ).a_goals.mean()
        return result

    if away == True:
        result = data[(data.a_team == team) & (data.result == 'Goal') & (data.key != team)]
        result['match'] = result['h_team'] + " - " + result['a_team']
        result = result.groupby(
            [data[(data.a_team == team) & (data.result == 'Goal') & (data.key != team)].index,
            result.match,
            result.matchday]
        ).h_goals.mean()
        return result

    if all == True:
        result_home = data[(data.h_team == team) & (data.result == 'Goal') & (data.key != team)]
        result_home['match'] = result_home['h_team'] + " - " + result_home['a_team']
        result_home = result_home.groupby(
            [data[(data.h_team == team) & (data.result == 'Goal') & (data.key != team)].index,
            result_home.match,
            result_home.matchday]
        ).a_goals.mean()

        result_away = data[(data.a_team == team) & (data.result == 'Goal') & (data.key != team)]
        result_away['match'] = result_away['h_team'] + " - " + result_away['a_team']
        result_away = result_away.groupby(
            [data[(data.a_team == team) & (data.result == 'Goal') & (data.key != team)].index,
            result_away.match,
            result_away.matchday]
        ).h_goals.mean()

        result_all = result_home.append(result_away).sort_index(ascending=True)
        result_all = pd.DataFrame(result_all).reset_index()

        return result_all

def max_scorers(team, matchdays, year, league):

    def goals(data, team, matchdays, home=False, away=False, all=False):
        result_home = pd.DataFrame(data[(data.h_team == team) & (data.result == 'Goal') & (data.key == team) & (data.matchday <= matchdays)].groupby(['player', 'player_id']).h_goals.count().sort_values(ascending=False))
        result_away = pd.DataFrame(data[(data.a_team == team) & (data.result == 'Goal') & (data.key == team) & (data.matchday <= matchdays)].groupby(['player', 'player_id']).a_goals.count().sort_values(ascending=False))
        result = pd.concat([result_home, result_away], axis=1).fillna(0).sum(axis=1).sort_values(ascending=False)
        return result
    
    player_info = open_squads_data(year, league)[['player_name', 'id', 'position']].rename(columns={'id': 'player_id'})
    goals_info = pd.DataFrame(goals(open_season_data(year, league), team, matchdays, all=True))
    result = pd.merge(player_info, goals_info, on=['player_id'])

    return result