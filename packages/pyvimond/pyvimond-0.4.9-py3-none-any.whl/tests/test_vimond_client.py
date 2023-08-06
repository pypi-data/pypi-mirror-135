import json
import requests_mock
import unittest
from pyvimond.vimond_client import VimondClient


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.vimond_client = VimondClient('http://example.com', 'user', 'secret')

    @requests_mock.Mocker()
    def test_get_video_files(self, m):
        m.get('http://example.com/api/web/asset/123/videoFiles', text=json.dumps({
            'videoFiles': [
                {
                    'id': 12345
                },
                {
                    'id': 23456
                }
            ]
        }))

        video_files = self.vimond_client.get_video_files('web', 123)
        self.assertEqual(2, len(video_files))
        self.assertEqual(12345, video_files[0]['id'])
        self.assertEqual(23456, video_files[1]['id'])

    @requests_mock.Mocker()
    def test_get_active_video_files(self, m):
        # Make the "web" platform return one two files and the "mobileapp" platform return three,
        # one of which is a duplicate of one in "web" and one which is deleted. Make them come in
        # reverse order based on their ID.
        m.get('http://example.com/api/web/asset/123/videoFiles', text=json.dumps({
            'videoFiles': [
                {
                    'id': 5564,
                    'deleted': False
                },
                {
                    'id': 4445,
                    'deleted': False
                }
            ]
        }))
        m.get('http://example.com/api/mobileapp/asset/123/videoFiles', text=json.dumps({
            'videoFiles': [
                {
                    'id': 5564,
                    'deleted': False
                },
                {
                    'id': 2344,
                    'deleted': True
                },
                {
                    'id': 1235,
                    'deleted': False
                }
            ]
        }))

        # Result should be a deduplicated, sorted, combined result of the video files
        # in the "web" and "mobileapp" platforms
        active_video_files = self.vimond_client.get_active_video_files(123)
        self.assertEqual([
            {
                'id': 1235,
                'deleted': False,
            },
            {
                'id': 4445,
                'deleted': False,
            },
            {
                'id': 5564,
                'deleted': False
            }
        ], active_video_files)

    @requests_mock.Mocker()
    def test_find_assets_by_image_url(self, m):
        expected_url = 'http://example.com/api/web/search/categories/33/assets.json?query=imageUrl:*/foo/*'
        expected_return = {'foo': True}
        m.get(expected_url, text=json.dumps(expected_return))

        self.assertEqual(expected_return, self.vimond_client.find_assets_by_image_url(33, '*/foo/*'))

    @requests_mock.Mocker()
    def test_get_asset_metadata(self, m):
        # Test that the correct URL is requested
        expected_url = 'http://example.com/api/metadata/asset/123.json'
        m.get(expected_url, text=json.dumps({}))

        self.assertEqual({}, self.vimond_client.get_asset_metadata(123))

    @requests_mock.Mocker()
    def test_get_category_metadata(self, m):
        # Test that the correct URL is requested
        expected_url = 'http://example.com/api/metadata/category/123.json'
        m.get(expected_url, text=json.dumps({}))

        self.assertEqual({}, self.vimond_client.get_category_metadata(123))


if __name__ == '__main__':
    unittest.main()
