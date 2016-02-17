#
# modulararithmetic
#
# Instances of "ModularX" provide addition, multiplication and exponentiation
# operations modulo  'MOD'.  'MOD' is supplied as the argument "modulus" to
# the class factory function 'mod' which produces "ModularX" classes.
# The ModularX classes produced by mod have a __class__.__name__ of "mod({})".format(modulus).
#
# Copyright 2014 Lewis Alexander Morrow
# All rights reserved
#
# You may use this code at Olin College of Engineering, Needham, MA
# so long as this copyright notice is retained in any derivative works.
#
# The code is a throught experiment and is not suitable for any purpose whatsoever
# in the real world.
#

def mod(modulus=16,opt: {None,"CRT","pow"} = None):
    """\
Factory function that returns a modular arithemtic class for a given modulus.
opt provides optimizations using the Chinese Remainder Theorem and/or the
the 'pow(a,b,c)' functions, which is computes a**b % c using the
# Python alogirithm shown in the __pow__ method.

"""

    return type("mod{}".format(modulus),(ModularX,),dict(MOD=modulus))

class ModularX(object):
#   Modular Arithmetic for a specified modulus, stored as self.MOD
#
#    The following operations are supported:
#   a + b  # modular addition
#   a - b  # modular subtraction 
#     - b  # modular negation 
#   a * b  # modular product       
#   a / b  # modular division (a*b/a == b) 
#     ~ b  # modular inverse  (a*~a) == 1  
#   a ** b # modular exponentiation (CRT optimized)
#            Uses Fermat's little theorem that for prime(p)
#                             ((a**p) %p) == a
#
#   For objects of type ModularX:
#   int(x) returns the value as an int,  e.g.   42
#   repr(x) string includes the modulus  e.g.  '42mod64'
#   str(x)  string just gives the number e.g.  '42'
#
    def __int__(self):
        return self.value
    
    def __init__(self,other,*T,**D):
        
        #print("{}__init__({},{},{})".format(self.__class__,value,T,D))  # decomment to watch object creation
                                               # this is handy for comparing
                                               # simple implementation with
                                               # Chinese Remainder Theorem
                                               # implementation
        if type(other) is int:
            self.value = other % self.MOD   
        elif type(other) is self.__class__:
            self.value = other.value % self.MOD

            
        else:
            raise ValueError("argument {} of class {} is cannot be used to initialize class {} objects").format(other,other.__class__,self.__class__)
            
    def __add__(self,other):
        " (self + other) % self.MOD"
        if self.MOD != other.MOD:
            raise TypeError("different modula")
        
        return self.__class__((int(self) + int(other)) % self.MOD)

    def __sub__(self,other):
        " (self - other) % self.MOD"
        if self.MOD != other.MOD:
            raise TypeError("different modula")
        
        return self.__class__((int(self) - int(other)) % self.MOD)

    def __neg__(self):
        " (- self) % self.MOD"
        
        return self.__class__(-int(self))

    def __mul__(self,other):
        " self * other % self.MOD"
        if self.MOD != other.MOD:
            raise TypeError("different modula")
        
        return self.__class__(((int(self) % self.MOD)*(int(other) % self.MOD)) % self.MOD)

    def __truediv__(self,other):
        " self / other % self.MOD "
        if self.MOD != other.MOD:
            raise TypeError("different modula")
        
        if not int(other):
            raise ZeroDivisionError
        
        return self.__class__(
            [b for b in range(self.MOD) if 1 == (
                b * int(other))%self.MOD][0])
    

    def __invert__(self):
        " returns k(1 / self) % self.MOD"
        
        t,tp,r,rp = 0,1,self.MOD,int(self)
        while rp:
            q = r // rp
            r,rp = rp, r - q*rp
            t,tp = tp, t - q*tp
        if r>1 :
            raise ValueError(repr(self),"has no multiplcative inverse mod ",self.MOD)
        
        return self.__class__(t if t >= 0 else self.MOD+t)
    
    def __pow__(self,other):
        """ Python version of exponentiation algorithm of self to a large power"""
        exp = int(other)
        r = self.__class__(1)
        b = self.__class__(int(self))
        for bit in range(exp+1):
            if (exp>>bit)%2:
                r = r*b
            b = b * b
        return self.__class__(r)

    


    def __repr__(self):
        return ("{}"+self.__class__.__name__).format(int(self))
    
    def __str__(self):
        return "'{}'".format(int(self))

    

if __name__ == "__main__":
    from sys import version
    print ("Python version {}".format(version))
    pyver = 2 if version.startswith("2.") else 3
    if pyver == 2:        
        print ("Unit tests for modulus".format(version))
    else:
        print ("Unit tests for module {}".format(version,__file__))

    print("These  results may seem a bit mysterious without an explanation.")
    print("""mod(5) produces a class.  The class has arithmetic operations:
          a+b, a-b, a*b, a/b, a**b which are used in RSA
          the operations are all modulus operations.
          thus, if a and b are objects of class mod(5), then
          a+b is the same as ((a%5)+(b%5))%5.  W
          It may be easier to read and understand than a op b % c

          Here are some examples.  Try your own after you see these.
          """)
    
    print("repr({}) == '{}',".format("mod(5)(7)",repr( mod(5)(7) ) ))
    print("because the integer value of {} is 2, just as integer value of 7%5 is 2.".format("mod(5)(7)" ))
    print("int({}) == {}".format("mod(5)(7)",int ( mod(5)(7) ) ))
    print("str({}) == {}".format("mod(5)(7)",str ( mod(5)(7) ) ))
    
    
    
    print("Now, let's look at multiplication and division")
    print("""mod(5)(3)*mod(5)(2) ==""")
    print("""mod(5)(3*2) ==""")
    print("""6 % 5 == 1""")
    print("2 modulo 5 is designated in this module by by mod(5)(2)")
    print("""the multiplicative inverse of 2 modulo 5 is designated here by ~mod(5)(2)""")
    print("""this module computes the unique multiplicative inverse of a mod(5) object
          when there is one""")
    print("~{} == {}".format(repr(mod(5)(2)),"mod(5)(3)"))
    print("Note that the result of taking the inverse is another mod(5) object")
    print("""
{} * {} ==
mod(5)(2) * mod(5)(3) ==
mod(5)(2*3) ==
mod(5)(6) ==
6 % 5 == {}""".format(repr(mod(5)(2)),"~mod(5)(2)",int(mod(5)(2)*~mod(5)(2))))
    

    


