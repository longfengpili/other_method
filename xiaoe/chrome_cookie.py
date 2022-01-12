# -*- coding: utf-8 -*-
# @Author: chunyang.xu
# @Date:   2022-01-05 07:03:17
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2022-01-12 08:05:42


import os
import sys
import json
import base64
import sqlite3
import time
from datetime import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from mysetting import DOMAIN

VERIFY = True  # 屏蔽SSL验证


class GetCooikiesFromChrome(object):
    '''[summary]
        Chrome 90.X版本解密Cookies文件
    [description]
    '''

    def __init__(self):
        pass

    def dpapi_decrypt(self, encrypted):
        import ctypes
        import ctypes.wintypes

        class DATA_BLOB(ctypes.Structure):
            _fields_ = [('cbData', ctypes.wintypes.DWORD),
                        ('pbData', ctypes.POINTER(ctypes.c_char))]

        p = ctypes.create_string_buffer(encrypted, len(encrypted))
        blobin = DATA_BLOB(ctypes.sizeof(p), p)
        blobout = DATA_BLOB()
        retval = ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
        if not retval:
            raise ctypes.WinError()
        result = ctypes.string_at(blobout.pbData, blobout.cbData)
        ctypes.windll.kernel32.LocalFree(blobout.pbData)
        return result

    def aes_decrypt(self, encrypted_txt):
        with open(os.path.join(os.environ['LOCALAPPDATA'],
                               r"Google\Chrome\User Data\Local State"), encoding='utf-8', mode="r") as f:
            jsn = json.loads(str(f.readline()))
        encoded_key = jsn["os_crypt"]["encrypted_key"]
        encrypted_key = base64.b64decode(encoded_key.encode())
        encrypted_key = encrypted_key[5:]
        key = self.dpapi_decrypt(encrypted_key)
        nonce = encrypted_txt[3:15]
        cipher = Cipher(algorithms.AES(key), None, backend=default_backend())
        cipher.mode = modes.GCM(nonce)
        decryptor = cipher.decryptor()
        return decryptor.update(encrypted_txt[15:])

    def chrome_decrypt(self, encrypted_txt):
        if sys.platform == 'win32':
            try:
                if encrypted_txt[:4] == b'x01x00x00x00':
                    decrypted_txt = self.dpapi_decrypt(encrypted_txt)
                    return decrypted_txt.decode()
                elif encrypted_txt[:3] == b'v10':
                    decrypted_txt = self.aes_decrypt(encrypted_txt)
                    return decrypted_txt[:-16].decode()
            except WindowsError:
                return None
        else:
            raise WindowsError

    def get(self, domain):
        sql = f'SELECT name, encrypted_value as value, expires_utc FROM cookies where host_key like "%{domain}%"'
        filename = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Google\Chrome\User Data\default\Network\Cookies')
        con = sqlite3.connect(filename)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql)

        cookie = ''
        for row in cur:
            if row['value'] is not None:
                name = row['name']
                expires_utc = row['expires_utc'] / 1000000
                expires_utc -= 11644473600
                now = time.time()
                if expires_utc > 0 and expires_utc < now:
                    localtime = datetime.fromtimestamp(expires_utc)
                    raise Exception(f'【{name}】expires_ts is {localtime}, please login again')
                
                value = self.chrome_decrypt(row['value'])
                if value is not None:
                    cookie += name + '=' + value + ';'
        con.close()
        # cookie = cookie.encode('utf-8')
        if not cookie:
            raise f"cookie is not exist! {cookie}"
        return cookie


if __name__ == '__main__':
    get_cookies = GetCooikiesFromChrome()
    cookies = get_cookies.get(DOMAIN)
    print(cookies)
