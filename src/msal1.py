"""
The configuration file would look like this:
{
    // Sign in users with personal Microsoft accounts (MSA) only.:
    "authority": "https://login.microsoftonline.com/consumers/",
    // https://docs.microsoft.com/en-us/azure/active-directory/develop/
    msal-client-application-configuration
    "client_id": "your_client_id",
    "username": "your_username@your_tenant.com",
    "password": "This is a sample only. You better NOT persist your password.",
    "scope": ["User.ReadBasic.All"],
    // You can find the other permission names from this document
    // https://docs.microsoft.com/en-us/graph/permissions-reference
    "endpoint": "https://graph.microsoft.com/v1.0/users"
    // You can find more Microsoft Graph API endpoints from Graph Explorer
    // https://developer.microsoft.com/en-us/graph/graph-explorer
}
You can then run this sample with a JSON configuration file:
    python sample.py parameters.json
"""
import os
import json
import logging
import requests
import msal


# Optional logging
# logging.basicConfig(level=logging.DEBUG)  # Enable DEBUG log for script
# logging.getLogger("msal").setLevel(logging.INFO)  # Optionally disable MSAL
# DEBUG logs
ROOT_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..')
CONFIG_PATH = os.path.join(ROOT_DIR, 'env.json')
with open(CONFIG_PATH, 'r') as config_file:
    config = json.load(config_file)

# Create a preferably long-lived app instance which maintains a token cache.
app = msal.PublicClientApplication(
    config["client_id"], authority=config["authority"],
    # token_cache=...  # Default cache is in memory only.
    # You can learn how to use SerializableTokenCache from
    # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
)

# The pattern to acquire a token looks like this.
result = None

# Firstly, check the cache to see if this end user has signed in before
accounts = app.get_accounts(username=config["username"])
if accounts:
    logging.info(
        "Account(s) exists in cache, probably with token too. Let's try.")
    result = app.acquire_token_silent(config["scope"], account=accounts[0])

# Try 1
# if not result:
#     logging.info(
#         "No suitable token exists in cache. Let's get a new one from AAD.")
#     # See this page for constraints of Username Password Flow.
#     # https://github.com/AzureAD/microsoft-authentication-library-for-python/
#     # wiki/Username-Password-Authentication
#     result = app.acquire_token_by_username_password(
#         config["username"], config["password"], scopes=config["scope"])

# Try 2
if not result:
    logging.info(
        "No suitable token exists in cache. Let's get a new one from AAD.")

    flow = app.initiate_device_flow(scopes=config["scope"])
    if "user_code" not in flow:
        raise ValueError(
            "Fail to create device flow. Err: %s" % json.dumps(flow, indent=4))

    print(flow["message"])

    # Ideally you should wait here, in order to save some unnecessary polling
    # input("Press Enter after signing in from another device to proceed,
    # CTRL+C to abort.")

    result = app.acquire_token_by_device_flow(flow)  # By default it will block
    # You can follow this instruction to shorten the block time
    #    https://msal-python.readthedocs.io/en/latest/
    # #msal.PublicClientApplication.acquire_token_by_device_flow
    # or you may even turn off the blocking behavior,
    # and then keep calling acquire_token_by_device_flow(flow) in your own
    # customized loop.

if "access_token" in result:
    # Calling graph using the access token
    graph_data = requests.get(  # Use token to call downstream service
        config["endpoint"],
        headers={'Authorization': 'Bearer ' + result['access_token']},).json()
    print("Graph API call result: %s" % json.dumps(graph_data, indent=2))
else:
    print(result.get("error"))
    print(result.get("error_description"))
    # You may need this when reporting a bug:
    print(result.get("correlation_id"))
    # Not mean to be coded programatically, but...:
    if 65001 in result.get("error_codes", []):
        # AAD requires user consent for U/P flow
        print("Visit this to consent:",
              app.get_authorization_request_url(config["scope"]))
