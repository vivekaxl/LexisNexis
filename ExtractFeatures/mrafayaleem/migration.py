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
Management the schema of key store.
"""
from paste.deploy import loadwsgi

from swift.common.utils import create_instance
from swift.common.key_manager.drivers.base import KeyDriver


def migrate(conf, driver):
    """
    Upgrading the schemes of the key store.

    :param conf: Application configuration.
    :param driver: Import path of a driver.
    """
    key_manager = create_instance(driver, KeyDriver, conf)
    key_manager.sync()


def synchronize(conf_file, filter_section):
    """
    Process schema synchronization.

    :param conf_file: Filename of configuration path.
    :param filter_section: Name of key_management filter section.
    """
    context = loadwsgi.loadcontext(loadwsgi.FILTER, "config:%s" % (conf_file,),
                                   name=filter_section)
    conf = context.config()
    driver = conf.get('crypto_keystore_driver')
    if driver:
        #NOTE(ikharin): The operation of data schema synchronization is
        #               not required for the default driver if it's not
        #               specified into configuration.
        migrate(conf, driver)
