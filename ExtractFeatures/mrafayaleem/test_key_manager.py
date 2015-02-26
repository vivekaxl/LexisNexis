# Copyright (c) 2011 OpenStack, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import mock

from swift.common.middleware import key_manager
from swift.common.key_manager.drivers.fake import FakeDriver


class FakeApp(object):
    """ Fake WSGI application """
    def __init__(self, body=['FAKE APP'], params="FAKE"):
        self.body = body
        self.params = params

    def __call__(self, env, start_response):
        return self.body


def start_response(*args):
    """ Fake function for WSGI application """
    pass


class TestKeyManager(unittest.TestCase):
    def setUp(self):
        """
        Set up for testing swift.common.middleware.key_manager.KeyManager.
        """
        self.conf = {}
        self.account_path = '/version/account'
        self.container_path = '/version/account/container'
        self.object_path = '/version/account/container/object'
        self.patcher = mock.patch('swift.common.middleware.key_manager.'
                                  'create_instance')
        self.mock_create_instance = self.patcher.start()
        self.mock_create_instance.return_value = FakeDriver(self.conf)
        self.app = key_manager.KeyManager(FakeApp, self.conf)

    def tearDown(self):
        """
        Tear down for testing swift.common.middleware.key_manager.KeyManager.
        """
        self.patcher.stop()

    def test_call_with_key_id_header(self):
        """
        Testing __call__ to set up X-Object-Meta-Key-Id
        """
        for method in ('POST', 'PUT'):
            resp = self.app({'PATH_INFO': self.object_path,
                             'REQUEST_METHOD': method},
                             start_response)
            self.assertTrue('HTTP_X_OBJECT_META_KEY_ID' in resp.body,
                            "Method: %r" % (method))
            self.assertEquals(resp.body['HTTP_X_OBJECT_META_KEY_ID'], '12345')

    def test_call_without_key_id_header(self):
        """
        Testing __call__ to don't set up X-Object-Meta-Key-Id
        header.
        """
        for method in ('GET', 'HEAD', 'DELETE', 'COPY', 'OPTIONS',
                         'POST', 'PUT'):
            for path in (self.account_path, self.container_path,
                         self.object_path):
                if method in ('PUT', 'POST') and path == self.object_path:
                    continue
                resp = self.app({'PATH_INFO': path,
                                 'REQUEST_METHOD': method},
                                 start_response)
                self.assertFalse('HTTP_X_OBJECT_META_KEY_ID' in resp.body,
                                 "Method: %r, Path: %r" % (method, path))


if __name__ == '__main__':
    unittest.main()
