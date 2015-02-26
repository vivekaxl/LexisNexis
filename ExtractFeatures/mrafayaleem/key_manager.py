# Copyright (c) 2010-2012 OpenStack, LLC.
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

"""
Implementation of key_manager for encryption objects.

This filter needed for cooperation with key store and supporting
following functions:
    getting key_id associated with account name or
    generating new key_id, if it not existed;
    updating "PUT" Request by key_id information.
"""

from swift.common.swob import Request
from swift.common.utils import split_path, create_instance
from swift.common.key_manager.drivers.base import KeyDriver


class KeyManager(object):
    """ WSGI KeyManager for managing of keys """

    def __init__(self, app, conf):
        """
        Standart initialization method for filter factory

        :param app: WSGI application
        :param conf: dictionary with configuration variables
        """

        self.app = app
        self.conf = conf
        key_manager = conf.get('crypto_keystore_driver',
                               'swift.common.key_manager.drivers.dummy.'
                               'DummyDriver')
        self.key_manager = create_instance(key_manager, KeyDriver, conf)

    def get_key_id(self, account):
        """
        Get key_id associated by account name.
        Create needed KeyDriver's child class for working with DB.

        :param account: user account name
        :returns key_id: key_id is associated by account
        """
        return self.key_manager.get_key_id(account)

    def __call__(self, env, start_response):
        """
        Get Request object from variable env, then get account name.
        Further generate or get associated key_id from key_manage_base
        and add this information in Headears of request.

        :param env: WSGI environment dictionary
        :param start_response: WSGI callable

        :return self.app: standart next WSGI app in the pipeline
        """
        req = Request(env)
        if req.method in ('PUT', 'POST'):
            _, account, container, obj = split_path(req.path, 1, 4, True)
            if account and container and obj:
                key_id = self.get_key_id(account)
                req.headers['X-Object-Meta-Key-Id'] = key_id
                env = req.environ
        return self.app(env, start_response)


def filter_factory(global_conf, **local_conf):
    """ Returns the WSGI filter for use with paste.deploy. """
    conf = global_conf.copy()
    conf.update(local_conf)

    def key_manager(app):
        return KeyManager(app, conf)
    return key_manager
