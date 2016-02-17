#
##  https://en.wikipedia.org/wiki/Euler's_totient_function
#

def totient(x):
    return sum([1 == gcd(i,x) for i in range(1,x)])

def gcd(a,b):
    if a>b:return gcd(b,a)
    if not a: return b
    return gcd(b%a,a)






