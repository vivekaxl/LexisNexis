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
""" Dummy key manager driver. """

import hashlib

from swift.common.key_manager.drivers import base


class DummyDriver(base.KeyDriver):
    """
    Dummy key manager dirver which just return md5sum of account name
    and key_id equal key.
    """

    def get_key(self, key_id):
        """
        Just return key_id which equal key.

        :param key_id: it is equal to key.
        :returns: encryption key
        """
        return key_id

    def get_key_id(self, account):
        """
        Just return md5sum of account name and return key in HEX format.

        :param account: string is name of account
        :returns: key which actually equal to md5sum of account
        """
        return hashlib.md5(account).hexdigest()

    def sync(self):
        """
        The dummy driver doesn't need to synchronize data storage
        schemas.
        """
        pass
