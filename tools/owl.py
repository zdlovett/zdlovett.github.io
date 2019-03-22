"""
Helpers for getting and working with OWL API data
"""
import os
import json
import requests
from datetime import datetime as dt

import util

from IPython import embed


URLS = {
    "matches" : "https://api.overwatchleague.com/matches",
    "teams" : "https://api.overwatchleague.com/teams"
}

def get_data(url, cached=False):
    if cached:
        match_data = util.load(os.path.split(url)[1])
    else:
        response = requests.get(url)
        match_data = json.loads(response.content)
    return match_data

def get_team_info(cached=False):
    data = get_data(URLS['teams'], cached=cached)

    divisions = data['owl_divisions']
    teams = [c['competitor'] for c in data['competitors']]

    embed()

    return teams


def get_team_wins(cached=False):
    matches = get_data(URLS['matches'], cached=cached)
    content = matches['content']

    "Build vega compatible json outputs given the match content"
    links = []
    teams = []
    results = [] # team -> team ordering

    for match in content:
        competitors = [team['name'] for team in match['competitors']]
        teams.extend(competitors)

        try:
            winner = match['winner']['name']
        except KeyError:
            start = match['startDate'] / 1000
            start = dt.fromtimestamp(start)
            #print(f"No winner for match on {start}")
            continue

        competitors.remove(winner)
        results.append((winner, competitors[0]))

    teams = list(set(teams))
    teams = [{'id':i+1, 'name':name, 'parent': 0} for i, name in enumerate(teams)]
    teams.append({'id':0, 'name':'root'})

    team_to_id = {t['name']:t['id'] for t in teams}

    for winner, loser in results:
        link = {
            "source" : team_to_id[winner],
            "target" : team_to_id[loser]
        }
        links.append(link)

    return teams, links


def get_match_datetimes(content):
    "given the content, return the match datetimes and the teams playing"
    game_dates = []
    for match in content:
        start = match['startDate'] / 1000
        start = dt.fromtimestamp(start)
        game_dates.append(start)

    return game_dates



if __name__ == "__main__":
    team_wins = get_team_wins(cached=True)

    teams = get_team_info()

