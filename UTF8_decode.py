#
## UTF8_decode 
#
from itertools import zip_longest
b2pre= {
     2:0x1F,
     3:0x0F,
     4:0x07}

#07      U+0000	        U+007F 	        1 	0xxxxxxx
#11 	U+01	        U+07FF 	        2 	110xxxxx 	10xxxxxx
#16 	U+0800 	        U+FFFF 	        3 	1110xxxx 	10xxxxxx 	10xxxxxx
#21 	U+10000 	U+1FFFFF 	4 	11110xxx 	10xxxxxx 	10xxxxxx 	10xxxxxx
def p(X,*T,**D):
    """embeddable print statement - returns first argument"""
    print(X,*T,**D)
    return X

def baseb2int(T:tuple,b:int)->int:
    "returns base b value of tuple T of ints"
    return sum([x*b**e for e,x in enumerate(reversed(T))])
    
def UTF8_decode(b:bytes)->chr:
    "decodes bytes containing utf-8"
    i = [j for j in range(len(b)) if b[j]&0xc0 != 0x80]+[len(b)] # index of first bytes of UTF-8 values in b
    utf8s=[b[i[j]:i[j+1]] for j in range(len(i)-1)]              # list of UTF-8 1 to 4 byte code points. 
    return "".join([chr(UTF8_decode1(utf8)) for utf8 in utf8s])  # UTF-8 code points converted to Python chr

def UTF8_decode1(b:bytes)-> int:
    "converts a single UTF-8 code point into a character_number (which is a Python 3 int)"
    B=[int(x) for x in b]  
    if len(B) == 1:
        return B[0] 
    
    character_number = baseb2int(
        [byte&mask for byte,mask in zip_longest(
            B,
            [b2pre[len(B)]],
            fillvalue=0x3f)],
        64)

    if character_number in range(0xd800,0xe000):
        raise UnicodeDecodError("character number is surrogate value")

    return character_number

if __name__ == "__main__":
    import unicodedata
    chrs = "A"+chr(946)+unicodedata.lookup("sailboat") #  +unicodedata.lookup("rowboat")
    print("chrs:",chrs)
    print("ords",[ord(c) for c in chrs])
    test = bytes(chrs,encoding="UTF-8")
    print("test",test)

    print("decode test",UTF8_decode (test))

    
    
    
                
