# -- encoding: utf8 --
# author: TYM
# date: 2015-3-11

def shorten(byte_code, length=4):
    step = len(byte_code) // length
    bias = 0
    shorten_bytes = [byte_code[i * step % len(byte_code) + bias] for i in range(n)]
    return bytes_to_string(shorten_bytes)


def bytes_to_string(shorten_bytes):
    byte_code = 0
    for byte in shorten_bytes:
        byte_code += byte
        byte_code = byte_code << 8

    # 为了便于辨识，去掉了loO01，chars长度64
    chars = 'abcdefghijkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ23456789@#$%&=+'
    char_code = []
    # 计算循环次数需要向上取整
    for i in range((len(shorten_bytes) * 8 + 4) // 5):
        index = byte_code & 0x1f
        char_code += chars[index]
        byte_code = byte_code >> 5
    return ''.join(char_code)
