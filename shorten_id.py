# -- encoding: utf-8 --
# author: TYM
# date: 2015-3-11
import random

def shorten(byte_code, length=4):
    length = 1 if length < 1 else int(length)
    length = len(byte_code) * 8 if length > len(byte_code) * 8 else length

    step = len(byte_code) * 8 // length
    shift = random.randint(0, len(byte_code) * 8)

    def get_bits(bias):
        bias = bias % (len(byte_code) * 8)
        index =  (bias // 8)
        bias -= index * 8
        bits = 0

        bits += (byte_code[index] & (0xf8 >> bias))
        # 只取5位
        next_bias = 5 - (8 - bias)
        if next_bias > 0:
            bits = bits << next_bias
            bits += (byte_code[(index + 1) % len(byte_code)] >> (8 - next_bias))
        return bits

    shorten_bytes = [get_bits(i * step + shift) for i in range(length)]

    def bytes_to_string(shorten_bytes):
        # 为了便于辨识，去掉了loO01，chars长度64
        chars = 'abcdefghijkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ23456789@#$%&=+'
        shorten_chars = ''
        # 计算循环次数需要向上取整
        for byte in shorten_bytes:
            index = byte & 0x1f
            shorten_chars += chars[index]
        return shorten_chars

    return bytes_to_string(shorten_bytes)
