"""SNaP OneDrive Report Aggregator

Instructions:
1. Get secret & id from Joe, and put in your environment or paste
here over the '...'s of os.getenv().
2. Run script
"""
import os
import onedrivesdk_fork as onedrivesdk
from onedrivesdk_fork.helpers import GetAuthCodeServer


# Issue: Thought this was what was recommended based on docs, but not seems
# to be issue w/ client_id.
# CONFIG = {
#     'redirect_uri': 'https://localhost:8080/',
#     'client_id': os.getenv('CLIENT_ID', '...'),
#     'client_secret': os.getenv('CLIENT_SECRET', '...'),
#     'api_base_url': 'https://api.onedrive.com/v1.0/',
#     'scopes': ['wl.signin', 'wl.offline_access', 'onedrive.readwrite']
# }

# Issue: W/ modeltb.org, When running, in Python, get:
# OSError: [Errno 49] Can't assign requested address
# CONFIG = {
#     'redirect_uri': 'https://www.modeltb.org',
#     'client_id': os.getenv('MANIFEST_APPID', '...'),
#     'client_secret': os.getenv('CLIENT_SECRET', '...'),
#     'api_base_url': 'https://api.onedrive.com/v1.0/',
#     'scopes': ['wl.signin', 'wl.offline_access', 'onedrive.readwrite']
# }

# Issue: Works, but redirects to localhost, which isn't actually running.
# CONFIG = {
#     'redirect_uri': 'https://localhost:8080/',
#     'client_id': os.getenv('MANIFEST_APPID', '...'),
#     'client_secret': os.getenv('CLIENT_SECRET', '...'),
#     'api_base_url': 'https://api.onedrive.com/v1.0/',
#     'scopes': ['wl.signin', 'wl.offline_access', 'onedrive.readwrite']
# }

# TODO: Try
# https://www.youtube.com/watch?v=YYcuyNfNdRw&t=791s
# https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/Authentication/quickStartType//sourceType/Microsoft_AAD_IAM/appId/3edae2b4-0150-450a-b8b6-bf2ee70c325f/objectId/40fc1653-1e91-4557-8655-0080aa65837a/isMSAApp/true/defaultBlade/Overview/appSignInAudience/PersonalMicrosoftAccount
CONFIG = {
    # 'redirect_uri': 'https://localhost:8080/',
    # 'redirect_uri': 'msal3edae2b4-0150-450a-b8b6-bf2ee70c325f://auth',
    'redirect_uri': 'https://login.live.com/oauth20_desktop.srf',
    'client_id': os.getenv('ATTEMPT2_APP_ID', '...'),
    # 'client_secret': os.getenv('ATTEMPT2_TENANT_ID', '...'),
    'client_secret': os.getenv('xxx', None),
    'api_base_url': 'https://api.onedrive.com/v1.0/',
    'scopes': ['wl.signin', 'wl.offline_access', 'onedrive.readwrite']
}


def run(config=CONFIG):
    """Run"""
    client = onedrivesdk.get_default_client(
        client_id=config['client_id'], scopes=config['scopes'])

    auth_url = client.auth_provider.get_auth_url(config['redirect_uri'])

    # this will block until we have the code
    code = GetAuthCodeServer.get_auth_code(
        auth_url, config['redirect_uri'])

    client.auth_provider.authenticate(
        code, config['redirect_uri'], config['client_secret'])

    print()


if __name__ == '__main__':
    run()
