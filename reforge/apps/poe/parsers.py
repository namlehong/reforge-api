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


def bench_craft_row_parser(rows):
    for row in rows:
        cols = row.find_all('td')

        # modifier details
        mod = cols[1].text
        # cost for the craft section
        cost = cols[2]
        # item types for crafts that can be applied on
        item_types = cols[3].text.split(', ')
        # unlock zones
        unlock = cols[4].text

        cost = cost.get_text()
        cost2 = cost.split('x ')
        # if there are 2 or more orbs (it appears that it is only these crafts, for now)
        # this is really not optimized but as of now I don't know other solutions
        # ~Remi
        if len(cost2) > 2:
            cost2[1] = cost2[1].replace('Instilling Orb5', 'Instilling Orb, 5')
            cost2 = [word for line in cost2 for word in line.split(', ')]
            cost2 = [cost2[i * 2:(i + 1) * 2]
                     for i in range((len(cost2) + 2 - 1) // 2)]

        # reverse so craft name comes first, amount later, may not work on multi crafts
        fin_cost = (cost2[::-1])

        yield {
            'mod': mod,
            'cost': fin_cost,
            'item_types': item_types,
            'unlock': unlock
        }


def bench_craft_poe_db_parser(html):
    soup = BeautifulSoup(html, 'html.parser')
    bench = soup.find('div', id="CraftingBench")
    rows = bench.find('table').find('tbody').find_all('tr')
    return bench_craft_row_parser(rows)
