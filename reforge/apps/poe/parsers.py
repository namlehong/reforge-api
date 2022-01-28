from unittest import skip
import requests
import json
import os
from bs4 import BeautifulSoup


def harvest_craft_poe_db_parser(html):
    #raise NotImplementedError
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    url = "https://poedb.tw/us/HarvestSeed"
    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')

    out = []

    table = soup.find('table')
    body = table.find('tbody')
    rows = body.find_all('tr')

    for row in rows:
        cols = row.find_all('td')

        seed_tier = cols[0].text
        monster_name = cols[1].text
        crafts = cols[2]
        # print(crafts)

        for option in crafts.select('li'):
            options = []
            keywords = [e.text for e in option.select('span') if e.text != ""]
            description = option.text

            options.append(keywords)

            craft_data = {
                'tier': seed_tier,
                'monster_name': monster_name,
                'description': description,
                'options': options
            }

            out.append(craft_data)

    return out


# open json and read, if it doesn't contain anything, dump data in.
"""#with open(r"harvestjson.json", 'r') as txtFile:
    try:
        content = json.load(txtFile)
    except json.JSONDecodeError:
        with open(r"harvestjson.json", 'a') as txtFile:
            json.dump((output), txtFile)
    else:
        print("HarvestJson already has contents")"""
