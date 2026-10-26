"""Behavior checks without accessing a real account or network."""
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, Mock

spec = importlib.util.spec_from_file_location('nutstore', Path(__file__).parents[1] / 'nutstore/scripts/nutstore.py')
client = importlib.util.module_from_spec(spec)
spec.loader.exec_module(client)


class NutstoreTests(unittest.TestCase):
    def test_paths_are_encoded_and_cannot_traverse(self):
        self.assertEqual(client.remote_path('/报告/one%20two'), '/dav/%E6%8A%A5%E5%91%8A/one%2520two')
        for value in ['../outside', '/ZeroClaw/../outside', '/a\\b', '/a\nvalue']:
            with self.assertRaises(ValueError):
                client.remote_path(value)
        for value in ['/', '/other', '/ZeroClaw-other/file']:
            with self.assertRaises(ValueError):
                client.write_path(value)

    def test_write_requires_confirmation_before_network(self):
        with patch.object(client, 'request') as request:
            with self.assertRaisesRegex(ValueError, 'confirmation_required'):
                client.mutate('mkdir', '/ZeroClaw/test', None, False)
            request.assert_not_called()

    def test_redirect_never_receives_another_request(self):
        connection = Mock()
        connection.getresponse.return_value.status = 302
        with patch.object(client, 'credentials', return_value={'account': 'synthetic', 'password': 'synthetic'}), patch.object(client.http.client, 'HTTPSConnection', return_value=connection):
            with self.assertRaisesRegex(ValueError, 'http_302'):
                client.request('GET', '/file')
        connection.request.assert_called_once()
        connection.close.assert_called_once()

    def test_upload_is_create_only_and_within_dedicated_root(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'source'
            source.write_bytes(b'synthetic')
            with patch.object(client, 'request', return_value=(Mock(), Mock(status=201))) as request:
                client.mutate('upload', '/ZeroClaw/file', str(source), True)
                self.assertEqual(request.call_args.args[3]['If-None-Match'], '*')
                self.assertEqual(request.call_args.args[3]['Content-Length'], '9')

    def test_download_does_not_overwrite_existing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'file'
            target.write_bytes(b'original')
            with patch.object(client, 'request') as request:
                with self.assertRaisesRegex(ValueError, 'local_destination_conflict'):
                    client.download('/file', str(target))
                request.assert_not_called()
            self.assertEqual(target.read_bytes(), b'original')

    def test_directory_listing_is_nonrecursive_and_ignores_foreign_origins(self):
        raw = b'''<d:multistatus xmlns:d="DAV:">
          <d:response><d:href>/dav/folder/</d:href><d:propstat><d:prop/></d:propstat></d:response>
          <d:response><d:href>/dav/folder/a.txt</d:href><d:propstat><d:prop><d:getcontentlength>4</d:getcontentlength></d:prop></d:propstat></d:response>
          <d:response><d:href>https://foreign.invalid/dav/folder/b.txt</d:href><d:propstat><d:prop/></d:propstat></d:response>
          <d:response><d:href>/dav/folder/deep/c.txt</d:href><d:propstat><d:prop/></d:propstat></d:response>
        </d:multistatus>'''
        with patch.object(client, 'request', return_value=(Mock(), io.BytesIO(raw))):
            value = client.list_files('/folder')
        self.assertEqual(value['count'], 1)
        self.assertEqual(value['entries'][0]['path'], '/folder/a.txt')
        self.assertFalse(value['recursive'])

    def test_entities_are_rejected(self):
        response = io.BytesIO(b'<!DOCTYPE a [<!ENTITY b "payload">]><a/>')
        with patch.object(client, 'request', return_value=(Mock(), response)):
            with self.assertRaisesRegex(ValueError, 'invalid_response'):
                client.list_files('/')

    def test_credentials_require_private_permissions(self):
        if os.name != 'posix':
            self.skipTest('POSIX permission check')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'credentials.json'
            path.write_text(json.dumps({'account': 'synthetic', 'password': 'synthetic'}))
            path.chmod(0o644)
            with self.assertRaisesRegex(ValueError, 'credentials_permissions'):
                client.credentials(path)
            path.chmod(0o600)
            self.assertEqual(client.credentials(path)['account'], 'synthetic')


if __name__ == '__main__':
    unittest.main()
