import requests

client = requests.session()
client.headers = {
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}

def extract_line(item):
    return item['currencyTypeName'], item['chaosEquivalent']

def currency_overview(league):
    payload = {
        'league': league,
        'type': 'Currency',
        'language': 'en'
    }

    r = client.get('https://poe.ninja/api/data/CurrencyOverview', params=payload)

    return list(map(extract_line, r.json()['lines']))
