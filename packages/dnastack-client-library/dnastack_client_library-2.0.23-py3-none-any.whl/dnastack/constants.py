import os

__version__ = "2.0.23"

# This is the public client wallet.publisher.dnastack.com used if the user does not set their own
DEFAULT_AUTH_PARAMS = {
    "url": "https://wallet.publisher.dnastack.com/",
    "client": {
        "redirect_url": "https://wallet.publisher.dnastack.com/",
        "id": "publisher-cli",
        "secret": "WpEmHtAiB73pCrhbEyci42sBFcfmWBdj",
    },
}
DEFAULT_AUTH_SCOPES = (
    "openid "
    "offline_access "
    "drs-object:write "
    "drs-object:access "
    "dataconnect:info "
    "dataconnect:data "
    "dataconnect:query "
    "wes"
)

CLI_DIRECTORY = f"{os.path.expanduser('~')}/.dnastack"

# NOTE: This is not necessarily all the possible config keys, but all of the settable ones
# also include types for the config keys
ACCEPTED_CONFIG_KEYS = {
    "data_connect": {
        "url": str,
        "auth": {
            "url": str,
            "authorization_url": str,
            "device_code_url": str,
            "token_url": str,
            "refresh_token": str,
            "email": str,
            "personal_access_token": str,
            "client": {"id": str, "secret": str, "redirect_url": str, "scope": str},
        },
    },
    "user": {
        "personal_access_token": str,
        "email": str,
    },
    "oauth": {
        "refresh_token": str,
    },
    "collections": {
        "url": str,
        "auth": {
            "url": str,
            "authorization_url": str,
            "device_code_url": str,
            "token_url": str,
            "refresh_token": str,
            "email": str,
            "personal_access_token": str,
            "client": {"id": str, "secret": str, "redirect_url": str, "scope": str},
        },
    },
    "wes": {
        "url": str,
        "auth": {
            "url": str,
            "authorization_url": str,
            "device_code_url": str,
            "token_url": str,
            "refresh_token": str,
            "email": str,
            "personal_access_token": str,
            "client": {"id": str, "secret": str, "redirect_url": str, "scope": str},
        },
    },
    "tokens": list,
    "service_registry": {"url": str},
}


# Config keys to not display/persist in config.yaml
HIDDEN_CONFIG_KEYS = ["client", "debug"]

# The configs in oauth.[SERVER].* that are settable by the user
ACCEPTED_OAUTH_KEYS = {"access_token": str, "refresh_token": str, "scope": list}

# Map old config keys to new ones
# If there isn't a perfect fit, set the value to None
DEPRECATED_CONFIG_KEYS = {
    "wes-url": "wes.url",
    "data-connect-url": "data_connect.url",
    "collections-url": "collections.url",
    "oauth_token.refresh_token": None,
    "personal_access_token": "user.personal_access_token",
    "email": "user.email",
    "wallet-url": None,
    "client-redirect-uri": None,
    "client-id": None,
    "client-secret": None,
    "oauth_token": None,
}

SUPPORTED_SERVICES = ["wes", "collections", "dataconnect"]

DEFAULT_SERVICE_REGISTRY = "https://ga4gh-service-registry.publisher.dnastack.com/"
