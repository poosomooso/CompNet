#
# RSA
#
# copyright 2014 Lewis Alexander Morrow
# all rights reserved
#
# permission is hereby granted for use of this work for 
# educational purposes within Olin College of Engineering, Needham, MA
#
#
from totient import gcd, totient
import modulararithmetic2 as Modular
import primetools
PT=primetools.primetools()

__doc__ = """

 

This Python package provides an implementation of the RSA encryption algorithm
intended to introduce it and explain its operation.   Its intent is to
show the use of Python as a notation for simplifying the description of
the algorithms used in the current computer networking.

This Python package provides an implementation of RSA in Python. 

Implementation Architecture

The RSA package has the following modules and class hierarchy.

   * module: primetools
   
            class Primetools:

               A collection of methods for working with primes
               Provides an iterator that yields primes in order
               Its primary goal is to be both easily understood
               and relatively efficient.



    * module: modulararithmetic

        class Modular_Arithmetic:

            Implements modular arithmetic operations for a given modulus
                
                a+b  a-b  a*b  a//b  a**b    -b  ~b   repr str int
                

        def modular(modulus):  
            
            A class factory for the Modular_Arithmetic class.
                
            Specifies the modulus for modular arithmetic operations.
                

   
"""       


class RSA:
    """ RSA Encryption algorithms  """
    def __init__(self,message_bit_length=8,opt=0,verbose=False):
        self.opt = opt
        self.verbose = verbose
        if self.verbose: print(message_bit_length,opt)
        
        """Create an RSA cryptosystem instance for a given message bit length"""

        startp = 2**(1+message_bit_length//2)
        # the bitlengths of p and q should each be about 1/2 the message bitlength
                                                  # notes: 1. the starting point for the search needs to be randomized
                                                  #        2. the current search for a suitable prime pair needs to be
                                                  #           changed to a search for a suitable pseudo-prime pair
                                                  #        3. (2.) requires a pseudo-prime generator
                                                  #        4. we will need to increase the specification msg_bit_length
                                                  #           to provide room for extra bits used for 
                                                  #           pre-processing prior to RSA modular exponentiation
                                                  #        5. RSA messages are often used to exchange keys for
                                                  #           symmetric encryption algorithms
                                                  
        p = None

        for P in range(startp,startp+100): # to be randomized
            if PT.prime(P):
                p = P # found a prime!
                break
            if not P:ValueError("Prime p not found")

        q = None    

        for Q in range(startp+200,startp+300):# to be randomized
            if PT.prime(Q):
                q = Q
                break
            if not q: ValueError("prime q not found")
            
        e = None
        
        for E in range(21,200): # to be randomizedd
            if PT.coprime(E,totient(p)*totient(q)):
                e = E
                break
            if not e: ValueError("prime e coprime to p*q not found")

        self.From_pqe(p,q,e,opt=self.opt)

    def From_pqe(self,p,q,e,opt=0):
        
        #print("From_pqe(p={},q={},e={},opt={})".format(p,q,e,opt))
            
        
        """Create an pair of RSA classes from a given p,q,e triple"""       

        self.private = RSA_private(p,q,e,opt=opt)

        n = p*q

        self.public = RSA_public(n,e)

class RSA_private:
    """
Private Key class:
    Instantiated with RSA values p,q,e and optimization value opt
               opt=0 is only used in decryption.
                    It is C(M)**d % totient(p*q) by plain exponentiation and opt=1 is Chinese Remainder Theorem 
    decrypts received cybertext
                      signs andcleartext to be sent"
    """
    
    def __init__(self,p,q,e,opt=0,verbose=False,*T,**D):
        """

Initialize private key operations by computing the decryption key and
choosing a decryption algorithm.

Note that the factorization of pq into p and q is
known to the private key instance but not the matching public key instance.

opt=3 hooses the pow(cybertext,d,p*q) build-in function using the Chinese Remainder Theorem
opt=2 chooses the pow(cybertext,d,p*q) build-in function
opt=1 chooses the Chinese Remainder Theorem.
opt=0 chooses plain exponentiation."""
        self.verbose = verbose
        print ("RSA_private(p={},q={},e={},opt={},verbose={})".format(
            p,q,e,opt,verbose))

        
# 1. determine d, the multiplicative inverse of e mod (totient(p)*totient(q))

        totient_p = totient(p)
        totient_q = totient(q)
        totient_pq = totient_p*totient_q  # since p,q are prime, totient(p*q) = (p-1)*(q-1)
        
        mod_totient_pq  = Modular.mod(totient(p)*totient(q))  # generate a modular arithmetic type for totient(p*q)
    
    
        d_mod_pq = ~mod_totient_pq(e)  # ~ creates (the multiplicative inverse modulo (p*q)) of e
                                       # the sublety here is that modular arithmetic has a special
                                       # function for multiplicative inverse.

        self.d = d = int(d_mod_pq)             # we want this to be an int for exponentiation - d may be quite large if p and q are large
        

# 2. choose optimization

#choose the decryption algorithm based on the
                                     # opt field.
                                     # opt=0 - plain (not optimized)
                                     # opt=1 - the Chinese Remainder Theorem
                                     # opt=2 - use built-in pow(a,b,c)
                                     # opt=3 - CRT with build-in pow(a,b,c)


        if opt == 0:
            self.modpq = Modular.mod(p*q)
            self.decrypt = self.plain_decrypt_init(d)
            
        elif opt == 1:
            self.modpq = Modular.mod(p*q)
            self.decrypt = self.crt_decrypt_init(p,q,e,d)

        elif opt == 2:
            self.decrypt = self.pow_decrypt_init(d,p,q)

        elif opt == 3:
            self.decrypt = self.pow_crt_decrypt_init(d,p,q)
                                     
        else:
            raise ValueError("opt must be in 0, 1, 2, or 3")

        pass ## end of __init__
#############################################################################
# Dummy decryption algorithms which are replaced by choice of opt = parame  #
#############################################################################
    def decrypt_init(self,d,p,q):
        "Initialize decrypt"
        raise NotImplementedError("logic error - should not happen")

    def decrypt(self,received_cyphertext):
        "This method is replaced by plain_decrypt or crt_decrypt " 
        raise NotImplementedError("logic error - should not happen")
 
#############################################################################
# Alternate decryption algorithms each of which initializes some constants  #
#############################################################################

## opt = 0:  plain decrypt using Python exponentiation
    
                                                                                        
    def plain_decrypt_init(self,d):
        if self.verbose: print("opt 0: plain decrypt")
    
        self.modpq_d = self.modpq(d)

        return self.plain_decrypt
        
    def plain_decrypt(self,receivedcybertext):

        return int(self.modpq(receivedcybertext) ** self.modpq_d)


## ope = 1  -- crt decrypt using Python exponentiation
#  See http://www.di-mgt.com.au/crt_rsa.html for details


  
    def crt_decrypt_init(self,p,q,e,d):
        """decryption requires factored primes (p and q)"""

        if self.verbose: print("opt = 1  - crt_decrypt")

        # precompute values used during decryption
        
        self.tp_d   = d % totient(p)     
        self.tq_d   = d % totient(q)
        
        self.modp = Modular.mod(p)
        self.modp_q_inv  = ~self.modp(q)   # this requires thought - it is the multiplicative inverse of q % p

        self.modq = Modular.mod(q)
        self.q  = q

        #print("setup values self.tp_d:{}, self.tq_d, self.modp_q_inv: {}".format(
        #    self.tp_d,                    self.tq_d, self.modp_q_inv))

        return self.crt_decrypt

    
    def crt_decrypt(self,received_cyphertext):
        

        ct_p = self.modp(received_cyphertext) ** self.modp(self.tp_d)
        ct_q = self.modq(received_cyphertext) ** self.modq(self.tq_d)
        modp_ct_q = self.modp(int(ct_q))
        h =    self.modp_q_inv * (ct_p - modp_ct_q)

        #print("values:  ct_p:{}, ct_q:{}, modp_ct_q:{}, h:{}, self.q:{}".format(
        #    ct_p,                ct_q,    modp_ct_q,    h,    self.q))

        return int(ct_q) + int(h) * self.q
    
# opt = 2  - plain decrypt using pow(a,b,c) built-in function

    def pow_decrypt_init(self,d,p,q):
        if self.verbose: print("opt=2 - pow decrypt")

        self.n = p*q
        self.d = d
        return self.pow_decrypt

    def pow_decrypt(self,received_cybertext):
        
        return pow(received_cybertext,self.d,self.n)


    
# opt = 3  - crt decrypt using pow(a,b,c) built-in function
#  See http://www.di-mgt.com.au/crt_rsa.html for details

    def pow_crt_decrypt_init(self,d,p,q):

        """decryption requires factored primes (p and q)"""

        if self.verbose: print("opt=3, pow_crt_decrypt")

        # precompute values used during decryption
        
        self.tp_d   = d % totient(p)     
        self.tq_d   = d % totient(q)
        
        self.p = p
        self.modp = Modular.mod(p)
        self.modp_q_inv  = ~self.modp(q)  # this requires thought - it is the multiplicative inverse of q % p

        self.modq = Modular.mod(q)
        self.q = q

        #print("setup values self.tp_d:{}, self.tq_d, self.modp_q_inv: {}".format(
        #    self.tp_d,                    self.tq_d, self.modp_q_inv))

        return self.pow_crt_decrypt

    def pow_crt_decrypt(self,received_cyphertext):
        

        ct_p = self.modp(pow(received_cyphertext,self.tp_d,self.p))
        
        ct_q = self.modq(pow(received_cyphertext,self.tq_d,self.q))

        modp_ct_q = self.modp(int(ct_q))
        
        h =    self.modp_q_inv * (ct_p - modp_ct_q)

        #print("values:  ct_p:{}, ct_q:{}, modp_ct_q:{}, h:{}, self.q:{}".format(
        #    ct_p,                ct_q,    modp_ct_q,    h,    self.q))

        return int(ct_q) + int(h) * self.q       

#  opt = 1   -  crt decrypt using python exonentiation

    def crt_decrypt(self,received_cyphertext):
        print("crt_decrypt")

        ct_p = self.modp(received_cyphertext) ** self.modp(self.tp_d)
              
    
              
        ct_q = self.modq(received_cyphertext) ** self.modq(self.tq_d)
        
        modp_ct_q = self.modp(int(ct_q))
        h =    self.modp_q_inv * (ct_p - modp_ct_q)

        #print("values:  ct_p:{}, ct_q:{}, modp_ct_q:{}, h:{}, self.q:{}".format(
        #    ct_p,                ct_q,    modp_ct_q,    h,    self.q))

        return int(ct_q) + int(h) * self.q

    def sign(self,cleartext_to_be_sent,opt=0):
        "Create digital signature using private key"
        return cleartext_to_be_sent,self.decrypt(cleartext_to_be_sent)

############################################################################    
class RSA_public:
    
    def __init__(self,n:int,e:int,verbose = False)->int:
        self.n = n
        self.e = e
        self.verbose = verbose

        if self.verbose: print("RSA_public(n={},e={})".format(n,e))
        
        """Instantiate RSA public key class with public key (n,e)"""

        self.mod_n = Modular.mod(n)  # modulus n
        
        self.e_mod_n = self.mod_n(e)       # exponent e modulus n
        
    def encrypt(self,cleartext):
        """ Encrypt cleartext using public key (n,e)"""
        print("encrypt cleartext:",cleartext)
        if type(cleartext) is not int or cleartext < 0:
            raise TypeError("Cleartext must be an non-negative int")
        
        self.cleartext = self.mod_n(cleartext)  # convert the message to an
                                                # instance of the modulararithmetic class
        if int(self.cleartext) != cleartext:    # if "modpq" class initialization truncated
                                                # the message, complain and quit
            raise ValueError("Message too long")
        

        return int(self.cleartext**self.e_mod_n)      # Public key encryption 

    def authenticate(self,receivedtext,signature):
        """\
Authenticate a document signed by a private key to prove it came from the holder of the privatre key.

The sample hash algorithm used here is just the built-in Python hash function. 
The actual hash algorithm used for a given private / public signature is negotiated by the two parties. 
        """
        return self.encrypt(signature) == receivedtext

    
    # Reverse private and pubic key to prove text was created by party
    # with private key that matches public key.
    #
    # returns True if the hash "decrypted" by the private key matches the
    # hash that has been "encrypted" by the public key
    def export_public_key(self):
        pubkey = """\
Olin College CompNet RSA Model
February 2, 2016
{}
{}
""".format(self.n,self.e)
        return pubkey

    
    def import_public_key(self,pubkey):
        pubkeyparse = pubkey.split("\n")
        if pubkeyparse[0] != "Olin College CompNet RSA Model" or pubkeyparse[1] != "February 2, 2016":
            raise ValueError("Invalid public key:{}".format(pubkey))
        self.n = int(pubkeyparse[2])
        self.e = int(pubkeyparse[3])
        return
    
    
if __name__ == "__main__":
    def loopback(cleartext):
        "loopback test of RSA encryption. cleartext is an integer"
        cyphertext = rsa.public.encrypt(cleartext)
        received   = rsa.private.decrypt(cyphertext)
        signed     = rsa.private.sign(cleartext)
        authenticated = rsa.public.authenticate (*signed)
        return """
Loopback test of RSA encryption and decryption
cleartext entered      = {}
cyphertext transmitted = {}
cleartext received     = {}

cleartext signed       = {}
signature autenticated = {}
        """.format(cleartext,cyphertext,received,signed,authenticated)
        pass
    
      
    print ("Unit tests for module {}".format(__file__))
    rsa = RSA()
    rsa.From_pqe(61,53,17,opt=0)
    print(loopback(65))
    print(loopback(128))
    print(loopback(1))
    print(loopback(2))
    print(loopback(3000))

    rsa.From_pqe(61,53,17,opt=1)
    print(loopback(65))
    print(loopback(128))
    print(loopback(1))
    print(loopback(2))
    print(loopback(3000))

    rsa.From_pqe(61,53,17,opt=2)
    print(loopback(65))
    print(loopback(128))
    print(loopback(1))
    print(loopback(2))
    print(loopback(3000))


    rsa.From_pqe(61,53,17,opt=3)
    print(loopback(65))
    print(loopback(128))
    print(loopback(1))
    print(loopback(2))
    print(loopback(3000))
