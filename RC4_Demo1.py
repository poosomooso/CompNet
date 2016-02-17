#
## RC4
#
def p(X,*T,**D):
    print (X,*T,**D)
    return X

class Olin_RC4:
    """T
A simple stream cypher by Ron Rivest of RSA, long in broad use.

Times change, though, and this encryption scheme is officially deprecated by the IETF for use in SSL/TLS suites.
See Feb 2015 RFC7465 (https://tools.ietf.org/rfc/rfc7465.txt).

It makes a fine learning tool though.
"""
    def __init__(self,password:bytes,base=256):

        if base != 256:
            raise NotImplementedError("This edition of Olin_RC4 supports only base 256")

        self.base = base

        "Key scheduling algorithm"

        if not password:
            self.S = ''
        else:
            S = [s for s in range(base)]
            K = [password[i % len(password)] for i in range(base)]
            j = 0
            for i in range(base):
                j = ( j + S[i] + K[i] ) % base
                S[j] , S[i] = S[i] , S[j]

            self.S = S  # password-generated random permutation of range(base)
                        # for use by prng during RC4 encryption/decryption

    def prng(self,n:int)->bytes:
        """A generator for pseudo-random Numbers"""

        S = [x for x in self.S] # make copy of S for this instance of prng
        base = self.base

        i = j = 0

        for i in range(n):
            i = (i + 1) % base
            j = (j + S[i]) % base

            S[i] , S[j] = S[j] , S[i]  # permute copy of S

            yield S[ (S[i] + S[j]) % base]

    def crypt(self,text):
        return bytes([b^k for b,k in zip(text,self.prng(len(text)))])

if __name__ == "__main__":

    def The_RC4_CHRONICLES(password):

        print("THE RC4 CHRONICLES.   CHAPTER 1\n\n")
        print("Eve, the owner of the chat room service,\n has been eavesdropping on Alice and Bob's chats")
        print()

        print("Alice and Bob meet and agree on the password",password)
        print()
        print("Alice gets back to her office Raspberry pi")
        print("She starts her local chat client with password",password)
        print()
        RC4_Alice = Olin_RC4(password)
        print("Bob gets back to his office Raspberry pi")
        print("He starts his local chat client with password",password)
        print()
        RC4_Bob = Olin_RC4(password)
        plaintext1 = b"See if you can eavesdrop on this, Eve!"
        print("Alice enters ",plaintext1)
        print()
        cybertext = RC4_Alice.crypt(plaintext1)
        print("Eve opens her chat snooping client and sees \n",cybertext)
        print()
        plaintext2 = RC4_Bob.crypt(cybertext)
        print("Bob sees ",plaintext2)
        if cybertext == plaintext1:
            print("Eve calls Alice and says 'I sure can!'")



The_RC4_CHRONICLES(b"The+Ph0en1x_Fl1e5")
