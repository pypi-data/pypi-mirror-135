import time
import logging

from pyvimond.utils import create_http_client, create_api_metadata, create_sumo_signature


class VimondClient:

    def __init__(self, api_url, user, secret, timeout=10):
        self.api_url = api_url
        self.user = user
        self.secret = secret
        self.timeout = timeout
        self.logger = logging.getLogger('VimondClient')
        self.http = create_http_client()

    def _get_auth_headers(self, method, path):
        timestamp = time.strftime("%a, %d %b %Y %H:%M:%S %z")
        signature = create_sumo_signature(method, path, self.secret, timestamp)
        auth_header = "SUMO " + self.user + ":" + signature
        return {"Authorization": auth_header,
                "x-sumo-date": timestamp}

    def _admin_request(self, method, path, body=None):
        send_headers = self._get_auth_headers(method, path)
        send_headers['Accept'] = 'application/json;v=3'
        send_headers['Content-Type'] = 'application/json;v=3'
        send_headers[
            'Accept-Language'] = '*'  # all metadata are stored with language = '*' and without this, api couldn't get any hits
        if method == "POST":
            response = self.http.post(self.api_url + path,
                                      json=body,
                                      headers=send_headers,
                                      timeout=self.timeout)
        elif method == "PUT":
            response = self.http.put(self.api_url + path,
                                     json=body,
                                     headers=send_headers,
                                     timeout=self.timeout)
        elif method == "GET":
            response = self.http.get(self.api_url + path,
                                     headers=send_headers,
                                     timeout=self.timeout)
        if response.status_code == 404:
            return None
        if response.status_code == 200:
            return response.json()
        raise Exception('Request failed: status=' + str(response.status_code) + ": " + str(response.text))

    def get_category(self, category_id):
        return self._admin_request("GET",
                                   f"/api/web/category/{str(category_id)}?expand=metadata&showHiddenMetadata=true")

    def create_asset(self, asset):
        return self._admin_request("POST", '/api/web/asset', asset)

    def get_asset(self, asset_id):
        return self._admin_request("GET", f"/api/web/asset/{str(asset_id)}?expand=metadata&showHiddenMetadata=true")

    def copy_asset(self, asset_id):
        return self._admin_request("POST", f"/api/web/asset/{asset_id}/copy", {})

    def update_asset_data(self, asset_id, payload):
        return self._admin_request("PUT", f"/api/web/asset/{str(asset_id)}", payload)

    def get_asset_metadata(self, asset_id):
        return self.get_metadata(asset_id, 'asset')

    def get_category_metadata(self, category_id):
        return self.get_metadata(category_id, 'category')

    def get_metadata(self, vman_id, vman_type):
        return self._admin_request('GET', f'/api/metadata/{vman_type}/{str(vman_id)}.json')

    def update_asset_metadata(self, asset_id, metadata):
        api_metadata = create_api_metadata(metadata)
        return self._admin_request("POST", f"/api/metadata/asset/{str(asset_id)}", api_metadata)

    def update_category_metadata(self, category_id, metadata):
        api_metadata = create_api_metadata(metadata)
        return self._admin_request("POST", f"/api/metadata/category/{str(category_id)}", api_metadata)

    def get_asset_relations(self, asset_id):
        return self._admin_request('GET', f'/api/web/asset/{asset_id}/relations')

    def get_video_files(self, platform, asset_id):
        response = self._admin_request("GET", f"/api/{platform}/asset/{asset_id}/videoFiles")
        if not response:
            return []
        return response.get('videoFiles', [])

    def get_active_video_files(self, asset_id):
        # all file types are not visible to all platforms
        web_files = self.get_video_files('web', asset_id)
        mobileapp_files = self.get_video_files('mobileapp', asset_id)
        files = web_files + mobileapp_files
        deduplicate = {}
        active_files = [file for file in files if not file['deleted']]
        for file in active_files:
            deduplicate[file['id']] = file
        deduped_files = list(deduplicate.values())
        return sorted(deduped_files, key=lambda x: x['id'])

    def find_assets_by_image_url(self, category_id, image_url_pattern):
        return self.find_assets_by_query(category_id, f'imageUrl:{image_url_pattern}')

    def find_assets_by_metadata(self, metadata_key, metadata_value):
        return self._admin_request('GET', f'/api/metadata/lookup/assets/{metadata_key}.json?value={metadata_value}')

    def find_assets_by_query(self, category_id, query):
        """
        Finds assets from the specified category using an arbitrary SOLR query string
        :param category_id: the category to search in. "root" can also be used instead of a numeric ID.
        :param query: the raw query, e.g. "assetMeta_foo_text:bar AND updateTime:[NOW-7DAYS TO NOW]"
        :return:
        """
        return self._admin_request('GET', f'/api/web/search/categories/{category_id}/assets.json?query={query}')
