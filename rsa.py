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
import modulararithmetic as Modular
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

        class Modular_Arithmetic(Euler):

            Implements modular arithmetic for a given modulus.

                Modular_Arithmetic It implements the following Modular Arithmetic Operations:
                
                a+b  a-b  a*b  a//b  a**b    -b  ~b   repr str int

            def modular(modulus):  
            
                A plain class factory for the Modular_Arithmetic class
                Separates specification of a modulus for modular arithmetic
                operations other modular arithmetic functions. See examples.
                

   
"""       


class RSA:
    """ RSA Encryption algorithms  """
    def __init__(self,*T,**D):
        pass
        
    def from_message_bit_length(self,message_bit_length=8,opt=0):
        """Create a pair of RSA classes for a given message bit length"""

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
                                                  
        P=None

        for p in range(startp,startp+100): # to be randomized
            if PT.prime(p):
                P=p
                break
            if not P:ValueError("Prime P not found")
        Q = None    
        for q in range(startp+200,startp+300):# to be randomized
            if PT.prime(q):
                Q=q
                break
            if not Q: ValueError("prime Q not found") 
            
        for e in range(21,200): # to be randomizedd
            if not PT.coprime(e,totient(P)*totient(Q)):
                continue
        #print(p,q,e)
        
        self._message_bit_length = message_bit_length
        
        pub = self.from_given_pqe(P,Q,e,opt=opt)
        return pub

    def from_given_pqe(self,p,q,e,opt=0):
        """Create an pair of RSA classes from a given p,q,e triple"""       
        print("{}.from_given_pqe(p={}, q={}, e={}, opt={})".format(self,p,q,e,opt))
##        print(totient(p*q) = {},\n gcd(e,totpq)={}".format(
##              totient(p*q),
##              gcd(e,totient(p*q))
##              ))
        self.private = RSA_private(p,q,e,opt=opt)
        self.public  = RSA_public(p*q,e) 
        return(self.public)
    
    def message_bit_length(self):
        return self._message_bit_length


    def loopback(self,cleartext):
        "loopback test of RSA encryption. cleartext is an integer"
        cyphertext = self.public.encrypt(cleartext)
        received   = self.private.decrypt(cyphertext)
        return """
Loopback test of RSA encryption and decryption
cleartext entered      = {}
cyphertext transmitted = {}
cleartext received     = {}
        """.format(cleartext,cyphertext,received)
    pass
    
                                
class RSA_public:
    """
RSA methods for hosts with public key = (pq,e)

encrypt,
  which encrypts a message which can only be decoded by the
  decrypt method of the same instance of an RSA object.

authenticate,
  which can validate a signature created which could only have been created
  by the sign method of the RSA_private class

The RSA_public class is provided with the RSA public key (pq,e) when it is
instantiated.

pq is the product of p and q.
e is the exponent

The RSA_public key class is not provided with the primes p and q.  The
RSA_private class is provided with p and q.  This is the only difference
between the two methods.
The RSA public key class does not have the factorization of the modulus pq into two primes.
Consequently, the RSA_public class does cannot calculate the totient
of p or that of q, and therefore does not know the totient of pq.

The RSA private key does have p and q and can therefor calculate the totient of pq.

The fundamental question of whether RSA encryption can be broken is this:
long would it take an attacker to factor pq into p and q, create to totient
of pq and therefore be able to calculate the decryption key d,
the multiplicative inverse of (e mod pq).

The answer to "how long it would take an attacker to factor pq" is therefore
the entire basis for RSA encryption.  

    """
    def __init__(self,pq:int,e:int,*T,**D)->int:
        
        """
        Instantiate instance of RSA public key class with public key(pq,e).
The methods available in the public key class are:
encrypt: converts cleartext to RSA cyphertext for cleartext and signature authentication given cleartext
for Olin spring semester Computer Networks class

   
        #print("{}.__init__(pq={},e={},{},{})".format(self,pq,e,T,D))

        The encryption algorithm is  m**e % pq
        """
        

        self.modpq = Modular.mod(pq) # create a modular arithmetic class for modulus pq 
        
        self.e = self.modpq(e)       # create e as an object that uses modular arithmetic modulo pq
        
    def encrypt(self,cleartext):
        """
Encrypt cleartext to be sent

Encrypt the integer "cleartext"  with public key (pq,e) provided
when this object was instantiated from the RSA_public class.

The RSA public key is the tuple (pq,e) where pq is the product of primes p and q
and e is an natural number relatively prime to totient(pq)

The RSA_public object
    knows pq and e
    Does not know p, q, or totient(p*q)
    totient (p*q) is (p-1)(q-1)
    
THe public key methods are ncryption and digital signatures.

Encryption is 

         (cleartext**e) % pq

         """
        
        if type(cleartext) is not int or cleartext < 0:
            raise TypeError("Cleartext must be an non-negative int")

        #print("cleartext=",bin(cleartext))
        
        self.cleartext = self.modpq(cleartext)  # convert the message to an
                                                # instance of the modulararithmetic class

        
        #print(bin(int(self.cleartext)))                                       

        if int(self.cleartext) != cleartext:    # if "modpq" class initialization truncated
                                                # the message, complain and quit
            raise ValueError("Message too long")
        
        # Encryption -- note that the operation ** is performed modulo pq
        # because cleartext and e are instances of modulararithmetic
        

        self.cyphertext = self.cleartext**self.e  # cyphertext is simply cleartext  raised to the power e in the modular arithemtic mod pq

        return int(self.cyphertext)

    def authenticate(self,receivedtext,signature):
        """\
Authenticate a document signed by a private key to prove it came from the holder of the privatre key.

The sample hash algorithm used here is just the built-in Python hash function. 
The actual hash algorithm used for a given private / public signature is negotiated by the two parties. 
        """
        return self.encrypt(signature) == hash(receivedtext)   # returns True if the hash matdhes; o
        
class RSA_private:
    """
Private Key class:
    Instantiated with RSA values p,q,e and optimization value opt
               opt=0 is only used in decryption.
                    It is C(M)**d % totient(p*q) by plain exponentiation and opt=1 is Chinese Remainder Theorem 
    decrypts received cybertext
                      signs andcleartext to be sent"
    """
    def __init__(self,p,q,e,opt=0,*T,**D):

        """
Initialize private key operations by computing the decryption key and
choosing a decryption algorithm.

Note that the factorization of pq into p and q is
known to the private key instance but not the matching public key instance.

opt=1 chooses the Chinese Remainder Theorem.
opt=0 chooses plain exponentiation."""

        totient_p = totient(p)
        totient_q = totient(q)
        totient_pq = totient_p*totient_q  # since p,q are prime, totient(p*q) = (p-1)*(q-1)
        
        mod_totient_pq  = Modular.mod(totient(p)*totient(q))  # generate a modular arithmetic type for totient(p*q)
    
    
        d_mod_pq = ~mod_totient_pq(e)  # ~ creates (the multiplicative inverse modulo (p*q)) of e
                                       # the sublety here is that modular arithmetic has a special
                                       # function for multiplicative inverse.

        #print("~mod_totient_pq({}) == {}".format(e,repr(d_mod_pq)))

        d = int(d_mod_pq)             # we want this to be an int for exponentiation - d may be quite large if p and q are large

                                     
        self.modpq = Modular.mod(p*q) # we need to calculate our results modulo p*q 

        self.decrypt = self.plain_decrypt_init(d) if opt==0 else self.crt_decrypt_init(p,q,e,d)
                                     #choose the decryption algorithm based on the
                                     # opt field.
                                     # opt=0 - plain (not optimized)
                                     # opt=1 - the Chinese Remainder Theorem                                                 
                                                                                        
    def plain_decrypt_init(self,d):
    
        self.modpq_d = self.modpq(d)

        return self.plain_decrypt
        
    def plain_decrypt(self,cybertext):

        return int(self.modpq(cybertext) ** self.modpq_d)

  
    def crt_decrypt_init(self,p,q,e,d):
        """decryption requires factored primes (p and q)"""

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
        print("crt_decrypt")

        ct_p = self.modp(received_cyphertext) ** self.modp(self.tp_d)
        ct_q = self.modq(received_cyphertext) ** self.modq(self.tq_d)
        modp_ct_q = self.modp(int(ct_q))
        h =    self.modp_q_inv * (ct_p - modp_ct_q)

        #print("values:  ct_p:{}, ct_q:{}, modp_ct_q:{}, h:{}, self.q:{}".format(
        #    ct_p,                ct_q,    modp_ct_q,    h,    self.q))

        return int(ct_q) + int(h) * self.q       
            
    def decrypt(self,received_cyphertext):
        "This method is replaced by plain_decrypt or crt_decrypt " 
        raise NotImplemented 

    def sign(self,cleartext_to_be_sent):
        return crt_decrypt(hash(cleartext_to_be_sent))
    

if __name__ == "__main__":
    print ("Unit tests for module {}".format(__file__))
    rsa = RSA()
    rsa.from_given_pqe(61,53,17,opt=0)
    print(rsa.loopback(65))
    rsa.from_given_pqe(61,53,17,opt=1)
    print(rsa.loopback(65))
    print(rsa.loopback(128))
    print(rsa.loopback(1))
    print(rsa.loopback(2))
    print(rsa.loopback(3000))

    
