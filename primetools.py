#
# primetools - functions of primes with cache
#
# copyright 2014, 2016 Lewis Alexander Morrow
# all rights reserved
#
#
#
from totient import gcd
from functools import reduce
from operator import mul
def prod(X):
    return reduce(mul,X,1)

class primetools:
    
    def __init__(self,verbose=False):  # in the following, a "known prime" is an int
                        # for which prime(x) has returned True in the
                        # history of this instance of primetools
        self.verbose = verbose
        if self.verbose: print ("init primetools")  
        self.dp =[2,3]  # dense primes (i.e. a sorted list of all primes <= lkdp)
        self.lkdp = 3   # last known dp
        self.sp=set()   # sparse primes (i.e., set of known primes > lkdp)
                
    def prime(self,X):
        """ Returns True if X is a prime"""
        
        if X < 2:
            raise ValueError("domain error: X<2")
        if 2 <= X <= self.lkdp:
            return X in self.dp
        if X in self.sp:
            return True
        if not self.firstdiv(X):
            self.sp.add(X)
            return True
        return False 
    
    def firstdiv(self,X):
        """
Returns empty list or singleton list [d]
where d is first prime divisor of X

A prime divisor of X is a prime p <= int(X**.5)
which divides X evenly (has no remainder)
        """
        if X < 2: 
            raise ValueError("domain error: X<2")
        if X in self.dp or X in self.sp:
            return []
        for i in self.ple(int(X**.5)):
            if not X % i: # "not X % i" is equivalent to "i divides X evenly"
                return [i]
        return []

    def ple(self,x):
        """ generates primes p for which 2 <= p <= x  """
        for i in self.dp:  # initial conditions: self.dp = [2,3]
            if i > x:
                raise StopIteration
            yield i
            
        for i in range(self.lkdp+2,x+1,2):  # skip even no's. Future: skip 5's
            if not self.firstdiv(i):
                self.dp.append(i)
                self.lkdp = i
                if i in self.sp:
                    self.sp.remove(i)
                yield i
                
        raise StopIteration

        self.pbe = self.ple  # Alternate name for pbe ("primes less than or equal to)
                              
        
    def factors(self, X):
        """ Returns a list of primes whose product is X """
        return (lambda fd: [X] if not fd else fd + self.factors(X // fd[0])) (self.firstdiv(X))

    def factorset(self,x):
        """ returns the set of factors seen in x"""
        return set(self.factors(x))

    def cofactors(self,x,y):
        """ Return the intersection of factorset(x) and factorset(y)"""
        return self.factorset(x) & self.factorset(y)

    def coprime(self,x,y):
        """ return True if the intersection of factorset(x) and factorset(y) is void"""
        return x == 1 or y == 1 or not bool(self.cofactors(x,y))

    def distr(self,X):
        """"return distribution of values in X as a dict
        whose keys are from set(X) and
        whose values give number of instances of key value"""
        return {x:X.count(x) for x in set(X)}

    def random(self,start,stop=None):
        """return a prime number between start and stop inclusive;
           random(x) signifies random(2,x)"""
        if not stop: 
            start, stop = 2, start
        import random
        
        for i in range(100):
            pc = random.randint(start,stop)
            if self.prime(pc):
                return pc

        raise ValueError("no prime found")
#
##  https://en.wikipedia.org/wiki/Euler's_totient_function
#
    
    def totient(self,x):
        """ Returns totient of x"""
        dist = self.distr(self.factors(x)).items()
        if self.verbose: print(dist)
        
        # return Euler's result based on product of each prime factor p and its power n
        # return prod([ p**n*(1-(1/p))  for p,n in dist])
        # return prod([ p**n*1 - p**n/p for p,n in dist])
        # return prod([ p**n - p**(n-1) for p,n in dist])
        
        return   prod([ p**n - p**(n-1) for p,n in dist])

            
if __name__ == "__main__":
    from sys import version
    print ("Python version {}".format(version))
    pyver = 2 if version.startswith("2.") else 3
    if pyver == 2:        
        print ("Unit tests for primetools".format(version))
    else:
        print ("Unit tests for module {}".format(version,__file__))
    pt = primetools(verbose=True)
    print("primes in range(2 , 102) == ",[p for p in range(2,102) if pt.prime(p)])
    print("primes in pt.ple(101)  == ",[p for p in pt.ple(101)])
    bignum = 1439874169812
    print("bignum = ",bignum)
    print("factors(bignum) ==",pt.factors(bignum))
    print("factorset(bignum) ==",pt.factorset(bignum))
    print("cofactors(bignum,2) ==",pt.cofactors(bignum,2))
    print("coprime(bignum,2) == ",pt.coprime(bignum,2))
    print("totient({}) ==",pt.totient(bignum))
    print("coprime(2,4) == ",pt.coprime(2,4))
    print("coprime(3,7) == ",pt.coprime(3,7))
    print("coprime(1,3) == ",pt.coprime(1,3))
    print("coprime(1,1) == ",pt.coprime(1,1))
    print("random(1000000,2000000) == ",pt.random(2000000))
    print("totient({}) ==",pt.totient(bignum))
    

    
    



    
