from urllib.parse import urljoin

import requests
from requests import Session
from django.conf import settings

client = requests.session()
client.headers = {
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'OAuth reforge/1.0.0 (contact: namlehong@gmail.com) StrictMode',
}


def auth_error_handler(r, *args, **kwargs):
    data = r.json()
    if data.get('error'):
        raise Exception(data.get('error_description'))


class GggApi(Session):
    def __init__(self, client_id=None, client_secret=None, token=None, base_url=None, scope=None, *args, **kwargs):
        self.client_id = client_id or settings.POE_AUTH_CLIENT
        self.client_secret = client_secret or settings.POE_AUTH_SECRET
        self.base_url = base_url or 'https://www.pathofexile.com/'
        self.token = token
        self.scope = scope or 'account:profile account:characters account:stashes'
        self.redirect_url = 'https://reforge.local.poe.dev/poe-auth'
        super(GggApi, self).__init__()
        self.headers.update({
            'User-Agent': 'OAuth reforge/1.0.0 (contact: namlehong@gmail.com) StrictMode',
        })

    @property
    def access_token(self):
        return self.token.get('access_token')

    def request(self, method, url, *args, **kwargs):
        if url.startswith('api'):
            kwargs.update(headers={
                'Authorization': 'Bearer {access_token}'.format(**self.token)
            })

        url = urljoin(self.base_url, url)
        return super(GggApi, self).request(method, url, *args, **kwargs)

    def get_token(self, code):
        data = {
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope,
            'redirect_uri': self.redirect_url
        }
        self.token = self.post('/oauth/token', data, hooks={'response': auth_error_handler}).json()
        return self.token

    def profile(self):
        return self.get('api/profile').json()

    def character(self, character_name=None):
        url = 'api/character'
        if character_name:
            url = 'api/character/{}'.format(character_name)
        return self.get(url).json()

    def stash(self, league, stash_id=None, substash_id=None):
        url = 'api/stash/{}'.format(league)
        if stash_id:
            url = 'api/stash/{}/{}/{}'.format(league, stash_id, substash_id)
            if substash_id:
                url = 'api/stash/{}/{}'.format(league, stash_id)
        return self.get(url).json()


def get_token(code):
    data = {
        'code': code,
        'grant_type': 'authorization_code',
        'client_id': settings.POE_AUTH_CLIENT,
        'client_secret': settings.POE_AUTH_SECRET,
        'scope': 'account:profile account:characters account:stashes',
        'redirect_uri': 'https://reforge.local.poe.dev/poe-auth'
    }

    r = client.post('https://www.pathofexile.com/oauth/token', data=data).json()

    if r.get('error'):
        raise Exception(r.get('error_description'))

    return r


def profile(token):
    headers = {
        'Authorization': '%s %s' % ('Bearer', token)
    }
    return client.get('https://www.pathofexile.com/api/profile', headers=headers).json()


def characters(token):
    headers = {
        'Authorization': '%s %s' % ('Bearer', token)
    }

    return client.get('https://www.pathofexile.com/api/character', headers=headers).json()


def username(code):
    r = get_token(code)
    r2 = profile(r.get('access_token'))

    if r2.get('error'):
        raise Exception(r.get('error').get('message'))

    return r2.get('name')
