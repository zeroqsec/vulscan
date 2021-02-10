import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes

from log.log import getLogger
from cores.colors import bad
logger = getLogger(__name__)

def generateKey(num):
    return get_random_bytes(num)

def getIv(key,mode=AES.MODE_CBC):
    return AES.new(key,mode).iv

def encrypt(originalData:bytes,key,iv,mode = AES.MODE_CBC):
    try:
        cipher = AES.new(key, mode,IV = iv)
        encryptedData = cipher.encrypt(pad(originalData, AES.block_size))
        return base64.b64encode(encryptedData)
    except TypeError:
        logger.error("%s aes original data can only for type of bytes" % bad)
    except ValueError:
        logger.error("%s aes key length error" %bad)
    except Exception as e:
        logger.error("%s {}".format(e) %bad)

def decrypt(key,iv,encrypteData,mode=AES.MODE_CBC):
    try:
        encrypteData = base64.b64decode(encrypteData)
        cipher = AES.new(key,mode,IV = iv)
        decrypteData = unpad(cipher.decrypt(encrypteData),AES.block_size)
        return decrypteData
    except TypeError:
        logger.error("%s aes decrypte data can only for type of bytes" % bad)
    except ValueError as e:
        logger.error("%s aes key length error" %bad)
    except Exception as e:
        logger.error("%s {}".format(e) %bad)

