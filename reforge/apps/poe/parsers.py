from bs4 import BeautifulSoup


def harvest_row_parser(rows):
    for row in rows:
        cols = row.find_all('td')

        seed_tier = int(cols[0].text)
        monster_name = cols[1].text
        crafts = cols[2]

        for option in crafts.select('li'):
            options = []
            keywords = [e.text for e in option.select('span') if e.text != ""]
            description = option.text

            options.append(keywords)

            seed_name, seed_id = monster_name.split('#')

            yield {
                'tier': seed_tier,
                'seed_name': seed_name,
                'seed_id': int(seed_id),
                'description': description,
                'keywords': options
            }


def harvest_craft_poe_db_parser(html):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find('table').find('tbody').find_all('tr')
    return harvest_row_parser(rows)
