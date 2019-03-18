"""
Script to update and re-generate plots.
The script is runs once a day (hour?) and updates the plots on the website.

The general process for this is:

1) git pull
2) pull the data from the overwatch api
3) update the relevent json files
4) git commit with auto generated message
5) git push to deploy it
"""

import time
from datetime import datetime as dt

from tqdm import tqdm

import owl
import util


def update_ring(teams, links):
    "given new teams and links, load and update the ring.json file"
    ring = util.load("../owl/data/ring.json")

    for d in ring['data']:
        if d['name'] == 'tree':
            d['values'] = teams
        elif d['name'] == 'dependencies':
            d['values'] = links

    util.dump(ring, '../owl/data/ring.json')


def main():
    while True:
        now = dt.now()

        # pull any changes
        util.pull()

        data = owl.get_match_data(cached=False)
        content = data['content']
        teams, links = owl.get_team_wins(content)
        update_ring(teams, links)

        # push to update the site
        util.push()

        # now we need to figure out how long to sleep before the next matce
        game_dates = owl.get_match_datetimes(content)

        for d in game_dates:
            next_match = d
            td = d - now
            delay = int(td.total_seconds() + 3600*2)
            if delay > 0:
                break

        if delay < 0:
            # if we reach this point then we have passed the end of the season
            break

        print(f"sleeping {delay} seconds until two hours after {next_match}")

        for i in tqdm(range(delay)):
            time.sleep(1)

if __name__ == "__main__":
    main()

