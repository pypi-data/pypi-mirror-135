import logging
from urllib.parse import quote
from pyvimond.utils import create_http_client, create_basic_auth_token


class VimondImageServiceClient:
    def __init__(self, api_url, username, password, timeout=10):
        self.api_url = api_url
        self.username = username
        self.password = password
        self.timeout = timeout
        self.logger = logging.getLogger('VimondImageServiceClient')
        self.http = create_http_client()

    def _image_service_request(self, method, path):
        self.logger.info('Request %s %s', method, self.api_url + path)

        send_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + create_basic_auth_token(self.username, self.password)
        }
        if method == "POST":
            response = self.http.post(self.api_url + path,
                                      # Omitting this empty request body results in HTTP 400 "[Invalid Json]"
                                      json={},
                                      headers=send_headers,
                                      timeout=self.timeout)
        else:
            raise ValueError('Only POST requests are supported')

        if response.status_code != 200:
            raise Exception('Request failed: status=' + str(response.status_code) + ' : ' + str(response.text),
                            response)

        return response.json()

    def create_image_pack(self):
        response = self._image_service_request('POST', '/adminAPI/imagePacks')
        return response['id']

    def send_image(self, imagepack_id, image_url, location):
        quoted_url = quote(image_url)
        path = f'/adminAPI/imagePack/{imagepack_id}/{location}/fetchImage?imageUrl={quoted_url}'
        response = self._image_service_request('POST', path)
        return response['id']

    def create_image_url(self, imagepack_id, location=None):
        if location is None:
            return f'{self.api_url}/api/v2/img/{imagepack_id}'

        return f'{self.api_url}/api/v2/img/{imagepack_id}?location={location}'
