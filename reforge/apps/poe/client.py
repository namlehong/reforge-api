import requests
import re
import json
from bs4 import BeautifulSoup

client = requests.session()
client.headers = {
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}


def create_client(session_id):
    session = requests.session()
    session.headers = {
        'Cookie': 'POESESSID=%s;' % session_id
    }

    return session


def get_account_info(session: requests.Session):
    html = session.get('https://www.pathofexile.com/account/view-profile').text

    account = re.findall(r'new\sA\((.*)\);', html)

    if account:
        account = json.loads(account[0])
    else:
        account = {}

    character = re.findall(r'new\sC\((.*)\);', html)

    if character:
        character = json.loads(character[0])
    else:
        character = {}

    challenge = re.findall(r'completed(\d+)', html)

    if challenge:
        challenge = {'challenge': challenge[0]}
    else:
        challenge = {}

    return {**account, **character, **challenge}


def public_profile(account):
    character_html = client.get('https://www.pathofexile.com/account/view-profile/%s/characters' % account).text
    account_html = client.get('https://www.pathofexile.com/account/view-profile/%s' % account).text

    account = re.findall(r'new\sA\((.*)\);', character_html)

    if account:
        account = json.loads(account[0])
    else:
        account = {}

    character = re.findall(r'new\sC\((.*)\);', character_html)

    if character:
        character = json.loads(character[0])
    else:
        character = {}

    challenge = re.findall(r'Challenges completed: (\d+/\d+)', account_html)

    if challenge:
        challenge = {'challenge': challenge[0]}
    else:
        challenge = {}

    achievements = re.findall(r'Achievements completed: (\d+/\d+)', account_html)

    if achievements:
        achievements = {'achievements': achievements[0]}
    else:
        achievements = {}

    joined = re.findall(r'<strong>Joined:</strong>\n(.*)<br>', account_html)

    if joined:
        joined = {'joined': joined[0].strip()}
    else:
        joined = {}

    return {**account, **challenge, **achievements, **joined, 'last_character': character}
