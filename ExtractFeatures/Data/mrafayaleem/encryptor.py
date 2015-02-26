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
Encryption drivers for object storage server.
"""

import M2Crypto


class CryptoDriver(object):
    """
    Base driver class that implements the functionality of encryption
    and decryption of data blocks of objects.

    :param conf: application configuration
    :param key_manager: instance of
                        swift.common.key_manager.base.KeyDriver which
                        store encryption keys
    """

    def __init__(self, conf, key_manager):
        self.conf = conf
        self.key_manager = key_manager

    def encrypted_chunk_size(self, context, original_size):
        """
        Calculates the size of the encrypted data block based on the
        size of the original data block.

        :param cotext: encryption context
        :param original_size: length of original string
        :returns: length of crypted string
        """
        chunk = " " * original_size
        return len(str(self.encrypt(context, chunk)))

    def encrypt(self, context, chunk):
        """
        Returns the encrypted data block.

        :param context: encryption context
        :param chunk: data block to encrypt
        :returns: encrypted data block
        """
        raise NotImplementedError

    def decrypt(self, context, chunk):
        """
        Returns the decrypted data block.

        :param context: encryption context
        :param chunk: data block to decrypt
        :returns: decrypted data block
        """
        raise NotImplementedError

    def encryption_context(self, key_id):
        """
        Returns the context which needed to encrypt or decrypt the
        data block.

        :param key_id: unique key identifier
        :returns: encryption context
        """
        context = {'key_id': key_id}
        return context


class DummyDriver(CryptoDriver):
    """
    Dummy implementation of CryptoDriver, which does nothing. While
    encryption/decryption it just return original string.
    """

    def encrypted_chunk_size(self, context, original_size):
        """
        Return original chunk size.

        :param cotext: encryption context
        :param original_size: length of original string
        :returns: length of crypted string
        """
        return original_size

    def encrypt(self, context, chunk):
        """
        Make dummy encryption. Just return original string.

        :param context: encryption context
        :param chunk: data block to decrypt
        :returns: original data block
        """
        return chunk

    def decrypt(self, context, chunk):
        """
        Make dummy decryption. Just return original string.

        :param context: encryption context
        :param chunk: data block to decrypt
        :returns: original data block
        """
        return chunk


class M2CryptoDriver(CryptoDriver):
    """
    Implementation of CryptoDriver based on m2crypto library.
    Initial vector, which used in some algorithm is hardcoded,
    because we use unified keys for all algorithm. So only key
    value is used for crypting. Also using hardcoded value provides
    better secure than not using it at all.

    :param conf: application configuration
    :param key_manager: instance of
                        swift.common.key_manager.base.KeyDriver which
                        store encryption keys
    """
    default_protocol = 'aes_128_cbc'
    default_iv = '3141527182810345'

    def __init__(self, conf, key_manager):
        CryptoDriver.__init__(self, conf, key_manager)
        self.protocol = conf.get('crypto_protocol', self.default_protocol)
        #TODO(ikharin): Now supported only aes_128_cbc protocol.
        if self.protocol != self.default_protocol:
            raise ValueError("M2CryptoDriver support only %r not %r "
                             "protocol." %
                             (self.default_protocol, self.protocol))

    def encrypt(self, context, chunk):
        """
        Encrypt data block using protocol from crypto_protocol config
        field. Key and initial vector extracted from encryption context.

        :param context: encryption context
        :param chunk: data block to encrypt
        :returns: encrypted data block
        """
        cipher = M2Crypto.EVP.Cipher(alg=self.protocol,
                                     key=context['key'],
                                     iv=context['iv'],
                                     op=1)
        v = cipher.update(chunk)
        v = v + cipher.final()
        return v

    def decrypt(self, context, chunk):
        """
        Decrypt data block using protocol from crypto_protocol config
        field. Key and initial vector extracted from encryption context.

        :param context: encryption context
        :param chunk: data block to decrypt
        :returns: decrypted data block
        """
        cipher = M2Crypto.EVP.Cipher(alg=self.protocol,
                                     key=context['key'],
                                     iv=context['iv'],
                                     op=0)
        v = cipher.update(chunk)
        v = v + cipher.final()
        return v

    def encryption_context(self, key_id):
        """
        Returns the context which needed to encrypt or decrypt the
        data block.

        :param key_id: unique key ID
        :returns: encryption context
        """
        context = super(M2CryptoDriver, self).encryption_context(key_id)
        #TODO(ikharin): IV hardcoded now it will be generated and stored
        #               into key manager.
        context.update({
            'key': self.key_manager.get_key(key_id),
            'iv': self.default_iv,
        })
        return context
