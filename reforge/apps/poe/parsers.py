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

    output = []

    tbl = soup.find('table')
    for team in tbl.find_all('tbody'):
        rows = team.find_all('tr')
        for seeds in rows:
            # seed tier
            seed_tier = seeds.find_all('td')[0].text
            # monster names
            monster_names = seeds.find_all('td')[1].text
            for crafts in seeds.find_all('td')[2]:
                # get descriptions
                try:
                    desc = (crafts.text)
                    print(desc)
                except AttributeError:
                    skip

                # get keywords and append into a list
                keyword_list = []
                try:
                    mods = crafts.select('span')
                except AttributeError:
                    skip
                else:
                    for kw in mods:
                        keyw = (kw.text)
                        keyword_list.append(keyw)
                    keyword_list = [i for i in keyword_list if i]
                    try:
                        len(keyword_list)
                    except TypeError:
                        continue
                    else:
                        if (len(keyword_list)) > 0:

                            craft_data = {
                                'tier': seed_tier,
                                'monster_name': monster_names,
                                'description': desc,
                                'options': keyword_list
                            }
                            #result = ('<"tier": {}, "monster_name": "{}", "description": "{}", "keywords": {}>,'.format(seed_tier, monster_names, desc, keyword_list))
                            print(craft_data)
                            output.append(craft_data)
                            #result = result.replace('<', '{')
                            #result = result.replace('>', '}')
                            # print(result)

    with open(r"harvestjson.json", 'a') as txtFile:
        json.dump((output), txtFile)
