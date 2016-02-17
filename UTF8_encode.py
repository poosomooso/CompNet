#
## UTF8_encode
#

from itertools import zip_longest
from math import log
def int2baseb(i:int,b:int)->tuple:
    """return the base b encoding of i"""
    return tuple([(i//b**n)%b for n in reversed(range(1+int(log(i,b))))]) if i else (0,)
def UTF8_encode(C):
    return b"".join([UTF8_encode1(c) for c in C])
def UTF8_encode1(c):
    """implements  chr.encode() e.g.: "A".encode(encoding="UTF-8")"""
    character_number = ord(c)
    if character_number in range(0xd800,0xe000):
        raise UnicodeEncodeError("Cannot encode a surrogate (a character number in range(0xd800,0xe000))")


# Note: adapted from From rfc3629, page 4

#   cnbl < 8     0000 0000-0000 007F | 0xxxxxxx
#   cnbl > 7     0000 0080-0000 07FF | 110xxxxx 10xxxxxx
#   cnbl > 11    0000 0800-0000 FFFF | 1110xxxx 10xxxxxx 10xxxxxx
#   cnbl > 16    0001 0000-0010 FFFF | 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx

    if character_number < 128:  # cnbl < 8 
        return bytes([character_number])
    
    cnbl = character_number.bit_length()
    byte_length = 1 + (cnbl > 7) + (cnbl > 11) + (cnbl > 16)
    utf8_hdr = ((0xc0,0xe0,0xf0)[byte_length-2],)
    
    base64cn = int2baseb(character_number,64) # 10xx xxxx 
    
    if len(base64cn) < byte_length:
        base64cn = (0,)+base64cn
    assert len(base64cn) == byte_length
    
    return bytes([b|a for a,b in zip_longest(base64cn,utf8_hdr,fillvalue=0x80)])


if __name__ == "__main__":
    import unicodedata
    testchr = "A"+chr(946)+unicodedata.lookup("sailboat")+unicodedata.lookup("rowboat")
    testbytes = bytes(testchr,encoding="UTF-8")
    testbytes2 = UTF8_encode(testchr)
    if testbytes == testbytes2:
        print("hooray!")
    


