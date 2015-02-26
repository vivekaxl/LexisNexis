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
Fake driver for KeyDriver class.
Fake methods for testing other implemented components.
"""

from swift.common.key_manager.drivers import base


class FakeDriver(base.KeyDriver):
    """ Fake driver for testing key store services """

    def get_key(self, key_id):
        """
        Give test value key="123456789abcd123456789abcd123456"

        :param key_id: number of key in database
        :return key: string is used for encryption process
        """
        key = "123456789abcd123456789abcd123456"
        return key

    def get_key_id(self, account):
        """
        Give test value key_id = 12345

        :param account: string is name of account
        :return key_id: number of key in database
        """
        key_id = 12345
        return key_id

    def sync(self):
        """
        The fake driver doesn't need to synchronize data storage
        schemas.
        """
        pass
