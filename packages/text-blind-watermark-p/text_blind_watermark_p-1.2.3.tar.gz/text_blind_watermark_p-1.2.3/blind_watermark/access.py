#!/usr/bin/env python3
# coding=utf-8

# import numpy as np
import datetime


# import crypto
# import sys

# sys.modules['Crypto'] = crypto

# from Crypto.Cipher import AES
# import binascii


# def generate_key(username="username"):
#     today = datetime.datetime.today().strftime('%Y%m%d')
#     password = today
#
#     text = username.encode('utf-8')
#     cryptor = AES.new(key='{:0<16}'.format(password).encode('utf-8'),
#                       mode=AES.MODE_ECB)  # key 长度必须是16,24,32 长度的 byte 格式
#
#     ciphertext_tmp = cryptor.encrypt(text + b' ' * (16 - len(text) % 16))  # 明文的长度必须是16的整数倍
#     ciphertext_tmp_hex = ciphertext_tmp.hex()  # 转16进制文本
#
#     # ciphertext_bin = bin(int(ciphertext_tmp_hex, 16))[2:]  # 转二进制
#     #
#     # ciphertext_arr = (np.array(list(ciphertext_bin)) == '1')
#     return ciphertext_tmp_hex


def generate_key(username="username"):
    today = datetime.datetime.today().strftime('%Y%m')
    password = int(today)
    username = 'guofei9987'
    text = username.encode('utf-8')
    text_hex = int(text.hex(), base=16)
    return hex(text_hex + password)[2:]


if __name__ == "__main__":
    username = 'user'
    key = generate_key(username="user")
    print("用户名={username}， 您购买的 key ={key} ".format(username=username, key=key))
