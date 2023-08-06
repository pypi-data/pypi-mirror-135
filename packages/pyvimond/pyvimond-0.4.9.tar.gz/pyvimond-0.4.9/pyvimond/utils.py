import base64
import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from Crypto.Hash import SHA1, HMAC


def create_http_client():
    """
    :return: an HTTP client that retries on connection errors (and limits redirects). Timeouts can apparently not be
    configured for all requests, so it's not done here.
    """

    # Vimond Image Service can be unreliable, so we have to retry POST requests as well
    retryable_methods = ["HEAD", "OPTIONS", "GET", "POST"]
    retry_strategy = Retry(connect=3, read=3, redirect=5, status=0, backoff_factor=1,
                           method_whitelist=retryable_methods)
    adapter = HTTPAdapter(max_retries=retry_strategy)

    client = requests.Session()
    client.mount("https://", adapter)
    client.mount("http://", adapter)

    return client


def create_api_metadata(metadata):
    api_metadata = {
        'entries': {},
        'empty': True,
    }
    for key in metadata:
        value = metadata[key]
        api_metadata['entries'][key] = [
            {'value': value, 'lang': '*'}
        ]
    return api_metadata


def parse_metadata(asset):
    metadata = asset.get('metadata', {}).get('entries', {})
    metadata_dict = {}
    for key in metadata.keys():
        entry = metadata.get(key)[0]
        # Value may be missing
        metadata_dict[key] = entry['value'] if 'value' in entry else None
    return metadata_dict


def get_metadata_value(key, asset):
    metadata = parse_metadata(asset)
    return metadata.get(key, None)


def parse_category_metadata(category):
    metadata = category.get('metadata', {})
    metadata_dict = {}

    for key in metadata.keys():
        if key == '@uri':
            continue

        metadata_dict[key] = metadata[key]['$']

    return metadata_dict


def get_category_metadata_value(key, category):
    metadata = parse_category_metadata(category)
    return metadata.get(key, None)


def create_sumo_signature(method, path, secret, timestamp):
    plain_path = re.sub(r"\?.*", "", path)
    string_to_sign = method + "\n" + plain_path + "\n" + timestamp
    sig_hash = HMAC.new(secret.encode('utf-8'), digestmod=SHA1)
    sig_hash.update(string_to_sign.encode('utf-8'))
    return base64.b64encode(sig_hash.digest()).decode("utf-8")


def create_basic_auth_token(username, password):
    credentials_bytes = f'{username}:{password}'.encode("utf-8")
    return base64.b64encode(credentials_bytes).decode("ascii")
