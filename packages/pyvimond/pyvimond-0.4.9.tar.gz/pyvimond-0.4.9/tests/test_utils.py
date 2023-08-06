import unittest
import pyvimond.utils as utils


class UtilsTest(unittest.TestCase):

    def test_create_http_client(self):
        self.assertIsNotNone(utils.create_http_client())

    def test_create_api_metadata(self):
        metadata = {
            'foo': True,
            'bar': 'very bar',
            'baz': 42
        }

        self.assertEqual({
            'entries': {
                'foo': [{'value': True, 'lang': '*'}],
                'bar': [{'value': 'very bar', 'lang': '*'}],
                'baz': [{'value': 42, 'lang': '*'}],
            },
            'empty': True
        }, utils.create_api_metadata(metadata))

    def test_parse_metadata(self):
        asset = {
            # Normally there are other fields here, but here we only need "metadata"
            'metadata': {
                'entries': {
                    'foo': [{'value': True, 'lang': '*'}],
                    'bar': [{'value': 'very bar', 'lang': '*'}],
                    'baz': [{'value': 42, 'lang': '*'}],
                },
                'empty': True
            }
        }

        self.assertEqual({
            'foo': True,
            'bar': 'very bar',
            'baz': 42
        }, utils.parse_metadata(asset))

    def test_get_metadata_value(self):
        asset = {
            # Normally there are other fields here, but here we only need "metadata"
            'metadata': {
                'entries': {
                    'foo': [{'value': True, 'lang': '*'}],
                    'bar': [{'value': 'very bar', 'lang': '*'}],
                    'baz': [{'value': 42, 'lang': '*'}],
                    # Metadata entries can inexplicably exist without values
                    'hurr': [{'lang': '*'}]
                },
                'empty': True
            }
        }

        self.assertTrue(utils.get_metadata_value('foo', asset))
        self.assertEqual('very bar', utils.get_metadata_value('bar', asset))
        self.assertEqual(42, utils.get_metadata_value('baz', asset))
        self.assertEqual(None, utils.get_metadata_value('hurr', asset))
        self.assertEqual(None, utils.get_metadata_value('ei ole', asset))

    def test_parse_category_metadata(self):
        category = {
            'metadata': {
                '@uri': '/api/metadata/category/123',
                'foo': {
                    '@xml:lang': '*',
                    '$': 'Category Foo',
                },
                'bar': {
                    '@xml:lang': '*',
                    '$': 'Category Bar',
                }
            }
        }

        self.assertEqual({
            'foo': 'Category Foo',
            'bar': 'Category Bar',
        }, utils.parse_category_metadata(category))

    def test_get_category_metadata_value(self):
        # get_category() uses this slightly unexpected format
        category = {
            'category': {
                'metadata': {
                    '@uri': '/api/metadata/category/123',
                    'string': {
                        '@xml:lang': '*',
                        '$': 'some string',
                    },
                    'int': {
                        '@xml:lang': '*',
                        '$': '42',
                    },
                    'bool': {
                        '@xml:lang': '*',
                        '$': 'false',
                    }
                }
            }
        }

        # Make sure no automatic type coercion is going on
        self.assertEqual('some string', utils.get_category_metadata_value('string', category['category']))
        self.assertEqual('42', utils.get_category_metadata_value('int', category['category']))
        self.assertEqual('false', utils.get_category_metadata_value('bool', category['category']))
        self.assertEqual(None, utils.get_category_metadata_value('baz', category['category']))

    def test_create_sumo_signature(self):
        method = 'GET'
        path = '/api/web/asset/1334686?expand=metadata&showHiddenMetadata=true'
        secret = 'secret'
        timestamp = 'Wed, 09 Dec 2020 09:48:44 +0200'

        self.assertEqual('Xm2Kr+xdb4uEp3F7COA+oj8EOpg=', utils.create_sumo_signature(method, path, secret, timestamp))

    def test_create_basic_auth_token(self):
        token = utils.create_basic_auth_token("username", "password")

        self.assertEqual('dXNlcm5hbWU6cGFzc3dvcmQ=', token)


if __name__ == '__main__':
    unittest.main()
