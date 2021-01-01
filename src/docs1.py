"""SNaP OneDrive Report Aggregator

# Resources
1. Docs: https://docs.microsoft.com/en-us/onedrive/developer/rest-api/
getting-started/msa-oauth?view=odsp-graph-online

# Minor to-do's
- Alternative to have user paste this into browser and copy/paste the token?
- how make code and token last longer?:
  - https://docs.microsoft.com/en-us/onedrive/developer/rest-api/getting-started/graph-oauth?view=odsp-graph-online#step-3-get-a-new-access-token-or-refresh-token
  - can update token max life via powershell only
"""
import os
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs
from typing import Dict
from pprint import pprint


ROOT_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..')
CODE_FILE_PATH = os.path.join(ROOT_DIR, 'code.env')
TOKEN_FILE_PATH = os.path.join(ROOT_DIR, 'token.env')

CONFIG = {
    # 'redirect_uri': 'msal3edae2b4-0150-450a-b8b6-bf2ee70c325f://auth',
    # 'redirect_uri':
    #     'https://login.microsoftonline.com/common/oauth2/nativeclient',
    'redirect_uri': 'https://login.live.com/oauth20_desktop.srf',
    'client_id': os.getenv('ATTEMPT2_APP_ID'),
    # 'client_id': os.getenv('CLIENT_ID'),
    # 'client_secret': os.getenv('ATTEMPT2_TENANT_ID'),
    # secret id; 74492a9c-175a-4418-b381-7ad535c38314
    # secret val; wCv35Dzw5AFgOMbE._CJ-EO-4C1-jfFVJH
    'client_secret': os.getenv('n/a', 'wCv35Dzw5AFgOMbE._CJ-EO-4C1-jfFVJH'),
    'api_base_url': 'https://api.onedrive.com/v1.0/',
    # 'scopes': ['onedrive.readwrite']
    'scopes': ['Files.ReadWrite.All']
}
client_id = CONFIG['client_id']
scope = CONFIG['scopes'][0]
redirect_uri = CONFIG['redirect_uri']
auth_url_base = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
fetch_url_base = 'https://graph.microsoft.com/v1.0/'
# auth_url_base = 'https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize'
# wont work w/ graph api:
# auth_url_base = 'https://login.live.com/oauth20_authorize.srf'
# token:
# auth_url = f'{auth_url_base}?client_id={client_id}' \
#       f'&scope={scope}&response_type=token&redirect_uri={redirect_uri}'
# code:
auth_url = f'{auth_url_base}?client_id={client_id}' \
           f'&scope={scope}&response_type=code&redirect_uri={redirect_uri}'
# https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={client_id}&scope={scope}&response_type=token&redirect_uri={redirect_uri}
# https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?client_id=3edae2b4-0150-450a-b8b6-bf2ee70c325f&response_type=token&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient&scope=onedrive.readwrite
code_token_headers = {
    'client_id': CONFIG['client_id'],
    'redirect_uri': CONFIG['redirect_uri'],
    # 'client_secret': CONFIG['client_secret'],
    'code': None,
    'grant_type': 'authorization_code'
}
CONFIG['fetch_headers'] = {
    'Host': 'graph.microsoft.com',
    # 'Authorization': 'Bearer {}'.format(token)
    'Authorization': 'Bearer {}'
}
CONFIG['token'] = 'token'
CONFIG['auth_url'] = auth_url
CONFIG['code_token_url'] = auth_url
CONFIG['code_token_headers'] = code_token_headers


def get_code(auth_url: str) -> str:
    """Get code"""
    # 1. Auth: Get code
    # - https://docs.microsoft.com/en-us/onedrive/developer/rest-api/getting-started/graph-oauth?view=odsp-graph-online#step-1-get-an-authorization-code
    # response1 = requests.get(config['url'])
    # Needs to be copy/pasted in browser I believe:
    msg = '2. In "step 1", you should either be asked to ' \
          'log in or auto-logged-in. After that, you should be redirected to ' \
          'a new blank page, and the URL in the address bar should look ' \
          'similar to this: \nhttps://login.live.com/oauth20_desktop.srf?' \
          'code=M.R3_BL2.64370af9-d97a-0e5c-89f8-458184fe1ba8&lc=1033\n\n' \
          'Copy and paste that entire URL here: '
    print('1. Open URL in browser to get auth code: \n', auth_url, '\n')
    url = input(msg)
    parsed = urlparse.urlparse(url)
    code = parse_qs(parsed.query)['code']
    if not code:
        raise RuntimeError('No code found. Url was: ', url)
    return code


def get_token(headers: Dict) -> str:
    """Get token"""
    # 2. redeem token from code
    # - https://docs.microsoft.com/en-us/onedrive/developer/rest-api/getting-started/graph-oauth?view=odsp-graph-online#step-2-redeem-the-code-for-access-tokens
    response: Dict = requests.post(
        'https://login.microsoftonline.com/common/oauth2/v2.0/token',
        data=headers).json()
    return response['access_token']


def download_files(headers: Dict):
    """Download files"""
    # 3. fetch resources
    # - https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/drive_sharedwithme?view=odsp-graph-online
    endpoint = 'me/drive/sharedWithMe'
    fetch_url = fetch_url_base + endpoint
    response: Dict = requests.get(
        fetch_url,
        headers=headers).json()
    if 'error' in response.keys():
        raise RuntimeError(response)
    print('Fetch: ' + fetch_url)
    pprint(response)
    print()


def run(config=CONFIG):
    """Run"""
    try:
        headers = config['fetch_headers']
        with open(TOKEN_FILE_PATH, 'r') as file:
            token = file.read()
        headers['Authorization'] = headers['Authorization'].format(token)
        download_files(headers)
    except (RuntimeError, FileNotFoundError):
        # 1. code
        code = get_code(config['auth_url'])
        with open(CODE_FILE_PATH, 'w') as file:
            file.write(code)
        headers = config['code_token_headers']
        headers['code'] = code
        # 2. token
        token = get_token(headers)
        with open(TOKEN_FILE_PATH, 'w') as file:
            file.write(token)
        headers = config['fetch_headers']
        headers['Authorization'] = headers['Authorization'].format(token)
        # 3. download
        download_files(headers)


if __name__ == '__main__':
    run()
