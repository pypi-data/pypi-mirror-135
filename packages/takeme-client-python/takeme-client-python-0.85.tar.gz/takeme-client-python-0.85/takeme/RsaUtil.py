import base64
import pkgutil
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


class RsaUtil(object):

    @staticmethod
    def encrypt(key):
        public_key_file = pkgutil.get_data(__name__, "templates/public.der")
        public_key = RSA.importKey(public_key_file)
        # print(public_key.exportKey().decode('ascii'))

        cipher_rsa = PKCS1_OAEP.new(public_key)
        encrypted = cipher_rsa.encrypt(str.encode(key))

        return base64.b64encode(encrypted).decode('ascii')
