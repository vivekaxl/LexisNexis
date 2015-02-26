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
from sqlalchemy import MetaData, Table, Column, String, Integer


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    table = Table('key_info', meta, autoload=True)
    table.c.account.alter(type=String(42))
    table.c.encryption_key.alter(type=String(42))


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    table = Table('key_info', meta, autoload=True)
    table.c.account.alter(type=String(30))
    table.c.encryption_key.alter(type=String(30))
