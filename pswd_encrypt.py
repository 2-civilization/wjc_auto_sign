from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random
import base64

def getAesString(data, key0, iv0):
    key0 = key0.strip()
    key = key0.encode('utf-8')
    iv = iv0.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    pad_pkcs7 = pad(data.encode('utf-8'), AES.block_size, style='pkcs7')
    encrypt_aes = cipher.encrypt(pad_pkcs7)
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 解码
    encrypted_text_str = encrypted_text.replace("\n", "")
    return encrypted_text_str

def encryptAES(data, aesKey):
    if not aesKey:
        return data
    random_string = ''.join(random.choice('ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678') for _ in range(64))
    iv = ''.join(random.choice('ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678') for _ in range(16))
    encrypted = getAesString(random_string + data, aesKey, iv)
    return encrypted



