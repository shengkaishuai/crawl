from __future__ import unicode_literals

import math

base62_chars = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "a", "b", "c", "d", "e", "f", "g", "h", "i",
    "j", "k", "l", "m", "n", "o", "p", "q",
    "r", "s", "t", "u", "v", "w", "x", "y",
    "z","A", "B", "C", "D", "E", "F", "G", "H",
    "I", "J", "K", "L", "M", "N", "O", "P",
    "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]


def str62to10(str62):
    """

    :param str62:
    :return:
    """
    long10 = 0
    for i in range(0, len(str62)):
        n = len(str62) - i - 1
        s = str62[i]
        long10 += base62_chars.index(s) * long(math.pow(62, n))

    return str(long10)


def str10to62(str10):
    """

    :param str10:
    :return:
    """
    str62 = ''
    long10 = long(str10)
    while long10 != 0:
        r = int(long10 % 62)
        str62 = base62_chars[r] + str62
        long10 = math.floor(long10/62)

    return str62


def mid_base62_encode(mid):
    """

    :return:
    """
    base62_mid = ''
    i = len(mid) - 7

    while i > -7:
        offset1 = 0 if i < 0 else i
        offset2 = i + 7
        substr10 = mid[offset1:offset2]
        substr62 = str10to62(substr10)
        if len(substr62) < 4 and i > 0:
            substr62 = '0'*(4-len(substr62)) + substr62
        base62_mid = substr62 + base62_mid
        i -= 7

    return base62_mid


def mid_base62_decode(base62_mid):
    """

    :return:
    """
    mid = ''
    i = len(base62_mid) - 4
    while i > -4:
        offset1 = 0 if i < 0 else i
        offset2 = i + 4
        substr62 = base62_mid[offset1:offset2]
        substr10 = str62to10(substr62)

        if offset1 > 0:
            # 若不是第一组，则不足7位补0
            substr10 = '0' * (7 - len(substr10)) + substr10

        mid = substr10 + mid

        i -= 4

    return mid


def test():

    base10_mid = '4105796030075794'
    convert_to_base62_mid = mid_base62_encode(base10_mid)
    print convert_to_base62_mid

    a = 'F2kAflgxm'
    print mid_base62_decode(a)


if __name__ == "__main__":
    test()

