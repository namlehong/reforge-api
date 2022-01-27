import requests
from django.conf import settings

client = requests.session()
client.headers = {
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'OAuth reforge/1.0.0 (contact: namlehong@gmail.com) StrictMode',
}


def auth(code):
    data = {
        'code': code,
        'grant_type': 'authorization_code',
        'client_id': settings.POE_AUTH_CLIENT,
        'client_secret': settings.POE_AUTH_SECRET,
        'scope': 'account:profile account:characters account:stashes',
        'redirect_uri': 'https://reforge.local.poe.dev/poe-auth'
    }

    return client.post('https://www.pathofexile.com/oauth/token', data=data).json()


def profile(token):
    headers = {
        'Authorization': '%s %s' % ('Bearer', token)
    }
    print(headers)
    return client.get('https://www.pathofexile.com/api/profile', headers=headers).json()


def username(code):
    r = auth(code)

    print(r)

    if r.get('error'):
        raise Exception(r.get('error_description'))

    r2 = profile(r.get('access_token'))

    if r2.get('error'):
        raise Exception(r.get('error').get('message'))

    return r2.get('name')
