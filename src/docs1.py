"""https://docs.microsoft.com/en-us/onedrive/developer/rest-api/
getting-started/msa-oauth?view=odsp-graph-online"""
import os
import requests


CONFIG = {
    # 'redirect_uri': 'msal3edae2b4-0150-450a-b8b6-bf2ee70c325f://auth',
    # 'redirect_uri':
    #     'https://login.microsoftonline.com/common/oauth2/nativeclient',
    'redirect_uri': 'https://login.live.com/oauth20_desktop.srf',
    'client_id': os.getenv('ATTEMPT2_APP_ID'),
    # 'client_id': os.getenv('CLIENT_ID'),
    # 'client_secret': os.getenv('ATTEMPT2_TENANT_ID'),
    'client_secret': os.getenv('n/a', None),
    'api_base_url': 'https://api.onedrive.com/v1.0/',
    'scopes': ['onedrive.readwrite']
}
client_id = CONFIG['client_id']
scope = CONFIG['scopes'][0]
redirect_uri = CONFIG['redirect_uri']
url_base = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
# url_base = 'https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize'
# wont work w/ graph api:
# url_base = 'https://login.live.com/oauth20_authorize.srf'
# token:
# auth_url = f'{url_base}?client_id={client_id}' \
#       f'&scope={scope}&response_type=token&redirect_uri={redirect_uri}'
# code:
auth_url = f'{url_base}?client_id={client_id}' \
      f'&scope={scope}&response_type=code&redirect_uri={redirect_uri}'
# https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={client_id}&scope={scope}&response_type=token&redirect_uri={redirect_uri}
# https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?client_id=3edae2b4-0150-450a-b8b6-bf2ee70c325f&response_type=token&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient&scope=onedrive.readwrite
token = 'EwAgA61DBAAUmcDj0azQ5tf1lkBfAvHLBzXl5ugAAYbGY97P2qKBjR6xnz5dMainhFptz4YN5Qvai6sQOoFNt/FkJiH3I45HTJwpQc%2b12cN9VXklg04qh%2bh%2b9R2HnwEb%2bXhhhxVA4pHzKLX98yzJ0zPMNqaOBwfgUUKcZ1Iedhpk2%2bkjv/jTV9tj6YY2pcO1ajUa3Y%2b1GCwI0IoNCJ864y/woR6uxolBU%2boHeMIrSirY6ISZP9cxmSweG%2bGiFnTY817fDdO4GX0KUayzhi19kNa5gmYuRlVLz0PGQDCNueE7RtfnXpeC2IN49JYjdHDe4RAdbIwEtUuuhSYrBQ558AAewpkxH2va9xbI4fHKX6GocuuT8AIw3YejfAjU7AoDZgAACHUUhH6Zj%2b8B8AG80V2NbEnRP3xu%2b87fXfRiSYpjzhCt8pyEPpKBB0KWgtJlo3TynQsfk88QCdYGt%2bZiVf9E5aoXUye2CpQeIdnVr3IlgxB6H4JC0tRzfzkyIPpWjexbN9vv2FCiwdCrPZYGg1NW4S3%2bJBsDaZ0sySexTeXmnxwoUg5L2laKy06okMM6ONqWSssWt2/AnMYPTo1Ax0qkhZEiT4uU5xP/%2b7z2HqKXsbWztJkSLbsIm6jcDQhXfpnR4sHq17IpKYxittBqyiWYV9sXP87wawohFdoWgzCk3nGt1xMjZrUNj/EC3cDQeRl9qjThc18PYsfVCy0FXKSOEPp7SsIj/upCHRcMDqatmhcJV/lbppgfz4H/FLTox9GRc3mEbS2jfeqUupmYddwTdsMa%2b4MAaB/sUeIgnct6HKNPJCw%2bcTi5fnLDTBUkD/yZbMwzQHXKN1o6X%2b1i0d3ntXk2JPf%2bM48Z%2bg0cnmP0p7PWQFnxWsxt08tsUrawEf1N8oxU%2bVj0NMXtQNUtNpMWEvOdjYhLKPlBo7X1K1fGE6/fDwidp9LOeNn1mHFxBhbprXWmaKnqn8DopYLkOidDZLWW6hvfbM3gu%2bFu1heoV/HT6eM9799HGLRNf6H27O9edlbV1bEn8HW/L1fOS6AjEIoMzeVXty1IXXO/HQI%3d'
CONFIG['auth_url'] = auth_url
CONFIG['headers'] = {
    'Host': 'graph.microsoft.com',
    'Authorization': 'Bearer {}'.format(token)
}


# to-dos:
# - have user paste this into browser and copy/paste dthe token?
def run(config=CONFIG):
    """Run"""
    # auth
    # response1 = requests.get(config['url'])
    # response = requests.get(config['url'], headers=config['headers'])
    # fetch
    print(config['auth_url'])
    # response: https://login.live.com/oauth20_desktop.srf?lc=1033#
    # accdess_token=EwAgA61DBAAUmcDj0azQ5tf1lkBfAvHLBzXl5ugAAcfFYd4R2l4adLcJxTc0j4gqv/O3txOMgzg0DUQe30J%2bMGtTvEDw97mVKf4OPsThUR5CTAJxvWznukQZbQ0izOby2wf2rCy/42ifCV868j0xPaJ6s2MHfayOxv2mG21AuG5ZMU2oVVTmJ/HePDqR9U6Lq3u%2boNwatfsgePt1qw9Bf1V9vUpzagbCh%2bWld7GMRL59jrRkGvHAK9cC7R7sF/OzdaZliDkwh7Uy2CfFDH2xhlo42hrTG7JXdwZlIW53VxbAlk7X3MCTb6SPnehZuwtaiTCIonMmX8B7RFzq%2b9Iw6VlP8U0OCKcjnHXRzV8meiCOOO6T8AA68U9bg3mdTHUDZgAACC01NrwEizVy8AFzBnQdtACFvED8tBexqc5WBk1EcuoMsA%2bGvocexfmrqrwmK9%2b4mGiisTbUj6UN8UxPVfzjManxDYOhJb6EzwYk78rWaQWG%2bmDmNWaCN65Q4FL1sgCB8DWPrFeQ8uRtztSULFdxiDBjGvdd4zlcKCJiGituWRVJhuttFT7TnHpc9/zzaLjhbrZ4zcJ6H0XiiHFG8AmqXqJYNAUsxpYN%2b9B0aSb2w7eA6ILOFo/fFLXyHBObBoxaUX2KlRfQFrTrHL/zEImlblH6UhDkxalJ/csuU8efx4insN9R7SSMiS5e77kzDbLuH8i0oksjOwhqGMw3BxmiIKh1jF0D6nA1kC87WtfKViwiWG4SDPeXZsJZARMGHn3fbxcK/xaJhEiGWodGDVWp7gNhjUssPve0bUfwFwF%2bfWAJ6tO3ao68nBzSEY1n5Q6TBeTzlkuPFBSzzivlOumS1UaVlDPdNDUDHT42eiRUv%2bWHJ%2bGz84WsQ9unJyLO8GpodWWC5MQJnBDD5eSFvpp6Px/mOCT0VAXxlRq1sjfgdsInZNa8q7lVKdKMmksPagCCcq6ASGA5OJM5KWGnv3AfPula7FuM3dWiIIHaKLxEQTz7Z5vOrikHWbPfkVSS1IjO74vhOqK1f4HHfc7ULaPV8dncSEZZKzH2TBzNHQI%3d
    # &token_type=bearer&expires_in=3600&scope=onedrive.readwrite
    # &user_id=AAAAAAAAAAAAAAAAAAAAAOWmQrxml364FNdeXznYRro

    # fetch resources
    response = requests.get(
        'https://graph.microsoft.com/v1.0/me/drives',
        headers=config['headers'])
    print()


if __name__ == '__main__':
    run()
