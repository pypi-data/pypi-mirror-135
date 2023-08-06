import requests_mock
import unittest
from pyvimond.vimond_image_service_client import VimondImageServiceClient


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.vimond_image_service_client = VimondImageServiceClient('http://example.com', 'user', 'secret')

    @requests_mock.Mocker()
    def test_url_formatting_headers_and_return_value(self, m):
        m.post(
            'http://example.com/adminAPI/imagePack/123456-789/main/fetchImage?imageUrl=http%3A//example.com/image.jpg',
            json={
                'id': '123456-new'
            },
            request_headers={
                'Content-Type': 'application/json',
                'Authorization': 'Basic dXNlcjpzZWNyZXQ='
            })

        image_pack_id = self.vimond_image_service_client.send_image('123456-789', 'http://example.com/image.jpg',
                                                                    'main')
        self.assertEqual('123456-new', image_pack_id)

    @requests_mock.Mocker()
    def test_exception_contains_response_object(self, m):
        # Throw an exception
        m.post(
            'http://example.com/adminAPI/imagePack/123456-789/main/fetchImage?imageUrl=http%3A//example.com/image.jpg',
            exc=Exception('some error', {
                'status_code': 404
            }))

        try:
            self.vimond_image_service_client.send_image('123456-789', 'http://example.com/image.jpg', 'main')
        except Exception as e:
            self.assertEqual('some error', e.args[0])
            self.assertEqual(404, e.args[1]['status_code'])


if __name__ == '__main__':
    unittest.main()
